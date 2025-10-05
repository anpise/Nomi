import streamlit as st
import logging
from auth import verify_login, create_user, init_users_file
from claude_handler import generate_login_greeting
from agents import nomi_workflow
from db import save_message, get_messages, get_unified_entries, get_entries_by_use_case, update_last_login, is_first_login_today, get_recent_conversation, save_unified_entry
from datetime import datetime, date
from styles import CUSTOM_CSS, get_hero_section, get_user_profile, get_quick_actions, get_workout_card, get_note_card

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Page config
st.set_page_config(
    page_title="Nomi - Personal Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS from styles module
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

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
    """Process user message using LangGraph agentic workflow"""
    logger.info(f"Processing message for user: {username}")

    # Get recent conversation history for context (last 10 messages or 24 hours)
    conversation_history = get_recent_conversation(username, max_messages=10, hours=24)
    logger.info(f"Retrieved {len(conversation_history)} messages from conversation history")

    # Prepare initial state for LangGraph workflow
    initial_state = {
        "username": username,
        "message": user_message,
        "conversation_history": conversation_history,
        "use_case": "",
        "response": "",
        "metadata": {},
        "next_agent": ""
    }

    # Invoke LangGraph workflow
    logger.info("Invoking LangGraph workflow")
    final_state = nomi_workflow.invoke(initial_state)
    logger.info(f"Workflow completed - routed to {final_state['use_case']} agent")

    # Extract results
    response = final_state["response"]
    metadata = final_state["metadata"]
    use_case = final_state["use_case"]

    # Save unified entry to database
    entry = {
        "username": username,
        "message": user_message,
        "response": response,
        "use_case": use_case,
        "metadata": metadata,
        "timestamp": datetime.now()
    }
    save_unified_entry(entry)
    logger.info(f"Saved unified entry to database")

    return response

# Login/Signup Page
if not st.session_state.logged_in:
    # Hero section with gradient
    st.markdown("""
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem; color: #CC785C;'>🤖 Nomi</h1>
        <p style='font-size: 1.5rem; color: #E89B7B; font-weight: 500; margin-bottom: 0.5rem;'>Your Personal Assistant</p>
        <p style='font-size: 1rem; color: #B8694F;'>Talk. Track. Transform.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)

        # Toggle between Login and Signup
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            with st.form("login_form"):
                st.markdown("<br>", unsafe_allow_html=True)
                username = st.text_input("Username", key="login_username", placeholder="Enter your username")
                password = st.text_input("Password", type="password", key="login_password", placeholder="Enter your password")
                st.markdown("<br>", unsafe_allow_html=True)
                submit = st.form_submit_button("Login", use_container_width=True)

                if submit:
                    if not username or not password:
                        st.error("Please enter both username and password")
                    elif verify_login(username, password):
                        # Check if first login today before updating
                        first_login_today = is_first_login_today(username)

                        # Update last login timestamp
                        update_last_login(username)

                        # Set session state
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.greeting_shown = not first_login_today  # Only show greeting if first login today

                        st.rerun()
                    else:
                        st.error("Invalid username or password")

        with tab2:
            with st.form("signup_form"):
                st.markdown("<br>", unsafe_allow_html=True)
                new_username = st.text_input("Choose Username", key="signup_username", placeholder="Create a username")
                new_password = st.text_input("Choose Password", type="password", key="signup_password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm Password", type="password", key="signup_confirm", placeholder="Re-enter password")
                st.markdown("<br>", unsafe_allow_html=True)
                signup = st.form_submit_button("Create Account", use_container_width=True)

                if signup:
                    if not new_username or not new_password:
                        st.error("Please fill all fields")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif new_password != confirm_password:
                        st.error("Passwords don't match")
                    elif create_user(new_username, new_password):
                        st.success("✓ Account created! Please login.")
                    else:
                        st.error("Username already exists")

# Main App - Chat Interface
else:
    # Sidebar
    with st.sidebar:
        # User profile section
        st.markdown(f"""
        <div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
            <div style='width: 60px; height: 60px; background: linear-gradient(135deg, #CC785C, #E89B7B);
                        border-radius: 50%; margin: 0 auto 0.75rem auto; display: flex;
                        align-items: center; justify-content: center; font-size: 1.8rem;'>
                👤
            </div>
            <p style='font-size: 1.1rem; font-weight: 600; margin: 0; color: #000000;'>{st.session_state.username}</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Logout", type="secondary", use_container_width=True):
            logout()
            st.rerun()

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # Navigation - radio buttons styled as cards
        st.markdown("<h3 style='color: #CC785C;'>💬 Chat with Nomi</h3>", unsafe_allow_html=True)

        st.markdown("<div style='margin: 1rem 0;'></div>", unsafe_allow_html=True)

        st.markdown("<p style='color: #000000; font-size: 0.85rem; font-weight: 500;'>Views</p>", unsafe_allow_html=True)
        tab = st.pills("Navigate", ["💬 Chat", "🏋️ Workouts", "📝 Notes", "📊 Summary"], label_visibility="collapsed", selection_mode="single", default="💬 Chat")

        st.markdown("<div style='margin: 1.5rem 0;'></div>", unsafe_allow_html=True)

        # Quick Commands section
        st.markdown("<h3 style='color: #CC785C;'>💡 Quick Actions</h3>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size: 0.8rem; color: #000000; line-height: 1.8;'>
        <p style='margin: 0.5rem 0; color: #000000;'>💪 Log workout</p>
        <p style='margin: 0.5rem 0; color: #000000;'>📝 Take note</p>
        <p style='margin: 0.5rem 0; color: #000000;'>📊 Daily summary</p>
        <p style='margin: 0.5rem 0; color: #000000;'>☀️ Morning motivation</p>
        </div>
        """, unsafe_allow_html=True)

    # Main content area
    if tab == "💬 Chat":
        # Move title to sidebar instead of main area
        pass

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

            with st.spinner("✨ Preparing your greeting..."):
                greeting = generate_login_greeting(st.session_state.username, day_of_week, hints)

            st.session_state.messages.append({"role": "assistant", "content": greeting})
            save_message(st.session_state.username, "assistant", greeting)
            st.session_state.greeting_shown = True

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Quick action hints above chat input - smaller, more subtle
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 0.85rem; color: #888; margin-bottom: 0.5rem;'>💡 Quick Actions</p>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("<p class='hint-text'>💪 Did 30 pushups</p>", unsafe_allow_html=True)
        with col2:
            st.markdown("<p class='hint-text'>📝 Meeting with team</p>", unsafe_allow_html=True)
        with col3:
            st.markdown("<p class='hint-text'>📊 What did I do today?</p>", unsafe_allow_html=True)

        # Chat input - keep light for visibility

        if prompt := st.chat_input("Type your message..."):
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            save_message(st.session_state.username, "user", prompt)

            with st.chat_message("user"):
                st.markdown(prompt)

            # Get response from agents with custom spinner
            with st.spinner("🤔 Nomi is thinking..."):
                response = handle_message(prompt, st.session_state.username)

            st.session_state.messages.append({"role": "assistant", "content": response})
            save_message(st.session_state.username, "assistant", response)

            with st.chat_message("assistant"):
                st.markdown(response)

            st.rerun()

    elif tab == "🏋️ Workouts":
        pass

        # Get health/fitness entries
        entries = get_entries_by_use_case(st.session_state.username, "health_fitness")

        if entries:
            for entry in entries:
                metadata = entry.get('metadata', {})
                activity = metadata.get('activity', 'workout')
                duration = metadata.get('duration', '')
                intensity = metadata.get('intensity', '')
                details = metadata.get('details', '')
                timestamp = entry['timestamp'].strftime('%b %d, %I:%M %p')

                # Complete card in one HTML block
                card_html = f"""
                <div style='background-color: #FAF8F5; padding: 1.5rem; border-radius: 12px;
                            margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                            border-left: 4px solid #CC785C;'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div style='flex: 1;'>
                            <p style='color: #000000; font-size: 1rem; font-weight: 600; margin: 0 0 0.5rem 0;'>💪 {activity.title()}</p>
                            {f"<p style='color: #666; font-size: 0.9rem; margin: 0.25rem 0;'>⏱️ {duration}</p>" if duration else ""}
                            {f"<p style='color: #888; font-size: 0.85rem; margin: 0.25rem 0;'>{details}</p>" if details else ""}
                        </div>
                        <div style='text-align: right; margin-left: 1rem;'>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>{timestamp}</p>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("💡 No workouts logged yet. Start by saying 'Did 30 pushups' in chat!")

    elif tab == "📝 Notes":
        pass

        # Get notes/reminders entries
        entries = get_entries_by_use_case(st.session_state.username, "notes_reminders")

        if entries:
            for entry in entries:
                metadata = entry.get('metadata', {})
                summary = metadata.get('summary', entry.get('message', ''))
                full_message = entry.get('message', '')
                timestamp = entry['timestamp'].strftime('%b %d, %I:%M %p')

                # Complete card in one HTML block
                card_html = f"""
                <div style='background-color: #FAF8F5; padding: 1.5rem; border-radius: 12px;
                            margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                            border-left: 4px solid #E89B7B;'>
                    <div style='display: flex; justify-content: space-between; align-items: start;'>
                        <div style='flex: 1;'>
                            <p style='color: #000000; font-size: 1rem; font-weight: 600; margin: 0 0 0.5rem 0;'>📝 {summary}</p>
                            {f"<p style='color: #666; font-size: 0.9rem; margin: 0.25rem 0;'>{full_message}</p>" if full_message and full_message != summary else ""}
                        </div>
                        <div style='text-align: right; margin-left: 1rem;'>
                            <p style='color: #999; font-size: 0.8rem; margin: 0;'>{timestamp}</p>
                        </div>
                    </div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.info("💡 No notes logged yet. Start by saying 'Note: meeting with team' in chat!")

    elif tab == "📊 Summary":
        pass

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
                st.markdown("""
                <div style='background-color: #FFF4EF; padding: 1.5rem; border-radius: 12px; text-align: center;'>
                    <p style='font-size: 2rem; margin: 0; color: #CC785C;'>{}</p>
                    <p style='font-size: 0.9rem; color: #666; margin: 0;'>Total Entries</p>
                </div>
                """.format(len(entries)), unsafe_allow_html=True)
            with col2:
                st.markdown("""
                <div style='background-color: #F0F9FF; padding: 1.5rem; border-radius: 12px; text-align: center;'>
                    <p style='font-size: 2rem; margin: 0; color: #0284C7;'>💪 {}</p>
                    <p style='font-size: 0.9rem; color: #666; margin: 0;'>Workouts</p>
                </div>
                """.format(len(health_entries)), unsafe_allow_html=True)
            with col3:
                st.markdown("""
                <div style='background-color: #FEF3C7; padding: 1.5rem; border-radius: 12px; text-align: center;'>
                    <p style='font-size: 2rem; margin: 0; color: #D97706;'>📝 {}</p>
                    <p style='font-size: 0.9rem; color: #666; margin: 0;'>Notes</p>
                </div>
                """.format(len(note_entries)), unsafe_allow_html=True)

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
