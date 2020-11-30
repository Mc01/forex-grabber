from flask import Flask

from flask_migrate import Migrate
from flask_restful import Api

from app.config import get_config
from app.db import db, ma
from app.errors import errors
from app.resources import GrabAndSave, Last


def create_app(name) -> Flask:
    app = Flask(name)
    app.config.from_object(get_config())

    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    api = Api(app, errors=errors)

    api.add_resource(GrabAndSave, "/grab_and_save")
    api.add_resource(Last, "/last")

    @app.cli.command("create-db")
    def create_db():
        db.create_all()

    return app
