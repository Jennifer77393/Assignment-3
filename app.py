import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from components.image_loader import ImageLoader
from components.image_resizer import ImageResizer
from components.image_cropper import ImageCropper
from components.canvas_renderer import CanvasRenderer
from components.image_rotator import ImageRotator
from styles.style_config import BUTTON_STYLE, CANVAS_STYLE
import cv2

class ImageEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.root.geometry("1200x600")

        self.image_loader = ImageLoader()
        self.image_resizer = ImageResizer()
        self.cropper = ImageCropper()
        self.canvas_renderer = CanvasRenderer()
        self.image_rotator = ImageRotator()

        self.image = None
        self.thumbnail = None
        self.cropped_image = None
        self.edited_image = None
        self.original_image = None
        self.is_cropped_frame_hidden = False

        self._setup_gui()

    def _setup_gui(self):
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(container)
        # control_frame.pack(side=tk.LEFT, fill=tk.Y)
        control_frame.grid(row=0, column=0, sticky="ns")

        self.load_button = ttk.Button(control_frame, text="Load Image", command=self.load_image, **BUTTON_STYLE)
        self.load_button.pack(pady=10)

        self.save_button = ttk.Button(control_frame, text="Save Image", command=self.save_image, **BUTTON_STYLE)
        self.save_button.pack(pady=10)

        self.save_button = ttk.Button(control_frame, text="Rotate Image", command=self.rotate_image, **BUTTON_STYLE)
        self.save_button.pack(pady=10)

        self.resize_slider = ttk.Scale(control_frame, from_=0.1, to=1.0, value=0.1, orient=tk.HORIZONTAL, command=self.resize_image)
        self.resize_slider.pack(pady=10)

        self.canvas = tk.Canvas(container, **CANVAS_STYLE)
        # self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas.grid(row=0, column=1, sticky="nsew", columnspan=6)

        self.cropped_canvas_frame = self.create_cropped_canvas_frame(container)

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.perform_crop)

    def create_cropped_canvas_frame (self,container) -> tk.Frame:
        return ttk.Frame(container, width=900, height=300)

    def load_image(self):
        """Load an image from the file system."""
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.JPG"), ("Image Files", "*.jpeg"), ("Image Files", "*.bmp")])
        if not file_path:
            return

        self.image, self.original_image = self.image_loader.load_image(file_path)
        self.thumbnail = self.image_resizer.resize_image(self.image, 600, 600)
        self.canvas_renderer.display_image(self.canvas, self.thumbnail)

    def save_image(self):
        """Save the cropped image."""
        if self.edited_image is None:
            messagebox.showerror("Error", "No any image to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.edited_image)
            messagebox.showinfo("Success", "Image saved successfully.")

    def rotate_image(self):
        """Rotate the image by 90 degrees."""
        self.cropped_canvas_frame.grid_forget()
        self.is_cropped_frame_hidden = True
        self.original_image = self.image_rotator.image_rotator(self.original_image, 90,self.canvas)
        self.edited_image = self.image_resizer.resize_image(self.original_image, 600, 600)
        self.canvas_renderer.display_image(self.canvas, self.edited_image)

    def resize_image(self, value):
        """Resize the image based on the slider value."""
        scale = float(value)
        self.thumbnail = self.image_resizer.resize_image(self.original_image, int(600 * scale), int(600 * scale))
        self.canvas_renderer.display_image(self.canvas, self.thumbnail)

    def start_crop(self, event):
        """Start the cropping process."""
        self.cropper.start_crop(event, self.canvas)

    def update_crop(self, event):
        """Update the cropping rectangle while dragging."""
        self.cropper.update_crop(event, self.canvas)

    def perform_crop(self, event):
        """Perform the crop when mouse is released."""
        self.edited_image = self.cropper.perform_crop(event, self.canvas, self.original_image, self.thumbnail)
        self.canvas_renderer.display_cropped_image(self.cropped_canvas_frame, self.edited_image,self.is_cropped_frame_hidden)
        self.is_cropped_frame_hidden = False

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()
