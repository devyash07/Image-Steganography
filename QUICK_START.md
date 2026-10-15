# Quick Start Guide - Image Steganography System

**Total Setup Time: 2 minutes**

---

## 1️⃣ Install Dependencies

```bash
cd "/Users/yashwaantdev/Downloads/Image Steganography"
pip install -r requirements.txt
```

Expected output: `Successfully installed Pillow` (or already satisfied)

---

## 2️⃣ Run Tests (Verify Everything Works)

```bash
python3 test_steganography.py
```

**Expected Output:**
```
============================================================
Tests Run: 12
Failures: 0
Errors: 0
============================================================
```

✅ If you see this, everything is working!

---

## 3️⃣ Launch the GUI Application

```bash
python3 main.py
```

A Tkinter window opens. You now have:
- **Hide Message tab** - Embed secrets in images
- **Extract Message tab** - Recover hidden messages

---

## 4️⃣ Hide a Message (Step-by-Step)

### Step 1: Get a PNG Image
- Find any PNG image on your computer
- Or create one in GIMP/Photoshop
- Recommended size: 200×200 or larger

### Step 2: Use the App
1. Click the **Hide Message** tab
2. Click **Browse** button
3. Select your PNG image
4. Type a secret message in the text box
5. Watch the **green capacity indicator** show you have space
6. Click **Hide Message** button
7. Choose where to save (e.g., `my_secret.png`)

### Step 3: Verify
- ✅ Success message appears
- 📁 New image file created with hidden message

---

## 5️⃣ Extract a Message (Step-by-Step)

### Step 1: Load the Stego Image
1. Click the **Extract Message** tab
2. Click **Browse** button
3. Select the image from Step 4 (the one with hidden message)

### Step 2: Extract
1. Click **Extract Message** button
2. The hidden text appears in the text box!
3. (Optional) Click **Copy to Clipboard** to copy the message

---

## 🔬 Technical Demo (For Viva)

### Show How LSB Works

```bash
python3 << 'EOF'
from steganography import hide_message, extract_message, get_max_message_size
from image_utils import create_test_image

# Create a test image
img = create_test_image(300, 300)
print(f"Image capacity: {get_max_message_size(img)} bytes")

# Hide message
msg = "Hello, LSB!"
stego = hide_message(img, msg)

# Extract message
extracted = extract_message(stego)
print(f"Original:  {msg}")
print(f"Extracted: {extracted}")
print(f"Match: {msg == extracted}")
EOF
```

---

## 📊 Test with Different Message Types

### Test 1: Simple Text
```
Message: "Hello, World!"
Result: ✅ Works perfectly
```

### Test 2: Unicode & Emojis
```
Message: "🔒 Secret 🔐 你好 مرحبا"
Result: ✅ Full Unicode support
```

### Test 3: Long Message
```
Message: "Lorem ipsum dolor sit amet..." (repeat many times)
Result: ✅ Works up to capacity
```

### Test 4: Empty Message
```
Message: "" (nothing)
Result: ✅ Handles gracefully
```

---

## ⚙️ File Reference

| File | Purpose | Size |
|------|---------|------|
| `main.py` | GUI Application | ~250 lines |
| `steganography.py` | Core LSB Algorithm | ~200 lines |
| `image_utils.py` | Image Utilities | ~100 lines |
| `test_steganography.py` | Unit Tests | ~150 lines |
| `requirements.txt` | Dependencies | 1 line |
| `README.md` | Full Documentation | ~400 lines |

---

## 🐛 Troubleshooting

### Issue: "No module named PIL"
```bash
pip install Pillow
```

### Issue: "No module named tkinter"
- **macOS**: `brew install python-tk`
- **Ubuntu**: `sudo apt-get install python3-tk`
- **Windows**: Should be included with Python

### Issue: "Message too large"
- Use a larger image (500×500 instead of 200×200)
- Check the capacity indicator in the GUI

### Issue: "Failed to load image"
- Make sure it's a valid PNG file
- Try opening it in an image viewer first

---

## 💡 Tips for Demonstration

### Tip 1: Pre-test Everything
Run the tests first to ensure system is ready:
```bash
python3 test_steganography.py
```

### Tip 2: Have Test Images Ready
Create a few test PNG images beforehand (200×200 minimum).

### Tip 3: Demonstrate Features
1. Hide a message
2. Save the output
3. Extract from the saved image
4. Show they match

### Tip 4: Explain the Algorithm
- Show how LSB modification is invisible
- Explain capacity calculation
- Mention why PNG is important

### Tip 5: Run Tests Live
Show that 12 tests pass in <1 second.

---

## 📝 Viva Questions (Practice)

**Q: How does LSB steganography work?**
A: We modify the least significant bit (last bit) of each pixel channel. This change is invisible but can be detected by software.

**Q: What's the capacity of a 200×200 image?**
A: 200 × 200 × 3 channels = 120,000 bits ÷ 8 = 15,000 bytes minus 4 bytes for length = ~15 KB.

**Q: Why use PNG instead of JPEG?**
A: PNG uses lossless compression, so all pixels are preserved. JPEG uses lossy compression, which destroys the LSBs.

**Q: Is this encryption?**
A: No, it's steganography. The message is hidden but not encrypted. Anyone who knows LSB steganography can extract it.

**Q: What if someone modifies the image?**
A: Any modification (resizing, rotation, compression) will corrupt the LSBs and make the message unrecoverable.

---

## ✅ Success Checklist

Before viva/demo:
- [ ] All tests pass (12/12)
- [ ] GUI launches without errors
- [ ] Can hide and extract messages
- [ ] Code is readable and commented
- [ ] README is complete
- [ ] Have test images ready
- [ ] Practice explaining algorithm
- [ ] Practice running demo end-to-end

---

## 🚀 Ready to Go!

You're all set! This project demonstrates:
✅ Image processing with Pillow  
✅ Binary operations and bit manipulation  
✅ GUI development with Tkinter  
✅ Unit testing with Python  
✅ Error handling and validation  

**Good luck with your viva! 🎉**
