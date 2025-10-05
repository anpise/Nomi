"""
LangGraph Agents for Nomi - Agentic architecture with supervisor and specialized agents
"""
import logging
from typing import TypedDict, Annotated, Literal
from datetime import datetime, date, timedelta
from langchain_anthropic import ChatAnthropic
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.graph import StateGraph, END
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger(__name__)

# Initialize LLM
llm = ChatAnthropic(
    model=os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929"),
    api_key=os.getenv("ANTHROPIC_API_KEY"),
    max_tokens=int(os.getenv("CLAUDE_MAX_TOKENS", "4000"))
)

# State definition
class AgentState(TypedDict):
    """State shared across all agents"""
    username: str
    message: str
    conversation_history: list
    use_case: str
    response: str
    metadata: dict
    next_agent: str


# SUPERVISOR AGENT - Entry point that routes to specialized agents
def supervisor_agent(state: AgentState) -> AgentState:
    """Supervisor agent that classifies and routes messages to specialized agents"""
    logger.info(f"Supervisor: Classifying message for user '{state['username']}'")

    message = state["message"]

    # Add current datetime context
    now = datetime.now()
    current_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    date_context = f"\n\nCurrent date and time: {current_datetime}"

    system_prompt = f"""You are a supervisor routing messages to specialized agents.

Classify the user's message into ONE category:
- health_fitness: Workouts, exercise, physical activity, health metrics
- notes_reminders: Notes, reminders, to-dos, tasks, meetings, events
- summary_analytics: Summaries, insights, analytics, reflections
- motivation_wellbeing: Morning motivation, encouragement, mental wellness

Keywords:
- health_fitness: "workout", "exercise", "ran", "gym", "pushups", "yoga", "lifted"
- notes_reminders: "note", "remember", "todo", "task", "meeting", "finished"
- summary_analytics: "summary", "what did i do", "recap", "insights", "progress"
- motivation_wellbeing: "motivate", "inspire", "morning", "feeling", "mood"

Respond with ONLY ONE WORD: health_fitness, notes_reminders, summary_analytics, or motivation_wellbeing.{date_context}"""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=message)
    ]

    response = llm.invoke(messages)
    use_case = response.content.strip().lower()

    valid_cases = ["health_fitness", "notes_reminders", "summary_analytics", "motivation_wellbeing"]
    if use_case not in valid_cases:
        logger.warning(f"Supervisor: Invalid use case '{use_case}', defaulting to notes_reminders")
        use_case = "notes_reminders"

    logger.info(f"Supervisor: Routed to '{use_case}' agent")

    state["use_case"] = use_case
    state["next_agent"] = use_case

    return state


# HEALTH/FITNESS AGENT
def health_fitness_agent(state: AgentState) -> AgentState:
    """Agent specialized in handling health and fitness messages"""
    logger.info(f"HealthAgent: Processing workout for '{state['username']}'")

    username = state["username"]
    message = state["message"]
    conversation_history = state.get("conversation_history", [])

    # Add current datetime
    now = datetime.now()
    current_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    date_context = f"\n\nCurrent date and time: {current_datetime}"

    # Parse workout details
    parse_system = f"""Extract workout info from the message.
Return JSON: {{"activity": "exercise type", "duration": "time/reps", "details": "context"}}.{date_context}"""

    parse_messages = [
        SystemMessage(content=parse_system),
        HumanMessage(content=message)
    ]

    import json
    parse_response = llm.invoke(parse_messages)
    try:
        workout_data = json.loads(parse_response.content)
        activity = workout_data.get("activity", "workout")
        duration = workout_data.get("duration", "")
        details = workout_data.get("details", "")
    except:
        activity = "workout"
        duration = ""
        details = message

    # Generate response
    response_system = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 8-10 words.

