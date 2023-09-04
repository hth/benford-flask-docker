import socket

from logging.config import dictConfig
from flask import Flask, render_template, request
from benford.api.benfordLaw import benfordLaw_page

# Get the database using the method we defined in databaseInit file
from benford.model.databaseInit import get_database

appInitialize = Flask(__name__)
appInitialize.register_blueprint(benfordLaw_page)


@appInitialize.route('/')
@appInitialize.route('/index')
def index():
    try:
        appInitialize.logger.info("Successfully Displayed Index")
        host_name = socket.gethostname()
        host_ip = socket.gethostbyname(host_name)

        if 'name' in request.args:
            name = request.args.get('name')
            array = request.args.getlist('array')
            image = request.args.get('image')
            errors = request.args.get('errors')
            appInitialize.logger.debug('Hostname: %s Ip: %s Filename: %s', host_name, host_ip, name)
            return render_template('index.html', hostname=host_name, ip=host_ip, db=get_database().client.is_primary, name=name, array=array, image=image, errors=errors)
        else:
            appInitialize.logger.debug('Hostname: %s Ip: %s', host_name, host_ip)
            return render_template('index.html', hostname=host_name, ip=host_ip, db=get_database().client.is_primary)
    except Exception as err:
        appInitialize.logger.error("Index Init %s", err)
        return render_template('error.html', userFriendlyErrorMessage="Cannot print the IP address of the container")


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

