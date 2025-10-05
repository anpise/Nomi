# Nomi 🤖

**Talk. Track. Transform.**

Nomi is an intelligent personal assistant powered by **LangGraph agentic architecture**. Message it about workouts, ideas, reminders, or how you're feeling—and specialized AI agents quietly turn your words into organized logs, insights, and daily reflections. Built with LangChain + LangGraph for autonomous agent routing and context-aware responses.

Live Demo - https://nomi-v1.streamlit.app/
---

## ✨ Features

### 🎯 **LangGraph Agentic Architecture**
- **Supervisor Agent** - Intelligent message classification and routing
- **4 Specialized Agents** - Each knows exactly what to do, no dependencies
- **Autonomous Decision Making** - Agents handle their use cases end-to-end
- **State Management** - Shared state flows seamlessly through workflow

### 💬 **Natural Conversations**
- Chat naturally, no rigid commands
- **24-hour conversation memory** (last 10 messages)
- Context-aware responses that remember your recent activity
- Ultra-brief responses (8-10 words max) for quick interactions

### 🏋️ **Health & Fitness Tracking**
- Log workouts with auto-extracted activity, duration, details
- Brief acknowledgments: *"Nice! 30 pushups crushed ✓"*
- Structured metadata saved to MongoDB
- Filtered workout view in UI

### 📝 **Smart Notes & Reminders**
- Automatic summarization (5-7 words)
- Ultra-brief confirmations: *"Got it ✓"* or *"Saved ✓"*
- Full content preserved with summary metadata
- Handles tasks, meetings, reminders

### 📊 **Daily Summaries & Analytics**
- Daily summaries (2-3 sentences max)
- Weekly summaries (3-4 sentences)
- Insights and patterns (2-3 sentences)
- Quick stats dashboard

### 🌅 **Motivation & Wellbeing**
- Morning motivation (8-10 words): *"Morning! Let's crush today! 💪"*
- Encouragement on demand
- Reflection support (2-3 sentences)
- Time-aware greetings (morning/afternoon/evening)

### 🔒 **Private & Secure**
- Your data stays in your local MongoDB
- User authentication with session management
- First-login-of-day detection
- Isolated user data

---

## 🏗️ Architecture

### LangGraph Workflow

```
                        User Message
                             ↓
                    ┌────────────────┐
                    │ Supervisor     │
                    │ Agent          │ ← Classifies use case
                    │ (Entry Point)  │
                    └────────┬───────┘
                             ↓
        ┌────────────────────┼────────────────────┐
        ↓                    ↓                    ↓
┌───────────────┐    ┌───────────────┐   ┌──────────────┐
│ Health Agent  │    │ Notes Agent   │   │Summary Agent │  ...
│               │    │               │   │              │
│ • Parse data  │    │• Summarize    │   │• Query DB    │
│ • Generate    │    │• Acknowledge  │   │• Generate    │
│   response    │    │               │   │  insights    │
│ • Max 8-10    │    │• Max 5-6      │   │• Max 2-3     │
│   words       │    │  words        │   │  sentences   │
└───────┬───────┘    └───────┬───────┘   └──────┬───────┘
        ↓                    ↓                    ↓
        └────────────────────┴────────────────────┘
                             ↓
                    Response + Metadata
                             ↓
                  Save to MongoDB (unified entry)
```

### Agents Overview

| Agent | Use Case | Response Length | Example |
|-------|----------|-----------------|---------|
| **Supervisor** | Routes messages | N/A | Classifies → health_fitness |
| **Health** | Workouts, exercise | 8-10 words | "Nice! 30 pushups crushed ✓" |
| **Notes** | Notes, tasks, reminders | 5-6 words | "Got it ✓" |
| **Summary** | Daily/weekly recaps | 2-3 sentences | "You crushed today! 2 workouts and 3 notes ✓" |
| **Wellbeing** | Motivation, reflection | 8-10 words / 2-3 sentences | "Morning! Let's go! 💪" |

### Tech Stack

| Layer | Technology |
|-------|-----------|
| **UI** | Streamlit |
| **Agents** | LangGraph + LangChain |
| **LLM** | Claude 3.5 Haiku (Anthropic) |
| **Database** | MongoDB (local) |
| **Language** | Python 3.11+ |

---

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
# Start MongoDB (if not running)
mongod

# Run Nomi
streamlit run app.py
```

Visit **http://localhost:8501** in your browser.

---

## 💡 Usage Examples

### Health & Fitness
```
User: "Did 30 pushups"
Agent: "Nice! 30 pushups crushed ✓"

User: "Ran 5k in 25 minutes this morning"
Agent: "Great 5k run! ✓"
```
→ Supervisor routes to **Health Agent**
→ Extracts: activity, duration, details
→ Saves to DB with `use_case: health_fitness`

### Notes & Reminders
```
User: "Note: Buy groceries tomorrow"
Agent: "Saved ✓"

