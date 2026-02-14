"""Flask API for managing users."""

from flask import Flask, request, jsonify
from .models import UserStore

app = Flask(__name__)
user_store = UserStore()


@app.route('/api/users', methods=['GET'])
def get_users():
    """Get all users.
    
    Returns:
        JSON list of all users
    """
    users = user_store.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID.
    
    Args:
        user_id: The user's ID
        
    Returns:
        JSON object for the user or 404 if not found
    """
    user = user_store.get_user(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(user.to_dict()), 200


@app.route('/api/users', methods=['POST'])
def create_user():
    """Create a new user.
    
    Request JSON format:
        {
            "name": "John Doe",
            "email": "john@example.com"
        }
    
    Returns:
        JSON object of created user with 201 status
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    if 'name' not in data or 'email' not in data:
        return jsonify({'error': 'Missing required fields: name, email'}), 400
    
    if not data['name'] or not data['email']:
        return jsonify({'error': 'Name and email cannot be empty'}), 400
    
    user = user_store.create_user(data['name'], data['email'])
    return jsonify(user.to_dict()), 201


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user by ID.
    
    Args:
        user_id: The user's ID
        
    Returns:
        Success message or 404 if user not found
    """
    if user_store.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint.
    
    Returns:
        Health status JSON
    """
    return jsonify({'status': 'healthy'}), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500
