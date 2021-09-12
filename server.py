from flask import Flask, jsonify
from flasgger import Swagger
# from flask_restplus import Api, Resource
# from app.blueprints.user.controllers import blueprint_user
# from app.blueprints.converter.converter import blueprint_converter
from app.blueprints.gateway.gateway import blueprint_gateway
import os

app = Flask(__name__)


# app.register_blueprint(blueprint_user)
# app.register_blueprint(blueprint_converter)
app.register_blueprint(blueprint_gateway)

swagger = Swagger(app)


def create_app():
    app = Flask(__name__)
    # app.register_blueprint(blueprint_user)
    # app.register_blueprint(blueprint_converter)
    app.register_blueprint(blueprint_gateway)
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