from PIL import Image
from django.core.exceptions import ValidationError

def validate_avatar(image):
    """
    Validate the avatar image.
    - Must be a valid image file.
    - Must not exceed 20MB in size.
    """    
    try:
        img = Image.open(image)
        img.verify()
    except Exception:
        raise ValidationError("Invalid image file.")

    if image.size > 20 * 1024 * 1024:  
        raise ValidationError("Image file too large. Size must be less than 20MB.")