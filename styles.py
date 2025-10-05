"""
Nomi UI Styles - CSS and HTML components
"""

# CSS Styles
CUSTOM_CSS = """
<style>
    /* Main color scheme inspired by Claude - Override Streamlit defaults */
    :root {
        --primary-color: #CC785C;
        --secondary-color: #E89B7B;
        --background-color: #F5F1ED;
        --text-color: #000000;
        --card-background: #FAF8F5;
        --card-hover: #F0EBE6;
        --border-color: #E0DBD6;
        --accent-peach: #FFF4EF;
    }

    /* Override Streamlit's default blue theme */
    .main {
        background-color: var(--background-color);
    }

    /* Remove all blue accents from Streamlit defaults */
    [data-testid="stAppViewContainer"] {
        background-color: var(--background-color);
    }

    [data-testid="stHeader"] {
        background-color: transparent;
    }

    /* Override radio button blue color */
    input[type="radio"]:checked {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
    }

    /* Override all blue links */
    a, a:visited, a:hover, a:active {
        color: var(--primary-color) !important;
    }

    /* Override streamlit default focus colors */
    *:focus, *:focus-visible {
        outline-color: var(--primary-color) !important;
    }

    /* Overall app background */
    .stApp {
        background-color: var(--background-color);
    }

    /* Chat message styling - remove bubbles, just show messages */
    .stChatMessage {
        background-color: transparent;
        border-radius: 0;
        padding: 0.75rem 0;
        margin-bottom: 0.5rem;
        box-shadow: none;
        border: none;
    }

    /* User message - no background, just icon and text */
    [data-testid="stChatMessageContent"] {
        font-size: 0.95rem;
        line-height: 1.6;
        color: var(--text-color);
    }

    div[data-testid="stChatMessage"] {
        background-color: transparent;
        border: none;
    }

    /* Remove all message backgrounds */
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageContentUser"]),
    div[data-testid="stChatMessage"]:has([data-testid="stChatMessageContentAssistant"]) {
        background-color: transparent;
        border: none;
    }

    /* Ensure text is readable in all messages */
    .stChatMessage p {
        color: #000000 !important;
        margin: 0;
    }

    /* Chat message text */
    [data-testid="stMarkdownContainer"] p {
        color: #000000 !important;
    }

    /* All text elements to black - override everything */
    *, p, span, div, label, h1, h2, h3, h4, h5, h6 {
        color: #000000 !important;
    }

    /* Sidebar text - force black */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label {
        color: #000000 !important;
    }

    /* Main content area - force all text black */
    .main p, .main span, .main div {
        color: #000000 !important;
    }

    /* Expander content */
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span {
        color: #000000 !important;
    }

    /* Headings keep peach color */
    h1, h2, h3, h4 {
        color: #CC785C !important;
    }

    /* Avatar icons styling */
    [data-testid="stChatMessageAvatarUser"],
    [data-testid="stChatMessageAvatarAssistant"] {
        background-color: var(--primary-color);
        border-radius: 50%;
    }

    /* Buttons */
    .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.2s ease;
        font-size: 1rem;
    }

    .stButton > button:hover {
        background-color: #B8694F;
        box-shadow: 0 4px 12px rgba(204, 120, 92, 0.4);
        transform: translateY(-2px);
    }

    /* Form submit buttons - full width, larger */
    button[kind="formSubmit"] {
        background-color: #1F1F1F !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 0.85rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        margin-top: 0.5rem !important;
    }

    button[kind="formSubmit"]:hover {
        background-color: #2F2F2F !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    /* Input fields */
    .stTextInput > div > div > input,
    .stChatInput > div > div > input {
        border-radius: 8px;
        border: 1px solid var(--border-color);
        padding: 0.85rem 1rem;
        background-color: var(--card-background);
        font-size: 0.95rem;
        transition: all 0.2s ease;
        color: var(--text-color);
    }

    .stTextInput > div > div > input:focus,
    .stChatInput > div > div > input:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(204, 120, 92, 0.15);
        outline: none;
    }

    /* Input placeholder styling */
    .stTextInput > div > div > input::placeholder,
    .stChatInput > div > div > input::placeholder {
        color: #B8694F;
        font-size: 0.9rem;
    }

    /* Chat input at bottom - dark theme */
    .stChatInput {
        border-top: 1px solid var(--border-color);
        padding-top: 1rem;
        background-color: transparent;
    }

    /* Send button in chat input */
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        background-color: var(--primary-color) !important;
        color: white !important;
        border: none !important;
    }

    button[kind="primary"]:hover,
    button[data-testid="baseButton-primary"]:hover {
        background-color: #B8694F !important;
    }

    /* Override all Streamlit primary button colors */
    .stButton > button[kind="primary"],
    [data-testid="stBaseButton-primary"] {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--card-background);
        border-right: 1px solid var(--border-color);
    }

    /* Sidebar logout button */
    [data-testid="stSidebar"] .stButton > button {
        background-color: var(--primary-color);
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1rem;
        font-weight: 500;
        font-size: 0.9rem;
    }

    /* Radio buttons in sidebar - card style */
    [data-testid="stSidebar"] .stRadio > div {
        gap: 0.5rem;
    }

    [data-testid="stSidebar"] .stRadio > div > label {
        background-color: var(--background-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        cursor: pointer;
        transition: all 0.2s ease;
        color: #000000 !important;
        display: flex !important;
        align-items: center !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label:hover {
        border-color: var(--primary-color) !important;
        background-color: var(--card-hover) !important;
    }

    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
        color: white !important;
        font-weight: 500;
    }

    /* Hide radio button circles - remove blue dot */
    [data-testid="stSidebar"] .stRadio input[type="radio"] {
        display: none !important;
        opacity: 0 !important;
    }

    /* Radio button circle replacement */
    [data-testid="stSidebar"] .stRadio input[type="radio"] + div {
        display: none !important;
    }

    /* Radio button text - force black when not selected */
    [data-testid="stSidebar"] .stRadio > div > label > div,
    [data-testid="stSidebar"] .stRadio > div > label > div > p,
    [data-testid="stSidebar"] .stRadio > div > label span,
    [data-testid="stSidebar"] .stRadio > div > label p {
        color: #000000 !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
    }

    /* Radio button text - white when selected */
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] > div,
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] > div > p,
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] span,
    [data-testid="stSidebar"] .stRadio > div > label[data-checked="true"] p {
        color: white !important;
    }

    /* Remove blue from radio selection indicator */
    [data-testid="stSidebar"] .stRadio [role="radiogroup"] div[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }

    /* Force visibility of radio label text */
    [data-testid="stSidebar"] .stRadio label div[data-testid="stMarkdownContainer"] {
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* Pills component styling for navigation */
    [data-testid="stSidebar"] .stPills {
        gap: 0.5rem;
    }

    [data-testid="stSidebar"] .stPills button {
        background-color: var(--background-color) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        color: #000000 !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        transition: all 0.2s ease;
        width: 100%;
        text-align: left;
    }

    [data-testid="stSidebar"] .stPills button:hover {
        border-color: var(--primary-color) !important;
        background-color: var(--card-hover) !important;
    }

    [data-testid="stSidebar"] .stPills button[aria-selected="true"],
    [data-testid="stSidebar"] .stPills button[data-selected="true"] {
        background-color: var(--primary-color) !important;
        border-color: var(--primary-color) !important;
        color: white !important;
        font-weight: 500 !important;
    }

    /* Hints - smaller font */
    .hint-text {
        font-size: 0.75rem;
        color: #666;
        background-color: var(--card-background);
        padding: 0.4rem 0.6rem;
        border-radius: 6px;
        border: 1px solid var(--border-color);
        font-family: 'Monaco', 'Menlo', monospace;
    }

    /* Cards */
    .element-container {
        transition: all 0.2s ease;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        background-color: var(--card-background);
        border-radius: 8px;
        padding: 0.5rem 1rem;
        border: 1px solid var(--border-color);
    }

    .stTabs [aria-selected="true"] {
        background-color: var(--primary-color);
        color: white;
    }

    /* Dividers */
    hr {
        margin: 1rem 0;
        border-color: var(--border-color);
    }

    /* Title styling */
    h1 {
        color: var(--primary-color);
        font-weight: 600;
    }

    h2, h3 {
        color: var(--primary-color);
        font-weight: 500;
    }

    /* Subtitle styling */
    .stMarkdown h3 {
        color: var(--secondary-color);
    }

    /* Spinner - custom loader */
    .stSpinner > div {
        border-color: var(--primary-color) transparent transparent transparent;
    }

    /* Success/Error messages */
    .stSuccess {
        background-color: #E8F5E9;
        border-left: 3px solid #4CAF50;
        border-radius: 8px;
    }

    .stError {
        background-color: #FFEBEE;
        border-left: 3px solid #F44336;
        border-radius: 8px;
    }

    /* Info messages */
    .stInfo {
        background-color: var(--accent-peach);
        border-left: 3px solid var(--primary-color);
        border-radius: 8px;
    }

    /* Code blocks for hints */
    code {
        background-color: var(--card-background);
        padding: 0.2rem 0.4rem;
        border-radius: 4px;
        font-size: 0.85rem;
        color: #666;
    }
</style>
"""

