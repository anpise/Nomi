"""
Notes & Reminders Handler - Specialized for note-taking and task management
"""
from claude_handler import get_claude_response
import json

def handle_notes_reminders(message, username):
    """Handle notes and reminders"""

    # Extract note/reminder data
    note_data = extract_note_data(message)

    # Generate response
    response = generate_note_response(username, note_data)

    # Prepare metadata
    metadata = {
        "summary": note_data.get("summary", ""),
        "category": note_data.get("category", ""),
        "priority": note_data.get("priority", ""),
        "has_reminder": note_data.get("has_reminder", False),
        "reminder_time": note_data.get("reminder_time", ""),
        "tags": note_data.get("tags", [])
    }

    return response, metadata, "notes_reminders"

def extract_note_data(message):
    """Extract structured note data from message"""
    system_prompt = """You are a note-taking assistant. Extract information from the message.

Return a JSON object with these fields:
- summary: A concise 5-8 word summary of the note
- category: Type of note (meeting, task, idea, event, personal, work)
- priority: Low, medium, or high (if implied)
- has_reminder: true if user wants to be reminded, false otherwise
- reminder_time: When to remind (if mentioned)
- tags: Array of relevant keywords/tags

Examples:
Input: "Had a great meeting with the design team about the new features"
Output: {"summary": "Productive design team meeting on features", "category": "meeting", "priority": "medium", "has_reminder": false, "reminder_time": "", "tags": ["design", "meeting", "features"]}

Input: "Remind me to call Sarah tomorrow about the Q1 report"
Output: {"summary": "Call Sarah about Q1 report", "category": "task", "priority": "high", "has_reminder": true, "reminder_time": "tomorrow", "tags": ["call", "Sarah", "Q1", "report"]}

Input: "Finished the project documentation"
Output: {"summary": "Completed project documentation", "category": "work", "priority": "medium", "has_reminder": false, "reminder_time": "", "tags": ["project", "documentation", "completed"]}

Respond with ONLY valid JSON, no extra text."""

    response = get_claude_response(message, system_prompt)

    try:
        data = json.loads(response)
        return data
    except:
        return {
            "summary": message[:50],
            "category": "note",
            "priority": "medium",
            "has_reminder": False,
            "reminder_time": "",
            "tags": []
        }

def generate_note_response(username, note_data):
    """Generate appropriate response for note"""
    system_prompt = f"""You are Nomi, a helpful assistant for {username}.

Generate a short 1 sentence confirmation that:
- Acknowledges the note/reminder
- Mentions the summary
- Sounds friendly and efficient
- Ends with a checkmark emoji ✓

Keep it concise."""

    summary = note_data.get("summary", "note")
    has_reminder = note_data.get("has_reminder", False)
    reminder_time = note_data.get("reminder_time", "")

    if has_reminder:
        prompt = f"""User saved a note with reminder: {summary}
Reminder time: {reminder_time}

Generate a confirmation that acknowledges both the note and reminder."""
    else:
        prompt = f"""User saved a note: {summary}

Generate a brief confirmation."""

    response = get_claude_response(prompt, system_prompt)
    return response.strip()
