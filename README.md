# Image Steganography System

A beginner-friendly Python application that hides secret text messages inside digital images and extracts them later using **Least Significant Bit (LSB) steganography**.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [How It Works](#how-it-works)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Algorithm Details](#algorithm-details)
- [Testing](#testing)
- [Limitations](#limitations)
- [FAQ](#faq)

---

## Overview

**Steganography** is the practice of hiding information within other data. This project uses the **LSB (Least Significant Bit)** technique to encode secret messages within digital images.

Unlike encryption, steganography doesn't encrypt the message—it hides the message itself. This makes the communication less conspicuous than encrypted messages.

### Key Characteristics
- **Non-destructive**: Uses PNG format (lossless) to preserve hidden data
- **Simple and Educational**: Easy to understand and explain
- **Beginner-friendly**: Clean code with detailed comments
- **GUI-based**: No command-line knowledge required

---

## Features

### ✅ Hide Messages
- Select any PNG image as the cover
- Enter any secret message (text, Unicode, special characters)
- Automatic capacity checking
- Saves the modified image without overwriting the original

### ✅ Extract Messages
- Load an image with a hidden message
- Automatically extracts and displays the secret message
- Handles errors gracefully

### ✅ User Interface
- Clean, tabbed Tkinter interface
- Real-time capacity indicator
- Status messages for user feedback
- Copy-to-clipboard functionality

### ✅ Unicode Support
- Supports emojis, accented characters, and non-Latin scripts
- All text is encoded as UTF-8

---

## How It Works

### The LSB Technique Explained

Every digital image is made of pixels, and each pixel has three color channels: Red (R), Green (G), and Blue (B). Each channel stores a value from 0 to 255.

For example:
- Pure red pixel: (255, 0, 0)
- Light gray pixel: (192, 192, 192)

Each value is stored in 8 bits: `11000000` for 192.

**The LSB technique modifies only the least significant bit (rightmost bit)** of each channel:
- `11000000` → `11000001` (LSB changed from 0 to 1)
- This change is invisible to the human eye but can be detected by software

### Hiding Process

1. **Convert message to UTF-8 bytes**
   - "Hi" → [0x48, 0x69] → [01001000, 01101001]

2. **Prepend length (4 bytes)**
   - Message length 2 → [0x00, 0x00, 0x00, 0x02]
   - Full data: [0x00, 0x00, 0x00, 0x02, 0x48, 0x69]

3. **Convert all bytes to bits**
   - 6 bytes = 48 bits: `0000000000000000000000000010010010000110101001...`

4. **Embed bits into image pixels**
   - Pixel 1 (RGB): [255, 128, 64] → [255, 128, 64] (embed 0, 0, 1)
   - Pixel 2 (RGB): [200, 100, 50] → [200, 100, 50] (embed 0, 0, 1)
   - Continue until all bits are embedded

5. **Save the modified image**
   - Save as PNG (lossless format)

### Extraction Process

1. **Load the image**
2. **Extract LSB from every pixel channel** (in same order as hiding)
3. **Convert first 32 bits to get message length**
4. **Extract next (length × 8) bits**
5. **Convert bits to bytes and decode as UTF-8**
6. **Display the message**

---

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download
```bash
cd ~/Downloads/Image\ Steganography
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- **Pillow** (PIL): For image processing

### Step 3: Verify Installation
```bash
python3 -c "from PIL import Image; print('✓ Pillow installed successfully')"
python3 -c "import tkinter; print('✓ Tkinter available')"
```

---

## Usage

### Running the Application

```bash
python3 main.py
```

This opens the Tkinter GUI.

### Hiding a Message

1. Go to the **"Hide Message"** tab
2. Click **"Browse"** and select a PNG image
3. Enter your secret message in the text box
4. Observe the capacity indicator to ensure your message fits
5. Click **"Hide Message"**
6. Choose a location to save the image (e.g., `secret.png`)
7. Success! The image now contains your hidden message

### Extracting a Message

1. Go to the **"Extract Message"** tab
2. Click **"Browse"** and select the image with the hidden message
3. Click **"Extract Message"**
4. The message appears in the text box
5. (Optional) Click **"Copy to Clipboard"** to copy the message

---

## Project Structure

```
Image Steganography/
├── main.py                    # GUI application (Tkinter)
├── steganography.py           # Core LSB encoding/decoding logic
├── image_utils.py             # Image loading, validation, saving
├── test_steganography.py      # Unit tests
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

### File Descriptions

| File | Purpose |
|------|---------|
| `main.py` | Tkinter GUI with Hide and Extract tabs |
| `steganography.py` | LSB algorithm implementation |
| `image_utils.py` | Image I/O and validation helpers |
| `test_steganography.py` | 12 unit tests covering all scenarios |
| `requirements.txt` | Dependencies (Pillow) |

---

## Algorithm Details

### Data Format

The hidden message is stored in the following format:

```
[Length Prefix (4 bytes)][Message Bytes]
    ↓
[0x00 0x00 0x00 0x05]  "Hello"
    ↓
Message length = 5 bytes
```

### Bit Embedding

Each pixel has 3 channels (R, G, B). We embed one bit per channel:

```
Pixel 1:  [R, G, B] → embed bits [b0, b1, b2]
Pixel 2:  [R, G, B] → embed bits [b3, b4, b5]
Pixel 3:  [R, G, B] → embed bits [b6, b7, b8]
...
```

### Capacity Calculation

For an image of size W × H pixels:
- Total channels = W × H × 3 (RGB)
- Total bits = W × H × 3
- Total bytes = (W × H × 3) / 8
- **Max message = Total bytes - 4 bytes** (4 bytes reserved for length prefix)

**Example**: A 200×200 PNG image:
- Total bytes = (200 × 200 × 3) / 8 = 15,000 bytes
- Max message = 15,000 - 4 = **14,996 bytes** ≈ 14.6 KB

### Why PNG and Not JPEG?

- **PNG**: Lossless compression. Every pixel is preserved exactly.
- **JPEG**: Lossy compression. Image quality is sacrificed for file size. Hidden bits are destroyed during compression.

**Recommendation**: Always use PNG for cover images and output.

---

## Testing

### Running Tests

```bash
python3 test_steganography.py
```

### Test Cases

The test suite includes 12 tests:

1. **Simple message** - Basic hide and extract
2. **Empty message** - Handling empty strings
3. **Unicode text** - Emojis and non-Latin characters
4. **Long message** - Message near capacity
5. **Message capacity** - Exceeding image capacity (should fail)
6. **Max capacity** - Message at maximum size
7. **Original unchanged** - Verify original image is not modified
8. **Different messages** - Different messages produce different images
9. **Clean image extraction** - Extracting from image without message (error handling)
10. **Save and load workflow** - Complete pipeline test
11. **Special characters** - Punctuation and symbols
12. **Whitespace preservation** - Newlines and tabs

### Expected Output

```
============================================================
IMAGE STEGANOGRAPHY - UNIT TESTS
============================================================

test_hide_and_extract_simple_message (__main__.TestSteganography) ... ok
test_hide_and_extract_empty_message (__main__.TestSteganography) ... ok
...
============================================================
Tests Run: 12
Failures: 0
Errors: 0
============================================================
```

---

## Limitations

### 🔴 Important Security Disclaimer

**LSB steganography is NOT cryptographically secure!**

1. **No Encryption**: The message is hidden but not encrypted. Someone with knowledge of LSB steganography can easily extract it.
2. **Detectable**: Statistical analysis (steganalysis) can reveal the presence of hidden data.
3. **Small Capacity**: Limited to ~50% of image file size as message.
4. **Reversible**: The original image can be recovered by extracting LSBs.

**Use Cases**:
- ✓ Educational projects
- ✓ Hiding low-sensitivity information
- ✗ Securing confidential/classified data
- ✗ Bypassing security systems

### 🟡 Technical Limitations

1. **PNG Only**: JPEG and other lossy formats will corrupt the message.
2. **Image Resizing**: Resizing the image will destroy the hidden message.
3. **Image Rotation**: Rotating more than 90° will corrupt the message.
4. **Compression**: Re-saving or re-compressing will destroy the message.
5. **Color Depth**: Images must be convertible to RGB mode.

### 📊 Capacity Constraints

- Small images (100×100): ~375 bytes capacity
- Medium images (500×500): ~9.4 KB capacity
- Large images (2000×2000): ~150 KB capacity

---

## FAQ

### Q: Can I use JPEG images?
**A:** Not recommended. JPEG uses lossy compression, which destroys the hidden message. Use PNG or BMP instead.

### Q: What happens if I resize or rotate the image?
**A:** The hidden message will be corrupted and cannot be extracted. Always preserve the exact image.

### Q: Can someone tell if a message is hidden?
**A:** Not easily with the naked eye. However, statistical analysis can reveal the presence of hidden data. This is different from encryption, where data remains secure.

### Q: How much can I hide?
**A:** It depends on image size:
- A 200×200 PNG can hide ~15 KB
- A 1000×1000 PNG can hide ~375 KB

Use the GUI indicator to check capacity.

### Q: Can I hide non-text data (like images)?
**A:** Currently, the system hides text only. You can encode images as base64 text and hide them, but this reduces capacity significantly.

### Q: Is my original image modified?
**A:** No. The application always creates a new output file without modifying the original.

### Q: Can I extract a message without knowing it's there?
**A:** Not easily. The system needs to know to extract. If you save a stego image and forget, the message remains hidden.

### Q: What about Unicode and special characters?
**A:** Fully supported. All text is encoded as UTF-8, so emojis (🔒), accented characters (é, ñ), and all languages work.

---

## Troubleshooting

### Issue: "Message too large"
**Solution**: Use a larger image. Check the capacity indicator in the GUI.

### Issue: "Failed to load image"
**Solution**: Ensure the file is a valid PNG image. Try opening it in an image viewer first.

### Issue: "Failed to decode message as UTF-8"
**Solution**: The image may not contain a hidden message or the message is corrupted. Try a different image.

### Issue: "Tkinter not found"
**Solution**: Install Tkinter:
```bash
# macOS
brew install python-tk

# Ubuntu/Debian
sudo apt-get install python3-tk

# Windows
# Tkinter comes bundled with Python
```

---

## How to Explain This Project in a Viva

### Short Explanation (1 minute)
"This is an Image Steganography application that hides secret text messages inside PNG images using LSB (Least Significant Bit) technique. The LSB method modifies only the least significant bit of pixel values, which is invisible to the human eye. I can hide messages up to ~50% of the image file size and extract them later with no data loss."

### Medium Explanation (3 minutes)
1. **What is steganography?** - Hiding information within other data (different from encryption)
2. **Why LSB?** - Simple, doesn't require heavy computation, educational value
3. **How does it work?**
   - Pixels have 3 channels (R, G, B), each 8 bits (0-255)
   - We modify only the last bit (LSB) of each channel
   - This change is invisible but can be detected by software
4. **Capacity?** - Example: 200×200 image = 15,000 bytes total, minus 4 for length = 14,996 bytes max
5. **Why PNG?** - PNG is lossless; JPEG compression would destroy the hidden message

### Deep Explanation (5 minutes)
Include the above, plus:
- **Data format**: 4-byte length prefix + UTF-8 message bytes
- **Algorithm steps**: Convert text → prepend length → convert to bits → embed in LSBs → save
- **Bit embedding**: Show pixel example: [255, 128, 64] → modify LSBs
- **Tests**: Show test results (12 tests passing)
- **Security note**: Clarify that this is NOT encryption; it's just hiding. For real security, combine with encryption.

### Code Walkthrough Points
1. `steganography.py` - Core algorithm
   - `hide_message()`: Convert text to bits, embed in LSBs
   - `extract_message()`: Read LSBs, convert back to text
   - `get_max_message_size()`: Calculate capacity
2. `image_utils.py` - Helper functions
   - Image loading and validation
3. `main.py` - GUI
   - Two tabs: Hide and Extract
   - Real-time capacity display

---

## License

This project is created for educational purposes as part of a Data Security & Privacy (DSP) college assignment.

---

## Author Notes

- **Difficulty Level**: Beginner to Intermediate
- **Estimated Time**: 2-3 hours to understand fully
- **Best For**: Learning about steganography, image processing, and GUI development

Good luck with your viva! 🎉

---

## Quick Start Checklist

- [ ] Install Python 3.7+
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run tests: `python3 test_steganography.py`
- [ ] Start GUI: `python3 main.py`
- [ ] Create a test image in an image editor or use the one created during testing
- [ ] Hide a message and save the output
- [ ] Extract the message from the saved image
- [ ] Verify the message matches the original
- [ ] Demonstrate to your professor

---

## Additional Resources

- [Steganography - Wikipedia](https://en.wikipedia.org/wiki/Steganography)
- [PIL/Pillow Documentation](https://python-pillow.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [Binary and Bitwise Operations](https://en.wikipedia.org/wiki/Bitwise_operation)

---

**Last Updated**: October 2024  
**Status**: Ready for production ✓
