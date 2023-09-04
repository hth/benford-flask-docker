from pymongo import MongoClient
from flask import Flask

import os
import configparser
import signal

databaseInit = Flask(__name__)

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))


# If database connection fails or when mongo stops working/responding, stop the web server
def get_database():
    client = None
    try:
        # Provide the mongodb url to connect python to mongodb using pymongo
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(config['PROD']['DB_URI'])

        if client.is_primary:
            databaseInit.logger.debug("DB Connection is success")
        else:
            databaseInit.logger.debug("DB Connection is failed, shutting down server")
            os.kill(os.getpid(), signal.SIGINT)

        # Create the database for our example (we will use the same database throughout the tutorial
        return client['benford_db']
    except client.errors.ServerSelectionTimeoutError as err:
        databaseInit.logger.error("Exiting server as not connected to db " + err)
        os.kill(os.getpid(), signal.SIGINT)
    except TypeError:
        databaseInit.logger.error("Exiting server as not connected to db")
        os.kill(os.getpid(), signal.SIGINT)


# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":
    databaseInit.config['MONGO_URI'] = config['PROD']['DB_URI']

    # Get the database
    dbname = get_database()
