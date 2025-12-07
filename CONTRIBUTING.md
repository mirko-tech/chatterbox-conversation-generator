# Contributing to Chatterbox Dialogue Generator

Thanks for thinking about contributing!
This project is meant to be simple, fun, and easy to hack on — so contributions of any size are welcome.

## 🚀 Ways You Can Contribute (Pick One!)

### 1. Fix Something

Check the list:
- ❗ Bugs
- 📄 Documentation improvements
- 🧪 Test coverage (even small!)

👉 Issues marked `good first issue` are perfect if you're new.

### 2. Add Something Cool

Examples:
- Background audio mixing
- Better normalization (dates, numbers, abbreviations)
- New languages
- Voice presets
- Text formatting improvements

If you're not sure whether your idea fits, open an issue — we'll try to respond fast.

### 3. Improve Audio Quality

If you know anything about:
- DSP
- Voice cloning
- TTS artifacts
- Compression
- Resampling

...your input is gold 🔥

## 🛠️ Local Dev Setup (Quickest Version)

**Requirements:**
- Python 3.11 or 3.12
- Virtualenv
- Git
- A GPU is not required (CPU works fine)

**Setup:**
```bash
git clone https://github.com/YOUR_USERNAME/chatterbox-conversation-generator.git
cd chatterbox-conversation-generator

python3.11 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Use the installation script (recommended)
./install_dependencies.sh   # macOS/Linux
# or
install_dependencies.bat    # Windows
```

**Test It Works:**
```bash
python -m app.main examples/sample_conversation.txt
```

If audio appears in `/outputs`, you're ready.

## 📐 Code Style (Simple Rules)

- PEP8-ish, but don't obsess
- Type hints encouraged
- Docstrings appreciated
- Keep functions small and clear
- Prefer readability over cleverness
- Avoid breaking changes unless discussed

## 🧪 Testing

No test suite yet — PR welcome 😅

For now:
```bash
python -m app.main examples/sample_conversation.txt
```

Test:
- Different languages
- Different pauses
- Actual voice templates
- Edge cases (emails, URLs, special chars)

## 🔄 Submit a Pull Request

**Create a branch:**
```bash
git checkout -b feature/your-feature
```

**Commit:**
```bash
git commit -m "feat: short description"
```

Use prefixes:
- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `perf:` - Performance improvement

**Push:**
```bash
git push origin feature/your-feature
```

**Open PR on GitHub.**

Please include:
- What it does
- Why it helps
- Before/after audio if relevant

We're not picky — even small PRs matter.

## 🐛 Reporting Issues

Include:
- OS & Python version
- Exact command you ran
- Audio result or error
- Dialogue file used

We prefer audio samples when debugging voice issues.

## ❤️ Recognition

All contributors appear in:
- GitHub Contributors list
- Release notes for major contributions
- We highlight standout PRs in the README

## 📜 License

By contributing, you agree your code is licensed under this project's license.

---

That's it. Keep it simple. Hack freely.

Thanks for helping build something fun 🎙️🔥
