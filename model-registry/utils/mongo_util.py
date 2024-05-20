
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo import MongoClient
from config.settings import Config
import logging

class MongoUtil:

    def __init__(self):
        ''' Constructor for MongoUtil class'''
        self.client = MongoClient(host=Config.MONGO_DB_CONNECTION_URI)
        try:
            self.client.server_info()
        except Exception as e:
            raise e
        self.logger = logging.getLogger(Config.APPLICATION_NAME + '.mongo_util')

    def find_one_by_filters(self, filter_dict):
        ''' Find one record by filters
        Args:
            filter_dict: dict : Filter dictionary
        Returns:
            dict : Record
        '''
        try:
            db:Database = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection:Collection = db[Config.MONGO_COLLECTION_NAME]
            res = collection.find_one(filter_dict, {"_id": 0})
            return res
        except Exception as e:
            self.logger.error("Error in find_one_by_filters: " + str(e))
            raise e

    def find_by_filters_update_one(self, filter_dict, new_record:dict, upsert=False):
        ''' Find by filters and update one record
        Args:
            filter_dict: dict : Filter dictionary
            new_record: dict : New record
            upsert: bool : Upsert flag
        Returns:
            dict : Record
        '''            
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]
            return collection.update_one(filter_dict, {"$set": new_record}, upsert=upsert)
        except Exception as e:
            self.logger.error("Error in find_by_filters_update_one: " + str(e))
            raise e
    
    def delete_by_filters(self, filter_dict):
        ''' Delete by filters
        Args:
            filter_dict: dict : Filter dictionary
        Returns: 
            dict : Record
        '''
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]
            return collection.delete_one(filter_dict)
        except Exception as e:
            self.logger.error("Error in delete_by_filters: " + str(e))
            raise e

    def find_and_update_many(self, filter_field:str, filter_value, new_record:dict):
        ''' Find and update many records
        Args:
            filter_field: str : Filter field
            filter_value: str : Filter value
            new_record: dict : New record
        Returns:
            dict : Record
        '''
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]            
            return collection.update_many({filter_field: filter_value}, {"$set": new_record}, upsert=True)
        except Exception as e:
            self.logger.error("Error in find_and_update_many: " + str(e))
            raise e

    def find_by_id_and_update_field(self, id:int, field:str, new_field_value:str):
        ''' Find by id and update field
        Args:
            id: int : Id
            field: str : Field
            new_field_value: str : New field value
        Returns:
            dict : Record
        '''
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]            
            return collection.find_one_and_update(
                    {"_id" : id },
                    {"$set":
                        { field: new_field_value} 
                    }
                )
        except Exception as e:
            self.logger.error("Error in find_by_id_and_update_field: " + str(e))
            raise e

    def insert_one(self, new_record:dict):
        ''' Insert one record
        Args:
            new_record: dict : New record
        Returns:
            dict : Record
        '''
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]            
            return collection.insert_one(
                   new_record)
        except Exception as e:
            self.logger.error("Error in insert_one: " + str(e))
            raise e

    def find_all_by_filter(self, page_num, pagesize, filter_dict):
        ''' Find all records by filter
        Args:
            filter_dict: dict : Filter dictionary
        Returns:
            list : Records
        '''
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]
            #record = collection.find(filter_dict, {"_id": 0}).limit(limit).skip(offset)
            record = collection.find(filter_dict, {"_id": 0}).skip(pagesize*(page_num-1)).limit(pagesize)
            return list(record)
        except Exception as e:
            self.logger.error("Error in find_all_by_filter: " + str(e))
            raise e
    
    def delete_all_records(self):
        ''' Delete all records
        Returns:
            dict : Record
        '''
        try:
            db = self.client.get_database(name = Config.MONGO_DB_NAME)
            collection = db[Config.MONGO_COLLECTION_NAME]
            return collection.delete_many({})
        except Exception as e:
            self.logger.error("Error in delete_all_records: " + str(e))
            raise e
    
mongo_util = MongoUtil()