Rules:
- Direct address: "Nice!" or "You crushed it!"
- ONE short sentence only
- End with ✓
- NO explanations, NO tips, NO extra encouragement
- If they mentioned it earlier, briefly acknowledge: "You did it!" ✓{date_context}"""

    response_messages = [SystemMessage(content=response_system)]

    # Add conversation history
    if conversation_history:
        for msg in conversation_history[-8:]:
            if msg["role"] == "user":
                response_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                response_messages.append(AIMessage(content=msg["content"]))

    response_messages.append(HumanMessage(content=f"{username} logged: {activity} ({duration})"))

    response = llm.invoke(response_messages)

    state["response"] = response.content.strip()
    state["metadata"] = {
        "activity": activity,
        "duration": duration,
        "details": details
    }
    state["next_agent"] = "end"

    logger.info(f"HealthAgent: Generated response")
    return state


# NOTES/REMINDERS AGENT
def notes_reminders_agent(state: AgentState) -> AgentState:
    """Agent specialized in handling notes and reminders"""
    logger.info(f"NotesAgent: Processing note for '{state['username']}'")

    username = state["username"]
    message = state["message"]
    conversation_history = state.get("conversation_history", [])

    # Add current datetime
    now = datetime.now()
    current_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    date_context = f"\n\nCurrent date and time: {current_datetime}"

    # Summarize note
    summary_system = f"""Summarize the note in 5-7 words. Be specific.{date_context}"""
    summary_messages = [
        SystemMessage(content=summary_system),
        HumanMessage(content=message)
    ]

    summary_response = llm.invoke(summary_messages)
    summary = summary_response.content.strip()

    # Generate response
    response_system = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses VERY SHORT - max 5-6 words.

Rules:
- Just acknowledge: "Got it ✓" or "Saved ✓"
- NO elaboration, NO explanations
- End with ✓{date_context}"""

    response_messages = [SystemMessage(content=response_system)]

    # Add conversation history
    if conversation_history:
        for msg in conversation_history[-8:]:
            if msg["role"] == "user":
                response_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                response_messages.append(AIMessage(content=msg["content"]))

    response_messages.append(HumanMessage(content=f"{username} noted: {summary}"))

    response = llm.invoke(response_messages)

    state["response"] = response.content.strip()
    state["metadata"] = {
        "summary": summary,
        "full_content": message
    }
    state["next_agent"] = "end"

    logger.info(f"NotesAgent: Generated response")
    return state


# SUMMARY/ANALYTICS AGENT
def summary_analytics_agent(state: AgentState) -> AgentState:
    """Agent specialized in generating summaries and analytics"""
    logger.info(f"SummaryAgent: Processing summary for '{state['username']}'")

    username = state["username"]
    message = state["message"]

    from db import get_unified_entries

    # Determine summary type
    message_lower = message.lower()
    if any(word in message_lower for word in ["week", "weekly", "past week", "last week"]):
        summary_type = "weekly"
        today_date = date.today()
        week_ago = today_date - timedelta(days=7)
        entries = get_unified_entries(username, start_date=week_ago, end_date=today_date)
    elif any(word in message_lower for word in ["insight", "pattern", "trend", "progress", "analysis"]):
        summary_type = "insights"
        today_date = date.today()
        week_ago = today_date - timedelta(days=7)
        entries = get_unified_entries(username, start_date=week_ago, end_date=today_date)
    else:
        summary_type = "daily"
        today_date = date.today()
        entries = get_unified_entries(username, start_date=today_date)

    if not entries:
        state["response"] = "Nothing logged yet."
        state["metadata"] = {"count": 0, "period": summary_type}
        state["next_agent"] = "end"
        return state

    health_count = len([e for e in entries if e.get("use_case") == "health_fitness"])
    notes_count = len([e for e in entries if e.get("use_case") == "notes_reminders"])

    # Add current datetime
    now = datetime.now()
    current_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    date_context = f"\n\nCurrent date and time: {current_datetime}"

    system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 2-3 short sentences.

Rules:
- Direct address: "You crushed today!"
- Celebrate briefly, no elaboration
- Mention key activities in ONE sentence
- End with ✓
- NO lengthy praise, NO extra encouragement{date_context}"""

    prompt = f"""Review {username}'s {summary_type}:
- {health_count} workouts
- {notes_count} notes/tasks

