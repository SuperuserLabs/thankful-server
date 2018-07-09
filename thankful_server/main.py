from sys import version_info
from typing import Dict, Optional, List, Any

from flask import Flask, request
from flask_restplus import Api, Resource, fields, reqparse

from . import __version__
from .rest import creators, thanks

# Backport
if (3, 5) <= version_info < (3, 7):
    from dataclasses import dataclass
elif version_info < (3, 6):
    raise Exception("Incompatible Python version")

app = Flask(__name__)
api = Api(app, version=__version__, title='Thankful Server API',
          description='An API for getting information about creators')
# TODO: Do some fancy stuff with blueprints to handle versions

api.add_namespace(creators.api)
api.add_namespace(thanks.api)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
