<div align="center">

![Chatterbox Dialogue Generator Banner](assets/banner.png)

[![Python Versions](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Open Issues](https://img.shields.io/github/issues/mirko-tech/chatterbox-conversation-generator)](https://github.com/mirko-tech/chatterbox-conversation-generator/issues)
[![Stars](https://img.shields.io/github/stars/mirko-tech/chatterbox-conversation-generator?style=social)](https://github.com/mirko-tech/chatterbox-conversation-generator)

**Generate AI Conversations with Voice Cloning & Natural Audio Processing**

</div>

---

## 🎧 What Is This?

A lightweight tool that turns simple text dialogues into **natural-sounding, multi-speaker audio** using Chatterbox TTS voice cloning.

**Think:**
- 🎙️ AI podcasts
- 💬 Realistic synthetic dialogues
- 🎮 Game NPC voices
- 📞 Customer support simulations
- 🌍 Language learning audio
- 🗣️ Voice cloned conversation generators

**Write:**
```
voice1="Hello!"
voice2="How are you?"
```

**Get** a full WAV conversation with fades, de-essing, normalized audio, silence timing, and cloned voices.

---

## ⭐ Why It's Different

Most TTS tools generate single lines.
**This one generates full conversations** — processed like real audio.

✅ Voice cloning from short samples
✅ Natural pauses between speakers
✅ De-essing & loudness normalization
✅ Smooth fade-in/out transitions
✅ High-pass filter to remove breathing noise
✅ Multi-language support (8 languages)
✅ Save individual lines separately
✅ Fine control (exaggeration, silence, device)

---

## 🎬 Demo

![Demo Conversation](assets/demo.gif)

---

## ⚡ Quick Start

```bash
python -m app.main examples/sample_conversation.txt
```

**Outputs:**
```
outputs/
  conversation.wav
  conversation_lines/
    001_voice1_Hello.wav
    002_voice2_How_are_you.wav
```

---

## 📦 Installation

**IMPORTANT:** Requires Python 3.11 or 3.12 (Python 3.13+ not yet supported)

### Windows
```bash
git clone https://github.com/mirko-tech/chatterbox-conversation-generator.git
cd chatterbox-conversation-generator
py -3.11 -m venv .venv
.venv\Scripts\activate
install_dependencies.bat
```

### macOS / Linux
```bash
git clone https://github.com/mirko-tech/chatterbox-conversation-generator.git
cd chatterbox-conversation-generator
python3.11 -m venv .venv
source .venv/bin/activate
chmod +x install_dependencies.sh
./install_dependencies.sh
```

### Manual Installation (Alternative)

If the scripts fail:

```bash
# 1. Setup virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Upgrade pip
python -m pip install --upgrade pip setuptools wheel

# 3. Install dependencies in order
pip install torch==2.6.0 torchaudio==2.6.0 numpy==1.24.0 pydub==0.25.1
pip install chatterbox-tts --no-deps
pip install resemble-perth==1.0.1 librosa==0.10.0 safetensors==0.5.3 s3tokenizer pykakasi==2.3.0
pip install transformers==4.46.3 diffusers==0.29.0 gradio==5.44.1 conformer==0.3.2
pip install pkuseg==0.0.25
```

---

## ✍️ Dialogue Format

Create a text file with your conversation:

```
voice1_wav="voices/mario.wav"
voice2_wav="voices/anna.wav"

voice1="Good morning!"
voice2="Did you sleep well?"
voice1="Not really… too much coding."
```

Voice files can be WAV or FLAC. Even short samples (5-10 seconds) work great for voice cloning.

---

## 🧠 Usage

```bash
python -m app.main <dialogue_file> [options]
```

### Options

| Option | Description | Default |
|--------|-------------|---------|
| `-o, --output` | Output filename prefix | `conversation` |
| `-s, --silence` | Silence between lines (ms) | `500` |
| `-l, --language` | Language code (en, it, es, fr, de, zh, ja, ko) | `en` |
| `-e, --exaggeration` | Expression intensity (1.0-3.0) | `1.5` |
| `-c, --cfg-weight` | Configuration weight (0.0-1.0) | `0.5` |
| `--no-individual` | Skip saving individual lines | `false` |
| `--no-processing` | Disable audio processing (de-essing, normalization, fades) | `false` |
| `-d, --device` | Device to use (cpu or cuda) | `cpu` |

### Examples

**Basic usage:**
```bash
python -m app.main examples/sample_conversation.txt
```

**Custom settings:**
```bash
python -m app.main debate.txt --output debate_audio --silence 700 --exaggeration 1.2
```

**Italian dialogue:**
```bash
python -m app.main dialogo.txt --language it
```

**Disable audio processing (raw TTS output):**
```bash
python -m app.main conversation.txt --no-processing
```

---

## 🔊 Audio Processing Pipeline

What makes conversations sound natural:

1. **High-pass filter (80Hz)** - Removes low-frequency breathing and rumble
2. **De-essing (5-8kHz, -6dB)** - Reduces harsh sibilants (S, SH, Z sounds)
3. **RMS normalization** - Equalizes volume levels between speakers
4. **Fade-in/out** - Smooth transitions (10ms in, 50ms out)
5. **Smart silence stitching** - Natural pauses between turns
6. **Email/URL normalization** - Converts `john@example.com` to "john at example dot com"

All processing is automatic but can be disabled with `--no-processing`.

---

## 🧩 Project Structure

```
chatterbox-conversation-generator/
├── app/
│   ├── __init__.py              # Package initialization
│   ├── dialogue_generator.py   # Dialogue parsing
│   ├── voice_pipeline.py        # TTS generation & audio processing
│   └── main.py                  # CLI interface
├── voices/                      # Your voice template files (add your own)
├── outputs/                     # Generated audio files
├── examples/                    # Example dialogue files
│   └── sample_conversation.txt
├── install_dependencies.bat     # Windows installation script
├── install_dependencies.sh      # macOS/Linux installation script
├── requirements.txt
├── CONTRIBUTING.md
├── TODO.md
└── README.md
```

---

## 🐍 Programmatic Usage

You can use the package in your Python code:

```python
from app.dialogue_generator import load_dialogue
from app.voice_pipeline import create_dialogue_audio

# Load dialogue from file
dialogue = load_dialogue("examples/sample_conversation.txt")

# Generate audio with processing
output_path = create_dialogue_audio(
    dialogue=dialogue,
    output_prefix="my_dialogue",
    silence_ms=500,
    language='en',
    exaggeration=1.5,
    process_audio=True  # Enable de-essing, normalization, fades
)

print(f"Audio saved to: {output_path}")
```

---

## 🌍 Language Support

Supported languages:
- 🇬🇧 `en` - English
- 🇮🇹 `it` - Italian
- 🇪🇸 `es` - Spanish
- 🇫🇷 `fr` - French
- 🇩🇪 `de` - German
- 🇨🇳 `zh` - Chinese
- 🇯🇵 `ja` - Japanese
- 🇰🇷 `ko` - Korean

---

## 🎤 Voice Recording Tips

For best results with voice cloning:

- **Length:** 5-10 seconds minimum
- **Quality:** Clear audio, minimal background noise
- **Format:** WAV or FLAC preferred
- **Content:** Natural speech, not reading robotically
- **Consistency:** Single speaker, consistent volume

---

## ❗ Troubleshooting

### Python Version Issues

**Error:** `numpy` or `setuptools` compatibility issues
**Solution:** Make sure you're using Python 3.11 or 3.12, not 3.13+

```bash
python --version  # Should show 3.11.x or 3.12.x
```

### Installation Script Fails

**Solution:** Use manual installation method (see above) or check:
- Virtual environment is activated
- Python version is correct
- Internet connection is stable for model downloads

### Text Too Short Error

**Error:** `Text too short for TTS generation`
**Solution:** Ensure all dialogue lines are at least 3 characters long

```
# ❌ Bad
voice1="Hi"

# ✅ Good
voice1="Hi there!"
```

### Email/URL Not Pronounced Correctly

**Solution:** Text normalization is enabled by default. Emails like `john.doe@example.com` are automatically converted to "john dot doe at example dot com"

To disable: Pass `normalize_text=False` in programmatic usage

### Model Download Takes Forever

**Info:** On first run, Chatterbox downloads ~2GB of model files from HuggingFace. This is normal and only happens once. The files are cached locally.

### Sibilant/Breathing Artifacts

**Solution:** Audio processing is enabled by default to fix this. If you still hear artifacts:
- Lower `--exaggeration` to 1.2 or 1.0
- Increase `--silence` to 700-1000ms for more natural pauses
- Check your voice template files for breathing sounds
- Ensure processing is enabled (don't use `--no-processing`)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

**Quick ways to help:**
- 🐛 Report bugs
- 💡 Suggest features
- 📄 Improve documentation
- 🎨 Add examples
- 🧪 Write tests
- 🔧 Fix issues

Check [TODO.md](TODO.md) for planned features and improvements.

---

## ⭐ Support the Project

If this tool helps you, consider starring the repo — it motivates development and helps others discover it.

**📌 [Star the project ⭐](https://github.com/mirko-tech/chatterbox-conversation-generator)** — takes 2 seconds
**📌 [Open an issue](https://github.com/mirko-tech/chatterbox-conversation-generator/issues)** — even ideas are welcome
**📌 [Create a PR](https://github.com/mirko-tech/chatterbox-conversation-generator/pulls)** — small improvements appreciated

---

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

## 🙏 Credits

This project uses [Chatterbox TTS](https://github.com/resemble-ai/chatterbox) for voice generation.

Built with ❤️ by the open source community.

---

**Made something cool with this tool? Share it in [Discussions](https://github.com/mirko-tech/chatterbox-conversation-generator/discussions)!**