# HTML Components
def get_hero_section():
    """Login page hero section"""
    return """
    <div style='text-align: center; padding: 2rem 0;'>
        <h1 style='font-size: 3rem; margin-bottom: 0.5rem; color: #CC785C;'>🤖 Nomi</h1>
        <p style='font-size: 1.5rem; color: #E89B7B; font-weight: 500; margin-bottom: 0.5rem;'>Your Personal Assistant</p>
        <p style='font-size: 1rem; color: #B8694F;'>Talk. Track. Transform.</p>
    </div>
    """

def get_user_profile(username):
    """Sidebar user profile section"""
    return f"""
    <div style='text-align: center; padding: 1.5rem 0 1rem 0;'>
        <div style='width: 60px; height: 60px; background: linear-gradient(135deg, #CC785C, #E89B7B);
                    border-radius: 50%; margin: 0 auto 0.75rem auto; display: flex;
                    align-items: center; justify-content: center; font-size: 1.8rem;'>
            👤
        </div>
        <p style='font-size: 1.1rem; font-weight: 600; margin: 0; color: #000000;'>{username}</p>
    </div>
    """

def get_quick_actions():
    """Sidebar quick actions section"""
    return """
    <div style='font-size: 0.8rem; color: #000000; line-height: 1.8;'>
    <p style='margin: 0.5rem 0; color: #000000;'>💪 Log workout</p>
    <p style='margin: 0.5rem 0; color: #000000;'>📝 Take note</p>
    <p style='margin: 0.5rem 0; color: #000000;'>📊 Daily summary</p>
    <p style='margin: 0.5rem 0; color: #000000;'>☀️ Morning motivation</p>
    </div>
    """

