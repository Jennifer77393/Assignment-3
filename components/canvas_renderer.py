import tkinter as tk
from PIL import Image, ImageTk


# from tkinter import ttk, filedialog, messagebox  # No need to import these here

class CanvasRenderer:
    def display_image(self, canvas, image):
        """Display the image on the canvas."""
        pil_image = Image.fromarray(image)
        tk_image = ImageTk.PhotoImage(pil_image)

        canvas.delete("all")  # Clear previous image
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image  # Keep reference to avoid garbage collection

    def display_cropped_image(self, frame, image):
        """Display the cropped image."""
        # Check if cropped_canvas exists, create it if not.
        if not hasattr(self, 'cropped_canvas') or self.cropped_canvas is None:  # Check if it exists or not.
            frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            self.cropped_canvas = tk.Canvas(frame, bg="gray")  # Removed fixed width and height
            self.cropped_canvas.pack(fill=tk.BOTH, expand=True)
            self.cropped_canvas.image = None  # Initialize image to None.

        pil_image = Image.fromarray(image)
        tk_image = ImageTk.PhotoImage(pil_image)

        self.cropped_canvas.delete("all")  # Clear previous image
        self.cropped_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.cropped_canvas.image = tk_image  # Keep reference

    def clear_canvas(self, canvas):
        canvas.delete("all")

    def clear_cropped_canvas(self, frame):
        # More robust way to clear the cropped image.
        for widget in frame.winfo_children():
            widget.destroy()
        self.cropped_canvas = None  # Reset the cropped canvas attribute
        # frame.pack_forget()  # Remove the frame itself (if needed)