import pytest


@pytest.fixture(scope='session')
def app(request):
    from app.create_app import create_app
    app = create_app(__name__)

    context = app.app_context()
    context.push()

    @request.addfinalizer
    def pop():
        context.pop()

    return app


@pytest.fixture(scope='session')
def _db(request, app):
    from app.db import db

    db.app = app
    db.create_all()

    @request.addfinalizer
    def pop():
        db.drop_all()

    return db
