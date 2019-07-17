import pytest
from flask import Flask
from flask.testing import FlaskClient

from core import create_app


@pytest.fixture(scope='session')
def app() -> Flask:
    """A testing instance of the Flask application."""

    app = create_app()
    app.testing = True

    return app


@pytest.fixture(scope='session')
def client(app: Flask) -> FlaskClient:
    """An instance of flask test client."""

    return app.test_client()
