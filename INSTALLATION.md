# Installation Guide

## Prerequisites

- Python 3.8 or higher
- Webcam or camera device
- AMD Ryzen AI PC (recommended for optimal performance)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/faffonfokhan/Assistive-Communication-Device-for-Speech-Impairments.git
cd Assistive-Communication-Device-for-Speech-Impairments
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Install AMD ROCm Support

If you have an AMD Ryzen AI PC, you can install ROCm support for better performance:

```bash
# Follow AMD ROCm installation guide for your platform
# https://rocm.docs.amd.com/en/latest/deploy/linux/quick_start.html
```

### 5. (Optional) Setup Llama 2 Access

To use Llama 2 models, you need to:

1. Create a HuggingFace account at https://huggingface.co
2. Request access to Llama 2 models at https://huggingface.co/meta-llama
3. Generate an access token at https://huggingface.co/settings/tokens
4. Login using the token:

```bash
huggingface-cli login
```

## Verification

Test your installation:

```bash
python main.py --help
```

## Troubleshooting

### Camera Not Detected

- Check if your camera is connected and working
- Try different camera IDs: `python main.py --camera 1`
- On Linux, ensure you have permissions: `sudo usermod -a -G video $USER`

### MediaPipe Installation Issues

If MediaPipe fails to install, try:

```bash
pip install --upgrade pip
pip install mediapipe --no-cache-dir
```

### Llama 2 Model Loading Issues

- Ensure you have sufficient RAM (16GB+ recommended)
- Use a smaller model variant if needed
- Check your HuggingFace authentication

### AMD Ryzen AI Support

- Ensure ROCm drivers are properly installed
- Set environment variable: `export HSA_OVERRIDE_GFX_VERSION=11.0.0`
- Check AMD ROCm documentation for your specific GPU

## Next Steps

See [USAGE.md](USAGE.md) for detailed usage instructions.
