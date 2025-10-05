"""
Wellbeing & Motivation Handler - Specialized for mental wellness and motivation
"""
from claude_handler import get_claude_response
from db import get_unified_entries
from datetime import date, timedelta

def handle_motivation_wellbeing(message, username):
    """Handle motivation and wellbeing messages"""

    # Determine what kind of wellbeing support is needed
    support_type = determine_support_type(message)

    # Generate appropriate response
    if support_type == "morning":
        response, metadata = generate_morning_motivation(username)
    elif support_type == "encouragement":
        response, metadata = generate_encouragement(username, message)
    elif support_type == "reflection":
        response, metadata = generate_reflection(username)
    else:
        response, metadata = generate_general_support(username, message)

    return response, metadata, "motivation_wellbeing"

def determine_support_type(message):
    """Determine what type of wellbeing support is needed"""
    message_lower = message.lower()

    if any(word in message_lower for word in ["morning", "good morning", "start day"]):
        return "morning"
    elif any(word in message_lower for word in ["motivate", "inspire", "encourage"]):
        return "encouragement"
    elif any(word in message_lower for word in ["reflect", "feeling", "mood", "how am i"]):
        return "reflection"
    else:
        return "general"

def generate_morning_motivation(username):
    """Generate morning motivation based on yesterday's activities"""
    yesterday = date.today() - timedelta(days=1)
    yesterday_entries = get_unified_entries(username, start_date=yesterday, end_date=yesterday)

    system_prompt = f"""You are Nomi, a motivational coach for {username}.

Generate a warm 1-2 sentence morning message that:
- Greets them energetically
- References yesterday's accomplishments if any
- Sets a positive tone for today
- Sounds encouraging and uplifting"""

    if yesterday_entries:
        health_count = len([e for e in yesterday_entries if e.get("use_case") == "health_fitness"])
        notes_count = len([e for e in yesterday_entries if e.get("use_case") == "notes_reminders"])

        prompt = f"""Good morning {username}!
Yesterday they logged:
- {health_count} workouts
- {notes_count} notes/tasks

Generate morning motivation referencing their progress."""
    else:
        prompt = f"Good morning {username}! Generate a fresh, energizing morning message."

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "morning_motivation",
        "yesterday_activity": len(yesterday_entries) if yesterday_entries else 0
    }

    return response.strip(), metadata

def generate_encouragement(username, message):
    """Generate personalized encouragement"""
    system_prompt = f"""You are Nomi, a supportive friend for {username}.

Generate a warm, encouraging 1-2 sentence response that:
- Acknowledges their request for motivation
- Provides genuine, heartfelt encouragement
- Relates to their personal journey
- Sounds authentic and caring"""

    prompt = f"""{username} is asking for encouragement.
Their message: {message}

Generate a supportive, motivating response."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "encouragement",
        "user_message": message
    }

    return response.strip(), metadata

def generate_reflection(username):
    """Generate reflective insights about their journey"""
    week_ago = date.today() - timedelta(days=7)
    recent_entries = get_unified_entries(username, start_date=week_ago)

    system_prompt = f"""You are Nomi, a reflective companion for {username}.

Generate a thoughtful 2-3 sentence reflection that:
- Acknowledges their recent journey
- Highlights positive patterns
- Offers gentle encouragement
- Sounds warm and insightful"""

    if recent_entries:
        total = len(recent_entries)
        health_count = len([e for e in recent_entries if e.get("use_case") == "health_fitness"])
        notes_count = len([e for e in recent_entries if e.get("use_case") == "notes_reminders"])

        prompt = f"""Reflect on {username}'s recent activity:
- Total activities: {total}
- Workouts: {health_count}
- Notes/tasks: {notes_count}

Generate a reflective, encouraging response."""
    else:
        prompt = f"Generate a gentle, encouraging reflection for {username} who is just starting their journey."

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "reflection",
        "recent_activity": len(recent_entries) if recent_entries else 0
    }

    return response.strip(), metadata

def generate_general_support(username, message):
    """Generate general supportive response"""
    system_prompt = f"""You are Nomi, a caring assistant for {username}.

Generate a warm, supportive 1-2 sentence response that:
- Addresses their emotional need
- Sounds genuine and caring
- Provides appropriate support
- Feels personal and thoughtful"""

    prompt = f"""{username} shared: {message}

Generate an appropriate supportive response."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "general_support",
        "user_message": message
    }

    return response.strip(), metadata
