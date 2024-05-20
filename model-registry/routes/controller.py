# third party imports
from flask import Blueprint, request
from werkzeug.wrappers import Response
# local imports
from services.model_registry_service import model_registry_service
from utils.registry_util import check_fields_of_registry
# python imports
import json

default_controller = Blueprint('default_controller', __name__, url_prefix='/model-registry')

@default_controller.route('/get-model', methods=["GET"])
def get_model_record():
    """
    This function retrieves a model record based on the provided model name and version.
    ---
    tags:
        - Model Registry
    parameters:
        - name: model_name
          in: query
          type: string
          required: true
          description: The name of the model.
        - name: version
          in: query
          type: string
          required: true
          description: The version of the model.
    responses:
        200:
            description: The model record.
            schema:
                type: object
        500:
            description: An error occurred while retrieving the model record.
    """
    try:
        model_name = request.args.get('model_name')
        model_version = request.args.get('version')
        model_data = model_registry_service.get_model(model_name, model_version)
        return Response(response=json.dumps(model_data),
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=str(e),
                    status=500,
                    mimetype="application/json")

@default_controller.route('/create-new-record', methods=["POST"])
def create_new_record():
    """
    This function creates a new model record.
    ---
    tags:
        - Model Registry
    parameters: 
        - name: meta_data
          in: formData
          type: string
          required: true
          description: The metadata for the model record.
        - name: model_file
          in: formData
          type: file
          required: true
          description: The model file. 
    responses:
        200:
            description: The model record was created successfully.
        500:
            description: An error occurred while creating the model record.
    """    
    try:
        model_record=json.loads(request.form.get('meta_data'))
        if 'model_file' not in request.files:
            raise Exception("Model file is required.")
        model_file = request.files['model_file']
        if model_file.filename == '':
            raise Exception("Model file is required")
        
        check_fields_of_registry(model_record)
        model_registry_service.create_and_save_model_record(model_record, model_file, file_name = model_file.filename)
        return Response(response="Created new record",
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=str(e),
                    status=500,
                    mimetype="application/json")
    
@default_controller.route('/list-models', methods=["GET"])
def get_model_list():
    """
    This function retrieves a list of model records.
    ---
    tags:
        - Model Registry
    parameters:
        - name: page_size
          in: query
          type: integer
          required: false
          description: The number of records to retrieve.
          default: 0
        - name: page_num
          in: query
          type: integer
          required: false
          description: The page number.
          default: 1
    responses:
        200:
            description: The list of model records.
            schema:
                type: object
        500:
            description: An error occurred while retrieving the list of model records.
    """    
    try:

        pagesize = int(request.args.get('page_size', 0))
        page_num = int(request.args.get('page_num', 1))
        model_list = model_registry_service.get_models(page_num, pagesize)
        return Response(response=json.dumps(model_list),
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=str(e),
                    status=500,
                    mimetype="application/json")
    
@default_controller.route('/update-record', methods=["POST"])
def update_record():
    """
    This function updates a model record.
    ---
    tags:
        - Model Registry
    parameters:
        - name: new_meta_data
          in: formData
          type: string
          required: true
          description: The updated metadata for the model record.
        - name: current_model_name
          in: formData
          type: string
          required: true
          description: The current name of the model.
        - name: current_version
          in: formData
          type: integer
          required: true
          description: The current version of the model.
        - name: model_file
          in: formData
          type: file
          required: false
          description: The new model file.
    responses:
        200:
            description: The model record was updated successfully.
        500:
            description: An error occurred while updating the model record.
    """

    updated_record=json.loads(request.form.get('new_meta_data'))
    current_model_name = request.form.get('current_model_name')
    current_version = int(request.form.get('current_version'))
    new_model_file = None
    new_file_name = None

    if 'model_file' in request.files:
        new_model_file = request.files['model_file']
        new_file_name = new_model_file.filename
        
    try:
        check_fields_of_registry(updated_record)
        model_registry_service.update_model_record_by_model_name_and_version(updated_record, current_model_name, current_version, new_model_file, new_file_name)
        return Response(response="Updated record",
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=str(e),
                    status=500,
                    mimetype="application/json")

@default_controller.route('/delete-record', methods=["POST"])
def delete_record():
    """
    This function deletes a model record.
    ---
    tags:
        - Model Registry
    parameters:
        - name: model_record
          in: body
          type: object
          required: true
          description: The model record to delete.
    responses:
        200:
            description: The model record was deleted successfully.
        500:
            description: An error occurred while deleting the model record.
    """
    try:
        model_record = request.json
        model_registry_service.delete_model_record(model_record)
        return Response(response="Deleted record",
                    status=200,
                    mimetype="application/json")
    except Exception as e:
        return Response(response=str(e),
                    status=500,
                    mimetype="application/json")
    

