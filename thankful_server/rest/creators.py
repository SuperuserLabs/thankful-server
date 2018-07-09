from sys import version_info
from typing import Dict, Optional, List, Any

from flask import request
from flask_restplus import Namespace, Resource, fields

# Backport
if (3, 5) <= version_info < (3, 7):
    from dataclasses import dataclass
elif version_info < (3, 6):
    raise Exception("Incompatible Python version")

api = Namespace('creators', description='Creator operatioapi')

creatorModel = api.model('Creator', {
    'id': fields.Integer(readOnly=True, description='The creator unique identifier'),
    'name': fields.String(required=True, description='The creator name'),
    'urls': fields.List(fields.String, required=True, description='URLs to the creators profiles'),
})


@dataclass
class Creator:
    id: Optional[int] = None
    name: Optional[str] = None
    urls: Optional[List[str]] = None
    data: Optional[Dict[str, Any]] = None

    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "urls": self.urls,
            "data": self.data,
        }


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
        if creator.id:
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
    print(creators[0].dict())
    assert creators[0].name == "Test"


@api.route('/')
class CreatorListResource(Resource):
    '''Shows a list of all creators, and lets you POST to add new creators'''

    @api.doc('list_creators')
    @api.marshal_list_with(creatorModel)
    def get(self) -> List[Creator]:
        '''List all creators'''
        return creatorDAO.list()

    @api.doc('create_creator')
    @api.expect(creatorModel)
    @api.marshal_with(creatorModel, code=201)
    def post(self):
        '''Create a new creator'''
        c = Creator(**request.payload)
        return creatorDAO.create(c), 201


@api.route('/<int:cid>')
@api.response(404, 'Creator not found')
@api.param('id', 'The creator identifier')
class CreatorResource(Resource):
    '''Show a single creator and lets you delete them'''

    @api.doc('get_creator')
    @api.marshal_with(creatorModel)
    def get(self, cid):
        '''Fetch a given resource'''
        c = creatorDAO.get(cid)
        if c is not None:
            return c
        else:
            api.abort(404, "Creator {} doesn't exist".format(cid))

    @api.doc('delete_creator')
    @api.response(204, 'Creator deleted')
    def delete(self, cid):
        '''Delete a creator given its identifier'''
        creatorDAO.delete(cid)
        return '', 204

    @api.expect(creatorModel)
    @api.marshal_with(creatorModel)
    def put(self, cid):
        '''Update a creator given its identifier'''
        return creatorDAO.update(cid, request.payload)
