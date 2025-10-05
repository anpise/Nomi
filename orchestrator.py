"""
Orchestrator - Routes user messages to appropriate specialized handlers
"""
from datetime import datetime
from claude_handler import get_claude_response

def classify_use_case(message):
    """Classify message into specific use case category"""
    import logging
    logger = logging.getLogger(__name__)

    logger.info(f"Classifying message: {message[:50]}...")

    system_prompt = """You are a use case classifier for Nomi, a personal assistant.

Classify the user's message into ONE of these categories:
- health_fitness: Workouts, exercise, physical activity, health metrics, fitness goals
- notes_reminders: General notes, reminders, to-dos, tasks, meetings, events
- summary_analytics: Requests for summaries, insights, analytics, reflections
- motivation_wellbeing: Morning motivation, encouragement, mental wellness

Keywords:
- health_fitness: "workout", "exercise", "ran", "gym", "pushups", "yoga", "lifted", "weight", "calories", "steps"
- notes_reminders: "note", "remember", "todo", "task", "meeting", "call", "finished", "completed", "remind me"
- summary_analytics: "summary", "what did i do", "recap", "analyze", "insights", "progress", "how many"
- motivation_wellbeing: "motivate", "inspire", "morning", "feeling", "mood", "stressed"

Respond with ONLY ONE WORD: health_fitness, notes_reminders, summary_analytics, or motivation_wellbeing.
If unclear, default to "notes_reminders"."""

    response = get_claude_response(message, system_prompt)
    use_case = response.strip().lower()

    valid_cases = ["health_fitness", "notes_reminders", "summary_analytics", "motivation_wellbeing"]
    if use_case not in valid_cases:
        logger.warning(f"Invalid use case '{use_case}', defaulting to notes_reminders")
        return "notes_reminders"

    logger.info(f"Classified as: {use_case}")
    return use_case

def route_message(message, username, use_case=None, conversation_history=None):
    """Route message to appropriate handler based on use case"""
    import logging
    logger = logging.getLogger(__name__)

    if not use_case:
        use_case = classify_use_case(message)

    logger.info(f"Routing message for user '{username}' to handler: {use_case}")

    # Import handlers
    from health_handler import handle_health_fitness
    from notes_handler import handle_notes_reminders
    from summary_handler import handle_summary_analytics
    from wellbeing_handler import handle_motivation_wellbeing

    # Route to appropriate handler
    handlers = {
        "health_fitness": handle_health_fitness,
        "notes_reminders": handle_notes_reminders,
        "summary_analytics": handle_summary_analytics,
        "motivation_wellbeing": handle_motivation_wellbeing
    }

    handler = handlers.get(use_case, handle_notes_reminders)

    # Each handler returns: (response_text, entry_data, entry_type)
    # Pass conversation history for context/memory
    logger.info(f"Invoking handler: {handler.__name__}")
    result = handler(message, username, conversation_history)
    logger.info(f"Handler returned response")

    return result

def save_unified_entry(username, message, response, use_case, metadata=None):
    """Save a unified entry to the database"""
    from db import save_unified_entry as db_save_entry

    entry = {
        "username": username,
        "message": message,
        "response": response,
        "use_case": use_case,
        "metadata": metadata or {},
        "timestamp": datetime.now()
    }

    db_save_entry(entry)
