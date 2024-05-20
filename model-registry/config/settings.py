from dotenv import load_dotenv
import os

DEPLOYMENT=os.getenv('DEPLOYMENT', "DEV")
if DEPLOYMENT == "DEV":
    load_dotenv('.env.dev')
elif DEPLOYMENT == "PROD":
    load_dotenv('.env.prod')
elif DEPLOYMENT == "TEST":
    load_dotenv('.env.test')
else:
    load_dotenv('.env.dev')

class Config:

    APPLICATION_NAME=os.getenv('APPLICATION_NAME', "model-registry")
    
    # MongoDB Configs
    MONGO_DB_HOST=os.getenv('MONGO_DB_HOST', "localhost")
    MONGO_DB_PORT=int(os.getenv('MONGO_DB_PORT', "27017"))
    MONGO_DB_USER=os.getenv('MONGO_DB_USER', "root")
    MONGO_DB_PASSWORD=str(os.getenv('MONGO_DB_PASSWORD'))

    MONGO_DB_NAME=os.getenv('MONGO_DB_NAME', "model-registry")
    MONGO_COLLECTION_NAME=os.getenv('MONGO_COLLECTION_NAME', "model-registry")

    MONGO_DB_CONNECTION_URI="mongodb://{username}:{password}@{hostname}:{port}/?authSource=admin&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    MONGO_DB_CONNECTION_URI=MONGO_DB_CONNECTION_URI.format(username = MONGO_DB_USER, password = MONGO_DB_PASSWORD, hostname = MONGO_DB_HOST, port = MONGO_DB_PORT)

    # Model Files Path
    MODEL_FILES_PATH = os.getenv('MODEL_FILES_PATH') #, "/$HOME/data/model-files"
    LOG_FILE_PATH = os.getenv('LOG_FILE_PATH')
    