"""
Unit Tests for the Steganography Module

This test suite validates the core functionality:
- Hiding and extracting messages with password protection
- Unicode text handling
- Image capacity checks
- Error handling
"""

import unittest
import os
import tempfile
from steganography import hide_message, extract_message, get_max_message_size
from image_utils import create_test_image, save_image, load_image


class TestSteganography(unittest.TestCase):
    """Test cases for the steganography module"""
    
    def setUp(self):
        """Create a test image before each test"""
        self.test_image = create_test_image(200, 200)
        self.temp_dir = tempfile.mkdtemp()
        self.test_password = "test_password_123"
    
    def tearDown(self):
        """Clean up temporary files after each test"""
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    # Test 1: Basic hide and extract
    def test_hide_and_extract_simple_message(self):
        """Test hiding and extracting a simple text message"""
        message = "Hello, World!"
        
        # Hide the message with password
        stego_image = hide_message(self.test_image, message, self.test_password)
        
        # Extract the message with password
        extracted = extract_message(stego_image, self.test_password)
        
        # Verify
        self.assertEqual(message, extracted)
        print("✓ Test 1 Passed: Simple message hide/extract")
    
    # Test 2: Empty message
    def test_hide_and_extract_empty_message(self):
        """Test hiding and extracting an empty message"""
        message = ""
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        extracted = extract_message(stego_image, self.test_password)
        
        self.assertEqual(message, extracted)
        print("✓ Test 2 Passed: Empty message handling")
    
    # Test 3: Unicode text
    def test_hide_and_extract_unicode_message(self):
        """Test hiding and extracting Unicode text"""
        message = "Hello! 你好! مرحبا! 🎉"
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        extracted = extract_message(stego_image, self.test_password)
        
        self.assertEqual(message, extracted)
        print("✓ Test 3 Passed: Unicode text handling")
    
    # Test 4: Long message
    def test_hide_and_extract_long_message(self):
        """Test hiding and extracting a long message"""
        message = "The quick brown fox jumps over the lazy dog. " * 10
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        extracted = extract_message(stego_image, self.test_password)
        
        self.assertEqual(message, extracted)
        print("✓ Test 4 Passed: Long message handling")
    
    # Test 5: Message too large
    def test_message_too_large(self):
        """Test that error is raised when message is too large"""
        max_size = get_max_message_size(self.test_image)
        # Create a message larger than max size
        message = "A" * (max_size + 100)
        
        with self.assertRaises(ValueError):
            hide_message(self.test_image, message, self.test_password)
        print("✓ Test 5 Passed: Message capacity check")
    
    # Test 6: Maximum capacity message
    def test_max_capacity_message(self):
        """Test hiding a message at maximum capacity"""
        max_size = get_max_message_size(self.test_image)
        # Create a message at max size (but use safe characters)
        message = "A" * max_size
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        extracted = extract_message(stego_image, self.test_password)
        
        self.assertEqual(message, extracted)
        print("✓ Test 6 Passed: Maximum capacity message")
    
    # Test 7: Original image unchanged
    def test_original_image_unchanged(self):
        """Test that original image is not modified"""
        original_pixels = list(self.test_image.getdata())
        message = "Secret"
        
        # Hide message (should not modify original)
        stego_image = hide_message(self.test_image, message, self.test_password)
        
        # Check original is unchanged
        current_pixels = list(self.test_image.getdata())
        self.assertEqual(original_pixels, current_pixels)
        print("✓ Test 7 Passed: Original image unchanged")
    
    # Test 8: Different messages produce different stego images
    def test_different_messages_different_images(self):
        """Test that different messages produce different stego images"""
        message1 = "First message"
        message2 = "Second message"
        
        stego1 = hide_message(self.test_image, message1, self.test_password)
        stego2 = hide_message(self.test_image, message2, self.test_password)
        
        pixels1 = list(stego1.getdata())
        pixels2 = list(stego2.getdata())
        
        # They should be different
        self.assertNotEqual(pixels1, pixels2)
        print("✓ Test 8 Passed: Different messages produce different images")
    
    # Test 9: Wrong password detection
    def test_wrong_password_detection(self):
        """Test that wrong password is detected"""
        message = "Secret message"
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        
        # Try to extract with wrong password
        with self.assertRaises(ValueError):
            extract_message(stego_image, "wrong_password")
        print("✓ Test 9 Passed: Wrong password detection")
    
    # Test 10: Save and load workflow
    def test_save_and_load_workflow(self):
        """Test the complete workflow: hide, save, load, extract"""
        message = "Save and load test"
        
        # Hide message
        stego_image = hide_message(self.test_image, message, self.test_password)
        
        # Save to file
        stego_path = os.path.join(self.temp_dir, "stego.png")
        save_image(stego_image, stego_path)
        
        # Load from file
        loaded_image = load_image(stego_path)
        
        # Extract message
        extracted = extract_message(loaded_image, self.test_password)
        
        # Verify
        self.assertEqual(message, extracted)
        print("✓ Test 10 Passed: Save and load workflow")
    
    # Test 11: Special characters
    def test_special_characters(self):
        """Test hiding and extracting special characters"""
        message = "!@#$%^&*()_+-=[]{}|;:',.<>?/\\"
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        extracted = extract_message(stego_image, self.test_password)
        
        self.assertEqual(message, extracted)
        print("✓ Test 11 Passed: Special characters handling")
    
    # Test 12: Newlines and whitespace
    def test_whitespace_preservation(self):
        """Test that whitespace is preserved"""
        message = "Line 1\nLine 2\n\tIndented\r\nWindows line"
        
        stego_image = hide_message(self.test_image, message, self.test_password)
        extracted = extract_message(stego_image, self.test_password)
        
        self.assertEqual(message, extracted)
        print("✓ Test 12 Passed: Whitespace preservation")
    
    # Test 13: Invalid image file
    def test_invalid_image_file(self):
        """Test handling of invalid or corrupted image files"""
        from image_utils import load_image
        
        # Create a temporary file that is not a valid image
        invalid_path = os.path.join(self.temp_dir, "not_an_image.txt")
        with open(invalid_path, 'w') as f:
            f.write("This is not an image file")
        
        # Try to load it - should raise an error
        with self.assertRaises((ValueError, Exception)):
            load_image(invalid_path)
        print("✓ Test 13 Passed: Invalid image file handling")


def run_tests():
    """Run all tests and display results"""
    print("\n" + "="*60)
    print("IMAGE STEGANOGRAPHY - UNIT TESTS")
    print("="*60 + "\n")
    
    # Create a test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSteganography)
    
    # Run with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Summary
    print("\n" + "="*60)
    print(f"Tests Run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print("="*60 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
