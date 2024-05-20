# 3rd party imports
from werkzeug.wrappers import Response
from flask import Blueprint, request
# python imports
import json
# local imports
from services.inference_service import inference_service

default_controller = Blueprint('default_controller', __name__, url_prefix='/')

@default_controller.route('/inference-model', methods=["POST"])
def inference_model():
    """ This function performs inference on the provided data.
    ---
    tags:
        - Inference
    parameters:
        - name: data
          in: body
          type: object
          required: true
          description: The data to perform inference on.
    responses:
        200:
            description: The result of the inference.
            schema:
                type: object
        500:
            description: An error occurred while performing inference.
    """
    try:
        data = request.get_json()
        result = inference_service.inference_model(data)
        return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"error": str(e)}),
                    status=500,
                    mimetype="application/json")
    

@default_controller.route('/load-model', methods=["POST"])
def load_model():
    """ This function loads a model.
    ---
    tags:
        - Inference
    parameters:
        - name: model_data
          in: body
          type: object
          required: true
          description: The data to load the model.
    responses:
        200:
            description: The result of the model load.
            schema:
                type: object
        500:
            description: An error occurred while loading the model.
    """
    try:
        model_data = request.get_json()
        result = inference_service.load_model(model_data)
        return Response(response=json.dumps(result),
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=json.dumps({"error": str(e)}),
                    status=500,
                    mimetype="application/json")    