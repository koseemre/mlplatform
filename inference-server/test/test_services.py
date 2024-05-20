import random, os, sys, unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from utils.model_util import ModelUtil
from services.inference_service import InferenceService
from config.settings import Config

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.model_util = ModelUtil()
        self.inference_service = InferenceService()

    def tearDown(self):
        self.model_util = None
        self.inference_service = None
    
    def test_load_and_predict(self):
        
        # preprare mock model_info (assumed fetched from model registry)
        model_info = {
            "model_name": "test_diabetes_dt",
            "version": 1,
            "location": "file_system",
            "model_file_path": "test-model-files/test_diabetes_dt_1.pkl",
            "model_type": "decision_tree_regressor",
            "model_class_name": None
        }
        # we need to make sure the model is loaded
        model_info['model_file_path'] = os.path.join(Config.MODEL_FILES_PATH, model_info['model_file_path'])
        print(model_info['model_file_path'])
        model = self.model_util.load_model(model_info)
        assert model is not None
        self.inference_service.model = model
        
        # prepare input data
        input_data = {
            "input_type": "numpy_array",
            "input": [[0.01991321417832592,0.05068011873981862,0.10480868947391528,0.07007229917592636,-0.035967781275239266,-0.02667890283117104,-0.024992656631590206,-0.002592261998183278,0.0037090603325595967,0.040343371647878594]]
        }
        response = self.inference_service.inference_model(input_data)
        print(response)
        assert response is not None
    

if __name__ == '__main__':
    unittest.main(verbosity=2)        