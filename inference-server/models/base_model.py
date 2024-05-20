
class BaseModel:
    """ Base class for all models """

    def train(self, X, y):
        """ Train the model with the given data
        :param X: input data
        :param y: target data
        """
        raise NotImplementedError("train method must be implemented in derived classes")

    def predict(self, X):
        """ Predict the target data with the given input data
        :param X: input data
        """
        raise NotImplementedError("predict method must be implemented in derived classes")

    def evaluate(self, X, y):
        """ Evaluate the model with the given data
        :param X: input data
        :param y: target data
        """
        raise NotImplementedError("evaluate method must be implemented in derived classes")
    
    def save(self, path: str):
        """ Save the model to the given path """
        raise NotImplementedError("save method must be implemented in derived classes")
    
    def load(self, path: str):
        """ Load the model from the given path """
        raise NotImplementedError("load method must be implemented in derived classes")

