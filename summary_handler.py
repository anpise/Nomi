"""
Summary & Analytics Handler - Specialized for generating insights and summaries
"""
from claude_handler import get_claude_response
from db import get_unified_entries
from datetime import date, timedelta

def handle_summary_analytics(message, username, conversation_history=None):
    """Handle summary and analytics requests"""

    # Determine what kind of summary is requested
    summary_type = determine_summary_type(message)

    # Generate the summary
    if summary_type == "daily":
        response, metadata = generate_daily_summary(username)
    elif summary_type == "weekly":
        response, metadata = generate_weekly_summary(username)
    elif summary_type == "insights":
        response, metadata = generate_insights(username)
    else:
        response, metadata = generate_daily_summary(username)

    return response, metadata, "summary_analytics"

def determine_summary_type(message):
    """Determine what type of summary is requested"""
    message_lower = message.lower()

    if any(word in message_lower for word in ["week", "weekly", "past week", "last week"]):
        return "weekly"
    elif any(word in message_lower for word in ["insight", "pattern", "trend", "progress", "analysis"]):
        return "insights"
    else:
        return "daily"

def generate_daily_summary(username):
    """Generate daily summary from all entries"""
    today = date.today()
    entries = get_unified_entries(username, start_date=today)

    if not entries:
        response = "You haven't logged anything yet today. Start by logging a workout or jotting down a note!"
        metadata = {"count": 0, "period": "today"}
        return response, metadata

    # Categorize entries
    health_entries = [e for e in entries if e.get("use_case") == "health_fitness"]
    note_entries = [e for e in entries if e.get("use_case") == "notes_reminders"]

    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 2-3 short sentences.

Rules:
- Direct address: "You crushed today!" not "{username} crushed today"
- Celebrate briefly, no elaboration
- Mention key activities in ONE sentence
- End with ✓
- NO lengthy praise, NO extra encouragement"""

    health_text = "\n".join([f"- {e['metadata'].get('activity', 'workout')} ({e['metadata'].get('duration', '')})"
                              for e in health_entries]) if health_entries else "No workouts today"
    notes_text = "\n".join([f"- {e['metadata'].get('summary', e.get('message', ''))}"
                             for e in note_entries]) if note_entries else "No notes today"

    prompt = f"""Review {username}'s day:

WORKOUTS: {health_text}
NOTES: {notes_text}

Respond in max 2-3 short sentences."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "count": len(entries),
        "health_count": len(health_entries),
        "notes_count": len(note_entries),
        "period": "today"
    }

    return response.strip(), metadata

def generate_weekly_summary(username):
    """Generate weekly summary"""
    today = date.today()
    week_ago = today - timedelta(days=7)
    entries = get_unified_entries(username, start_date=week_ago, end_date=today)

    if not entries:
        response = "You haven't logged anything this week yet."
        metadata = {"count": 0, "period": "week"}
        return response, metadata

    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 3-4 short sentences.

Rules:
- Direct address: "You stayed consistent!"
- Mention workout count and key pattern in ONE sentence
- Brief celebration only
- End with ✓
- NO lengthy feedback, NO extra encouragement"""

    health_entries = [e for e in entries if e.get("use_case") == "health_fitness"]
    note_entries = [e for e in entries if e.get("use_case") == "notes_reminders"]

    prompt = f"""Review {username}'s week:
- {len(health_entries)} workouts
- {len(note_entries)} notes/tasks

Respond in max 3-4 short sentences."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "count": len(entries),
        "health_count": len(health_entries),
        "notes_count": len(note_entries),
        "period": "week"
    }

    return response.strip(), metadata

def generate_insights(username):
    """Generate insights and patterns"""
    today = date.today()
    week_ago = today - timedelta(days=7)
    entries = get_unified_entries(username, start_date=week_ago, end_date=today)

    if not entries:
        response = "Not enough data yet to generate insights. Keep logging your activities!"
        metadata = {"count": 0, "period": "insights"}
        return response, metadata

    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 2-3 short sentences.

Rules:
- Direct address: "You're most active in mornings"
- Identify ONE key pattern
- ONE brief actionable tip
- End with ✓
- NO lengthy analysis, NO extra suggestions"""

    health_entries = [e for e in entries if e.get("use_case") == "health_fitness"]
    note_entries = [e for e in entries if e.get("use_case") == "notes_reminders"]

    prompt = f"""{username}'s past week:
- Total: {len(entries)}
- Workouts: {len(health_entries)}
- Notes: {len(note_entries)}

Share ONE key insight in max 2-3 short sentences."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "count": len(entries),
        "health_count": len(health_entries),
        "notes_count": len(note_entries),
        "period": "insights"
    }

    return response.strip(), metadata
