import pytest
from app import create_app
from app.models import User
from mongoengine import connect, disconnect

# in tests/test_auth.py

# ... (fixtures from above)

def test_register_success(client):
    """Tests successful user registration."""
    # Arrange: Define user data
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    # Act: Make a POST request to register
    response = client.post('/api/auth/register', json=user_data)
    
    # Assert: Check the results
    assert response.status_code == 201
    assert response.json['msg'] == "User created successfully."
    assert User.objects(email="test@example.com").count() == 1

def test_register_duplicate_email(client):
    """Tests registration with a duplicate email."""
    # Arrange: Create an initial user
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    client.post('/api/auth/register', json=user_data)

    # Act: Try to register with the same email
    response = client.post('/api/auth/register', json=user_data)

    # Assert: Check for a 409 Conflict error
    assert response.status_code == 409
    assert response.json['error'] == "Email already exists"

def test_login_success(client):
    """Tests successful user login."""
    # Arrange: Create a user to log in with
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    client.post('/api/auth/register', json=user_data)

    # Act: Make a POST request to log in
    response = client.post('/api/auth/login', json=user_data)

    # Assert: Check for a 200 OK status and the presence of tokens
    assert response.status_code == 200
    assert 'access_token' in response.json
    assert 'refresh_token' in response.json

def test_login_wrong_password(client):
    """Tests login with an incorrect password."""
    # Arrange: Create a user
    user_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    client.post('/api/auth/register', json=user_data)

    # Act: Try to log in with the wrong password
    login_data = {
        "email": "test@example.com",
        "password": "wrongpassword"
    }
    response = client.post('/api/auth/login', json=login_data)

    # Assert: Check for a 401 Unauthorized error
    assert response.status_code == 401
    assert response.json['error'] == "Invalid email or password"