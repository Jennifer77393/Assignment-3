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
        window_width = 1200
        window_height = 600
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.image_loader = ImageLoader()
        self.image_resizer = ImageResizer()
        self.cropper = ImageCropper()
        self.canvas_renderer = CanvasRenderer()
        self.image_rotator = ImageRotator()

        self.image = None
        self.thumbnail = None
        self.cropped_image = None
        self.original_image = None

        self.undo_stack = []
        self.redo_stack = []

        self._setup_gui()

    def _setup_gui(self):
        container = ttk.Frame(self.root, padding=10)
        container.pack(fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(container)
        control_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        self.load_button = ttk.Button(control_frame, text="Load Image", command=self.load_image, **BUTTON_STYLE)
        self.load_button.pack(pady=10)

        self.save_button = ttk.Button(control_frame, text="Save Image", command=self.save_image, **BUTTON_STYLE)
        self.save_button.pack(pady=10)

        self.save_button = ttk.Button(control_frame, text="Rotate Image", command=self.rotate_image,**BUTTON_STYLE)
        self.save_button.pack(pady=10)

        self.undo_button = ttk.Button(control_frame, text="Undo", command=self.undo, **BUTTON_STYLE)
        self.undo_button.pack(pady=10)

        self.redo_button = ttk.Button(control_frame, text="Redo", command=self.redo, **BUTTON_STYLE)
        self.redo_button.pack(pady=10)

        self.clear_button = ttk.Button(control_frame, text="Clear", command=self.clear_all, **BUTTON_STYLE)
        self.clear_button.pack(pady=10)

        self.resize_slider = ttk.Scale(control_frame, from_=0.1, to=1.0, value=1.0, orient=tk.HORIZONTAL,
                                       command=self.resize_image)
        self.resize_slider.pack(pady=10)

        self.canvas = tk.Canvas(container, **CANVAS_STYLE)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.cropped_canvas_frame = ttk.Frame(container , width=1000 , height=1000)
        self.cropped_canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind("<ButtonPress-1>", self.start_crop)
        self.canvas.bind("<B1-Motion>", self.update_crop)
        self.canvas.bind("<ButtonRelease-1>", self.perform_crop)

        self.root.bind("<Control-s>", self.save_image)
        self.root.bind("<Control-z>", lambda event: self.undo())
        self.root.bind("<Control-y>", lambda event: self.redo())


    def load_image(self):
        """Load an image from the file system."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.png"), ("Image Files", "*.jpg"), ("Image Files", "*.JPG"),
                       ("Image Files", "*.jpeg"), ("Image Files", "*.bmp")])
        if not file_path:
            return

        self.image, self.original_image = self.image_loader.load_image(file_path)
        self.thumbnail = self.image_resizer.resize_image(self.image, 600, 600)
        self.canvas_renderer.display_image(self.canvas, self.thumbnail)

    def save_image(self, event=None):  # Add an optional event parameter
        if self.cropped_image is None:
            messagebox.showerror("Error", "No cropped image to save.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                 filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"),
                                                            ("All files", "*.*")])
        if file_path:
            cv2.imwrite(file_path, self.cropped_image)
            messagebox.showinfo("Success", "Image saved successfully.")

    def resize_image(self, value):
        if self.original_image is None:
            return  # Do nothing if no image is loaded

        scale = float(value)
        self.thumbnail = self.image_resizer.resize_image(self.original_image, int(600 * scale), int(600 * scale))
        self._push_to_undo_stack(self.thumbnail.copy())
        self.canvas_renderer.display_image(self.canvas, self.thumbnail)

    def start_crop(self, event):
        self.cropper.start_crop(event, self.canvas)

    def update_crop(self, event):
        self.cropper.update_crop(event, self.canvas)

    def perform_crop(self, event):
        self.cropped_image = self.cropper.perform_crop(event, self.canvas, self.original_image, self.thumbnail)
        if self.cropped_image is not None:  # Check if cropping is done or not.
            self._push_to_undo_stack(self.cropped_image.copy())
            self.canvas_renderer.display_cropped_image(self.cropped_canvas_frame, self.cropped_image)

    def _push_to_undo_stack(self, image):
        self.undo_stack.append(image)
        self.redo_stack.clear()

    def rotate_image(self):
        """Rotate the image by 90 degrees."""
        self.cropped_canvas_frame.grid_forget()
        self.is_cropped_frame_hidden = True
        self.original_image = self.image_rotator.image_rotator(self.original_image, 90, self.canvas)
        self.edited_image = self.image_resizer.resize_image(self.original_image, 600, 600)
        self.canvas_renderer.display_image(self.canvas, self.edited_image)

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack.pop())
            self.cropped_image = self.undo_stack[-1]
            self.canvas_renderer.display_cropped_image(self.cropped_canvas_frame, self.cropped_image)

    def redo(self):
        if self.redo_stack:
            self.cropped_image = self.redo_stack.pop()
            self.undo_stack.append(self.cropped_image)
            self.canvas_renderer.display_cropped_image(self.cropped_canvas_frame, self.cropped_image)

    def clear_all(self):
        self.image = None
        self.thumbnail = None
        self.cropped_image = None
        self.original_image = None
        self.undo_stack = []
        self.redo_stack = []

        self.canvas_renderer.clear_canvas(self.canvas)
        self.canvas_renderer.clear_cropped_canvas(self.cropped_canvas_frame)
        self.resize_slider.set(1.0)

        # Reset the cropped image frame (important!)
        for widget in self.cropped_canvas_frame.winfo_children():
            widget.destroy()
        self.cropped_canvas_frame.pack_forget()

        messagebox.showinfo("Cleared", "Image editor reset.")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorApp(root)
    root.mainloop()