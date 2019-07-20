from typing import Iterator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from flask import Flask
from flask.testing import FlaskClient

from app.forms import SubscriptionForm
from core import create_app, db


@pytest.fixture(scope='session')
def monkey_session():
    """Monkey patch for a whole session."""

    monkey_patch = MonkeyPatch()
    yield monkey_patch
    monkey_patch.undo()


@pytest.fixture(scope='session')
def app(monkey_session) -> Flask:
    """A testing instance of the Flask application."""

    monkey_session.setenv('APP_ENV', 'testing')
    app = create_app()

    # Creates in memory tables..
    with app.app_context():
        db.create_all()

    yield app

    # Drops from memory tables.
    with app.app_context():
        db.drop_all()


@pytest.fixture(scope='session')
def client(app: Iterator[Flask]) -> FlaskClient:
    """An instance of flask test client."""

    return app.test_client()


@pytest.fixture
def order_data():
    """A stub of the order data that used by utils."""

    return {
        'name': 'Tester',
        'city': 'Kyiv',
        'department': '1',
        'payment_option': SubscriptionForm.CREDIT_CARD,
        'email': 'tester@test.com',
        'phone': '+380123456789',
        'subscription_type': SubscriptionForm.SENIOR,
        'stones': True,
        'matches': True,
        'guillotine': True,
        'cigar': True,
        'preferences': '',
        'csrf_token': 'a1b1dd40899d053ea3f97849b3b8257ce89afe54'
    }
