import cv2

class ImageResizer:
    def resize_image(self, image, canvas_width, canvas_height):
        """Resize the image to fit the canvas dimensions while maintaining aspect ratio."""
        height, width = image.shape[:2]
        scale = min(canvas_width / width, canvas_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
        return resized_image
