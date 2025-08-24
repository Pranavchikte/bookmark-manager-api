import pytest
from app import create_app
from app.models import User, Item # <-- Import the Item model
from mongoengine import connect, disconnect

@pytest.fixture(scope='module')
def app():
    """Create and configure a new app instance for each test module."""
    app = create_app({
        'TESTING': True,
        'MONGO_URI': 'mongodb://localhost:27017/bookmark_manager_test'
    })
    yield app
    disconnect(alias='default')

@pytest.fixture()
def client(app):
    """A test client for the app that cleans the database before each test."""
    # Clean up collections before each test
    User.objects().delete()
    Item.objects().delete() # <-- ADD THIS LINE
    return app.test_client()