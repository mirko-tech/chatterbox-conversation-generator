"""
Chatterbox Dialogue Generator - Main CLI Entry Point

A tool for generating synthetic dialogues and converting them to audio
using Chatterbox TTS voice cloning.

Usage:
    python -m apps.api.main <dialogue_file> [options]

Example:
    python -m apps.api.main examples/conversation.txt --output my_dialogue --silence 700
"""

import argparse
import sys
from pathlib import Path


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        Parsed argument namespace
    """
    parser = argparse.ArgumentParser(
        description="Generate audio dialogues using Chatterbox TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage
  python -m apps.api.main conversation.txt

  # Custom output name and longer pauses
  python -m apps.api.main debate.txt --output debate_audio --silence 700

  # Italian dialogue with custom voice settings
  python -m apps.api.main dialogo.txt --language it --exaggeration 2.5

  # Don't save individual lines
  python -m apps.api.main quick.txt --no-individual
        """
    )

    parser.add_argument(
        'dialogue_file',
        type=str,
        help='Path to dialogue text file'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='conversation',
        help='Output filename prefix (default: conversation)'
    )

    parser.add_argument(
        '-s', '--silence',
        type=int,
        default=500,
        help='Milliseconds of silence between lines (default: 500)'
    )

    parser.add_argument(
        '-l', '--language',
        type=str,
        default='en',
        choices=['en', 'it', 'es', 'fr', 'de', 'zh', 'ja', 'ko'],
        help='Language code (default: en)'
    )

    parser.add_argument(
        '-e', '--exaggeration',
        type=float,
        default=1.5,
        help='Expression intensity, 1.0-3.0 (default: 1.5 for natural sound)'
    )

    parser.add_argument(
        '-c', '--cfg-weight',
        type=float,
        default=0.5,
        help='Configuration weight, 0.0-1.0 (default: 0.5)'
    )

    parser.add_argument(
        '--no-individual',
        action='store_true',
        help='Do not save individual dialogue lines as separate files'
    )

    parser.add_argument(
        '--no-processing',
        action='store_true',
        help='Disable audio processing (de-essing, normalization, fades)'
    )

    parser.add_argument(
        '-d', '--device',
        type=str,
        default='cpu',
        choices=['cpu', 'cuda'],
        help='Device to run on (default: cpu)'
    )

    return parser.parse_args()


def validate_arguments(args):
    """
    Validate command-line arguments.

    Args:
        args: Parsed arguments namespace

    Raises:
        ValueError: If arguments are invalid
    """
    # Check if dialogue file exists
    dialogue_path = Path(args.dialogue_file)
    if not dialogue_path.exists():
        raise FileNotFoundError(
            f"Dialogue file not found: {args.dialogue_file}\n"
            f"Please provide a valid path to a dialogue text file."
        )

    # Validate exaggeration range
    if not (1.0 <= args.exaggeration <= 3.0):
        raise ValueError(
            f"Exaggeration must be between 1.0 and 3.0, got: {args.exaggeration}"
        )

    # Validate cfg_weight range
    if not (0.0 <= args.cfg_weight <= 1.0):
        raise ValueError(
            f"CFG weight must be between 0.0 and 1.0, got: {args.cfg_weight}"
        )

    # Validate silence duration
    if args.silence < 0:
        raise ValueError(
            f"Silence duration must be non-negative, got: {args.silence}"
        )


def main():
    """
    Main entry point for the dialogue generator.
    """
    try:
        # Parse and validate arguments
        args = parse_arguments()
        validate_arguments(args)

        # Import heavy dependencies only when needed
        from apps.api.dialogue_generator import load_dialogue
        from apps.api.voice_pipeline import create_dialogue_audio

        print("=" * 60)
        print("Chatterbox Dialogue Generator")
        print("=" * 60)

        # Step 1: Load and parse dialogue
        print(f"\n[*] Loading dialogue from: {args.dialogue_file}")
        dialogue = load_dialogue(args.dialogue_file)
        print(f"[+] Parsed {len(dialogue)} dialogue turns")

        # Print dialogue summary
        print("\n[*] Dialogue preview:")
        for i, turn in enumerate(dialogue[:3], 1):
            text_preview = turn['text'][:60] + ('...' if len(turn['text']) > 60 else '')
            print(f"  {i}. {turn['voice']}: {text_preview}")
        if len(dialogue) > 3:
            print(f"  ... and {len(dialogue) - 3} more turns")

        # Step 2: Generate audio
        print(f"\n[*] Generating audio with Chatterbox TTS...")
        print(f"   Language: {args.language}")
        print(f"   Silence between turns: {args.silence}ms")
        print(f"   Exaggeration: {args.exaggeration}")
        print(f"   Audio processing: {'disabled' if args.no_processing else 'enabled (de-essing, normalization, fades)'}")
        print(f"   Device: {args.device}")

        output_path = create_dialogue_audio(
            dialogue=dialogue,
            output_prefix=args.output,
            silence_ms=args.silence,
            language=args.language,
            exaggeration=args.exaggeration,
            cfg_weight=args.cfg_weight,
            save_individual=not args.no_individual,
            process_audio=not args.no_processing,
            device=args.device
        )

        # Success message
        print("\n" + "=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print(f"[+] Audio saved to: {output_path.absolute()}")

        if not args.no_individual:
            lines_folder = output_path.parent / f"{args.output}_lines"
            print(f"[+] Individual lines: {lines_folder.absolute()}")

        print("\nYou can now play the audio file with your favorite audio player.")

    except FileNotFoundError as e:
        print(f"\n[-] Error: {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        print(f"\n[-] Invalid argument: {e}", file=sys.stderr)
        sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n[!] Generation interrupted by user.", file=sys.stderr)
        sys.exit(130)

    except Exception as e:
        print(f"\n[-] Unexpected error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
