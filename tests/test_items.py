import pytest
from app.models import Item, User

# Note: The 'client' and 'app' fixtures are automatically provided by conftest.py

def test_create_item_success(client):
    """Tests successful creation of an item for an authenticated user."""
    # Arrange: First, register and log in a user to get a token
    client.post('/api/auth/register', json={"email": "test@user.com", "password": "password"})
    login_res = client.post('/api/auth/login', json={"email": "test@user.com", "password": "password"})
    token = login_res.json['access_token']

    item_data = {
        "title": "Test Bookmark",
        "item_type": "bookmark",
        "content": "https://test.com",
        "tags": ["testing"]
    }
    
    # Act: Make the request with the auth header
    response = client.post('/api/items/', 
                           json=item_data, 
                           headers={'Authorization': f'Bearer {token}'})
    
    # Assert
    assert response.status_code == 201
    assert response.json['title'] == "Test Bookmark"
    assert Item.objects.count() == 1

def test_create_item_no_auth(client):
    """Tests that creating an item fails without authentication."""
    # Arrange
    item_data = {"title": "Test Bookmark", "item_type": "bookmark", "content": "https://test.com"}
    
    # Act: Make the request without the auth header
    response = client.post('/api/items/', json=item_data)
    
    # Assert
    assert response.status_code == 401 # Unauthorized

def test_get_items_success(client):
    """Tests that a user can only retrieve their own items."""
    # Arrange: Create user 1 and their item
    client.post('/api/auth/register', json={"email": "user1@test.com", "password": "password"})
    login_res1 = client.post('/api/auth/login', json={"email": "user1@test.com", "password": "password"})
    token1 = login_res1.json['access_token']
    client.post('/api/items/', json={"title": "User 1 Item", "item_type": "note", "content": "note1"}, headers={'Authorization': f'Bearer {token1}'})

    # Arrange: Create user 2 and their item
    client.post('/api/auth/register', json={"email": "user2@test.com", "password": "password"})
    login_res2 = client.post('/api/auth/login', json={"email": "user2@test.com", "password": "password"})
    token2 = login_res2.json['access_token']
    client.post('/api/items/', json={"title": "User 2 Item", "item_type": "note", "content": "note2"}, headers={'Authorization': f'Bearer {token2}'})
    
    # Act: User 1 requests their items
    response = client.get('/api/items/', headers={'Authorization': f'Bearer {token1}'})
    
    # Assert
    assert response.status_code == 200
    assert len(response.json) == 1 # Should only get 1 item back
    assert response.json[0]['title'] == "User 1 Item"

def test_delete_item_security(client):
    """Tests that a user cannot delete another user's item."""
    # Arrange: Create two users and one item for user 1
    client.post('/api/auth/register', json={"email": "user1@test.com", "password": "password"})
    login_res1 = client.post('/api/auth/login', json={"email": "user1@test.com", "password": "password"})
    token1 = login_res1.json['access_token']
    create_res = client.post('/api/items/', json={"title": "User 1 Item", "item_type": "note", "content": "note1"}, headers={'Authorization': f'Bearer {token1}'})
    item_id = create_res.json['id']
    
    client.post('/api/auth/register', json={"email": "user2@test.com", "password": "password"})
    login_res2 = client.post('/api/auth/login', json={"email": "user2@test.com", "password": "password"})
    token2 = login_res2.json['access_token'] # This is the attacker's token
    
    # Act: User 2 (attacker) tries to delete User 1's item
    response = client.delete(f'/api/items/{item_id}', headers={'Authorization': f'Bearer {token2}'})
    
    # Assert
    assert response.status_code == 404 # The item is "not found" for user 2
    assert Item.objects.count() == 1 # The item should still exist