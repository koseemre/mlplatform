__author__ = "Emre Kose"
__status__ = "Development"

import warnings
warnings.filterwarnings("ignore")

from utils.mongo_util import mongo_util
from config.settings import Config
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from datetime import datetime, timezone
from flask import Request
import os, json
from werkzeug.datastructures import FileStorage
import logging
from services.file_service import file_service

class ModelRegistryService:
    
    def __init__(self) -> None:
        ''' Constructor for ModelRegistryService class'''
        # create a collection in MongoDB if it does not exist
        db:Database = mongo_util.client.get_database(name = Config.MONGO_DB_NAME)
        self.logger = logging.getLogger(Config.APPLICATION_NAME + '.model_registry_service')

        try:
            collection_list = db.list_collection_names()

            if Config.MONGO_COLLECTION_NAME not in collection_list:
                print("Creating collection:", Config.MONGO_COLLECTION_NAME)
                db.create_collection(Config.MONGO_COLLECTION_NAME)
        except Exception as e:
            self.logger.error("Error in creating collection: " + str(e))
            pass
        # create an index for the collection
        platform_collection:Collection = db[Config.MONGO_COLLECTION_NAME]
        platform_collection.create_index({"model_name":1, "version":1}, unique=True)

    def create_and_save_model_record(self, new_model_record, model_file:FileStorage, file_name:str):
        ''' Create and save a new model record
        Args:
            new_model_record: dict : New model record
            model_file: FileStorage : Model file
            file_name: str : File name
        Returns:    
            dict : Insert result
        '''
        try:

            # create a new file name by combining model_name, version and file extension
            extension = file_name.split('.')[1]
            if len(extension) == 0:
                raise Exception("Invalid file extension.")
            
            new_file_name = new_model_record['model_name'] + '_' + str(new_model_record['version']) + '.' + extension
            model_file_path = os.path.join(Config.MODEL_FILES_PATH, new_file_name)
            new_model_record['model_file_path'] = model_file_path
            # save the model file
            self.logger.info("model is started to save:" + model_file_path)
            file_service.save_file(new_model_record['location'], model_file_path, model_file)
            #model_file.save(model_file_path)

            self.logger.info("model has saved to:" + model_file_path)

            # save the model record
            now = datetime.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')
            new_model_record['creation_date'] = now
            new_model_record['update_date'] = now
            insert_result = mongo_util.insert_one(new_model_record)

            # return the result of the insert operation
            return insert_result
        except DuplicateKeyError as e:
            self.logger.error("Error in create_and_save_model_record: " + str(e))
            raise Exception("Model record already exists with the same model_name and version.")
        except Exception as e:
            self.logger.error("Error in create_and_save_model_record: " + str(e))
            raise e

    def update_model_record_by_model_name_and_version(self, updated_record, current_model_name, current_version, new_model_file, new_file_name):
        ''' Update a model record by model_name and version
        Args:
            request: Request : Request object
        Returns:    
            dict : Update result
        '''

        filter_dict = {'model_name': current_model_name, 'version': current_version}
        updated_record['update_date'] = datetime.now().astimezone(timezone.utc).strftime('%Y-%m-%d %H:%M:%S.%f%z')

        # get the current model record by model_name and version and check if it exists, if not raise an exception
        old_model_record = mongo_util.find_one_by_filters(filter_dict)
        if old_model_record is None:
            raise Exception("Model record not found by given model_name and version.")
        
        if new_model_file is not None and new_file_name is not None and new_file_name != '':
            # remove old model file
            old_model_file_path = old_model_record['model_file_path']
            #os.remove(old_model_file_path)
            file_service.remove_file(old_model_record['location'], old_model_file_path)
            # create a new file name by combining model_name, version and file extension
            extension = new_file_name.split('.')[1]
            if len(extension) == 0:
                self.logger.error("Invalid file extension.")
                raise Exception("Invalid file extension.")
            new_file_name_ = updated_record['model_name'] + '_' + str(updated_record['version']) + '.' + extension
            model_file_path = os.path.join(Config.MODEL_FILES_PATH, new_file_name_)
            updated_record['model_file_path'] = model_file_path
            # save the model file
            file_service.save_file(updated_record['location'], model_file_path, new_model_file)
            self.logger.info("new model has saved to:" + model_file_path)
        else:
            # if model file will not being updated, keep the old model file name and version same
            updated_record['version'] = old_model_record['version']
            updated_record['model_name'] = old_model_record['model_name']

        # update the model record
        update_result = mongo_util.find_by_filters_update_one(filter_dict, updated_record)
        if update_result.modified_count == 0:
            error_message = "Model record not found by given model_name and version."
            self.logger.error(error_message)
            raise Exception(error_message)
        
        self.logger.info("Model record updated successfully.")
        return update_result

    def delete_model_record(self, delete_record: dict):
        ''' Delete a model record
        Args:
            delete_record: dict : Delete record
        Returns:
            dict : Delete result
        '''
        # get the current model record by model_name and version and check if it exists, if not raise an exception
        filter_dict = {'model_name': delete_record['model_name'], 'version': delete_record['version']}
        model_record = mongo_util.find_one_by_filters(filter_dict)
        if model_record is None:
            self.logger.error("Model record not found by given model_name and version.")
            raise Exception("Model record not found by given model_name and version.")
        
        delete_result = mongo_util.delete_by_filters(delete_record)
        if delete_result.deleted_count == 0:
            self.logger.error("Model could not be deleted.")
            raise Exception("Model could not be deleted.")
        else:
            # remove old model file
            model_file_path = model_record['model_file_path']
            #os.remove(model_file_path)
            file_service.remove_file(model_record['location'], model_file_path)

            self.logger.info("Model record deleted successfully.")
        return delete_result

    def get_model(self, model_name, model_version):
        ''' Get a model record by model_name and version
        Args:
            model_name: str : Model name
            model_version: int : Model version
        Returns:
            dict : Model record
        '''
        filter_dict = {'model_name': model_name, 'version': int(model_version)}
        model_data = mongo_util.find_one_by_filters(filter_dict)
        if model_data is None:
            self.logger.error("Model record not found by given model_name and version.")
            raise Exception("Model record not found by given model_name and version.")
        return model_data
    
    def get_models(self, page_num, pagesize):
        ''' Get all model records
        Args:
            page_num: int : Page number
            pagesize: int : Page size
        Returns:    
            list : Model records
        '''
        return mongo_util.find_all_by_filter(page_num, pagesize, filter_dict = {})

    def delete_all_records(self):
        ''' Delete all model records
        Returns:
            dict : Delete result
        '''
        return mongo_util.delete_all_records()
    
model_registry_service = ModelRegistryService()