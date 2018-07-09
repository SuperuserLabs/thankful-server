from typing import Dict, Optional, List, Any

from flask import Flask, request
from flask_restplus import Api, Resource, fields, reqparse

from . import __version__

app = Flask(__name__)
api = Api(app, version=__version__, title='Thankful Server API',
          description='An API for getting information about creators')
# TODO: Do some fancy stuff with blueprints to handle versions

ns = api.namespace('creators', description='Creator operations')

creatorModel = api.model('Creator', {
    'id': fields.Integer(readOnly=True, description='The creator unique identifier'),
    'name': fields.String(required=True, description='The creator name'),
    'youtube_id': fields.String(required=True, description='The creators YouTube ID'),
})


class Creator:
    def __init__(self, name, cid=None, youtube_id=None, data: Dict[str, Any] = None) -> None:
        self.id = cid
        self.name = name
        self.youtube_id = youtube_id
        self.data = data if data else dict()

    def __repr__(self):
        return f"<Creator name='{self.name}'>"


class CreatorDAO:
    def __init__(self):
        self.counter = 0
        self.creators: Dict[int, Creator] = {}

    def get(self, cid: int) -> Optional[Creator]:
        if cid in self.creators:
            return self.creators[cid]
        return None

    def list(self) -> List[Creator]:
        return list(self.creators.values())

    def create(self, creator: Creator):
        creator.id = self.counter = self.counter + 1
        self.creators[creator.id] = creator
        return creator

    def update(self, cid, creator):
        self.creators[cid] = creator
        return creator

    def delete(self, cid):
        self.creators.pop(cid)


creatorDAO = CreatorDAO()


def test_creator_create():
    dao = CreatorDAO()
    dao.create(Creator(name="Test"))

    creators = dao.list()
    assert creators
    print(dir(creators[0]))
    assert creators[0].name == "Test"


@ns.route('/')
class CreatorListResource(Resource):
    '''Shows a list of all creators, and lets you POST to add new creators'''

    @ns.doc('list_creators')
    @ns.marshal_list_with(creatorModel)
    def get(self) -> List[Creator]:
        '''List all creators'''
        return creatorDAO.list()

    @ns.doc('create_creator')
    @ns.expect(creatorModel)
    @ns.marshal_with(creatorModel, code=201)
    def post(self):
        '''Create a new creator'''
        c = Creator(**api.payload)
        return creatorDAO.create(c), 201


@ns.route('/<int:cid>')
@ns.response(404, 'Creator not found')
@ns.param('id', 'The creator identifier')
class CreatorResource(Resource):
    '''Show a single creator and lets you delete them'''

    @ns.doc('get_creator')
    @ns.marshal_with(creatorModel)
    def get(self, cid):
        '''Fetch a given resource'''
        c = creatorDAO.get(cid)
        if c is not None:
            return c
        else:
            api.abort(404, "Creator {} doesn't exist".format(cid))

    @ns.doc('delete_creator')
    @ns.response(204, 'Creator deleted')
    def delete(self, cid):
        '''Delete a creator given its identifier'''
        creatorDAO.delete(cid)
        return '', 204

    @ns.expect(creatorModel)
    @ns.marshal_with(creatorModel)
    def put(self, cid):
        '''Update a creator given its identifier'''
        return creatorDAO.update(cid, api.payload)

nst = api.namespace('thanks', description='Creator operations')

thanksModel = api.model('Thanks', {
    'creator_id': fields.Integer(required=True, description='The creator unique identifier'),
    'user_id': fields.String(required=True, description='The user id'),
    'content_url': fields.String(required=True, description='Content thanked'),
})

@nst.route('/<int:cid>')
@nst.response(404, 'Creator not found')
@nst.param('cid', 'The creator identifier')
class ThanksResource(Resource):
    '''Show a single creator and lets you delete them'''

    @ns.doc('thank_creator')
    @ns.param('content_url', help="URL to thank")
    def post(self, cid):
        content_url = request.args["content_url"]
        return 'cid: {}, url: {}'.format(cid, content_url)

def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
