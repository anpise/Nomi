import os
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

# Initialize LangChain ChatAnthropic
llm = ChatAnthropic(
    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_tokens=int(os.getenv("CLAUDE_LOGIN_GREETING_MAX_TOKENS", "1024"))
)

def get_claude_response(prompt, system_prompt=None, model="claude-sonnet-4-5-20250929", conversation_history=None):
    """Get response from Claude API via LangChain with optional conversation context"""
    import logging
    logger = logging.getLogger(__name__)

    # Add current date and time context to system prompt
    now = datetime.now()
    current_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    date_context = f"\n\nCurrent date and time context: Today is {current_datetime}."

    if system_prompt:
        system_prompt = system_prompt + date_context
    else:
        system_prompt = date_context

    # Build messages with conversation history
    messages = []

    # Add system message
    if system_prompt:
        messages.append(SystemMessage(content=system_prompt))

    # Add conversation history if provided (for context/memory)
    if conversation_history:
        logger.info(f"Adding {len(conversation_history[-8:])} messages from conversation history")
        # Only include last few messages to avoid token limits
        for msg in conversation_history[-8:]:  # Last 8 messages for context
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    # Add current prompt as latest user message
    messages.append(HumanMessage(content=prompt))

    logger.info(f"Invoking LangChain LLM with {len(messages)} messages")

    # Invoke LangChain LLM
    response = llm.invoke(messages)
    logger.info(f"Received response from LLM: {len(response.content)} chars")

    return response.content

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
    # Get current time for appropriate greeting
    current_hour = datetime.now().hour
    if current_hour < 12:
        time_greeting = "morning"
    elif current_hour < 17:
        time_greeting = "afternoon"
    else:
        time_greeting = "evening"

    system_prompt = f"""You are Nomi, {username}'s personal assistant.

Speak directly to {username} using "you/your".

Generate a SHORT welcome message (1-2 sentences ONLY) that:
- Uses appropriate time greeting (it's {time_greeting} now, NOT morning)
- Mentions it's {day_of_week}
- Sounds warm but BRIEF
- NO need to list actions - just welcome them"""

    prompt = f"""Greet {username}. It's {time_greeting} on {day_of_week}.

Give a short, warm welcome (1-2 sentences max)."""

    response = get_claude_response(prompt, system_prompt)
    return response.strip()
