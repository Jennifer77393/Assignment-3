class ImageCropper:
    def __init__(self):
        self.start_x = self.start_y = None
        self.rect_id = None
        self.cropped_image = None

    def start_crop(self, event, canvas):
        """Start the cropping process by capturing the initial coordinates."""
        self.start_x = event.x
        self.start_y = event.y
        if self.rect_id is not None:
                self.canvas.delete(self.rect_id)
        self.rect_id = canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y, outline="red", width=2)

    def update_crop(self, event, canvas):
        """Update the cropping rectangle while the mouse is being dragged."""
        if self.rect_id is not None:
            canvas.coords(self.rect_id, self.start_x, self.start_y, event.x, event.y)

    def perform_crop(self, event, canvas, original_image, thumbnail):
        """Perform the cropping once the mouse button is released."""
        x1, y1, x2, y2 = canvas.coords(self.rect_id)
        x1, x2 = sorted((int(x1), int(x2)))
        y1, y2 = sorted((int(y1), int(y2)))

        thumbnail_height, thumbnail_width = thumbnail.shape[:2]
        scale_x = original_image.shape[1] / thumbnail_width
        scale_y = original_image.shape[0] / thumbnail_height

        x1 = int(x1 * scale_x)
        x2 = int(x2 * scale_x)
        y1 = int(y1 * scale_y)
        y2 = int(y2 * scale_y)

        self.cropped_image = original_image[y1:y2, x1:x2]
        return self.cropped_image
