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

    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 8-10 words.

Rules:
- Greet briefly: "Morning! Let's crush today!"
- If yesterday was active, ONE quick reference
- End with ✓ or 💪
- NO lengthy motivation, NO elaboration"""

    if yesterday_entries:
        health_count = len([e for e in yesterday_entries if e.get("use_case") == "health_fitness"])
        notes_count = len([e for e in yesterday_entries if e.get("use_case") == "notes_reminders"])

        prompt = f"""Morning greeting for {username}. Yesterday: {health_count} workouts, {notes_count} notes.

Respond in max 8-10 words."""
    else:
        prompt = f"""Morning greeting for {username}.

Respond in max 8-10 words."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "morning_motivation",
        "yesterday_activity": len(yesterday_entries) if yesterday_entries else 0
    }

    return response.strip(), metadata

def generate_encouragement(username, message):
    """Generate personalized encouragement"""
    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 8-10 words.

Rules:
- Brief encouragement: "You've got this!"
- Direct address only
- End with ✓ or 💪
- NO lengthy support, NO elaboration"""

    prompt = f"""{username} said: "{message}"

Respond in max 8-10 words."""

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

    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 2-3 short sentences.

Rules:
- Brief reflection: "You've been consistent this week"
- ONE key observation
- End with brief encouragement and ✓
- NO lengthy insights, NO elaboration"""

    if recent_entries:
        total = len(recent_entries)
        health_count = len([e for e in recent_entries if e.get("use_case") == "health_fitness"])
        notes_count = len([e for e in recent_entries if e.get("use_case") == "notes_reminders"])

        prompt = f"""Reflect on {username}'s week: {total} total, {health_count} workouts, {notes_count} notes.

Respond in max 2-3 short sentences."""
    else:
        prompt = f"""Reflect on {username} just beginning.

Respond in max 2-3 short sentences."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "reflection",
        "recent_activity": len(recent_entries) if recent_entries else 0
    }

    return response.strip(), metadata

def generate_general_support(username, message):
    """Generate general supportive response"""
    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 8-10 words.

Rules:
- Brief support: "I hear you, you're doing great"
- Direct address only
- End with ✓ or 💪
- NO lengthy responses, NO elaboration"""

    prompt = f"""{username} said: "{message}"

Respond in max 8-10 words."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "type": "general_support",
        "user_message": message
    }

    return response.strip(), metadata
