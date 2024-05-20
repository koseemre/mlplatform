from enum import Enum

class ModelType(Enum):
    PYTORCH_VISION = "pytorch_vision"
    PYTORCH_TEXT = "pytorch_text"
    PYTORCH_MULTIMODAL = "pytorch_multimodal"
    XGBOOST = "xgboost"
    LIGHTGBM = "lightgbm"