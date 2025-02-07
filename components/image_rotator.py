import cv2
import numpy as np

class ImageRotator:
    def __init__(self):
        self.rect_id = None

    def image_rotator(self, image, angle, canvas):
        """Rotate the image by the specified angle without cropping."""
        height, width = image.shape[:2]
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

        # Calculate new dimensions to accommodate the rotated image
        cos = np.abs(rotation_matrix[0, 0])
        sin = np.abs(rotation_matrix[0, 1])
        new_width = int((height * sin) + (width * cos))
        new_height = int((height * cos) + (width * sin))

        # Adjust the rotation matrix to center the rotated image
        rotation_matrix[0, 2] += (new_width / 2) - (width / 2)
        rotation_matrix[1, 2] += (new_height / 2) - (height / 2)


        rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height))
        return rotated_image