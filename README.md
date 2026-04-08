# Visual Cryptography Scheme

This project implements a basic 2-out-of-2 visual cryptography scheme for black-and-white images.

## Features
- Converts an input image to binary
- Generates two secret shares
- Reconstructs the hidden image by overlaying the shares

## Concept
Each share individually reveals no meaningful information, but stacking both shares recovers the secret image.

## Run
```bash
pip install -r requirements.txt
python main.py
