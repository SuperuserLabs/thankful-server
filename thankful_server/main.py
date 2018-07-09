from sys import version_info

from flask import Flask
from flask_restplus import Api

from . import __version__
from .rest import creators, thanks

app = Flask(__name__)
api = Api(app, version=__version__, title='Thankful Server API',
          description='An API for getting information about creators')
# TODO: Do some fancy stuff with blueprints to handle versions

api.add_namespace(creators.api)
api.add_namespace(thanks.api)


def main() -> None:
    app.run(debug=True)


if __name__ == '__main__':
    main()
