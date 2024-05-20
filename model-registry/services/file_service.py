from enums.file_location_types import FileLocationType
from werkzeug.datastructures import FileStorage
import os, logging
from config.settings import Config

class FileService:
    """Service class for model file operations"""
    def __init__(self) -> None:
        self.logger = logging.getLogger(Config.APPLICATION_NAME + '.file_service')

    def save_file(self, file_location_type:str, file_path:str, file:FileStorage):
        ''' Save file to a location
        Args:
            file_location_type: FileLocationType : File location type
            file_path: str : File path
            file: FileStorage : Model file
        Returns:
            bool : True if file is saved successfully, False otherwise
        '''
        try:
            if file_location_type == FileLocationType.FILE_SYSTEM.value:
                file.save(file_path)
                return True
            elif file_location_type == FileLocationType.CLOUD_GCP_BUCKET.value:
                return self.save_file_to_gcp_bucket(file_path, file)
        except Exception as e:
            self.logger.error("Error in saving file: " + str(e))
            raise e
    
    def remove_file(self, file_location_type:str, file_path:str):
        ''' Remove file from a location
        Args:
            file_location_type: FileLocationType : File location type
            file_path: str : File path
        Returns:
            bool : True if file is removed successfully, False otherwise
        '''
        try:
            if file_location_type == FileLocationType.FILE_SYSTEM.value:
                os.remove(file_path)
                return True
            elif file_location_type == FileLocationType.CLOUD_GCP_BUCKET.value:
                return self.remove_file_from_gcp_bucket(file_path)
        except Exception as e:
            self.logger.error("Error in removing file: " + str(e))
            raise e
        
    def remove_file_from_gcp_bucket(self, file_path:str):
        ''' Remove file from GCP bucket
        Args:
            file_path: str : File path
        Returns:
            bool : True if file is removed successfully, False otherwise
        '''
        # code to remove file from GCP bucket
        raise NotImplementedError
    
    def save_file_to_gcp_bucket(self, file_path:str, file:FileStorage):
        ''' Save file to GCP bucket
        Args:
            file_path: str : File path
            file: FileStorage : File
        Returns:
            bool : True if file is saved successfully, False otherwise
        '''
        # code to save file to GCP bucket
        raise NotImplementedError

        ''' Save file to S3
        Args:
            file_path: str : File path
            file: FileStorage : File
        Returns:
            bool : True if file is saved successfully, False otherwise
        '''
        # code to save file to S3
        raise NotImplementedError

file_service = FileService()

    