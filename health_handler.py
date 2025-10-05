"""
Health & Fitness Handler - Specialized for workout and health tracking
"""
from claude_handler import get_claude_response
import json

def handle_health_fitness(message, username):
    """Handle health and fitness related messages"""

    # Extract workout/health data
    workout_data = extract_workout_data(message)

    # Generate response
    response = generate_fitness_response(username, workout_data)

    # Prepare metadata for unified entry
    metadata = {
        "activity": workout_data.get("activity", ""),
        "duration": workout_data.get("duration", ""),
        "intensity": workout_data.get("intensity", ""),
        "calories": workout_data.get("calories", ""),
        "details": workout_data.get("details", "")
    }

    return response, metadata, "health_fitness"

def extract_workout_data(message):
    """Extract structured workout data from message"""
    system_prompt = """You are a fitness tracking assistant. Extract workout information from the message.

Return a JSON object with these fields:
- activity: Type of exercise (running, yoga, pushups, swimming, etc.)
- duration: Time or reps/sets (e.g., "30 min", "3x10", "5k", "100 reps")
- intensity: Low, moderate, or high (if mentioned)
- calories: Estimated calories if mentioned
- details: Any additional context (time of day, location, feeling, etc.)

Examples:
Input: "Did 30 pushups and ran 5k this morning"
Output: {"activity": "pushups and running", "duration": "30 reps, 5k", "intensity": "moderate", "calories": "", "details": "morning workout"}

Input: "Intense 45 min HIIT session, burned about 400 calories"
Output: {"activity": "HIIT", "duration": "45 min", "intensity": "high", "calories": "400", "details": "intense session"}

Respond with ONLY valid JSON, no extra text."""

    response = get_claude_response(message, system_prompt)

    try:
        data = json.loads(response)
        return data
    except:
        return {
            "activity": "workout",
            "duration": "",
            "intensity": "",
            "calories": "",
            "details": message
        }

def generate_fitness_response(username, workout_data):
    """Generate encouraging fitness response"""
    system_prompt = f"""You are Nomi, a supportive fitness coach for {username}.

Generate a short, encouraging 1-2 sentence response that:
- Celebrates their workout/activity
- Mentions specific details (activity, duration, intensity)
- Sounds motivating and supportive
- Ends with a checkmark emoji ✓

Keep it enthusiastic but concise."""

    activity = workout_data.get("activity", "workout")
    duration = workout_data.get("duration", "")
    intensity = workout_data.get("intensity", "")

    prompt = f"""{username} just completed: {activity}
Duration: {duration}
Intensity: {intensity}

Generate an encouraging response."""

    response = get_claude_response(prompt, system_prompt)
    return response.strip()
