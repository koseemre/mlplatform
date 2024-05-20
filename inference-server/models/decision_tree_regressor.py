from sklearn.tree import DecisionTreeRegressor
from models.base_model import BaseModel
import joblib

# load the model

class DecisionTreeRegressorModel(BaseModel):

    def __init__(self) -> None:
        self.model:DecisionTreeRegressor = None

    def predict(self, input_data, input_data_type):
        prediction = self.model.predict(input_data)
        return prediction.tolist()
    
    def save(self, path, model_info):
        save_path = path + model_info['model_name'] + '_' + model_info['version'] + '.pkl'
        joblib.dump(self.model, save_path)

    def load(self, model_path, decision_tree_regressor_model_class_name: str):
        print("Decision Tree Regressor Model Class Name:", decision_tree_regressor_model_class_name)
        self.model = joblib.load(model_path)
        self.model_class_name = decision_tree_regressor_model_class_name