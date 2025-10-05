from pymongo import MongoClient
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
DB_NAME = "nomi_db"

def get_db():
    """Get MongoDB database instance"""
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def init_collections():
    """Initialize MongoDB collections with indexes"""
    db = get_db()

    # Create indexes for better performance
    db.users.create_index("username", unique=True)
    db.notes.create_index([("username", 1), ("timestamp", -1)])
    db.workouts.create_index([("username", 1), ("timestamp", -1)])
    db.messages.create_index([("username", 1), ("timestamp", -1)])

    # Unified entries collection (new orchestration system)
    db.entries.create_index([("username", 1), ("timestamp", -1)])
    db.entries.create_index([("username", 1), ("use_case", 1), ("timestamp", -1)])

# User operations
def create_user(username, password):
    """Create a new user"""
    db = get_db()
    try:
        db.users.insert_one({
            "username": username,
            "password": password,
            "created_at": datetime.now()
        })
        return True
    except:
        return False

def verify_user(username, password):
    """Verify user credentials"""
    db = get_db()
    user = db.users.find_one({"username": username, "password": password})
    return user is not None

# Note operations
def save_note(username, content, summary):
    """Save a note"""
    db = get_db()
    db.notes.insert_one({
        "username": username,
        "content": content,
        "summary": summary,
        "timestamp": datetime.now()
    })

def get_notes(username, date=None):
    """Get notes for a user, optionally filtered by date"""
    db = get_db()
    query = {"username": username}

    if date:
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        query["timestamp"] = {"$gte": start, "$lte": end}

    return list(db.notes.find(query).sort("timestamp", -1))

# Workout operations
def save_workout(username, activity, duration, details):
    """Save a workout"""
    db = get_db()
    db.workouts.insert_one({
        "username": username,
        "activity": activity,
        "duration": duration,
        "details": details,
        "timestamp": datetime.now()
    })

def get_workouts(username, date=None):
    """Get workouts for a user, optionally filtered by date"""
    db = get_db()
    query = {"username": username}

    if date:
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        query["timestamp"] = {"$gte": start, "$lte": end}

    return list(db.workouts.find(query).sort("timestamp", -1))

# Message history operations
def save_message(username, role, content):
    """Save a chat message"""
    db = get_db()
    db.messages.insert_one({
        "username": username,
        "role": role,
        "content": content,
        "timestamp": datetime.now()
    })

def get_messages(username, limit=50):
    """Get recent messages for a user"""
    db = get_db()
    return list(db.messages.find({"username": username})
                .sort("timestamp", -1)
                .limit(limit))[::-1]  # Reverse to show oldest first

def clear_messages(username):
    """Clear chat history for a user"""
    db = get_db()
    db.messages.delete_many({"username": username})

# Unified entries operations (Orchestration system)
def save_unified_entry(entry):
    """Save a unified entry to the database"""
    db = get_db()
    db.entries.insert_one(entry)

def get_unified_entries(username, start_date=None, end_date=None, use_case=None, limit=100):
    """Get unified entries with optional filters"""
    db = get_db()
    query = {"username": username}

    # Date filtering
    if start_date or end_date:
        date_query = {}
        if start_date:
            start_dt = datetime.combine(start_date, datetime.min.time())
            date_query["$gte"] = start_dt
        if end_date:
            end_dt = datetime.combine(end_date, datetime.max.time())
            date_query["$lte"] = end_dt
        query["timestamp"] = date_query

    # Use case filtering
    if use_case:
        query["use_case"] = use_case

    return list(db.entries.find(query).sort("timestamp", -1).limit(limit))

def get_entries_by_use_case(username, use_case, limit=50):
    """Get entries for a specific use case"""
    return get_unified_entries(username, use_case=use_case, limit=limit)

def get_all_entries(username, limit=100):
    """Get all entries for a user"""
    return get_unified_entries(username, limit=limit)
