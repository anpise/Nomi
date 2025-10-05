# Nomi Testing Guide

Comprehensive testing scenarios for the LangGraph agentic architecture.

---

## Prerequisites

1. **Start MongoDB**: `mongod` (ensure MongoDB is running locally)
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set API key**: Add `ANTHROPIC_API_KEY` to `.env` file
4. **Run app**: `streamlit run app.py`

---

## Test Scenarios

### 1. Authentication Tests

#### 1.1 New User Signup
- **Action**: Click "Signup" tab
- **Input**:
  - Username: `testuser1`
  - Password: `password123`
- **Expected**: Success message, auto-login, greeting shown

#### 1.2 Login with Existing User
- **Action**: Login with created credentials
- **Expected**:
  - Login successful
  - If first login of day: Greeting shown (time-appropriate: morning/afternoon/evening)
  - If not first login: No greeting, previous messages loaded

#### 1.3 Login Greeting Time-Awareness
- **Test at different times**:
  - Before 12 PM: Should say "morning"
  - 12 PM - 5 PM: Should say "afternoon"
  - After 5 PM: Should say "evening"
- **Expected**: Max 1-2 sentences, appropriate time greeting

---

### 2. Health/Fitness Agent Tests

#### 2.1 Simple Workout Log
- **Input**: `Did 30 pushups`
- **Expected**:
  - Supervisor routes to `health_fitness` agent
  - Response: Max 8-10 words (e.g., "Nice! 30 pushups crushed ✓")
  - Saved to DB with:
    - `use_case: health_fitness`
    - `metadata.activity: "pushups"`
    - `metadata.duration: "30 reps"`

#### 2.2 Complex Workout with Duration
- **Input**: `Ran 5k in 25 minutes this morning`
- **Expected**:
  - Response: Brief acknowledgment (8-10 words)
  - Metadata captures: activity="running", duration="5k, 25 min"

#### 2.3 Multiple Activities
- **Input**: `Did yoga for 20 mins then lifted weights`
- **Expected**:
  - Response: Short encouragement
  - Metadata captures both activities

#### 2.4 Workout with Context from History
- **Setup**: Log a workout, then log similar one later
- **Input 1**: `Did 20 pushups`
- **Input 2** (later): `Did 25 pushups today`
- **Expected**: Response acknowledges previous context if in last 24hrs

---

### 3. Notes/Reminders Agent Tests

#### 3.1 Simple Note
- **Input**: `Note: Buy groceries tomorrow`
- **Expected**:
  - Supervisor routes to `notes_reminders` agent
  - Response: Max 5-6 words (e.g., "Got it ✓" or "Saved ✓")
  - Metadata:
    - `summary: "Buy groceries tomorrow"`
    - `full_content: original message`

#### 3.2 Task Completion
- **Input**: `Finished the quarterly report`
- **Expected**:
  - Response: Brief acknowledgment
  - Summary captures key action

#### 3.3 Meeting Note
- **Input**: `Had a great meeting with the design team about new features`
- **Expected**:
  - Response: 5-6 words max
  - Summary: ~5-7 words capturing essence

#### 3.4 Reminder
- **Input**: `Remind me to call Sarah at 3pm`
- **Expected**:
  - Classified as note/reminder
  - Brief confirmation

---

### 4. Summary/Analytics Agent Tests

#### 4.1 Daily Summary (with data)
- **Setup**: Log 2 workouts and 3 notes during the day
- **Input**: `What did I do today?` or `Summary` or `Give me today's recap`
- **Expected**:
  - Supervisor routes to `summary_analytics` agent
  - Response: Max 2-3 short sentences
  - Mentions workout count and notes count
  - Ends with ✓
  - Metadata: `period: "daily"`, counts included

#### 4.2 Daily Summary (no data)
- **Setup**: Fresh day, nothing logged
- **Input**: `What did I do today?`
- **Expected**: "Nothing logged yet." or similar

#### 4.3 Weekly Summary
- **Setup**: Log activities over several days
- **Input**: `What did I do this week?` or `Weekly summary` or `Past week recap`
- **Expected**:
  - Response: Max 3-4 short sentences
  - Shows 7-day aggregate (workout count, notes count)
  - Brief celebration
  - Metadata: `period: "weekly"`

