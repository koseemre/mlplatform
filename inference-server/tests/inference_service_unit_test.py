import unittest
from unittest.mock import patch, MagicMock
from services.inference_service import InferenceService

class TestInferenceService(unittest.TestCase):
    @patch('service.inference_service.model_util')
    def setUp(self, mock_model_util):
        self.mock_model = MagicMock()
        mock_model_util.get_model_info_from_registry.return_value = 'model_info'
        mock_model_util.load_model.return_value = self.mock_model
        self.service = InferenceService()

    @patch('service.inference_service.model_util')
    def test_init(self, mock_model_util):
        mock_model_util.get_model_info_from_registry.assert_called_once()
        mock_model_util.load_model.assert_called_once_with('model_info')
        self.assertEqual(self.service.model, self.mock_model)

    @patch('service.inference_service.model_util')
    def test_init_no_model(self, mock_model_util):
        mock_model_util.load_model.return_value = None
        with self.assertRaises(Exception):
            InferenceService()

    def test_inference_model(self):
        data = {"input": "input_data", "input_type": "input_data_type"}
        self.mock_model.predict.return_value = ("max_prob", "predicted_class")
        result = self.service.inference_model(data)
        self.mock_model.predict.assert_called_once_with("input_data", "input_data_type")
        self.assertEqual(result, {"max_prob": "max_prob", "predicted_class": "predicted_class"})

if __name__ == '__main__':
    unittest.main()