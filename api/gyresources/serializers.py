from flask_restplus import fields
from api.restplus import api

"""
Here we have something like parsers, the difference here, we're building
default json models, which can be used in swagger as example.
"""

images = api.model('Image', {
    'id': fields.Integer(readOnly=True, description='Disease identification'),
    'idDisease': fields.String(readOnly=True,
                               required=True,
                               attribute='disease.id',
                               description='Disease ID'),
    'url': fields.String(description='URL image or base64 image'),
    'description': fields.String(description='Description'),
    'source': fields.String(description='Metadata info'),
    'size': fields.Integer(description='Size type'),
})

disease = api.model('Disease', {
    'id': fields.Integer(readOnly=True, description='Disease identification'),
    'idPlant': fields.Integer(required=True,
                              attribute='plant.id',
                              description='Plant ID'),
    'plant': fields.String(attribute='plant.id'),
    'scientificName': fields.String(required=True,
                                    description='Scientific name'),
    'commonName': fields.String(required=True,
                                description='Common name'),
    'images': fields.List(fields.Nested(images)),
})

plant = api.model('Plant', {
    'id': fields.Integer(readOnly=True, description='Plant identification'),
    'scientificName': fields.String(required=True,
                                    description='Scientific name'),
    'commonName': fields.String(required=True,
                                description='Common name'),
    'diseases': fields.List(fields.Nested(disease))
})