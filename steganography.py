"""
LSB (Least Significant Bit) Steganography Module

This module handles hiding and extracting secret messages in images using the
LSB technique. The LSB method modifies the least significant bit of each pixel
channel to encode message data.

Algorithm:
1. For hiding: Convert text to UTF-8 bytes → prepend length (4 bytes) →
   encode each bit into the LSB of consecutive pixel channels
2. For extraction: Read LSB from pixel channels → extract length prefix →
   read that many bytes → convert back to text
"""

from PIL import Image
from typing import Tuple
import hashlib


# Constants for the steganography algorithm
BITS_PER_CHANNEL = 1  # We use 1 bit per RGB channel
BYTES_FOR_LENGTH = 4  # Use 4 bytes (32 bits) to store message length
PASSWORD_HASH_SIZE = 32  # SHA256 produces 32 bytes


def hash_password(password: str) -> bytes:
    """
    Create a SHA256 hash of the password.
    
    Args:
        password: Password string to hash
        
    Returns:
        32-byte SHA256 hash
    """
    return hashlib.sha256(password.encode('utf-8')).digest()


def get_max_message_size(image: Image.Image, password: str = "") -> int:
    """
    Calculate the maximum number of bytes that can be hidden in an image.
    
    Args:
        image: PIL Image object
        password: Password (not used in calculation, kept for API compatibility)
        
    Returns:
        Maximum number of bytes that can be stored (accounts for length prefix and password hash)
    """
    width, height = image.size
    # Each pixel has 3 channels (RGB), each channel can store 1 bit
    total_bits = width * height * 3
    # Total bytes = bits / 8, minus 4 bytes reserved for length prefix
    # Always reserve 32 bytes for password hash (required)
    reserved_bytes = BYTES_FOR_LENGTH + PASSWORD_HASH_SIZE
    
    total_bytes = total_bits // 8
    max_message_bytes = total_bytes - reserved_bytes
    return max(0, max_message_bytes)


def hide_message(image: Image.Image, message: str, password: str) -> Image.Image:
    """
    Hide a secret message inside an image using LSB steganography.
    Works with any image format (JPEG, PNG, BMP, GIF, TIFF, etc.)
    automatically converts to RGB for processing.
    Password protection is required.
    
    Args:
        image: PIL Image object (any format, will be converted to RGB)
        message: Secret message string to hide
        password: Password to protect the message (required, cannot be empty)
        
    Returns:
        New PIL Image with the hidden message (RGB format)
        
    Raises:
        ValueError: If message is too large for the image or password is empty
        TypeError: If image is not a valid PIL Image
    """
    # Validate inputs
    if not isinstance(image, Image.Image):
        raise TypeError("Image must be a PIL Image object")
    
    if not isinstance(message, str):
        raise TypeError("Message must be a string")
    
    if not password or not isinstance(password, str):
        raise ValueError("Password is required and must be a non-empty string")
    
    # Convert message to UTF-8 bytes
    message_bytes = message.encode('utf-8')
    message_length = len(message_bytes)
    
    # Check if message fits in the image
    max_size = get_max_message_size(image, password)
    if message_length > max_size:
        raise ValueError(
            f"Message too large. Max size: {max_size} bytes, "
            f"Attempted: {message_length} bytes"
        )
    
    # Convert image to RGB mode (handles JPEG, RGBA, grayscale, etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Create a copy of the image to modify
    stego_image = image.copy()
    pixels = stego_image.load()
    width, height = stego_image.size
    
    # Prepare data to hide
    data_to_hide = message_length.to_bytes(BYTES_FOR_LENGTH, byteorder='big')
    
    # Add password hash (now always required)
    pwd_hash = hash_password(password)
    data_to_hide += pwd_hash
    
    data_to_hide += message_bytes
    
    # Convert all bytes to bits
    bits = ''.join(format(byte, '08b') for byte in data_to_hide)
    
    # Embed bits into LSBs of pixel channels
    bit_index = 0
    for y in range(height):
        for x in range(width):
            # Get the pixel (R, G, B values)
            pixel = list(pixels[x, y])
            
            # Embed bits into each of the 3 channels
            for channel in range(3):
                if bit_index < len(bits):
                    # Extract the current bit from the message
                    bit = int(bits[bit_index])
                    # Replace the LSB of this channel
                    pixel[channel] = (pixel[channel] & 0xFE) | bit
                    bit_index += 1
            
            # Update the pixel in the image
            pixels[x, y] = tuple(pixel)
    
    return stego_image


