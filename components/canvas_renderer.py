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

    def display_cropped_image(self, frame, image):
      
      """Display the image on the canvas."""

      if not hasattr(self, 'cropped_canvas'):
        frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.cropped_canvas = tk.Canvas(frame, bg="gray", width=500, height=500)
        self.cropped_canvas.pack(fill=tk.BOTH, expand=True)
      frame.update_idletasks()
      # self.root.update()
      pil_image = Image.fromarray(image)
      tk_image = ImageTk.PhotoImage(pil_image)

      self.cropped_canvas.delete("all")
      self.cropped_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
      self.cropped_canvas.image = tk_image  # Keep reference to avoid garbage collection
