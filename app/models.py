"""User model for the API."""

class User:
    """User data model."""
    
    def __init__(self, id: int, name: str, email: str):
        """Initialize a User.
        
        Args:
            id: Unique identifier for the user
            name: User's full name
            email: User's email address
        """
        self.id = id
        self.name = name
        self.email = email
    
    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class UserStore:
    """In-memory store for users."""
    
    def __init__(self):
        """Initialize the user store."""
        self.users = {}
        self.next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        """Create a new user.
        
        Args:
            name: User's name
            email: User's email
            
        Returns:
            The created User object
        """
        user = User(self.next_id, name, email)
        self.users[self.next_id] = user
        self.next_id += 1
        return user
    
    def get_user(self, user_id: int):
        """Get a user by ID.
        
        Args:
            user_id: The user's ID
            
        Returns:
            User object or None if not found
        """
        return self.users.get(user_id)
    
    def get_all_users(self):
        """Get all users.
        
        Returns:
            List of all User objects
        """
        return list(self.users.values())
    
    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID.
        
        Args:
            user_id: The user's ID
            
        Returns:
            True if deleted, False if user not found
        """
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False
