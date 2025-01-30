import cv2

class ImageLoader:
    def __init__(self):
        self.image = None
        self.original_image = None

    def load_image(self, file_path):
        """Load an image from the file system."""
        self.original_image = cv2.imread(file_path)
        if self.original_image is None:
            raise ValueError("Failed to load the image.")
        
        self.image = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2RGB)
        return self.image, self.original_image
