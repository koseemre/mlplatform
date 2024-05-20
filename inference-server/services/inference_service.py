import warnings
warnings.filterwarnings("ignore")
import logging
from config.settings import Config

# local imports
from utils.model_util import model_util


class InferenceService:
    
    def __init__(self) -> None:
        self.model = None
        self.logger = logging.getLogger(Config.APPLICATION_NAME + '.inference_service')

        model_info = model_util.get_model_info_from_registry()
        if model_info is not None:
            self.logger.info("Model Info: %s", model_info)
            self.model = model_util.load_model(model_info)

    def inference_model(self, data) -> dict:
        ''' Inference model
        Args:
            data (dict): Input data
            Returns: Prediction
        '''
        if self.model is None:
            self.logger.error("Model is not loaded")
            raise Exception("Model is not loaded")
        
        input_data = data["input"]
        input_data_type = data["input_type"]
        prediction = self.model.predict(input_data, input_data_type)
        return prediction

    def load_model(self, model_data) -> dict:
        ''' Load model from model registry
        Args:
            model_data (dict): Model information
            Returns: Message
        '''
        model_name = model_data["model_name"]
        model_version = model_data["version"]
        model_info = model_util.get_model_info_from_registry(model_name, model_version)
        self.model = model_util.load_model(model_info)
        return {"message": "Model loaded successfully"}

inference_service = InferenceService()    