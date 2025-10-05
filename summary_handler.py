"""
Summary & Analytics Handler - Specialized for generating insights and summaries
"""
from claude_handler import get_claude_response
from db import get_unified_entries
from datetime import date, timedelta

def handle_summary_analytics(message, username):
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

    system_prompt = f"""You are Nomi, a supportive personal assistant for {username}.

Generate a warm 2-4 sentence daily summary that:
- Celebrates their accomplishments today
- Mentions key activities (workouts and notes)
- Sounds encouraging and personal
- Uses a friendly, supportive tone"""

    health_text = "\n".join([f"- {e['metadata'].get('activity', 'workout')} ({e['metadata'].get('duration', '')})"
                              for e in health_entries]) if health_entries else "No workouts today"
    notes_text = "\n".join([f"- {e['metadata'].get('summary', e.get('message', ''))}"
                             for e in note_entries]) if note_entries else "No notes today"

    prompt = f"""Here's what {username} did today:

WORKOUTS & HEALTH:
{health_text}

NOTES & TASKS:
{notes_text}

Generate a 2-4 sentence daily summary."""

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

    system_prompt = f"""You are Nomi, a supportive personal assistant for {username}.

Generate a brief 3-5 sentence weekly summary that:
- Highlights key accomplishments this week
- Mentions workout frequency and note patterns
- Provides encouraging feedback
- Sounds warm and supportive"""

    health_entries = [e for e in entries if e.get("use_case") == "health_fitness"]
    note_entries = [e for e in entries if e.get("use_case") == "notes_reminders"]

    prompt = f"""This week {username} logged:
- {len(health_entries)} workouts/health activities
- {len(note_entries)} notes/tasks

Generate a weekly summary celebrating their week."""

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

    system_prompt = f"""You are Nomi, an analytical assistant for {username}.

Generate 2-3 sentence insights about their habits and patterns that:
- Identifies positive trends
- Provides actionable suggestions
- Sounds encouraging and data-informed"""

    health_entries = [e for e in entries if e.get("use_case") == "health_fitness"]
    note_entries = [e for e in entries if e.get("use_case") == "notes_reminders"]

    prompt = f"""Analyze {username}'s activity over the past week:
- Total entries: {len(entries)}
- Workout frequency: {len(health_entries)} sessions
- Notes logged: {len(note_entries)}

Generate insights about patterns and suggestions."""

    response = get_claude_response(prompt, system_prompt)

    metadata = {
        "count": len(entries),
        "health_count": len(health_entries),
        "notes_count": len(note_entries),
        "period": "insights"
    }

    return response.strip(), metadata