#### 4.4 Insights Request
- **Input**: `Show me insights` or `What are my patterns?` or `Analyze my progress`
- **Expected**:
  - Response: 2-3 short sentences
  - ONE key pattern identified
  - Brief actionable tip
  - Metadata: `period: "insights"`

---

### 5. Motivation/Wellbeing Agent Tests

#### 5.1 Morning Motivation
- **Input**: `Good morning` or `Morning` or `Start my day`
- **Expected**:
  - Supervisor routes to `motivation_wellbeing` agent
  - Response: Max 8-10 words
  - Energetic, brief greeting
  - Ends with ✓ or 💪
  - Metadata: `type: "morning"`

#### 5.2 Encouragement Request
- **Input**: `I need motivation` or `Motivate me` or `Inspire me`
- **Expected**:
  - Response: Max 8-10 words
  - Direct, supportive
  - Metadata: `type: "encouragement"`

#### 5.3 Reflection Request
- **Input**: `How am I doing?` or `How do I feel?` or `Reflect on my week`
- **Expected**:
  - Response: Max 2-3 short sentences
  - ONE key observation
  - Brief encouragement
  - Metadata: `type: "reflection"`

#### 5.4 General Wellbeing
- **Input**: `I'm feeling stressed` or `Need some support`
- **Expected**:
  - Response: Max 8-10 words
  - Brief, empathetic
  - Metadata: `type: "encouragement"` or `type: "general_support"`

---

### 6. Conversation Memory Tests

#### 6.1 Context Retention (within 24 hours)
- **Setup**:
  1. Log: `Did 20 pushups`
  2. Wait 5 minutes
  3. Log: `Also ran 3k`
- **Expected**: Second response may acknowledge first workout if relevant

#### 6.2 Context from Multiple Messages
- **Setup**: Have conversation with 5-10 messages
- **Expected**: Agent has access to last 8 messages for context

#### 6.3 Context After 24 Hours
- **Setup**: Log message, wait 24+ hours
- **Expected**: Old messages not included in conversation history

#### 6.4 Max 10 Messages Limit
- **Setup**: Send 15 messages in quick succession
- **Expected**: Only last 10 messages used for context

---

### 7. Edge Cases & Ambiguity Tests

#### 7.1 Ambiguous Message
- **Input**: `Just finished` (unclear what)
- **Expected**: Defaults to `notes_reminders` agent

#### 7.2 Mixed Intent
- **Input**: `Did 30 pushups and need to remember to call John`
- **Expected**: Supervisor classifies as primary intent (likely health_fitness)

#### 7.3 Empty/Very Short Message
- **Input**: `ok`
- **Expected**: Classified as note, brief acknowledgment

#### 7.4 Long Message
- **Input**: Very long paragraph describing day
- **Expected**:
  - Proper classification
  - Response still brief despite long input

---

### 8. Response Brevity Tests

**CRITICAL**: All responses must be SHORT per requirements

#### 8.1 Health Responses
- **Max**: 8-10 words
- **Test**: Send 5 different workouts, verify all responses ≤10 words

#### 8.2 Notes Responses
- **Max**: 5-6 words
- **Test**: Send 5 different notes, verify all responses ≤6 words

#### 8.3 Summary Responses
- **Max**: 2-3 short sentences (daily), 3-4 sentences (weekly)
- **Test**: Request daily/weekly summaries, count sentences

#### 8.4 Motivation Responses
- **Max**: 8-10 words (morning/encouragement), 2-3 sentences (reflection)
- **Test**: Test all support types

---

### 9. Database Persistence Tests

#### 9.1 Unified Entries Collection
- **Action**: Send messages to all 4 agent types
- **Verify in MongoDB**:
  ```javascript
  use nomi_db
  db.entries.find({username: "testuser1"})
  ```
- **Expected**: All entries have:
  - `username`
  - `message`
  - `response`
  - `use_case` (health_fitness, notes_reminders, summary_analytics, motivation_wellbeing)
  - `metadata` (specific to agent type)
  - `timestamp`

