"""
Image Steganography System - Main GUI Application

A Tkinter-based graphical interface for hiding and extracting secret messages
in digital images using LSB (Least Significant Bit) steganography.

Features:
- Hide secret messages in PNG images
- Extract hidden messages from images
- Real-time capacity checking
- User-friendly interface with clear feedback
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
from steganography import hide_message, extract_message, get_max_message_size
from image_utils import load_image, save_image, validate_image_for_steganography


class SteganographyApp:
    """Main application class for the Steganography GUI"""
    
    def __init__(self, root):
        """Initialize the application"""
        self.root = root
        self.root.title("Image Steganography System")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Store current image paths and objects
        self.hide_image_path = None
        self.hide_image = None
        self.extract_image_path = None
        self.extract_image = None
        
        # Create the GUI
        self.create_widgets()
    
    def create_widgets(self):
        """Create all GUI elements"""
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Image Steganography System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # Subtitle
        subtitle = ttk.Label(main_frame, 
                            text="Hide and extract secret messages in PNG images using LSB technology",
                            font=("Arial", 10, "italic"), foreground="gray")
        subtitle.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Hide Message Tab
        hide_frame = ttk.Frame(notebook, padding="15")
        notebook.add(hide_frame, text="Hide Message")
        self.create_hide_tab(hide_frame)
        
        # Extract Message Tab
        extract_frame = ttk.Frame(notebook, padding="15")
        notebook.add(extract_frame, text="Extract Message")
        self.create_extract_tab(extract_frame)
    
    def create_hide_tab(self, parent):
        """Create the Hide Message tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(5, weight=1)
        
        # Image selection section
        ttk.Label(parent, text="Step 1: Select Cover Image (PNG)", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        img_frame = ttk.Frame(parent)
        img_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        img_frame.columnconfigure(1, weight=1)
        
        self.hide_image_label = ttk.Label(img_frame, text="No image selected", 
                                          foreground="gray")
        self.hide_image_label.grid(row=0, column=1, sticky="w", padx=10)
        
        ttk.Button(img_frame, text="Browse", 
                  command=self.select_hide_image).grid(row=0, column=0, sticky="w")
        
        # Image info
        self.hide_info_label = ttk.Label(parent, text="", foreground="blue")
        self.hide_info_label.grid(row=2, column=0, sticky="w", pady=(0, 15))
        
        # Message input section
        ttk.Label(parent, text="Step 2: Enter Secret Message", 
                 font=("Arial", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(0, 10))
        
        self.hide_message_text = tk.Text(parent, height=6, wrap="word", 
                                         font=("Arial", 10))
        self.hide_message_text.grid(row=4, column=0, sticky="nsew", pady=(0, 15))
        self.hide_message_text.bind("<KeyRelease>", self.update_hide_capacity)
        
        # Capacity indicator
        self.hide_capacity_label = ttk.Label(parent, text="", foreground="green")
        self.hide_capacity_label.grid(row=5, column=0, sticky="w", pady=(0, 15))
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=6, column=0, sticky="ew", pady=20)
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Hide Message", 
                  command=self.hide_message_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_hide_tab).pack(side="left", padx=5)
        
        # Status label
        self.hide_status_label = ttk.Label(parent, text="", font=("Arial", 10))
        self.hide_status_label.grid(row=7, column=0, sticky="w", pady=(0, 10))
    
    def create_extract_tab(self, parent):
        """Create the Extract Message tab"""
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(3, weight=1)
        
        # Image selection section
        ttk.Label(parent, text="Step 1: Select Image with Hidden Message", 
                 font=("Arial", 11, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        img_frame = ttk.Frame(parent)
        img_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        img_frame.columnconfigure(1, weight=1)
        
        self.extract_image_label = ttk.Label(img_frame, text="No image selected", 
                                             foreground="gray")
        self.extract_image_label.grid(row=0, column=1, sticky="w", padx=10)
        
        ttk.Button(img_frame, text="Browse", 
                  command=self.select_extract_image).grid(row=0, column=0, sticky="w")
        
        # Message display section
        ttk.Label(parent, text="Step 2: Extracted Message", 
                 font=("Arial", 11, "bold")).grid(row=2, column=0, sticky="w", pady=(0, 10))
        
        self.extract_message_text = tk.Text(parent, height=8, wrap="word", 
                                            font=("Arial", 10), state="disabled")
        self.extract_message_text.grid(row=3, column=0, sticky="nsew", pady=(0, 15))
        
        # Buttons frame
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=4, column=0, sticky="ew", pady=20)
        button_frame.columnconfigure(0, weight=1)
        
        ttk.Button(button_frame, text="Extract Message", 
                  command=self.extract_message_action).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Copy to Clipboard", 
                  command=self.copy_to_clipboard).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_extract_tab).pack(side="left", padx=5)
        
        # Status label
        self.extract_status_label = ttk.Label(parent, text="", font=("Arial", 10))
        self.extract_status_label.grid(row=5, column=0, sticky="w", pady=(0, 10))
    
    def select_hide_image(self):
        """Handle hide image selection"""
        file_path = filedialog.askopenfilename(
            title="Select PNG Image",
            filetypes=[("PNG Images", "*.png"), ("All Images", "*.*")]
        )
        
        if file_path:
            try:
                # Validate the image
                is_valid, msg = validate_image_for_steganography(file_path)
                if not is_valid:
                    messagebox.showwarning("Image Warning", msg)
                    return
                
                # Load the image
                self.hide_image = load_image(file_path)
                self.hide_image_path = file_path
                
                # Update label
                filename = os.path.basename(file_path)
                self.hide_image_label.config(text=filename, foreground="black")
                
                # Show image info
                max_size = get_max_message_size(self.hide_image)
                info_text = f"Image: {self.hide_image.width}x{self.hide_image.height} | " \
                           f"Max capacity: {max_size} bytes"
                self.hide_info_label.config(text=info_text, foreground="blue")
                
                # Clear previous message
                self.hide_message_text.delete("1.0", tk.END)
                self.update_hide_capacity()
                self.set_hide_status("Image loaded successfully", "green")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.set_hide_status(f"Error: {e}", "red")
    
    def select_extract_image(self):
        """Handle extract image selection"""
        file_path = filedialog.askopenfilename(
            title="Select Image with Hidden Message",
            filetypes=[("PNG Images", "*.png"), ("All Images", "*.*")]
        )
        
        if file_path:
            try:
                self.extract_image = load_image(file_path)
                self.extract_image_path = file_path
                
                filename = os.path.basename(file_path)
                self.extract_image_label.config(text=filename, foreground="black")
                
                self.set_extract_status("Image loaded. Click 'Extract Message' to proceed.", "green")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load image: {e}")
                self.set_extract_status(f"Error: {e}", "red")
    
    def update_hide_capacity(self, event=None):
        """Update the capacity display in real-time"""
        if not self.hide_image:
            self.hide_capacity_label.config(text="")
            return
        
        message = self.hide_message_text.get("1.0", tk.END).rstrip("\n")
        message_bytes = len(message.encode('utf-8'))
        max_size = get_max_message_size(self.hide_image)
        remaining = max_size - message_bytes
        
        if remaining < 0:
            color = "red"
            text = f"❌ Message too large! Excess: {abs(remaining)} bytes"
        elif remaining < 100:
            color = "orange"
            text = f"⚠️  Message size: {message_bytes} / {max_size} bytes (Remaining: {remaining})"
        else:
            color = "green"
            text = f"✓ Message size: {message_bytes} / {max_size} bytes (Remaining: {remaining})"
        
        self.hide_capacity_label.config(text=text, foreground=color)
    
    def hide_message_action(self):
        """Handle hide message button click"""
        if not self.hide_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        message = self.hide_message_text.get("1.0", tk.END).rstrip("\n")
        
        if not message:
            messagebox.showwarning("Warning", "Please enter a message to hide")
            return
        
        try:
            # Hide the message
            self.set_hide_status("Processing... hiding message...", "blue")
            self.root.update()
            
            stego_image = hide_message(self.hide_image, message)
            
            # Ask user where to save
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Images", "*.png")],
                initialfile="stego.png"
            )
            
            if save_path:
                save_image(stego_image, save_path)
                self.set_hide_status(f"✓ Message hidden successfully! Saved to: {os.path.basename(save_path)}", "green")
                messagebox.showinfo("Success", f"Message hidden successfully!\n\nSaved to:\n{save_path}")
            else:
                self.set_hide_status("Save cancelled", "gray")
        
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            self.set_hide_status(f"Error: {e}", "red")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            self.set_hide_status(f"Error: {e}", "red")
    
    def extract_message_action(self):
        """Handle extract message button click"""
        if not self.extract_image:
            messagebox.showwarning("Warning", "Please select an image first")
            return
        
        try:
            self.set_extract_status("Processing... extracting message...", "blue")
            self.root.update()
            
            message = extract_message(self.extract_image)
            
            # Display the message
            self.extract_message_text.config(state="normal")
            self.extract_message_text.delete("1.0", tk.END)
            self.extract_message_text.insert("1.0", message)
            self.extract_message_text.config(state="disabled")
            
            self.set_extract_status(f"✓ Message extracted successfully! ({len(message)} characters)", "green")
        
        except Exception as e:
            self.extract_message_text.config(state="normal")
            self.extract_message_text.delete("1.0", tk.END)
            self.extract_message_text.config(state="disabled")
            
            messagebox.showerror("Error", f"Failed to extract message: {e}")
            self.set_extract_status(f"Error: {e}", "red")
    
    def copy_to_clipboard(self):
        """Copy extracted message to clipboard"""
        message = self.extract_message_text.get("1.0", tk.END).rstrip("\n")
        if message:
            self.root.clipboard_clear()
            self.root.clipboard_append(message)
            messagebox.showinfo("Copied", "Message copied to clipboard!")
        else:
            messagebox.showwarning("Warning", "No message to copy")
    
    def clear_hide_tab(self):
        """Clear the hide tab"""
        self.hide_message_text.delete("1.0", tk.END)
        self.hide_capacity_label.config(text="")
        self.hide_status_label.config(text="")
        self.update_hide_capacity()
    
    def clear_extract_tab(self):
        """Clear the extract tab"""
        self.extract_message_text.config(state="normal")
        self.extract_message_text.delete("1.0", tk.END)
        self.extract_message_text.config(state="disabled")
        self.extract_status_label.config(text="")
    
    def set_hide_status(self, text, color="black"):
        """Update hide tab status label"""
        self.hide_status_label.config(text=text, foreground=color)
    
    def set_extract_status(self, text, color="black"):
        """Update extract tab status label"""
        self.extract_status_label.config(text=text, foreground=color)


def main():
    """Main entry point"""
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
