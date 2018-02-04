from flask import Flask, Blueprint
from api.gyresources.endpoints.PlantController import ns as plant_namespace
from api.gyresources.endpoints.TextController import ns as text_namespace
from api.gyresources.endpoints.TypeController import ns as type_namespace
from api.gyresources.endpoints.ImageController import ns as image_namespace
from api.restplus import api


# import settings
app = Flask(__name__)

def initialize_app(flask_app):
    flask_app.config.from_object('config.DefaultConfig')
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(plant_namespace)
    api.add_namespace(text_namespace)
    api.add_namespace(type_namespace)
    api.add_namespace(image_namespace)
    flask_app.register_blueprint(blueprint)
    return flask_app


def main():
    initialize_app(app)
    app.run(debug=True)


if __name__ == '__main__':
    main()
