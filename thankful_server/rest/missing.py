from sys import version_info

from flask import request
from flask_restplus import Namespace, Resource, fields

# Backport
if (3, 5) <= version_info < (3, 7):
    from dataclasses import dataclass
elif version_info < (3, 6):
    raise Exception("Incompatible Python version")

api = Namespace('missing', description='For telling us about creators without' + 
    'addresses')

missingModel = api.model('Missing', {
    #'creator_url': fields.Url(required=True, description='The creator url,' +
    #    ' at least for this website'),
    'missing_info': fields.Raw(required=True, description='JSON')
    #'donation_amount': fields.Float(required=False, description='The amount' +
    #    ' that the user wanted to donate'),
})


@api.route('/')
class MissingResource(Resource):
    '''beep boop documentation'''

    @api.doc('thank_creator')
    @api.param('missing_info', help="The json")
    def post(self):
        info = request.args["missing_info"]
        # TODO: Do fancier logging here
        print(info)
        return 'thx'