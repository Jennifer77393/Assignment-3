import cv2;

class ImageRotator:
    def __init__(self):
        self.rect_id = None

    def image_rotator(self,image, angle,canvas):
      """Rotate the image by the specified angle."""
      height, width = image.shape[:2]
      rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
      rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))
      return rotated_image
