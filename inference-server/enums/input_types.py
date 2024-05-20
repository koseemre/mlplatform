from enum import Enum

class InputType(Enum):
    BASE64_IMAGE = "base64_image"
    BYTES_IMAGE = "bytes_image"
    TEXT = "text"
    NUMPY_ARRAY = "numpy_array"