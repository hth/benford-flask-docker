import os
import configparser
import socket
import signal

from flask import Flask, render_template, request
from benford.api.benfordLaw import benfordLaw_page
from benford.api.benfordLawPRG import benfordLawRPG_page
from logging.config import dictConfig
from werkzeug.local import LocalProxy
from pymongo import MongoClient


appInitialize = Flask(__name__)
appInitialize.register_blueprint(benfordLaw_page)
appInitialize.register_blueprint(benfordLawRPG_page)

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join("config.ini")))
mongoClient = MongoClient(config['PROD']['DB_URI'])
db = mongoClient.get_database()


# This needs to be called once to check connection when server starts. Now being called all the time. Fix me.
# If database connection fails, stop the server
def init():
    try:
        if mongoClient.is_primary:
            appInitialize.logger.debug("DB Connection is success")
        else:
            appInitialize.logger.debug("DB Connection is failed, shutting down server")
            os.kill(os.getpid(), signal.SIGINT)
    except mongoClient.errors.ServerSelectionTimeoutError as err:
        appInitialize.logger.error("Exiting server as not connected to db " + err)
        os.kill(os.getpid(), signal.SIGINT)


@appInitialize.route('/')
@appInitialize.route('/index')
def index():
    try:
        init()

        appInitialize.logger.info("Successfully Displayed Index")
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        if 'name' in request.args:
            name = request.args.get('name')
            array = request.args.getlist('array')
            image = request.args.get('image')
            errors = request.args.get('errors')
            appInitialize.logger.debug('Hostname: %s Ip: %s %s', host_name, host_ip, name)

            result = db['result']
            new_id = result.insert_one({"name": name, "array": array}).inserted_id

            return render_template('index.html', hostname=host_name, ip=host_ip, db=db.client.is_primary, name=name, array=array, image=image, errors=errors)
        else:
            appInitialize.logger.debug('Hostname: %s Ip: %s', host_name, host_ip)
            return render_template('index.html', hostname=host_name, ip=host_ip, db=db.client.is_primary)
    except Exception as err:
        appInitialize.logger.error("Index Init %s", err)
        return render_template('error.html', userFriendlyErrorMessage="Can not print the IP address of the container")


dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})



if __name__ == "__main__":
    appInitialize.run(host='0.0.0.0', port=8080, debug=True)
    appInitialize.config['DEBUG'] = True
    appInitialize.config['MONGO_URI'] = config['PROD']['DB_URI']

