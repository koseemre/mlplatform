import random, os, sys, unittest

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask_main_unit_test import create_unit_test_app
from requests_toolbelt.multipart.encoder import MultipartEncoder

class TestWebApp(unittest.TestCase):

    def setUp(self):
        self.app = create_unit_test_app()
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        # remove all the files in the test-model-files directory
        model_files_path = self.app.config['MODEL_FILES_PATH']
        for file in os.listdir(model_files_path):
            file_path = os.path.join(model_files_path, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        # remove all the records in the test-model-registry collection
        from services.model_registry_service import ModelRegistryService
        model_registry_service = ModelRegistryService()
        model_registry_service.delete_all_records()
        self.app = None
        self.appctx = None

    def test_healthcheck(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data == b'Healthy'
    
    def test_create_new_record(self):
        # generate 10 digit decimal number
        random_version_number = random.randint(1000000000, 9999999999)
        model_name = 'model1'
        self.create_record(model_name, random_version_number)
    
    def test_update_record(self):
        
        # As first step, create a new record
        # generate 10 digit decimal number
        random_version_number = random.randint(1000000000, 9999999999)
        model_name = 'model1'
        self.create_record(model_name, random_version_number) 
        
        # As second step, update the record
        # prepare the new meta data
        test_model_file_name = 'test_model_file.txt'
        with open(test_model_file_name, 'w', newline='') as file:
            file.write('New line of text')
                
        new_meta_data = '{{ "model_name": "{}", "version": {},  "model_class_name": null, "model_type": "test_type", "feature_list": ["feature1", "feature3"], "owner_id": 542, "location": "file_system" }}'.format(model_name, random_version_number)
        # prepare multipart request
        file = open(test_model_file_name, 'rb')
        multipart_data = MultipartEncoder(
            fields={
                    # a file upload field
                    'model_file': (test_model_file_name, file, 'text/plain'),
                    'new_meta_data': new_meta_data,
                    'current_model_name': model_name,
                    'current_version': str(random_version_number)
                }
            )
        response = self.client.post('/model-registry/update-record', data=multipart_data,
                        headers={'Content-Type': multipart_data.content_type})
        assert response.status_code == 200
        file.close()

    def test_delete_record(self):
        # As first step, create a new record
        # generate 10 digit decimal number
        random_version_number = random.randint(1000000000, 9999999999)
        model_name = 'model1'
        self.create_record(model_name, random_version_number)
        # As second step, delete the record
        #print("Deleting record with model_name: {} and version: {}".format(model_name, random_version_number))
        delete_record = '{{ "model_name": "{}", "version": {} }}'.format(model_name, random_version_number)
        response = self.client.post('/model-registry/delete-record', data=delete_record,
                        headers={'Content-Type': 'application/json'})
        assert response.status_code == 200
    
    def test_get_record(self):
        # As first step, create a new record
        test_model_file_name = 'test_model_file.txt'
        with open(test_model_file_name, 'w', newline='') as file:
            file.write('New line of text')
        # generate 10 digit decimal number
        random_version_number = random.randint(1000000000, 9999999999)
        model_name = 'model1'
        self.create_record(model_name, random_version_number)      
        # As second step, get the record
        response = self.client.get('/model-registry/get-model?model_name={}&version={}'.format(model_name, random_version_number))
        assert response.status_code == 200

    def test_get_all_records(self):
        # As first step, create a new record
        test_model_file_name = 'test_model_file.txt'
        with open(test_model_file_name, 'w', newline='') as file:
            file.write('New line of text')
        # generate 10 digit decimal number
        random_version_number = random.randint(1000000000, 9999999999)
        model_name = 'model1'
        self.create_record(model_name, random_version_number)
        # As second step, get all the records
        response = self.client.get('/model-registry/list-models?page_num=1&pagesize=10')
        assert response.status_code == 200
        records = response.json
        assert len(records) > 0

    def create_record(self, model_name, version):
        test_model_file_name = 'test_model_file.txt'
        with open(test_model_file_name, 'w', newline='') as file:
            file.write('New line of text')
        create_meta_data = '{{ "model_name": "{}", "model_class_name": null, "model_type": "test_type", "version": {}, "feature_list": [], "owner_id": 123, "location": "file_system" }}'.format(model_name, version)
        
        file = open(test_model_file_name, 'rb')
        multipart_data = MultipartEncoder(
            fields={
                    # a file upload field
                    'model_file': (test_model_file_name, file, 'text/plain'),
                    'meta_data': create_meta_data
                }
            )
        response = self.client.post('/model-registry/create-new-record', data=multipart_data,
                        headers={'Content-Type': multipart_data.content_type})
        file.close()
        assert response.status_code == 200

if __name__ == '__main__':
    unittest.main(verbosity=2)        