# Quick Start Guide

Get up and running with the Assistive Communication Device in 5 minutes!

## Prerequisites

- Python 3.8+
- Webcam
- (Optional) AMD Ryzen AI PC for best performance

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/faffonfokhan/Assistive-Communication-Device-for-Speech-Impairments.git
cd Assistive-Communication-Device-for-Speech-Impairments
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Installation may take a few minutes as it includes OpenCV, MediaPipe, and other libraries.

### 3. Verify Installation

```bash
python test_structure.py
```

You should see "✓ All tests passed!"

## Running the Application

### Basic Mode (Without Llama 2)

```bash
python main.py
```

When prompted to load Llama 2, type `n` and press Enter.

### What to Expect

1. **Camera Window Opens**: You'll see yourself on screen
2. **Face Detection**: Green dots appear around your lips
3. **Movement Detection**: Numbers show lip movement magnitude
4. **Text Display**: Recognized text appears at the bottom

### Controls

- **Press `q`**: Quit the application
- **Press `s`**: Speak the current recognized text
- **Press `r`**: Reset and clear the text buffer

## Testing Components

Run the demo script to test individual components:

```bash
python demo.py
```

This tests each module independently and reports any issues.

## Troubleshooting

### Camera Not Working

```bash
# Try different camera ID
python main.py --camera 1
```

### Dependencies Not Installed

```bash
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Low Performance

- Reduce camera resolution in `config/default_config.json`
- Close other applications
- Ensure good lighting for face detection

## Next Steps

- Read [USAGE.md](USAGE.md) for detailed features
- See [INSTALLATION.md](INSTALLATION.md) for advanced setup
- Check [ARCHITECTURE.md](ARCHITECTURE.md) to understand the system

## Using Llama 2 (Advanced)

For advanced text generation with Llama 2:

1. Create HuggingFace account: https://huggingface.co
2. Request Llama 2 access: https://huggingface.co/meta-llama/Llama-2-7b-chat-hf
3. Generate token: https://huggingface.co/settings/tokens
4. Login:
   ```bash
   pip install huggingface-hub
   huggingface-cli login
   ```
5. Run with Llama 2:
   ```bash
   python main.py
   # Answer 'y' when prompted to load model
   ```

**Note**: First run will download ~13GB model. Requires 16GB+ RAM.

## Getting Help

- Check documentation in the repo
- Open an issue on GitHub
- See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines

---

**Happy communicating!** 🎉
