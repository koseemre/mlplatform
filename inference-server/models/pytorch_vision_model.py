import torch

from models.base_model import BaseModel
from enums.input_types import InputType
from torchvision.models import get_model
import torchvision.transforms as transforms
from PIL import Image
from io import BytesIO
import base64

class PytorchVisionModel(BaseModel):
    def __init__(self):
        self.model = None
        self.preprocess = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
    def predict(self, input_data, input_data_type):
        """ Predict using Pytorch Vision Model
        Args:
            input_data: Input data
            input_data_type (str): Input data type
        Returns: Prediction output
        """
        if input_data_type == InputType.BASE64_IMAGE.value:
            image = Image.open(BytesIO(base64.b64decode(input_data)))
            input_tensor = self.preprocess(image)
            input_batch = input_tensor.unsqueeze(0)
            input_batch = input_batch.to(self.device)
        else:
            raise Exception("Input data type not supported")
        
        self.model.eval()
        with torch.no_grad():
            output = self.model(input_batch)
            max_prob, predicted_idx = torch.max(output, 1)
            return {"max_prob": max_prob.item(), "predicted_class": predicted_idx.item()}            
    
    def save(self, path: str, model_info: dict):
        """ Save Pytorch Vision Model
        Args:
            path (str): Model path
            model_info (dict): Model information
        """
        save_path = path + model_info['model_name'] + '_' + model_info['version'] + '.pth'
        torch.save(self.model.state_dict(), save_path)

    def load(self, model_path, pytorch_vision_model_class_name: str, custom_model=False):
        """ Load Pytorch Vision Model
        Args:
            model_path (str): Model path
            pytorch_vision_model_class_name (str): Pytorch Vision Model Class Name
            custom_model (bool): Custom model flag
        """
        print("Pytorch Vision Model Class Name:", pytorch_vision_model_class_name)
        pretrained_weights = torch.load(model_path)
        if custom_model:
            # Load custom model
            raise Exception("Custom model loading is not implemented yet")
        else:
            # Get model from torchvision repository
            self.model = get_model(pytorch_vision_model_class_name, pretrained=False)
        self.model.load_state_dict(pretrained_weights)
        self.model.to(self.device)
        self.model_class_name = pytorch_vision_model_class_name

    def train(self, X, y):
        """ Train Pytorch Vision Model
        Args:
            X (array): Input data
            y (array): Target data
        """
        raise Exception("Training is not implemented for Pytorch Vision Model")
    
    def evaluate(self, X, y):
        """
        Evaluate Pytorch Vision Model
        Args:
            X (array): Input data
            y (array): Target data
        """
        raise Exception("Evaluation is not implemented for Pytorch Vision Model")
                