def extract_message(image: Image.Image, password: str) -> str:
    """
    Extract a hidden message from an image using LSB steganography.
    Works with any image format (JPEG, PNG, BMP, GIF, TIFF, etc.)
    automatically converts to RGB for processing.
    
    Password is required to extract the message.
    
    Args:
        image: PIL Image object containing a hidden message (any format)
        password: Password to decrypt the message (required, must match the one used during hiding)
        
    Returns:
        Extracted message string
        
    Raises:
        ValueError: If no valid message is found or password is incorrect
        TypeError: If image is not a valid PIL Image
    """
    # Validate input
    if not isinstance(image, Image.Image):
        raise TypeError("Image must be a PIL Image object")
    
    if not password or not isinstance(password, str):
        raise ValueError("Password is required and must be a non-empty string")
    
    # Convert image to RGB mode if needed (handles JPEG, RGBA, grayscale, etc.)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    pixels = image.load()
    width, height = image.size
    
    # Extract all LSBs from pixel channels
    bits = ''
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]
            # Extract LSB from each of the 3 channels
            for channel in range(3):
                bits += str(pixel[channel] & 1)
    
    # Extract the message length (first 4 bytes = 32 bits)
    if len(bits) < BYTES_FOR_LENGTH * 8:
        raise ValueError("Image too small to contain a valid message")
    
    length_bits = bits[:BYTES_FOR_LENGTH * 8]
    message_length = int(length_bits, 2)
    
    # Validate message length
    max_size = get_max_message_size(image, password)
    if message_length > max_size or message_length < 0:
        raise ValueError(
            f"Invalid message length: {message_length}. "
            f"Expected between 0 and {max_size}"
        )
    
    # Extract password hash (next 32 bytes)
    hash_start = BYTES_FOR_LENGTH * 8
    hash_end = hash_start + PASSWORD_HASH_SIZE * 8
    
    if len(bits) < hash_end:
        raise ValueError("Image too small to contain password hash")
    
    hash_bits = bits[hash_start:hash_end]
    stored_hash = bytearray()
    for i in range(PASSWORD_HASH_SIZE):
        byte_bits = hash_bits[i * 8:(i + 1) * 8]
        if len(byte_bits) == 8:
            stored_hash.append(int(byte_bits, 2))
    
    # Verify password (password is now required)
    pwd_hash = hash_password(password)
    if bytes(stored_hash) != pwd_hash:
        raise ValueError("❌ Incorrect password! Cannot extract message.")
    
    # Extract message bytes
    message_start = BYTES_FOR_LENGTH * 8 + PASSWORD_HASH_SIZE * 8
    message_end = message_start + message_length * 8
    message_bits = bits[message_start:message_end]
    
    if len(message_bits) < message_length * 8:
        raise ValueError("Incomplete message data in image")
    
    # Convert bits back to bytes
    message_bytes = bytearray()
    for i in range(message_length):
        byte_bits = message_bits[i * 8:(i + 1) * 8]
        if len(byte_bits) == 8:
            message_bytes.append(int(byte_bits, 2))
    
    # Decode UTF-8 bytes to string
    try:
        message = message_bytes.decode('utf-8')
    except UnicodeDecodeError as e:
        raise ValueError(f"Failed to decode message as UTF-8: {e}")
    
    return message
