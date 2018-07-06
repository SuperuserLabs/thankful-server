from thankful_server import api

from flask_restplus import Resource

ns = api.namespace('thanks', description='Creator operations')

@ns.route('/<int:cid>/<int:thx>')
@ns.response(404, 'Creator not found')
@ns.param('cid', 'The creator identifier')
class CreatorResource(Resource):
    '''Show a single creator and lets you delete them'''

    @ns.doc('thank_creator')
    def post(self, cid, thx):
        return 'cid: {}, thx: {}'.format(cid, thx)