from dotenv import load_dotenv
import os

DEPLOYMENT=os.getenv('DEPLOYMENT', "DEV")
if DEPLOYMENT == "DEV":
    load_dotenv('.env.dev')
elif DEPLOYMENT == "PROD":
    load_dotenv('.env.prod')
elif DEPLOYMENT == "TEST":
    load_dotenv('.env.test')

class Config:

    APPLICATION_NAME = os.getenv('APPLICATION_NAME', "inference-server")

    MODEL_NAME = os.getenv("MODEL_NAME")
    MODEL_VERSION = os.getenv("MODEL_VERSION")
    if MODEL_VERSION is not None:
        MODEL_VERSION = int(MODEL_VERSION)

    CAN_START_EMPTY = eval(os.getenv("CAN_START_EMPTY", "True"))

    # According to model location, model path could be different like local, s3, etc.
    MODEL_REGISTRY_HOST = os.getenv("MODEL_REGISTRY_HOST", "host.docker.internal")
    MODEL_REGISTRY_PORT = int(os.getenv("MODEL_REGISTRY_PORT", 8080))

    MODEL_REGISTRY_URI = os.getenv("MODEL_REGISTRY_URI", "http://{service_name}:{port}")
    MODEL_REGISTRY_URI = MODEL_REGISTRY_URI.format(service_name=MODEL_REGISTRY_HOST, port=MODEL_REGISTRY_PORT)
    
    MODEL_FILES_PATH = os.getenv('MODEL_FILES_PATH')
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')