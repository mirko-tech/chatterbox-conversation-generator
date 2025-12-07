# TODO

Quick list of what's next for Chatterbox Dialogue Generator.

If you want to tackle something, just open an issue or PR — we're flexible.

---

## 🔥 High Impact (Do These First)

- [ ] **Number normalization** - "123" → "one hundred twenty-three"
- [ ] **Currency formatting** - "$50.99" → "fifty dollars and ninety-nine cents"
- [ ] **Date/time formatting** - "12/25/2024" → "December twenty-fifth"
- [ ] **Unit tests** - pytest suite for normalizations and audio processing
- [ ] **Better error messages** - Make errors actually helpful

## 🎯 Audio Quality

- [ ] **Dynamic range compression** - Even out volume peaks
- [ ] **Noise gate** - Remove silence/background below threshold
- [ ] **Crossfade between lines** - Instead of hard silence cuts
- [ ] **Voice activity detection (VAD)** - Auto-trim silence at edges
- [ ] **EQ presets** - "podcast", "radio", "natural" modes

## 💡 Features People Want

- [ ] **Background music mixing** - Add ambient audio
- [ ] **MP3/FLAC export** - Not just WAV
- [ ] **Stereo panning** - Place speakers left/right
- [ ] **Batch processing** - Multiple files at once
- [ ] **Progress bar** - See generation progress
- [ ] **Config files** - YAML/JSON for defaults

## 🧪 Text Normalization

- [ ] **Abbreviations** - "Dr." → "Doctor", "Inc." → "Incorporated"
- [ ] **Units** - "5km" → "five kilometers"
- [ ] **Hashtags/mentions** - "#AI" → "hashtag AI"
- [ ] **Emoji to text** - "😊" → "smiling face"

## 🔬 Advanced (Experimental)

- [ ] **Emotion tags** - `[happy]`, `[sad]`, `[excited]` in dialogue
- [ ] **Prosody control** - `[pause:500ms]`, `[speed:fast]`
- [ ] **Per-speaker settings** - Different exaggeration per voice
- [ ] **Voice mixing** - Blend multiple voice samples
- [ ] **GPU optimization** - Better CUDA memory handling
- [ ] **Streaming generation** - Start playback while generating

## 🐛 Known Issues

- [ ] Long conversations can cause memory issues
- [ ] Special characters in filenames sometimes fail
- [ ] No progress indicator on first model download
- [ ] Deprecation warnings from dependencies (non-critical)

## 📚 Documentation

- [ ] Video tutorial
- [ ] Best practices guide for voice recording
- [ ] More example dialogue files
- [ ] FAQ section
- [ ] Architecture deep-dive

---

## ✅ Recently Done

**v0.2.0:**
- ✅ Audio processing (de-essing, normalization, fades)
- ✅ Email/URL/phone normalization
- ✅ Lower default exaggeration (2.0 → 1.5)
- ✅ Text normalization framework

**v0.1.0:**
- ✅ Basic TTS generation
- ✅ Voice cloning support
- ✅ 8 languages
- ✅ CLI interface

---

## 🗺️ Rough Roadmap

**v0.3** - Text normalization (numbers, currency, dates)
**v0.4** - Audio quality (compression, formats, presets)
**v0.5** - Advanced features (emotions, prosody, stereo)
**v1.0** - Production ready (tests, docs, stable API)

---

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)

Got an idea not listed here? Open an issue — we're open to anything.
