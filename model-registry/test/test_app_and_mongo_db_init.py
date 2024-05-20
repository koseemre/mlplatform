from flask import current_app
import unittest
import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from flask_main_unit_test import create_unit_test_app

class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.app = create_unit_test_app()
        self.appctx = self.app.app_context()
        self.appctx.push()
        self.client = self.app.test_client()

    def tearDown(self):
        self.appctx.pop()
        self.app = None
        self.appctx = None

    def test_app(self):
        assert self.app is not None
        assert current_app == self.app

    def test_healthcheck(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert response.data == b'Healthy'
    
if __name__ == '__main__':
    unittest.main(verbosity=2)        