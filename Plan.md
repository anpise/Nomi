# Nomi MVP Plan

## Product Summary
Intelligent personal assistant with Streamlit chat UI that uses an orchestrated architecture to handle health tracking, notes, summaries, and wellbeing support via MongoDB + Claude API.

## User Stories
- Log a workout in natural language ("Did 30 pushups and ran 5k")
- Jot a note with automatic categorization ("Finished the design mockups")
- Ask for daily/weekly summary ("What did I do today?")
- Get personalized morning motivation
- Receive insights and analytics on habits

## Architecture

### **Orchestration System**
Messages are routed to specialized handlers based on use case:

1. **orchestrator.py** - Classifies messages and routes to appropriate handler
2. **Specialized Handlers:**
   - **health_handler.py** - Workouts, fitness, health metrics (intensity, calories, etc.)
   - **notes_handler.py** - Notes, reminders, tasks (priority, category, tags)
   - **summary_handler.py** - Daily/weekly summaries, insights, analytics
   - **wellbeing_handler.py** - Morning motivation, encouragement, reflections
3. **Unified Storage** - One entry per message with rich metadata

### **Flow:**
```
User Message → Orchestrator (classify) → Handler (specialized prompt)
→ Claude API → Response + Metadata → Unified Entry Saved
```

## Features

1. **Chat Interface** - Streamlit chat UI with personalized greetings
2. **Login Required** - Username/password authentication (MongoDB)
3. **Auto-Classification** - Intelligent routing to specialized handlers
4. **Rich Metadata:**
   - Health: activity, duration, intensity, calories
   - Notes: summary, category, priority, tags, reminders
   - Summaries: period, counts, insights
   - Wellbeing: motivation type, context
5. **Quick Actions** - Copyable hint boxes above chat input
6. **Multi-Tab Views:**
   - Chat - Main conversation
   - Workouts - Health/fitness entries
   - Notes - Notes and reminders
   - Summary - Daily analytics and insights

## Data Model (MongoDB Collections)

**users** - Authentication
```json
{
  "username": "string",
  "password": "string",
  "created_at": "datetime"
}
```

**entries** - Unified storage (NEW - Orchestration System)
```json
{
  "username": "string",
  "message": "string",
  "response": "string",
  "use_case": "health_fitness | notes_reminders | summary_analytics | motivation_wellbeing",
  "metadata": {
    // Health/Fitness
    "activity": "string",
    "duration": "string",
    "intensity": "low | moderate | high",
    "calories": "string",
    "details": "string",

    // Notes/Reminders
    "summary": "string",
    "category": "meeting | task | idea | event | personal | work",
    "priority": "low | medium | high",
    "has_reminder": "boolean",
    "reminder_time": "string",
    "tags": ["array"],

    // Summary/Analytics
    "count": "number",
    "health_count": "number",
    "notes_count": "number",
    "period": "today | week | insights",

    // Wellbeing
    "type": "morning_motivation | encouragement | reflection | general_support"
  },
  "timestamp": "datetime"
}
```

**messages** - Chat history
```json
{
  "username": "string",
  "role": "user | assistant",
  "content": "string",
  "timestamp": "datetime"
}
```

**Legacy Collections** (deprecated, kept for migration)
- notes, workouts (replaced by unified entries)

## Files Structure

### **Core Application**
1. **app.py** — Main Streamlit app with chat UI
2. **auth.py** — Login/logout authentication
3. **db.py** — MongoDB connection and CRUD operations

### **Orchestration System**
4. **orchestrator.py** — Message routing and classification
5. **health_handler.py** — Health/fitness use case handler
6. **notes_handler.py** — Notes/reminders use case handler
7. **summary_handler.py** — Summary/analytics use case handler
8. **wellbeing_handler.py** — Motivation/wellbeing use case handler

### **AI Integration**
9. **claude_handler.py** — Claude API wrapper with date context

### **Configuration**
10. **requirements.txt** — Dependencies (streamlit, anthropic, pymongo, python-dotenv)
11. **.env.example** — Environment template
12. **Plan.md** — This file
13. **README.md** — Setup and usage guide

## Demo Flow

1. **Login** → Personalized greeting with today's date
2. **Health:** "Did 30 pushups and ran 5k" → Extracts activity, duration, intensity
3. **Notes:** "Remind me to call Sarah tomorrow" → Categorizes, adds reminder flag
4. **Summary:** "What did I do today?" → Daily reflection with metrics
5. **Wellbeing:** "/morning" → Personalized motivation based on yesterday
6. **View Tabs:**
   - Workouts tab → See all fitness entries with intensity
   - Notes tab → See categorized notes with priority
   - Summary tab → Analytics dashboard with counts
7. **Logout**

## Key Differentiators

✅ **Orchestrated Architecture** - Specialized handlers for each use case
✅ **Rich Metadata** - Automatic extraction of structured data
✅ **Unified Storage** - One entry per message, easy querying
✅ **Personalized Context** - Username + date in every Claude prompt
✅ **Login Greetings** - Welcome message with hints on first login
✅ **Copyable Hints** - Quick action examples above chat input