def get_workout_card(activity, duration, details, timestamp):
    """Workout card HTML"""
    duration_html = f"<p style='color: #666; font-size: 0.9rem; margin: 0.25rem 0;'>⏱️ {duration}</p>" if duration else ""
    details_html = f"<p style='color: #888; font-size: 0.85rem; margin: 0.25rem 0;'>{details}</p>" if details else ""

    return f"""
    <div style='background-color: #FAF8F5; padding: 1.5rem; border-radius: 12px;
                margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                border-left: 4px solid #CC785C;'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div style='flex: 1;'>
                <p style='color: #000000; font-size: 1rem; font-weight: 600; margin: 0 0 0.5rem 0;'>💪 {activity.title()}</p>
                {duration_html}
                {details_html}
            </div>
            <div style='text-align: right; margin-left: 1rem;'>
                <p style='color: #999; font-size: 0.8rem; margin: 0;'>{timestamp}</p>
            </div>
        </div>
    </div>
    """

def get_note_card(summary, full_message, timestamp):
    """Note card HTML"""
    message_html = f"<p style='color: #666; font-size: 0.9rem; margin: 0.25rem 0;'>{full_message}</p>" if full_message and full_message != summary else ""

    return f"""
    <div style='background-color: #FAF8F5; padding: 1.5rem; border-radius: 12px;
                margin-bottom: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
                border-left: 4px solid #E89B7B;'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div style='flex: 1;'>
                <p style='color: #000000; font-size: 1rem; font-weight: 600; margin: 0 0 0.5rem 0;'>📝 {summary}</p>
                {message_html}
            </div>
            <div style='text-align: right; margin-left: 1rem;'>
                <p style='color: #999; font-size: 0.8rem; margin: 0;'>{timestamp}</p>
            </div>
        </div>
    </div>
    """