#### 9.2 Message History
- **Action**: Send several messages
- **Verify**:
  ```javascript
  db.messages.find({username: "testuser1"}).sort({timestamp: -1})
  ```
- **Expected**: Both user and assistant messages saved

#### 9.3 Last Login Tracking
- **Action**: Login multiple times
- **Verify**:
  ```javascript
  db.users.findOne({username: "testuser1"})
  ```
- **Expected**: `last_login` timestamp updates

---

### 10. UI/Tabs Tests

#### 10.1 Chat Tab
- **Action**: Navigate to Chat tab
- **Expected**:
  - All message history shown
  - Input box available
  - Messages display user/assistant correctly

#### 10.2 Workouts Tab
- **Action**: Navigate to Workouts tab
- **Expected**:
  - Only `health_fitness` entries shown
  - Displays activity, duration, timestamp
  - Sorted by recent first

#### 10.3 Notes Tab
- **Action**: Navigate to Notes tab
- **Expected**:
  - Only `notes_reminders` entries shown
  - Shows summary and timestamp

#### 10.4 Summary Tab
- **Action**: Navigate to Summary tab
- **Expected**:
  - Quick stats (total workouts, notes)
  - Option to request daily/weekly summary

---

### 11. Multi-User Tests

#### 11.1 User Isolation
- **Setup**: Create 2 users (`user1`, `user2`)
- **Action**: Both log messages
- **Expected**: Each user only sees their own data

#### 11.2 Concurrent Sessions
- **Setup**: Open 2 browser windows
- **Action**: Login as different users in each
- **Expected**: No data leakage between sessions

---

### 12. LangGraph Workflow Tests

#### 12.1 Supervisor Routing Accuracy
- **Test**: Send 20 messages (5 per category)
- **Verify logs**: Check each routes to correct agent
- **Expected**: >90% accuracy

#### 12.2 Workflow State Flow
- **Action**: Send message and check logs
- **Expected log flow**:
  ```
  Supervisor: Classifying message
  Supervisor: Routed to 'health_fitness' agent
  Router: Next agent is 'health_fitness'
  HealthAgent: Processing workout
  HealthAgent: Generated response
  ```

#### 12.3 End-to-End Latency
- **Action**: Time from message submit to response
- **Expected**: <5 seconds for simple messages

---

## Testing Checklist

Use this checklist to verify all scenarios:

### Authentication
- [ ] New user signup works
- [ ] Existing user login works
- [ ] First login greeting shows (time-appropriate)
- [ ] Subsequent login no greeting
- [ ] Logout clears session

### Health/Fitness Agent
- [ ] Simple workout logged (8-10 words response)
- [ ] Complex workout parsed correctly
- [ ] Multiple activities captured
- [ ] Context from history acknowledged
- [ ] Metadata saved correctly

### Notes/Reminders Agent
- [ ] Simple note saved (5-6 words response)
- [ ] Task completion acknowledged
- [ ] Meeting notes summarized
- [ ] Reminder captured

### Summary/Analytics Agent
- [ ] Daily summary with data (2-3 sentences)
- [ ] Daily summary without data
- [ ] Weekly summary (3-4 sentences)
- [ ] Insights generated (2-3 sentences)
- [ ] Correct counts in metadata

### Motivation/Wellbeing Agent
- [ ] Morning motivation (8-10 words)
- [ ] Encouragement (8-10 words)
- [ ] Reflection (2-3 sentences)
- [ ] General wellbeing support

### Conversation Memory
- [ ] Context retained within 24 hours
- [ ] Max 10 messages used
- [ ] Old messages (>24hrs) excluded

### Response Brevity
- [ ] All health responses ≤10 words
- [ ] All notes responses ≤6 words
- [ ] All summaries within sentence limits
- [ ] All motivation responses within limits

### Database
- [ ] Unified entries saved correctly
- [ ] Message history saved
- [ ] Last login tracked
- [ ] User data isolated

### UI
- [ ] Chat tab shows all messages
- [ ] Workouts tab filters correctly
- [ ] Notes tab filters correctly
- [ ] Summary tab displays stats

