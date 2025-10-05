from db import create_user as db_create_user, verify_user, init_collections

def init_users_file():
    """Initialize MongoDB collections"""
    init_collections()

def verify_login(username, password):
    """Verify username and password"""
    return verify_user(username, password)

def create_user(username, password):
    """Create a new user"""
    return db_create_user(username, password)
