"""
Image Utilities Module

This module provides helper functions for loading, validating, and saving images.
It ensures consistent image handling across the application.
"""

from PIL import Image
import os
from typing import Tuple, Optional


def load_image(image_path: str) -> Image.Image:
    """
    Load an image from the given file path.
    Accepts any image format (JPEG, PNG, BMP, GIF, TIFF, etc.)
    and automatically converts to RGB for consistent processing.
    
    Args:
        image_path: Path to the image file (any format)
        
    Returns:
        PIL Image object in RGB mode
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        ValueError: If the file is not a valid image
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    try:
        image = Image.open(image_path)
        # Validate that it's actually an image by checking if we can load it
        image.load()
        
        # Convert to RGB for consistent processing (handles JPEG, PNG, RGBA, grayscale, etc.)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        return image
    except Exception as e:
        raise ValueError(f"Failed to load image: {e}")


def save_image(image: Image.Image, output_path: str, format: str = 'PNG') -> None:
    """
    Save an image to the given file path.
    
    Args:
        image: PIL Image object to save
        output_path: Path where the image should be saved
        format: Image format (default: 'PNG' - recommended for lossless storage)
        
    Raises:
        ValueError: If the image cannot be saved
        TypeError: If image is not a PIL Image
    """
    if not isinstance(image, Image.Image):
        raise TypeError("Image must be a PIL Image object")
    
    try:
        # Ensure output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Determine format from file extension if not specified
        if format == 'PNG':
            # Force PNG for lossless saving
            image.save(output_path, format='PNG')
        else:
            # Save with detected or specified format
            image.save(output_path, format=format)
    except Exception as e:
        raise ValueError(f"Failed to save image: {e}")


def validate_image_for_steganography(image_path: str) -> Tuple[bool, str]:
    """
    Validate that an image is suitable for steganography.
    Accepts any image format (JPEG, PNG, BMP, GIF, TIFF, etc.)
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (is_valid, message). is_valid is True if suitable, message explains any issues.
    """
    try:
        image = load_image(image_path)
    except (FileNotFoundError, ValueError) as e:
        return False, f"Cannot load image: {e}"
    
    # Check image size (at least 100x100 for practical use)
    width, height = image.size
    if width < 100 or height < 100:
        return False, f"Image too small: {width}x{height}. Minimum recommended: 100x100"
    
    # All formats are now accepted (auto-converted to RGB)
    return True, "Image is suitable for steganography"


def get_image_info(image_path: str) -> dict:
    """
    Get information about an image file.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Dictionary containing image properties
        
    Raises:
        FileNotFoundError: If image file not found
        ValueError: If not a valid image
    """
    image = load_image(image_path)
    
    return {
        'width': image.width,
        'height': image.height,
        'mode': image.mode,
        'format': image.format,
        'size_bytes': os.path.getsize(image_path),
    }


def create_test_image(width: int = 200, height: int = 200) -> Image.Image:
    """
    Create a simple test image for testing purposes.
    
    Args:
        width: Image width in pixels (default: 200)
        height: Image height in pixels (default: 200)
        
    Returns:
        PIL Image object with random RGB data
    """
    import random
    
    image = Image.new('RGB', (width, height))
    pixels = image.load()
    
    # Fill with random colors
    for y in range(height):
        for x in range(width):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pixels[x, y] = (r, g, b)
    
    return image
