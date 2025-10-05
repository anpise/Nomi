import streamlit as st
from auth import verify_login, create_user, init_users_file
from claude_handler import generate_login_greeting
from orchestrator import route_message, save_unified_entry
from db import save_message, get_messages, get_unified_entries, get_entries_by_use_case
from datetime import datetime, date

# Page config
st.set_page_config(
    page_title="Nomi - Personal Assistant",
    page_icon="🤖",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'greeting_shown' not in st.session_state:
    st.session_state.greeting_shown = False

# Initialize users file
init_users_file()

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.messages = []
    st.session_state.greeting_shown = False

def handle_message(user_message, username):
    """Process user message using the orchestrator"""
    # Route message to appropriate handler
    response, metadata, use_case = route_message(user_message, username)

    # Save unified entry
    save_unified_entry(username, user_message, response, use_case, metadata)

    return response

# Login Page
if not st.session_state.logged_in:
    st.title("🤖 Nomi - Your Personal Assistant")
    st.markdown("### Talk. Track. Transform.")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("---")
        st.markdown("### Login")

        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)

            if submit:
                if not username or not password:
                    st.error("Please enter both username and password")
                elif verify_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("Invalid username or password")

        st.markdown("---")
        st.caption("Contact admin to create an account")

# Main App - Chat Interface
else:
    # Sidebar
    with st.sidebar:
        st.title(f"👤 {st.session_state.username}")

        if st.button("Logout", type="secondary"):
            logout()
            st.rerun()

        st.markdown("---")

        st.markdown("### 📋 Commands")
        st.markdown("""
        - `/workout` - Log workout
        - `/note` - Log note
        - `/summary` - Daily summary
        - `/morning` - Morning motivation
        """)

        st.markdown("---")

        # Navigation tabs
        tab = st.radio("Navigate", ["💬 Chat", "🏋️ Workouts", "📝 Notes", "📊 Summary"])

    # Main content area
    if tab == "💬 Chat":
        st.title("💬 Chat with Nomi")

        # Load chat history from DB on first load
        if not st.session_state.messages:
            db_messages = get_messages(st.session_state.username)
            for msg in db_messages:
                st.session_state.messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })

        # Show greeting on first login
        if not st.session_state.greeting_shown:
            day_of_week = datetime.now().strftime("%A")
            hints = [
                "Check today's summary",
                "Log a workout or note",
                "Ask for morning motivation"
            ]

            with st.spinner("Generating greeting..."):
                greeting = generate_login_greeting(st.session_state.username, day_of_week, hints)

            st.session_state.messages.append({"role": "assistant", "content": greeting})
            save_message(st.session_state.username, "assistant", greeting)
            st.session_state.greeting_shown = True

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Quick action hints above chat input
        st.markdown("---")
        st.markdown("**💡 Quick Actions:**")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.code("Log a workout: Did 30 pushups", language=None)
        with col2:
            st.code("Take a note: Meeting with team", language=None)
        with col3:
            st.code("Get summary: What did I do today?", language=None)

        # Chat input
        if prompt := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            save_message(st.session_state.username, "user", prompt)

            with st.chat_message("user"):
                st.markdown(prompt)

            # Get response from Claude
            with st.spinner("Thinking..."):
                response = handle_message(prompt, st.session_state.username)

            st.session_state.messages.append({"role": "assistant", "content": response})
            save_message(st.session_state.username, "assistant", response)

            with st.chat_message("assistant"):
                st.markdown(response)

            st.rerun()

    elif tab == "🏋️ Workouts":
        st.title("🏋️ Your Workouts")

        # Get health/fitness entries
        entries = get_entries_by_use_case(st.session_state.username, "health_fitness")

        if entries:
            for entry in entries:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        metadata = entry.get('metadata', {})
                        activity = metadata.get('activity', 'workout')
                        duration = metadata.get('duration', '')
                        intensity = metadata.get('intensity', '')

                        st.markdown(f"**{activity}** - {duration}")
                        if intensity:
                            st.caption(f"Intensity: {intensity}")
                        if metadata.get('details'):
                            st.caption(metadata['details'])
                    with col2:
                        st.caption(entry['timestamp'].strftime("%b %d, %I:%M %p"))
                    st.divider()
        else:
            st.info("No workouts logged yet. Start by saying 'Did 30 pushups' in chat!")

    elif tab == "📝 Notes":
        st.title("📝 Your Notes")

        # Get notes/reminders entries
        entries = get_entries_by_use_case(st.session_state.username, "notes_reminders")

        if entries:
            for entry in entries:
                with st.container():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        metadata = entry.get('metadata', {})
                        summary = metadata.get('summary', entry.get('message', ''))
                        category = metadata.get('category', '')
                        priority = metadata.get('priority', '')

                        st.markdown(f"**{summary}**")
                        if category:
                            st.caption(f"Category: {category} | Priority: {priority}")
                        with st.expander("View full note"):
                            st.write(entry.get('message', ''))
                    with col2:
                        st.caption(entry['timestamp'].strftime("%b %d, %I:%M %p"))
                    st.divider()
        else:
            st.info("No notes logged yet. Start by saying 'Note: meeting with team' in chat!")

    elif tab == "📊 Summary":
        st.title("📊 Daily Summary")

        # Get all entries for today
        today = date.today()
        entries = get_unified_entries(st.session_state.username, start_date=today, end_date=today)

        if entries:
            # Categorize entries
            health_entries = [e for e in entries if e.get("use_case") == "health_fitness"]
            note_entries = [e for e in entries if e.get("use_case") == "notes_reminders"]
            summary_entries = [e for e in entries if e.get("use_case") == "summary_analytics"]

            st.markdown("### Today's Activity")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Entries", len(entries))
            with col2:
                st.metric("Workouts", len(health_entries))
            with col3:
                st.metric("Notes", len(note_entries))

            st.markdown("---")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### 🏋️ Workouts")
                if health_entries:
                    for e in health_entries:
                        metadata = e.get('metadata', {})
                        st.write(f"- {metadata.get('activity', 'workout')} ({metadata.get('duration', '')})")
                else:
                    st.caption("No workouts today")

            with col2:
                st.markdown("#### 📝 Notes")
                if note_entries:
                    for e in note_entries:
                        metadata = e.get('metadata', {})
                        st.write(f"- {metadata.get('summary', e.get('message', ''))}")
                else:
                    st.caption("No notes today")

            # Show latest summary if any
            if summary_entries:
                st.markdown("---")
                st.markdown("### Latest Summary")
                st.info(summary_entries[0].get('response', ''))
        else:
            st.info("Nothing logged yet today. Start chatting with Nomi to track your day!")
