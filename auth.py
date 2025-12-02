import hashlib
import os

def hash_password(password):
    """Hash a password for storing."""
    salt = os.environ.get('AUTH_SALT', 'default-salt')
    return hashlib.sha256((password + salt).encode()).hexdigest()

def check_auth(username, password):
    """Check if a username/password combination is valid."""
    # Get credentials from environment variables
    valid_username = os.environ.get('GAME_BACKLOG_USER', 'admin')
    valid_password_hash = os.environ.get('GAME_BACKLOG_PASS_HASH', 
                                        hash_password('password'))
    
    # Check if provided credentials match
    if username == valid_username and hash_password(password) == valid_password_hash:
        return True
    return False
