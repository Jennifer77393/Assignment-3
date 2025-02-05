import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk, filedialog, messagebox

class CanvasRenderer:
    def display_image(self, canvas, image):
        """Display the image on the canvas."""
        pil_image = Image.fromarray(image)
        tk_image = ImageTk.PhotoImage(pil_image)

        canvas.delete("all")
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        canvas.image = tk_image  # Keep reference to avoid garbage collection

    def display_cropped_image(self, frame, image, is_cropped_frame_hidden):
        """Display the image on the canvas."""
        print(frame.winfo_width(), frame.winfo_height())

        # Check if the canvas exists, and if the cropped frame is hidden
        if is_cropped_frame_hidden:
            frame.grid(row=1, column=1, columnspan=6, sticky="nsew")
        if not hasattr(self, 'cropped_canvas'):
            # Show the frame if hidden
            frame.grid(row=1, column=1, columnspan=6, sticky="nsew")

            # Create the canvas if it doesn't exist
            self.cropped_canvas = tk.Canvas(frame, bg="gray", width=1500, height=800)
            self.cropped_canvas.pack(fill=tk.BOTH, expand=True)

        # Update the canvas with the new image
        frame.update_idletasks()

        # Convert the image to PIL format and then to Tkinter format
        pil_image = Image.fromarray(image)
        tk_image = ImageTk.PhotoImage(pil_image)

        # Clear any previous image and set the new one
        self.cropped_canvas.delete("all")
        self.cropped_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
        self.cropped_canvas.image = tk_image  # Keep reference to avoid garbage collection

