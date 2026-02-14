"""Unit tests for the User API."""

import pytest
from app.api import app
from app.models import User, UserStore


@pytest.fixture
def client():
    """Create a test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def reset_user_store():
    """Reset the user store before each test."""
    from app.api import user_store

    user_store.users.clear()
    user_store.next_id = 1
    yield
    user_store.users.clear()
    user_store.next_id = 1


class TestUserModel:
    """Test the User model."""

    def test_user_creation(self):
        """Test creating a user."""
        user = User(1, "John Doe", "john@example.com")
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_user_to_dict(self):
        """Test converting user to dictionary."""
        user = User(1, "John Doe", "john@example.com")
        user_dict = user.to_dict()
        assert user_dict == {"id": 1, "name": "John Doe", "email": "john@example.com"}


class TestUserStore:
    """Test the UserStore class."""

    def test_create_user(self):
        """Test creating a user in the store."""
        store = UserStore()
        user = store.create_user("John Doe", "john@example.com")
        assert user.id == 1
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    def test_get_user(self):
        """Test retrieving a user from the store."""
        store = UserStore()
        created_user = store.create_user("John Doe", "john@example.com")
        retrieved_user = store.get_user(1)
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == created_user.name

    def test_get_user_not_found(self):
        """Test retrieving a non-existent user."""
        store = UserStore()
        user = store.get_user(999)
        assert user is None

    def test_get_all_users(self):
        """Test retrieving all users."""
        store = UserStore()
        store.create_user("John Doe", "john@example.com")
        store.create_user("Jane Doe", "jane@example.com")
        users = store.get_all_users()
        assert len(users) == 2

    def test_delete_user(self):
        """Test deleting a user."""
        store = UserStore()
        store.create_user("John Doe", "john@example.com")
        assert store.delete_user(1) is True
        assert store.get_user(1) is None

    def test_delete_user_not_found(self):
        """Test deleting a non-existent user."""
        store = UserStore()
        assert store.delete_user(999) is False

    def test_auto_incrementing_ids(self):
        """Test that user IDs auto-increment."""
        store = UserStore()
        user1 = store.create_user("User 1", "user1@example.com")
        user2 = store.create_user("User 2", "user2@example.com")
        user3 = store.create_user("User 3", "user3@example.com")
        assert user1.id == 1
        assert user2.id == 2
        assert user3.id == 3


class TestUserAPI:
    """Test the User API endpoints."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/api/health")
        assert response.status_code == 200
        assert response.json == {"status": "healthy"}

    def test_get_users_empty(self, client, reset_user_store):
        """Test getting users when list is empty."""
        response = client.get("/api/users")
        assert response.status_code == 200
        assert response.json == []

    def test_create_user(self, client, reset_user_store):
        """Test creating a user via API."""
        data = {"name": "John Doe", "email": "john@example.com"}
        response = client.post("/api/users", json=data)
        assert response.status_code == 201
        assert response.json["name"] == "John Doe"
        assert response.json["email"] == "john@example.com"
        assert "id" in response.json

    def test_create_user_missing_fields(self, client, reset_user_store):
        """Test creating a user with missing fields."""
        data = {"name": "John Doe"}
        response = client.post("/api/users", json=data)
        assert response.status_code == 400
        assert "error" in response.json

    def test_create_user_empty_fields(self, client, reset_user_store):
        """Test creating a user with empty fields."""
        data = {"name": "", "email": "john@example.com"}
        response = client.post("/api/users", json=data)
        assert response.status_code == 400
        assert "error" in response.json

    def test_create_user_no_data(self, client, reset_user_store):
        """Test creating a user with no data."""
        response = client.post("/api/users", json={})
        assert response.status_code == 400
        assert "error" in response.json

    def test_get_all_users(self, client, reset_user_store):
        """Test getting all users."""
        # Create two users
        client.post("/api/users", json={"name": "John Doe", "email": "john@example.com"})
        client.post("/api/users", json={"name": "Jane Doe", "email": "jane@example.com"})

        response = client.get("/api/users")
        assert response.status_code == 200
        assert len(response.json) == 2
        assert response.json[0]["name"] == "John Doe"
        assert response.json[1]["name"] == "Jane Doe"

    def test_get_user_by_id(self, client, reset_user_store):
        """Test getting a specific user by ID."""
        # Create a user
        create_response = client.post(
            "/api/users", json={"name": "John Doe", "email": "john@example.com"}
        )
        user_id = create_response.json["id"]

        response = client.get(f"/api/users/{user_id}")
        assert response.status_code == 200
        assert response.json["id"] == user_id
        assert response.json["name"] == "John Doe"

    def test_get_user_not_found(self, client, reset_user_store):
        """Test getting a non-existent user."""
        response = client.get("/api/users/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_delete_user(self, client, reset_user_store):
        """Test deleting a user."""
        # Create a user
        create_response = client.post(
            "/api/users", json={"name": "John Doe", "email": "john@example.com"}
        )
        user_id = create_response.json["id"]

        response = client.delete(f"/api/users/{user_id}")
        assert response.status_code == 200
        assert "message" in response.json

        # Verify user is deleted
        get_response = client.get(f"/api/users/{user_id}")
        assert get_response.status_code == 404

    def test_delete_user_not_found(self, client, reset_user_store):
        """Test deleting a non-existent user."""
        response = client.delete("/api/users/999")
        assert response.status_code == 404
        assert "error" in response.json

    def test_404_endpoint_not_found(self, client):
        """Test accessing a non-existent endpoint."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
        assert "error" in response.json
