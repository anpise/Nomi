# Nomi 🤖

**Talk. Track. Transform.**

Nomi is an intelligent personal assistant that lives in your chat. Message it about workouts, ideas, reminders, or how you're feeling—and it quietly turns your words into organized logs, insights, and daily reflections. Built with an orchestrated architecture, Nomi uses specialized AI handlers to understand context and provide personalized support.

## ✨ Features

- 💬 **Natural Conversations** - Chat naturally, no rigid commands
- 🏋️ **Health Tracking** - Log workouts with auto-extracted intensity, duration, calories
- 📝 **Smart Notes** - Automatic categorization, priority, and reminder detection
- 📊 **Daily Summaries** - Get insights on your day, week, or trends
- 🌅 **Morning Motivation** - Personalized encouragement based on your progress
- 🎯 **Orchestrated AI** - Specialized handlers for different use cases
- 🔒 **Private & Local** - Your data stays in your MongoDB instance

## 🏗️ Architecture

### Orchestration System

```
User Message
    ↓
Orchestrator (classifies use case)
    ↓
┌─────────────────────────────────────┐
│  Specialized Handlers:              │
│  • health_handler.py                │
│  • notes_handler.py                 │
│  • summary_handler.py               │
│  • wellbeing_handler.py             │
└─────────────────────────────────────┘
    ↓
Claude API (specialized prompts)
    ↓
Response + Rich Metadata
    ↓
Unified Entry Saved to MongoDB
```

### Tech Stack

- **Frontend:** Streamlit (chat UI)
- **Backend:** Python 3.11+
- **Database:** MongoDB (local)
- **AI:** Claude 3.5 Haiku via Anthropic API
- **Architecture:** Orchestrated use-case handlers

## 🚀 Quick Start

### Prerequisites

1. **Python 3.11+**
2. **MongoDB** running locally on port 27017
   - Install: [MongoDB Community](https://www.mongodb.com/try/download/community)
   - Or via Docker: `docker run -d -p 27017:27017 mongo`
3. **Anthropic API Key** - Get one at [console.anthropic.com](https://console.anthropic.com/)

### Installation

```bash
# Clone or navigate to project directory
cd Nomi

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Add your API key to .env
# ANTHROPIC_API_KEY=your_key_here
# MONGO_URI=mongodb://localhost:27017/
```

### Run

```bash
streamlit run app.py
```

Visit **http://localhost:8501** in your browser.

### Demo Login

- **Username:** `demo`
- **Password:** `demo123`

## 💡 Usage Examples

### Health & Fitness
```
"Did 30 pushups and ran 5k this morning"
→ Extracts: activity, duration, intensity
→ Response: "Amazing work on those pushups and 5k run! ✓"
```

### Notes & Reminders
```
"Remind me to call Sarah tomorrow about Q1 report"
→ Extracts: summary, category, priority, reminder flag
→ Response: "✓ Saved: Call Sarah about Q1 report (reminder set)"
```

### Summaries & Analytics
```
"What did I do today?"
→ Generates daily summary with workout/note counts
→ Response: "Today you crushed a 5k run and logged 3 tasks..."
```

### Wellbeing & Motivation
```
"/morning"
→ Personalized based on yesterday's activity
→ Response: "Good morning! Yesterday you stayed active—let's keep it going!"
```

## 📁 Project Structure

```
Nomi/
├── app.py                    # Streamlit UI
├── auth.py                   # Authentication
├── db.py                     # MongoDB operations
├── orchestrator.py           # Message routing
├── health_handler.py         # Fitness use case
├── notes_handler.py          # Notes use case
├── summary_handler.py        # Analytics use case
├── wellbeing_handler.py      # Motivation use case
├── claude_handler.py         # Claude API wrapper
├── requirements.txt          # Dependencies
├── .env.example             # Environment template
├── Plan.md                  # Detailed plan
└── README.md                # This file
```

## 🗄️ Database Schema

### Collections

**entries** - Unified storage (one entry per message)
```javascript
{
  username: "demo",
  message: "Did 30 pushups",
  response: "Great work! ✓",
  use_case: "health_fitness",
  metadata: {
    activity: "pushups",
    duration: "30 reps",
    intensity: "moderate"
  },
  timestamp: ISODate("2025-01-06T10:30:00Z")
}
```

**messages** - Chat history
**users** - Authentication

## 🎨 UI Features

- **Personalized Greetings** - Welcome message with hints on login
- **Quick Actions** - Copyable example commands above chat
- **Multi-Tab Views:**
  - 💬 Chat - Main conversation
  - 🏋️ Workouts - Fitness entries with intensity
  - 📝 Notes - Categorized notes with priority
  - 📊 Summary - Daily analytics dashboard

## 🔧 Configuration

### Environment Variables (.env)

```env
ANTHROPIC_API_KEY=your_anthropic_key_here
MONGO_URI=mongodb://localhost:27017/
```

### MongoDB Setup

The app auto-creates collections and indexes on first run. No manual setup needed.

## 🛠️ Development

### Adding New Use Cases

1. Create handler in `new_handler.py`
2. Add classification logic in `orchestrator.py`
3. Update UI tabs in `app.py` if needed

### Handler Template

```python
def handle_new_use_case(message, username):
    """Handle new use case"""
    # Extract data
    data = extract_data(message)

    # Generate response
    response = generate_response(username, data)

    # Prepare metadata
    metadata = {...}

    return response, metadata, "new_use_case"
```

## 📝 License

MIT

## 🤝 Contributing

This is a personal project, but feel free to fork and adapt for your needs!

---

**Built with ❤️ using Claude AI**