User: "Finished the quarterly report"
Agent: "Got it ✓"
```
→ Supervisor routes to **Notes Agent**
→ Summarizes in 5-7 words
→ Saves with `use_case: notes_reminders`

### Summaries & Analytics
```
User: "What did I do today?"
Agent: "You crushed today! 2 workouts and 3 notes logged. Keep going ✓"

User: "Weekly summary"
Agent: "Solid week! 8 workouts completed. You're consistent ✓"
```
→ Supervisor routes to **Summary Agent**
→ Queries MongoDB for aggregated data
→ Generates 2-3 sentence summary

### Wellbeing & Motivation
```
User: "Good morning"
Agent: "Morning! Let's crush today! 💪"

User: "Motivate me"
Agent: "You've got this! Keep pushing! ✓"
```
→ Supervisor routes to **Wellbeing Agent**
→ Time-aware greetings (morning/afternoon/evening)
→ Brief, energetic responses (8-10 words)

---

## 📁 Project Structure

```
Nomi/
├── app.py                    # Streamlit UI + main entry point
├── agents.py                 # LangGraph workflow + all agents ⭐
├── claude_handler.py         # LangChain LLM wrapper
├── db.py                     # MongoDB operations
├── auth.py                   # User authentication
├── requirements.txt          # Dependencies (langchain, langgraph, streamlit, pymongo)
├── .env.example              # Environment template
├── Plan.md                   # Original MVP plan
├── TESTING.md                # Comprehensive testing guide ⭐
├── PROJECT_STATUS.md         # Current status + roadmap ⭐
└── README.md                 # This file

# Deprecated files (replaced by agents.py):
├── orchestrator.py           # [DEPRECATED - use agents.py]
├── health_handler.py         # [DEPRECATED - use agents.py]
├── notes_handler.py          # [DEPRECATED - use agents.py]
├── summary_handler.py        # [DEPRECATED - use agents.py]
└── wellbeing_handler.py      # [DEPRECATED - use agents.py]
```

---

## 🗄️ Database Schema

### Collections

#### **entries** (Unified Storage)
One entry per message, regardless of type:
```javascript
{
  username: "demo",
  message: "Did 30 pushups",              // Original user message
  response: "Nice! 30 pushups crushed ✓", // Agent response
  use_case: "health_fitness",             // health_fitness | notes_reminders | summary_analytics | motivation_wellbeing
  metadata: {                             // Agent-specific structured data
    activity: "pushups",
    duration: "30 reps",
    details: ""
  },
  timestamp: ISODate("2025-10-05T10:30:00Z")
}
```

**Indexes**:
- `(username, timestamp)` - Fast user queries
- `(username, use_case, timestamp)` - Filtered views

#### **messages** (Conversation History)
```javascript
{
  username: "demo",
  role: "user",                           // user | assistant
  content: "Did 30 pushups",
  timestamp: ISODate("2025-10-05T10:30:00Z")
}
```
→ Used for **24-hour conversation memory** (last 10 messages)

#### **users** (Authentication)
```javascript
{
  username: "demo",
  password: "hashed_password",
  created_at: ISODate("2025-10-01T00:00:00Z"),
  last_login: ISODate("2025-10-05T08:00:00Z")  // Tracks first-login-of-day
}
```

---

## 🎨 UI Features

### Login/Signup
- Tab-based interface (Login | Signup)
- Session management
- Time-aware greeting on first login of day

### Main Chat Interface
- WhatsApp-style chat window
- User messages (right, blue) | Assistant messages (left, gray)
- Message history persisted
- Input box with auto-focus

### Multi-Tab Views
- **💬 Chat** - Full conversation history
- **🏋️ Workouts** - Filtered `health_fitness` entries
- **📝 Notes** - Filtered `notes_reminders` entries
- **📊 Summary** - Quick stats + summary request

### Quick Actions
- Copyable example commands above chat
- Logout button in sidebar

---

## 🔧 Configuration

### Environment Variables (.env)

```env
ANTHROPIC_API_KEY=your_anthropic_key_here
MONGO_URI=mongodb://localhost:27017/
```

### MongoDB Setup

The app auto-creates collections and indexes on first run. No manual setup needed.

---

## 🛠️ Development

### Adding New Agents

1. **Create agent function in `agents.py`**:
```python
def new_agent(state: AgentState) -> AgentState:
    """Agent specialized in new use case"""
    username = state["username"]
    message = state["message"]

    # Your logic here
    response = "Your response"
    metadata = {"key": "value"}

    state["response"] = response
    state["metadata"] = metadata
    state["next_agent"] = "end"
    return state