Respond in max 2-3 short sentences."""

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=prompt)
    ]

    response = llm.invoke(messages)

    state["response"] = response.content.strip()
    state["metadata"] = {
        "count": len(entries),
        "health_count": health_count,
        "notes_count": notes_count,
        "period": summary_type
    }
    state["next_agent"] = "end"

    logger.info(f"SummaryAgent: Generated {summary_type} summary")
    return state


# MOTIVATION/WELLBEING AGENT
def motivation_wellbeing_agent(state: AgentState) -> AgentState:
    """Agent specialized in motivation and wellbeing support"""
    logger.info(f"WellbeingAgent: Processing motivation for '{state['username']}'")

    username = state["username"]
    message = state["message"]
    conversation_history = state.get("conversation_history", [])

    # Add current datetime
    now = datetime.now()
    current_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    date_context = f"\n\nCurrent date and time: {current_datetime}"

    # Determine support type
    message_lower = message.lower()
    if any(word in message_lower for word in ["morning", "good morning", "start day"]):
        support_type = "morning"
    elif any(word in message_lower for word in ["reflect", "feeling", "mood", "how am i"]):
        support_type = "reflection"
    else:
        support_type = "encouragement"

    if support_type == "morning":
        system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 8-10 words.

Rules:
- Greet briefly: "Morning! Let's crush today!"
- End with ✓ or 💪
- NO lengthy motivation, NO elaboration{date_context}"""

        prompt = f"""Morning greeting for {username}.

Respond in max 8-10 words."""

    elif support_type == "reflection":
        system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 2-3 short sentences.

Rules:
- Brief reflection: "You've been consistent this week"
- ONE key observation
- End with brief encouragement and ✓
- NO lengthy insights, NO elaboration{date_context}"""

        prompt = f"""Reflect on {username}.

Respond in max 2-3 short sentences."""

    else:  # encouragement
        system_prompt = f"""You are Nomi, {username}'s PA.

CRITICAL: Keep responses SHORT - max 8-10 words.

Rules:
- Brief encouragement: "You've got this!"
- Direct address only
- End with ✓ or 💪
- NO lengthy support, NO elaboration{date_context}"""

        prompt = f"""{username} said: "{message}"

Respond in max 8-10 words."""

    messages = [SystemMessage(content=system_prompt)]

    # Add conversation history
    if conversation_history:
        for msg in conversation_history[-8:]:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                messages.append(AIMessage(content=msg["content"]))

    messages.append(HumanMessage(content=prompt))

    response = llm.invoke(messages)

    state["response"] = response.content.strip()
    state["metadata"] = {
        "type": support_type
    }
    state["next_agent"] = "end"

    logger.info(f"WellbeingAgent: Generated {support_type} response")
    return state


# ROUTING LOGIC
def route_to_agent(state: AgentState) -> Literal["health_fitness", "notes_reminders", "summary_analytics", "motivation_wellbeing", "end"]:
    """Router function that determines which agent to call next"""
    next_agent = state.get("next_agent", "end")
    logger.info(f"Router: Next agent is '{next_agent}'")
    return next_agent


# BUILD LANGGRAPH WORKFLOW
def build_workflow():
    """Build the LangGraph workflow with supervisor and specialized agents"""
    logger.info("Building LangGraph workflow")

    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("supervisor", supervisor_agent)
    workflow.add_node("health_fitness", health_fitness_agent)
    workflow.add_node("notes_reminders", notes_reminders_agent)
    workflow.add_node("summary_analytics", summary_analytics_agent)
    workflow.add_node("motivation_wellbeing", motivation_wellbeing_agent)

    # Set entry point
    workflow.set_entry_point("supervisor")

    # Add conditional edges from supervisor to specialized agents
    workflow.add_conditional_edges(
        "supervisor",
        route_to_agent,
        {
            "health_fitness": "health_fitness",
            "notes_reminders": "notes_reminders",
            "summary_analytics": "summary_analytics",
            "motivation_wellbeing": "motivation_wellbeing",
            "end": END
        }
    )

    # Add edges from specialized agents to END
    workflow.add_edge("health_fitness", END)
    workflow.add_edge("notes_reminders", END)
    workflow.add_edge("summary_analytics", END)
    workflow.add_edge("motivation_wellbeing", END)

    # Compile
    app = workflow.compile()

    logger.info("LangGraph workflow built successfully")
    return app


# Main workflow instance
nomi_workflow = build_workflow()