### LangGraph
- [ ] Supervisor routes correctly
- [ ] Workflow completes successfully
- [ ] Logs show proper flow
- [ ] Response latency acceptable

---

## Sample Test Script

```python
# test_script.py - Run from Python console or script

test_messages = [
    # Health/Fitness
    "Did 30 pushups",
    "Ran 5k in 25 minutes",
    "Yoga for 20 mins",

    # Notes/Reminders
    "Note: Buy groceries tomorrow",
    "Finished the quarterly report",
    "Meeting with design team went well",

    # Summary/Analytics
    "What did I do today?",
    "Weekly summary",
    "Show me insights",

    # Motivation/Wellbeing
    "Good morning",
    "Motivate me",
    "How am I doing?",

    # Edge cases
    "Just finished",
    "ok",
    "Did pushups and need to call John"
]

# Send each message through UI and verify:
# 1. Correct agent routing (check logs)
# 2. Response brevity
# 3. Database entry created
# 4. Metadata correct
```

---

## MongoDB Verification Queries

```javascript
// Connect to DB
use nomi_db

// Check all entries for user
db.entries.find({username: "testuser1"}).pretty()

// Count entries by use_case
db.entries.aggregate([
  {$match: {username: "testuser1"}},
  {$group: {_id: "$use_case", count: {$sum: 1}}}
])

// Check recent conversation history
db.messages.find({username: "testuser1"})
  .sort({timestamp: -1})
  .limit(10)

// Verify user last_login
db.users.findOne({username: "testuser1"})

// Check today's entries only
db.entries.find({
  username: "testuser1",
  timestamp: {
    $gte: new Date(new Date().setHours(0,0,0,0))
  }
})
```

---

## Expected Logging Output

```
2025-10-05 14:23:45 - __main__ - INFO - Processing message for user: testuser1
2025-10-05 14:23:45 - __main__ - INFO - Retrieved 5 messages from conversation history
2025-10-05 14:23:45 - __main__ - INFO - Invoking LangGraph workflow
2025-10-05 14:23:45 - agents - INFO - Supervisor: Classifying message for user 'testuser1'
2025-10-05 14:23:46 - agents - INFO - Supervisor: Routed to 'health_fitness' agent
2025-10-05 14:23:46 - agents - INFO - Router: Next agent is 'health_fitness'
2025-10-05 14:23:46 - agents - INFO - HealthAgent: Processing workout for 'testuser1'
2025-10-05 14:23:47 - agents - INFO - HealthAgent: Generated response
2025-10-05 14:23:47 - __main__ - INFO - Workflow completed - routed to health_fitness agent
2025-10-05 14:23:47 - db - INFO - Saving unified entry for user 'testuser1' with use_case 'health_fitness'
2025-10-05 14:23:47 - __main__ - INFO - Saved unified entry to database
```

---

## Troubleshooting

### Issue: Responses too long
- **Check**: System prompts in [agents.py](agents.py) have "CRITICAL: Keep responses SHORT" instructions
- **Verify**: Word count in actual responses

### Issue: Wrong agent routing
- **Check**: Supervisor classification keywords in [agents.py](agents.py:14-66)
- **Add**: More keywords if specific terms aren't caught

### Issue: No conversation context
- **Check**: MongoDB messages collection has entries
- **Verify**: `get_recent_conversation()` returns data
- **Check**: Timestamps are within 24 hours

### Issue: Login greeting wrong time
- **Check**: `datetime.now().hour` returns correct hour
- **Verify**: Time logic in [claude_handler.py](claude_handler.py:166-175)

---

## Performance Benchmarks

- **Message processing**: <5s end-to-end
- **Supervisor classification**: <1s
- **Agent response generation**: <3s
- **Database save**: <500ms
- **UI update**: <1s

---

## Success Criteria

✅ All 12 test categories pass
✅ All responses meet brevity requirements
✅ Database entries correct and isolated
✅ Workflow routing >90% accurate
✅ No errors in logs during normal operation
✅ UI responsive and data displayed correctly
