import os
from anthropic import Anthropic
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def get_claude_response(prompt, system_prompt=None, model="claude-3-5-haiku-20241022"):
    """Get response from Claude API"""
    # Add current date context to system prompt
    current_date = datetime.now().strftime("%A, %B %d, %Y")
    date_context = f"\n\nCurrent date and time context: Today is {current_date}."

    if system_prompt:
        system_prompt = system_prompt + date_context
    else:
        system_prompt = date_context

    messages = [{"role": "user", "content": prompt}]

    kwargs = {
        "model": model,
        "max_tokens": 1024,
        "messages": messages,
        "system": system_prompt
    }

    response = client.messages.create(**kwargs)
    return response.content[0].text

def classify_intent(message):
    """Classify user intent using Claude"""
    system_prompt = """You are an intent classifier for Nomi, a personal assistant.

Classify the user's message into ONE of these intents:
- workout: User is logging exercise/physical activity
- note: User is recording a thought, task, or event
- summary: User wants a summary of their day
- morning: User wants morning motivation

Keywords:
- workout: "did", "ran", "lifted", "exercised", "workout", "gym", "pushups", "yoga", "miles", "km"
- note: "note:", "finished", "completed", "meeting", "called", "remember", "todo"
- summary: "summary", "what did i do", "recap", "today", "/summary", "/eod"
- morning: "/morning", "motivate", "motivation", "inspire"

Respond with ONLY ONE WORD: workout, note, summary, or morning.
If unclear, default to "note"."""

    response = get_claude_response(message, system_prompt)
    intent = response.strip().lower()

    # Validate intent
    valid_intents = ["workout", "note", "summary", "morning"]
    if intent not in valid_intents:
        return "note"  # Default fallback

    return intent

def parse_workout(message):
    """Parse workout details from message using Claude"""
    system_prompt = """Extract workout information from the user's message.

Return a JSON object with these fields:
- activity: The type of exercise (running, yoga, pushups, etc.)
- duration: Time spent or reps/sets (e.g., "30 min", "3x10", "5k")
- details: Any additional context

Example:
Input: "Did 30 pushups and ran 5k this morning"
Output: {"activity": "pushups and running", "duration": "30 reps, 5k", "details": "morning workout"}

Respond with ONLY valid JSON, no extra text."""

    response = get_claude_response(message, system_prompt)

    try:
        # Try to parse JSON response
        data = json.loads(response)
        return data.get("activity", "workout"), data.get("duration", ""), data.get("details", "")
    except:
        # Fallback if JSON parsing fails
        return "workout", "", message

def summarize_note(message):
    """Summarize note in 5-7 words using Claude"""
    system_prompt = """Summarize the user's note in 5-7 words. Be specific and actionable.

Examples:
Input: "Had a great meeting with the design team about the new features"
Output: "Productive design team meeting on features"

Input: "Finished the Q1 report draft and sent to Sarah"
Output: "Completed Q1 report, sent to Sarah"

Respond with ONLY the summary, no extra text."""

    response = get_claude_response(message, system_prompt)
    return response.strip()

def generate_daily_summary(notes, workouts, username=None):
    """Generate daily summary from notes and workouts"""
    user_greeting = f"{username}" if username else "there"
    system_prompt = f"""You are Nomi, a supportive personal assistant for {user_greeting}.

Review the user's day and write a warm 2-4 sentence reflection that:
- Celebrates their accomplishments
- Mentions both workouts and notes
- Feels encouraging and personal
- Uses a friendly, supportive tone
- Address them by name when appropriate

Keep it concise and uplifting."""

    notes_text = "\n".join([f"- {n.get('summary', n.get('content', ''))}" for n in notes]) if notes else "No notes today"
    workouts_text = "\n".join([f"- {w.get('activity', '')} ({w.get('duration', '')})" for w in workouts]) if workouts else "No workouts today"

    prompt = f"""Here's what {user_greeting} did today:

WORKOUTS:
{workouts_text}

NOTES:
{notes_text}

Write a 2-4 sentence daily summary."""

    response = get_claude_response(prompt, system_prompt)
    return response.strip()

def generate_morning_motivation(username=None, yesterday_summary=None):
    """Generate morning motivation message"""
    user_greeting = f"{username}" if username else "there"
    system_prompt = f"""You are Nomi, a supportive personal assistant for {user_greeting}.

Give the user a warm, motivational 1-2 sentence message to start their day.
Be encouraging, positive, and energizing.
Address them by name when appropriate.
If you know what they did yesterday, reference it briefly."""

    if yesterday_summary:
        prompt = f"{user_greeting}'s yesterday: {yesterday_summary}\n\nGive morning motivation for today."
    else:
        prompt = f"Give a motivational morning message for {user_greeting} to start the day."

    response = get_claude_response(prompt, system_prompt)
    return response.strip()

def generate_login_greeting(username, day_of_week, hints=None):
    """Generate personalized greeting on login"""
    system_prompt = f"""You are Nomi, a supportive personal assistant for {username}.

Generate a warm welcome message that:
- Greets the user by name
- Mentions today's day ({day_of_week})
- Provides helpful next steps from the hints provided
- Keeps it to 2-3 sentences
- Sounds friendly and encouraging"""

    hints_text = ""
    if hints:
        hints_text = "\n\nSuggested next steps to mention:\n" + "\n".join([f"- {hint}" for hint in hints])

    prompt = f"""Welcome {username} back! Today is {day_of_week}.{hints_text}

Generate a friendly greeting message."""

    response = get_claude_response(prompt, system_prompt)
    return response.strip()
