from config.settings import Config
from enums.model_types import ModelType
import requests, os, logging

class ModelUtil:

    def __init__(self) -> None:
        self.logger = logging.getLogger(Config.APPLICATION_NAME + '.model_util')

    def get_model_info_from_registry(self, model_name=None, model_version=None) -> dict:
        """ Get model information from model registry
        Args:
            model_name (str): Model name
            model_version (str): Model version
            Returns: Model information """
        
        if model_name is None:
            model_name = Config.MODEL_NAME
        if model_version is None:
            model_version = str(Config.MODEL_VERSION)

        if model_name is None or model_version is None:
            if not Config.CAN_START_EMPTY:
                self.logger.error("Model name and version required")
                raise Exception("Model name and version required")
            return None
        else:
            print("Model Name:", model_name)
            print("Model Version:", model_version)
            # Get model info from model registry
            request_uri = Config.MODEL_REGISTRY_URI + "/model-registry/get-model?model_name=" + model_name + "&version=" + str(model_version)
            print("Request URI:", request_uri)
            model_info = requests.get(request_uri)
            if model_info.status_code != 200:
                self.logger.error("Error in getting model info: " + model_info.text)
                raise Exception(model_info.text)
            
            model_info = model_info.json()
            return model_info

    def load_model(self, model_info):
        """ Load model based on model type
        Args:
            model_info (dict): Model information from model registry
            Returns: Model object """

        model = None
        model_path = self.get_model_path(model_info['location'], model_info)
        model_type = model_info['model_type']
        print("Model Path:", model_path)

        if model_type is None:
            self.logger.error("Model type is required")
            raise Exception("Model type is required")
        
        if model_type == ModelType.PYTORCH_VISION.value:
            from models.pytorch_vision_model import PytorchVisionModel
            model = PytorchVisionModel()
            model.load(model_path, model_info['model_class_name'])
        elif model_type == "decision_tree_regressor":
            from models.decision_tree_regressor import DecisionTreeRegressorModel
            model = DecisionTreeRegressorModel()
            model.load(model_path, model_info['model_class_name'])
        elif model_type == "lightgbm":
            self.logger.error("Model type not implemented yet")
            raise Exception("Model type not implemented yet")
        else:
            self.logger.error("Model type not implemented yet")
            raise Exception("Model type not implemented yet")
        return model

    def get_model_path(self, location, model_info) -> str:
        """ Get model path from model registry based on model location
        Args:
            location (str): Model location
            model_info (dict): Model information from model registry """
        
        if location == "file_system":
            file_extension = model_info['model_file_path'].split('.')[-1]
            model_path = os.path.join(Config.MODEL_FILES_PATH, model_info['model_name'] + '_' + str(model_info['version']) + '.' + file_extension)
            return model_path
        elif location == "s3":
            # prepare model path, download model from s3 and return the model path
            pass
        elif location == "gcp":
            # prepare model path, download model from gcp and return the model path
            pass
        elif location == "azure":
            # prepare model path, download model from azure and return the model path
            pass
    
model_util = ModelUtil()    