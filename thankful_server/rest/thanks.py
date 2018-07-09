from sys import version_info

from flask import request
from flask_restplus import Namespace, Resource, fields

# Backport
if (3, 5) <= version_info < (3, 7):
    from dataclasses import dataclass
elif version_info < (3, 6):
    raise Exception("Incompatible Python version")

api = Namespace('thanks', description='Creator operations')

thanksModel = api.model('Thanks', {
    'creator_id': fields.Integer(required=True, description='The creator unique identifier'),
    'user_id': fields.String(required=True, description='The user id'),
    'content_url': fields.String(required=True, description='Content thanked'),
})


@api.route('/<int:cid>')
@api.response(404, 'Creator not found')
@api.param('cid', 'The creator identifier')
class ThanksResource(Resource):
    '''Show a single creator and lets you delete them'''

    @api.doc('thank_creator')
    @api.param('content_url', help="URL to thank")
    def post(self, cid: int):
        content_url = request.args["content_url"]
        return 'cid: {}, url: {}'.format(cid, content_url)