```

2. **Update supervisor classification**:
Add keywords in `supervisor_agent()` system prompt

3. **Add to workflow**:
```python
workflow.add_node("new_agent", new_agent)
workflow.add_conditional_edges(
    "supervisor",
    route_to_agent,
    {"new_agent": "new_agent", ...}
)
workflow.add_edge("new_agent", END)
```

4. **Update UI** (optional):
Add filtered tab in `app.py` if needed

---

## 📊 Performance

- **Message Response Time**: <5s end-to-end
- **Supervisor Classification**: <1s
- **Agent Response Generation**: <3s
- **Database Save**: <500ms
- **Conversation Memory**: Last 10 messages OR 24 hours (whichever smaller)

---

## 🧪 Testing

See **[TESTING.md](TESTING.md)** for comprehensive testing guide with:
- 12 test categories (200+ scenarios)
- Testing checklist
- MongoDB verification queries
- Expected logging output
- Troubleshooting guide

**Quick Test**:
```bash
# Send these messages and verify routing:
"Did 30 pushups"           → health_fitness agent
"Note: Call John"          → notes_reminders agent
"What did I do today?"     → summary_analytics agent
"Good morning"             → motivation_wellbeing agent
```

---

## 📈 Project Status

**Current Version**: v1.0 (LangGraph Agentic Architecture)

**Completed**:
- ✅ LangGraph workflow with supervisor + 4 specialized agents
- ✅ MongoDB unified storage + conversation memory
- ✅ LangChain integration with comprehensive logging
- ✅ Response brevity enforcement (user feedback-driven)
- ✅ Time-aware personalization
- ✅ Full documentation (README, Plan, Testing, Status)

**Roadmap** (see [PROJECT_STATUS.md](PROJECT_STATUS.md)):
- Phase 1: Smart reminders, analytics charts, voice input
- Phase 2: Proactive suggestions, natural language queries, images
- Phase 3: Social features, leaderboards, export/integrations
- Phase 4: Mobile app, cloud deployment, scaling
- Phase 5: Custom agent training, multi-agent collaboration, predictive analytics

---

## 🐛 Known Issues

1. **No error handling for MongoDB connection failures** - Priority: High
2. **LLM responses occasionally exceed word limits** - Priority: Medium
3. **No input validation on message length** - Priority: Low

See [PROJECT_STATUS.md](PROJECT_STATUS.md#-known-issues) for full list.

---

## 💡 Key Features

### What Makes Nomi Different?

1. **LangGraph Agents** - Not just prompt routing; actual autonomous agents with state management
2. **Ultra-Brief Responses** - 8-10 words max for most interactions (user feedback-driven)
3. **Conversation Memory** - 24-hour context window for coherent multi-turn conversations
4. **Unified Storage** - Single collection for all message types with rich metadata
5. **Time-Aware Personalization** - Greetings adapt to time of day, responses use first-person
6. **Comprehensive Logging** - Every agent action logged for debugging and monitoring

---

## 📚 Documentation

- **[README.md](README.md)** - This file (setup, usage, architecture)
- **[Plan.md](Plan.md)** - Original MVP planning and decisions
- **[TESTING.md](TESTING.md)** - Comprehensive testing guide (12 categories)
- **[PROJECT_STATUS.md](PROJECT_STATUS.md)** - Current status + future roadmap

---

## 🎓 Learnings

**What Went Well**:
- LangGraph provided clean abstraction for agent routing
- User feedback on verbosity led to major UX improvement
- Unified storage simplified queries significantly
- Modular agents made debugging trivial

**Key Insights**:
- Brevity is gold for chat interfaces
- Autonomous agents > simple prompt routing
- Conversation memory = 10x better UX
- Logging is essential for LangGraph workflows

See [PROJECT_STATUS.md](PROJECT_STATUS.md#-learnings) for full analysis.

---

## 📝 License

MIT

---

## 🤝 Contributing

This is a personal project MVP, but feel free to fork and adapt!

**To contribute**:
1. Run tests (see [TESTING.md](TESTING.md))
2. Create feature branch
3. Add logging for new code
4. Update relevant docs
5. Submit PR with test results

---

## 📞 Support

**Issues**: Open an issue on GitHub
**Questions**: See [TESTING.md](TESTING.md#troubleshooting) for common problems

---

**Built with ❤️ using:**
- Claude 3.5 Haiku by Anthropic
- LangGraph by LangChain
- Streamlit for rapid UI development
- MongoDB for flexible data storage

**Timeline**: MVP built in ~5 hours
**Status**: Functional, ready for Phase 1 enhancements
**Next Steps**: Deploy to Streamlit Cloud, add smart reminders, analytics charts

---

*Last Updated: 2025-10-05*
