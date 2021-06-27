from flask import Flask, jsonify
from flasgger import Swagger
# from flask_restplus import Api, Resource
from app.blueprints.user.controllers import blueprint_user
from app.blueprints.converter.converter import blueprint_converter
import os

app = Flask(__name__)



app.register_blueprint(blueprint_user)
app.register_blueprint(blueprint_converter)
swagger = Swagger(app)

# restplus_app = Api(app=app)

# name_space = restplus_app.namespace('main', description='Main APIs')

def create_app():
    app = Flask(__name__)

    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    # app.config['CELERY_BROKER_URL'] = 'pyamqp://guest@localhost//'
    # app.config['CELERY_RESULT_BACKEND']= 'redis://localhost:6379'

    mail = Mail(app)

    app.register_blueprint(blueprint_user)
    app.register_blueprint(blueprint_converter)
    swagger = Swagger(app)
    return app

@app.cli.command()
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

if __name__ == "__main__":
    app.run()