#!/bin/bash

echo "========================================"
echo "Chatterbox Dialogue Generator"
echo "Dependency Installation Script"
echo "========================================"
echo ""

echo "Step 1: Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to upgrade pip"
    exit 1
fi
echo ""

echo "Step 2: Installing core dependencies (torch, numpy, etc.)..."
pip install torch==2.6.0 torchaudio==2.6.0 numpy==1.24.0 pydub==0.25.1
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install core dependencies"
    exit 1
fi
echo ""

echo "Step 3: Installing Chatterbox TTS without dependencies..."
pip install chatterbox-tts --no-deps
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install chatterbox-tts"
    exit 1
fi
echo ""

echo "Step 4: Installing remaining dependencies in order..."
pip install resemble-perth==1.0.1
pip install librosa==0.10.0
pip install safetensors==0.5.3
pip install s3tokenizer
pip install pykakasi==2.3.0
echo ""

echo "Step 5: Installing transformers and diffusers..."
pip install transformers==4.46.3
pip install diffusers==0.29.0
pip install gradio==5.44.1
pip install conformer==0.3.2
echo ""

echo "Step 6: Installing pkuseg (requires numpy already installed)..."
pip install pkuseg==0.0.25
if [ $? -ne 0 ]; then
    echo "WARNING: pkuseg failed to install, but this may not be critical"
    echo "Continuing..."
fi
echo ""

echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo ""
echo "Testing installation..."
python -m app.main -h
if [ $? -ne 0 ]; then
    echo ""
    echo "WARNING: There may be missing dependencies."
    echo "Try running the script again or install manually."
else
    echo ""
    echo "SUCCESS! The installation is complete."
    echo "You can now use: python -m app.main examples/sample_conversation.txt"
fi
echo ""
