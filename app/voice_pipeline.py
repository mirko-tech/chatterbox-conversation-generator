"""
Voice Pipeline Module

Handles TTS generation and audio processing using Chatterbox TTS.
Converts structured dialogue data into WAV audio files.
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional

import torch
import torchaudio as ta
import torchaudio.functional as F
from chatterbox.mtl_tts import ChatterboxMultilingualTTS


# Output directory for generated audio files
OUTPUT_DIR = Path("outputs")


class TextNormalizer:
    """
    Text preprocessing utilities to make text more speakable for TTS.

    Handles emails, URLs, special characters, and other patterns that
    TTS models struggle to pronounce correctly.
    """

    @staticmethod
    def normalize_email(text: str) -> str:
        """
        Convert email addresses to speakable format.

        Example: john.doe@example.com -> john dot doe at example dot com

        Args:
            text: Text potentially containing email addresses

        Returns:
            Text with emails converted to speakable format
        """
        # Email regex pattern
        email_pattern = r'\b([a-zA-Z0-9._-]+)@([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})\b'

        def replace_email(match):
            local_part = match.group(1)  # john.doe
            domain_part = match.group(2)  # example.com

            # Replace dots, underscores, hyphens in local part
            local_speakable = local_part.replace('.', ' dot ').replace('_', ' underscore ').replace('-', ' dash ')

            # Replace dots in domain
            domain_speakable = domain_part.replace('.', ' dot ')

            return f"{local_speakable} at {domain_speakable}"

        return re.sub(email_pattern, replace_email, text)

    @staticmethod
    def normalize_url(text: str) -> str:
        """
        Convert URLs to speakable format.

        Example: https://www.example.com -> H T T P S colon slash slash W W W dot example dot com

        Args:
            text: Text potentially containing URLs

        Returns:
            Text with URLs converted to speakable format
        """
        # Simple URL pattern
        url_pattern = r'(https?://)?([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})(\/[^\s]*)?'

        def replace_url(match):
            protocol = match.group(1) or ''
            domain = match.group(2)
            path = match.group(3) or ''

            result = ''

            # Handle protocol
            if protocol:
                if 'https' in protocol:
                    result += 'H T T P S colon slash slash '
                elif 'http' in protocol:
                    result += 'H T T P colon slash slash '

            # Handle www
            if domain.startswith('www.'):
                result += 'W W W dot '
                domain = domain[4:]

            # Replace dots in domain
            result += domain.replace('.', ' dot ')

            # Skip path for now as it's complex
            if path:
                result += ' slash ' + path.replace('/', ' slash ').strip()

            return result

        return re.sub(url_pattern, replace_url, text)

    @staticmethod
    def normalize_phone(text: str) -> str:
        """
        Convert phone numbers to speakable format.

        Example: +1-555-123-4567 -> plus one, five five five, one two three, four five six seven

        Args:
            text: Text potentially containing phone numbers

        Returns:
            Text with phone numbers converted to speakable format
        """
        # Phone number pattern (various formats)
        phone_pattern = r'(\+?\d{1,3})?[\s.-]?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'

        def replace_phone(match):
            phone = match.group(0)
            # Remove formatting characters
            digits = re.sub(r'[^\d+]', '', phone)

            # Convert to spoken format
            spoken = ''
            for char in digits:
                if char == '+':
                    spoken += 'plus '
                else:
                    spoken += char + ' '

            return spoken.strip()

        return re.sub(phone_pattern, replace_phone, text)

    @staticmethod
    def normalize_text(text: str, normalize_emails: bool = True,
                      normalize_urls: bool = False,
                      normalize_phones: bool = False) -> str:
        """
        Apply all text normalizations.

        Args:
            text: Input text
            normalize_emails: Convert emails to speakable format
            normalize_urls: Convert URLs to speakable format
            normalize_phones: Convert phone numbers to speakable format

        Returns:
            Normalized text ready for TTS
        """
        result = text

        if normalize_emails:
            result = TextNormalizer.normalize_email(result)

        if normalize_urls:
            result = TextNormalizer.normalize_url(result)

        if normalize_phones:
            result = TextNormalizer.normalize_phone(result)

        return result


class AudioProcessor:
    """
    Audio processing utilities for natural-sounding dialogue.

    Handles fade-in/fade-out, de-essing, normalization, and artifact removal.
    """

    @staticmethod
    def apply_fade(audio: torch.Tensor,
                   sample_rate: int,
                   fade_in_ms: int = 10,
                   fade_out_ms: int = 50) -> torch.Tensor:
        """
        Apply smooth fade-in and fade-out to prevent hard transitions.

        Args:
            audio: Audio tensor (1, num_samples)
            sample_rate: Sample rate in Hz
            fade_in_ms: Fade-in duration in milliseconds
            fade_out_ms: Fade-out duration in milliseconds

        Returns:
            Audio with fades applied
        """
        num_samples = audio.shape[1]
        fade_in_samples = int(sample_rate * fade_in_ms / 1000)
        fade_out_samples = int(sample_rate * fade_out_ms / 1000)

        # Ensure fade lengths don't exceed audio length
        fade_in_samples = min(fade_in_samples, num_samples // 2)
        fade_out_samples = min(fade_out_samples, num_samples // 2)

        # Manual fade implementation for compatibility
        audio_copy = audio.clone()

        # Fade in
        if fade_in_samples > 0:
            fade_in_curve = torch.linspace(0, 1, fade_in_samples).to(audio.device)
            audio_copy[:, :fade_in_samples] *= fade_in_curve

        # Fade out
        if fade_out_samples > 0:
            fade_out_curve = torch.linspace(1, 0, fade_out_samples).to(audio.device)
            audio_copy[:, -fade_out_samples:] *= fade_out_curve

        return audio_copy

    @staticmethod
    def normalize_rms(audio: torch.Tensor, target_rms: float = 0.1) -> torch.Tensor:
        """
        Normalize audio to target RMS level for consistent volume.

        Args:
            audio: Audio tensor (1, num_samples)
            target_rms: Target RMS level (0.0-1.0, default 0.1)

        Returns:
            Normalized audio
        """
        # Calculate current RMS
        rms = torch.sqrt(torch.mean(audio ** 2))

        # Avoid division by zero
        if rms > 1e-8:
            scaling_factor = target_rms / rms
            # Prevent clipping by capping the scaling factor
            scaling_factor = min(scaling_factor, 1.0 / (torch.max(torch.abs(audio)).item() + 1e-8))
            audio = audio * scaling_factor

        return audio

    @staticmethod
    def high_pass_filter(audio: torch.Tensor,
                        sample_rate: int,
                        cutoff_freq: int = 80) -> torch.Tensor:
        """
        Apply high-pass filter to remove low-frequency breathing artifacts.

        Args:
            audio: Audio tensor (1, num_samples)
            sample_rate: Sample rate in Hz
            cutoff_freq: Cutoff frequency in Hz (default 80Hz removes breath noise)

        Returns:
            Filtered audio
        """
        return F.highpass_biquad(audio, sample_rate, cutoff_freq)

    @staticmethod
    def de_ess(audio: torch.Tensor,
               sample_rate: int,
               reduction_db: float = -6.0) -> torch.Tensor:
        """
        Reduce sibilant frequencies (harsh S, SH, Z sounds).

        Uses a gentle reduction in the 5-8 kHz range where sibilants are strongest.

        Args:
            audio: Audio tensor (1, num_samples)
            sample_rate: Sample rate in Hz
            reduction_db: Amount to reduce sibilants in dB (negative value, default -6dB)

        Returns:
            De-essed audio
        """
        # Sibilant frequency range: 5-8 kHz
        # Apply bandpass to isolate sibilants
        sibilant_freq = 6500  # Center frequency for sibilants
        Q = 0.7  # Quality factor (bandwidth)

        # Extract sibilant band
        sibilant_band = F.bandpass_biquad(audio, sample_rate, sibilant_freq, Q)

        # Reduce sibilant band
        reduction_factor = 10 ** (reduction_db / 20)
        sibilant_band_reduced = sibilant_band * reduction_factor

        # Subtract reduced sibilants from original
        audio_deessed = audio - sibilant_band + sibilant_band_reduced

        return audio_deessed

    @staticmethod
    def process_line(audio: torch.Tensor,
                    sample_rate: int,
                    apply_deess: bool = True,
                    apply_normalize: bool = True,
                    apply_highpass: bool = True,
                    apply_fade: bool = True) -> torch.Tensor:
        """
        Apply full audio processing pipeline to a dialogue line.

        Args:
            audio: Audio tensor (1, num_samples)
            sample_rate: Sample rate in Hz
            apply_deess: Enable de-essing filter
            apply_normalize: Enable RMS normalization
            apply_highpass: Enable high-pass filter for breathing removal
            apply_fade: Enable fade-in/fade-out

        Returns:
            Processed audio
        """
        # High-pass filter to remove breathing (do first to clean signal)
        if apply_highpass:
            audio = AudioProcessor.high_pass_filter(audio, sample_rate)

        # De-essing to reduce sibilants
        if apply_deess:
            audio = AudioProcessor.de_ess(audio, sample_rate)

        # Normalize volume
        if apply_normalize:
            audio = AudioProcessor.normalize_rms(audio, target_rms=0.1)

        # Apply fades (do last to ensure smooth transitions)
        if apply_fade:
            audio = AudioProcessor.apply_fade(audio, sample_rate)

        return audio


class VoicePipeline:
    """
    Manages TTS generation and audio assembly for dialogues.

    Uses Chatterbox Multilingual TTS to convert text to speech with
    voice cloning capabilities.
    """

    def __init__(self, device: str = "cpu"):
        """
        Initialize the voice pipeline with Chatterbox TTS.

        Args:
            device: Device to run the model on ("cpu" or "cuda")
        """
        self.device = device
        self.map_location = torch.device(device)

        # Patch torch.load to use the specified device
        self._patch_torch_load()

        print("[*] Loading ChatterboxMultilingualTTS model...")
        self.model = ChatterboxMultilingualTTS.from_pretrained(device=device)
        self.sr = self.model.sr
        print(f"[+] Model loaded successfully! Sample rate: {self.sr} Hz")

    def _patch_torch_load(self):
        """
        Patch torch.load to automatically use the configured device.
        This prevents CUDA errors when loading on CPU.
        """
        torch_load_original = torch.load

        def patched_torch_load(*args, **kwargs):
            if 'map_location' not in kwargs:
                kwargs['map_location'] = self.map_location
            return torch_load_original(*args, **kwargs)

        torch.load = patched_torch_load

    def generate_line(self,
                     text: str,
                     voice_path: str,
                     language_id: str = 'en',
                     exaggeration: float = 1.5,
                     cfg_weight: float = 0.5,
                     process_audio: bool = True,
                     normalize_text: bool = True) -> torch.Tensor:
        """
        Generate audio for a single dialogue line.

        Args:
            text: Text to convert to speech
            voice_path: Path to the voice template WAV file
            language_id: Language code ('en', 'it', 'es', 'fr', 'de', 'zh', 'ja', 'ko')
            exaggeration: Expression intensity (1.0-3.0, default 1.5 for natural sound)
            cfg_weight: Configuration weight (0.0-1.0, default 0.5)
            process_audio: Apply audio processing (de-essing, normalization, etc.)
            normalize_text: Normalize text (emails, URLs, etc.) for better pronunciation

        Returns:
            Audio tensor (1, num_samples)

        Raises:
            ValueError: If text is too short (less than 3 characters)
        """
        # Normalize text for better TTS pronunciation
        if normalize_text:
            original_text = text
            text = TextNormalizer.normalize_text(text, normalize_emails=True)
            if text != original_text:
                print(f"  [i] Text normalized for pronunciation")

        # Chatterbox TTS has issues with very short text
        if len(text.strip()) < 3:
            raise ValueError(
                f"Text too short for TTS generation: '{text}'. "
                f"Text must be at least 3 characters long."
            )

        text_preview = text[:50] + ('...' if len(text) > 50 else '')
        print(f"  [>] Generating: '{text_preview}'")

        wav = self.model.generate(
            text,
            audio_prompt_path=voice_path,
            exaggeration=exaggeration,
            cfg_weight=cfg_weight,
            language_id=language_id
        )

        # Apply audio processing to remove artifacts and improve naturalness
        if process_audio:
            wav = AudioProcessor.process_line(wav, self.sr)

        return wav

    def create_silence(self, duration_ms: int = 500) -> torch.Tensor:
        """
        Create silence between dialogue lines.

        Args:
            duration_ms: Duration of silence in milliseconds

        Returns:
            Silent audio tensor
        """
        silence_samples = int(self.sr * duration_ms / 1000)
        return torch.zeros(1, silence_samples)

    def dialogue_to_audio(self,
                         dialogue: List[Dict],
                         output_prefix: str = "conversation",
                         silence_between: int = 500,
                         language_id: str = 'en',
                         exaggeration: float = 1.5,
                         cfg_weight: float = 0.5,
                         save_individual: bool = True,
                         process_audio: bool = True,
                         normalize_text: bool = True) -> Path:
        """
        Convert dialogue turns into a single WAV file.

        Args:
            dialogue: List of dialogue turns from dialogue_generator
            output_prefix: Prefix for output filename (without extension)
            silence_between: Milliseconds of pause between lines (default 500ms)
            language_id: Language code for TTS
            exaggeration: Expression intensity (1.0-3.0, default 1.5 for natural sound)
            cfg_weight: Configuration weight (0.0-1.0)
            save_individual: If True, save each line as a separate file
            process_audio: Apply audio processing to remove artifacts (default True)
            normalize_text: Normalize text (emails, URLs) for better pronunciation (default True)

        Returns:
            Path to the generated WAV file

        Raises:
            ValueError: If dialogue list is empty
        """
        if not dialogue:
            raise ValueError("Dialogue list is empty. Cannot generate audio.")

        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        output_file = OUTPUT_DIR / f"{output_prefix}.wav"
        print(f"\n[*] Generating audio for {len(dialogue)} dialogue lines")

        # Create folder for individual lines if requested
        individual_folder = None
        if save_individual:
            individual_folder = OUTPUT_DIR / f"{output_prefix}_lines"
            individual_folder.mkdir(parents=True, exist_ok=True)
            print(f"[*] Saving individual lines to: {individual_folder}\n")

        # Generate audio for all lines
        audio_segments = []

        for i, line in enumerate(dialogue, 1):
            print(f"[{i}/{len(dialogue)}] {line['voice']}:")

            # Generate audio for this line
            wav = self.generate_line(
                text=line['text'],
                voice_path=line['voice_path'],
                language_id=language_id,
                exaggeration=exaggeration,
                cfg_weight=cfg_weight,
                process_audio=process_audio,
                normalize_text=normalize_text
            )

            # Save individual line if requested
            if save_individual and individual_folder:
                individual_file = self._save_individual_line(
                    wav, line, i, individual_folder
                )
                print(f"  [+] Saved: {individual_file.name}")

            audio_segments.append(wav)

            # Add pause between lines (except after the last line)
            if i < len(dialogue):
                silence = self.create_silence(silence_between)
                audio_segments.append(silence)

        # Concatenate all audio segments
        print("\n[*] Merging audio segments...")
        full_dialogue = torch.cat(audio_segments, dim=1)

        # Save the final audio file
        ta.save(str(output_file), full_dialogue, self.sr)

        # Calculate duration
        duration = full_dialogue.shape[1] / self.sr

        print(f"\n[+] Dialogue completed!")
        print(f"[+] File saved: {output_file}")
        print(f"[+] Duration: {duration:.2f} seconds")

        return output_file

    def _save_individual_line(self,
                             wav: torch.Tensor,
                             line: Dict,
                             index: int,
                             folder: Path) -> Path:
        """
        Save an individual dialogue line as a WAV file.

        Args:
            wav: Audio tensor
            line: Dialogue line dictionary
            index: Line number (1-indexed)
            folder: Directory to save the file

        Returns:
            Path to the saved file
        """
        # Create clean filename from text
        clean_text = re.sub(r'[^\w\s-]', '', line['text'][:30])
        clean_text = re.sub(r'\s+', '_', clean_text)

        filename = f"{index:03d}_{line['voice']}_{clean_text}.wav"
        filepath = folder / filename

        ta.save(str(filepath), wav, self.sr)
        return filepath


def create_dialogue_audio(dialogue: List[Dict],
                         output_prefix: str = "conversation",
                         silence_ms: int = 500,
                         language: str = 'en',
                         exaggeration: float = 1.5,
                         cfg_weight: float = 0.5,
                         save_individual: bool = True,
                         process_audio: bool = True,
                         normalize_text: bool = True,
                         device: str = "cpu") -> Path:
    """
    Convenience function to generate audio from dialogue data.

    Args:
        dialogue: List of dialogue turns
        output_prefix: Output filename prefix
        silence_ms: Milliseconds of pause between lines
        language: Language code ('en', 'it', 'es', 'fr', 'de', 'zh', 'ja', 'ko')
        exaggeration: Expression intensity (1.0-3.0, default 1.5 for natural sound)
        cfg_weight: Configuration weight (0.0-1.0, default 0.5)
        save_individual: Save each line separately
        process_audio: Apply audio processing to remove artifacts (default True)
        normalize_text: Normalize text (emails, URLs) for pronunciation (default True)
        device: Device to run on ("cpu" or "cuda")

    Returns:
        Path to the generated WAV file

    Example:
        >>> from app.dialogue_generator import load_dialogue
        >>> dialogue = load_dialogue("examples/conversation.txt")
        >>> output = create_dialogue_audio(dialogue, output_prefix="my_conversation")
    """
    pipeline = VoicePipeline(device=device)
    return pipeline.dialogue_to_audio(
        dialogue=dialogue,
        output_prefix=output_prefix,
        silence_between=silence_ms,
        language_id=language,
        exaggeration=exaggeration,
        cfg_weight=cfg_weight,
        save_individual=save_individual,
        process_audio=process_audio,
        normalize_text=normalize_text
    )
