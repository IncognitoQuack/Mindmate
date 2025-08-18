# main.py
import streamlit as st
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import requests
from typing import List, Dict, Optional
from dotenv import load_dotenv
import re

# --- Load Environment Variables ---
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="Mindmate AI Advisor",
    page_icon="🧠",
    layout="wide"
)

# --- Application Styling ---
st.markdown("""
<style>
    .stApp {
        background-color: #0E1117; 
        color: #FFFFFF;
    }
    .st-chat-message {
        background-color: #262730;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        color: #FFFFFF;
        border-left: 5px solid #6c5ce7;
    }
    .st-sidebar .st-emotion-cache-1jicfl2 {
        background-color: #1a1a1a;
    }
    .st-sidebar > div:first-child {
         background-color: #0E1117;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background-color: #6c5ce7;
        color: white;
        border: 1px solid #6c5ce7;
    }
    .stButton>button:hover {
        background-color: #5849c1;
        border: 1px solid #5849c1;
        color: white;
    }
    .st-chat-input {
        background-color: #0E1117;
    }
    .stAlert {
        border-radius: 8px;
    }
    /* Main Tabs Style */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 8px;
        border: 1px solid #262730;
        color: #FFFFFF;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6c5ce7;
        border: 1px solid #6c5ce7;
    }
    /* Custom containers for dashboard */
    .dashboard-card {
        background-color: #262730;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)


# --- System Configuration ---
class Config:
    DATA_DIR = "mental_health_kb"
    EMBEDDING_MODEL = 'paraphrase-multilingual-mpnet-base-v2'
    API_MODEL_CHAT = 'google/gemma-3-27b-it:free'
    API_MODEL_DASHBOARD = 'deepseek/deepseek-r1-0528:free'
    API_MODEL_CLASSIFY = 'google/gemma-2-9b-it:free'
    TOP_K = 4 
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'harm myself', 'want to die', 'end my life'
    ]

# --- Caching for Performance ---
@st.cache_resource
def load_embedding_model():
    return SentenceTransformer(Config.EMBEDDING_MODEL)

@st.cache_data
def load_knowledge_base():
    knowledge_base = []
    data_dir = Config.DATA_DIR
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        return [], None
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    if not json_files:
        return [], None
    for file_name in json_files:
        file_path = os.path.join(data_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    text = item.get('text', item.get('content', '')) if isinstance(item, dict) else str(item)
                    if text:
                        knowledge_base.append({"source": file_name, "text": text})
        except (json.JSONDecodeError, UnicodeDecodeError):
            pass
    if knowledge_base:
        model = load_embedding_model()
        all_texts = [doc['text'] for doc in knowledge_base]
        embeddings = model.encode(all_texts, convert_to_tensor=True, show_progress_bar=True)
        return knowledge_base, embeddings
    return [], None

# --- Core AI and API Functions ---
def call_ai_api(messages: List[Dict], model: str, api_key: Optional[str]) -> str:
    if not api_key:
        return "Error: API Key for this function is not set."
    headers = {
        "Authorization": f"Bearer {api_key}", "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Sanjit-Mathur/Mindmate", "X-Title": "Mindmate AI Advisor",
    }
    data = {"model": model, "messages": messages}
    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=180)
        response.raise_for_status()
        api_response = response.json()
        return api_response["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as http_err:
        return f"API Request Error: {http_err} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"API Connection Error: {e}"
    except (KeyError, IndexError):
        return "API Response Error: Received an unexpected or malformed response."

# --- Flagging System & Crisis Response ---
def get_severity_score(prompt: str) -> int:
    instruction = f"Triage bot: Analyze the user's message for mental health severity. Return ONLY a single integer from 1 to 10 (1=neutral, 10=crisis). Message: \"{prompt}\""
    messages = [{"role": "system", "content": instruction}]
    try:
        response = call_ai_api(messages, model=Config.API_MODEL_CLASSIFY, api_key=st.session_state.api_key)
        return int(re.search(r'\d+', response).group())
    except (ValueError, AttributeError):
        return 3

def get_crisis_response() -> str:
    return """
    It sounds like you are going through a very difficult time. Your safety is the most important thing, and there are people who want to support you right now.
    **Please reach out for immediate help. Here are some resources in India:**
    * **Vandrevala Foundation Helpline:** `9999666555` (24/7)
    * **KIRAN Mental Health Helpline:** `1800-599-0019`
    * **AASRA (Suicide Prevention):** `9820466726` (24/7)
    """

# --- Dynamic Prompt Improvement ---
def get_prompt_improvement_suggestion(history: List[Dict]) -> str:
    if len(history) < 4: return "" 
    conversation_summary = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-4:]])
    instruction = f"Meta-analyst AI: Based on the recent conversation, suggest ONE concise, actionable directive for the main AI to improve its next response (e.g., 'Focus on validation', 'Introduce a CBT technique'). Conversation:\n{conversation_summary}\nReturn ONLY the single directive."
    messages = [{"role": "system", "content": instruction}]
    return call_ai_api(messages, model=Config.API_MODEL_CLASSIFY, api_key=st.session_state.api_key)

# --- System Prompt ---
def get_system_prompt() -> str:
    base_prompt = """
    You are a compassionate and thoughtful companion. Your purpose is to provide a supportive, non-judgmental space. Your persona is warm, empathetic, and consistently human-like.
    **Core Directives:**
    1.  **Embody Empathy:** Always start by validating the user's feelings.
    2.  **Listen More, Advise Less:** Guide with gentle, open-ended questions.
    3.  **Introduce Concepts Naturally:** Frame ideas from your knowledge base as shared wisdom.
    4.  **Maintain a Safe Space:** If a user expresses thoughts of self-harm, become clear and direct, guiding them to professional help.
    5.  **Uphold Boundaries Gracefully:** Never claim to be a human or a licensed therapist.
    """
    if st.session_state.dynamic_directive:
        base_prompt += f"\n**Dynamic Directive for This Turn:** {st.session_state.dynamic_directive}"
    return base_prompt

# --- UI Rendering Functions ---
def render_dashboard_view():
    st.header("📊 Your Session Dashboard")
    st.markdown("An overview of your conversation, designed to provide gentle insights.")

    if 'dashboard' not in st.session_state or not st.session_state.dashboard:
        st.info("Your dashboard is ready to be generated. Once you've had a conversation, click the 'Generate Dashboard Insights' button in the sidebar.")
        return

    dashboard_data = st.session_state.dashboard
    
    # --- NEW: Sub-tabs for Dashboard ---
    dash_tab1, dash_tab2 = st.tabs(["✨ Overview", "📝 Session Journal"])

    with dash_tab1:
        col1, col2 = st.columns(2)
        with col1:
            with st.container():
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("Session Sentiment")
                st.success(f"**Overall Mood:** {dashboard_data.get('sentiment', 'N/A')}")
                st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            with st.container():
                st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
                st.subheader("Key Themes")
                themes = dashboard_data.get('themes', [])
                if themes:
                    for theme in themes:
                        st.markdown(f"- {theme}")
                else:
                    st.markdown("No specific themes identified yet.")
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
        st.subheader("Suggestions to Explore")
        recommendations = dashboard_data.get('recommendations', [])
        if recommendations:
            for i, rec in enumerate(recommendations):
                st.info(f"**Suggestion {i+1}:** {rec.get('suggestion')}")
                st.markdown(f"*{rec.get('reason')}*")
                if i < len(recommendations) - 1:
                    st.divider()
        else:
            st.markdown("No specific recommendations generated yet.")
        st.markdown('</div>', unsafe_allow_html=True)

    with dash_tab2:
        with st.container():
            st.markdown('<div class="dashboard-card">', unsafe_allow_html=True)
            st.subheader("Complete Journal")
            st.text_area(
                "Journal", 
                st.session_state.session_journal, 
                height=400, 
                key="journal_viewer_main", 
                disabled=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

def render_chat_view():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# --- Main Application ---
st.title("🧠 Mindmate")

# Initialize session state variables
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_journal" not in st.session_state:
    st.session_state.session_journal = "Journal started."
if "dynamic_directive" not in st.session_state:
    st.session_state.dynamic_directive = ""
if "severity_warning_shown" not in st.session_state:
    st.session_state.severity_warning_shown = False
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("OPENROUTER_API_KEY", "")
if "api_key_dashboard" not in st.session_state:
    st.session_state.api_key_dashboard = os.getenv("OPENROUTER_API_KEY_DASHBOARD", "")

# Load data once
model = load_embedding_model()
kb_docs, kb_embeddings = load_knowledge_base()

# --- Sidebar Controls ---
with st.sidebar:
    st.header("⚙️ Settings")
    st.session_state.api_key = st.text_input("Primary API Key", type="password", value=st.session_state.api_key)
    st.session_state.api_key_dashboard = st.text_input("Dashboard API Key (Optional)", type="password", value=st.session_state.api_key_dashboard)

    st.header("Actions")
    if st.button("Generate Dashboard Insights"):
        dashboard_key = st.session_state.api_key_dashboard or st.session_state.api_key
        if not dashboard_key:
            st.error("Please enter at least a primary API key.")
        elif len(st.session_state.session_journal) < 100:
            st.warning("Journal is too short for meaningful insights.")
        else:
            with st.spinner("Analyzing your session..."):
                instruction = f"""
                Analyze the following journal text. Provide a privacy-respecting summary as a JSON object with three keys:
                1. "sentiment": A single string describing the overall mood (e.g., "Anxious but hopeful").
                2. "themes": A list of 3-4 main string topics (e.g., "Work-Life Balance").
                3. "recommendations": A list of 2-3 JSON objects. Each object must have two keys: "suggestion" (an actionable idea) and "reason" (why it might help).
                Journal: "{st.session_state.session_journal}"
                Respond with ONLY the raw JSON object.
                """
                messages = [{"role": "system", "content": instruction}]
                dashboard_data_str = call_ai_api(messages, model=Config.API_MODEL_DASHBOARD, api_key=dashboard_key)
                try:
                    json_match = re.search(r'\{.*\}', dashboard_data_str, re.DOTALL)
                    if json_match:
                        st.session_state.dashboard = json.loads(json_match.group())
                        st.success("Dashboard generated!")
                    else:
                        st.error("Failed to parse insights.")
                except json.JSONDecodeError:
                    st.error("Could not generate insights due to an invalid format.")
    
    if st.button("Clear Conversation History"):
        st.session_state.messages = []
        st.session_state.session_journal = "Journal started."
        st.session_state.dynamic_directive = ""
        st.session_state.severity_warning_shown = False
        if 'dashboard' in st.session_state:
            del st.session_state['dashboard']
        st.rerun()

# --- Main View with Tabs ---
tab1, tab2 = st.tabs(["💬 Chat", "📊 Dashboard"])

with tab1:
    render_chat_view()

with tab2:
    render_dashboard_view()

# --- Chat Input Logic (runs outside tabs) ---
if prompt := st.chat_input("You can talk to me..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if any(keyword in prompt.lower() for keyword in Config.CRISIS_KEYWORDS):
        crisis_response = get_crisis_response()
        st.session_state.messages.append({"role": "assistant", "content": crisis_response})
        st.rerun()

    severity_score = get_severity_score(prompt)
    if severity_score >= 8 and not st.session_state.severity_warning_shown:
        st.session_state.severity_warning_shown = True
        st.warning("It seems like you are going through a significant challenge. Please remember that professional resources are available for immediate, confidential support.")

    with st.spinner("Listening and reflecting..."):
        relevant_texts = []
        if kb_embeddings is not None and len(kb_docs) > 0:
            query_embedding = load_embedding_model().encode(prompt)
            search_results = util.semantic_search(query_embedding, kb_embeddings, top_k=Config.TOP_K)[0]
            relevant_texts = [kb_docs[result['corpus_id']]['text'] for result in search_results]

        context_prompt = ""
        if relevant_texts:
            context_prompt += "--- RELEVANT THERAPEUTIC CONCEPTS ---\n" + "\n---\n".join(relevant_texts)
        if st.session_state.session_journal:
            context_prompt += f"\n--- CURRENT SESSION JOURNAL ---\n{st.session_state.session_journal}"
        
        final_query = f"{context_prompt}\n\n**User's latest message:** {prompt}"
        
        messages_for_api = [
            {"role": "system", "content": get_system_prompt()},
            *st.session_state.messages[-6:-1],
            {"role": "user", "content": final_query}
        ]
        
        response = call_ai_api(messages_for_api, model=Config.API_MODEL_CHAT, api_key=st.session_state.api_key)
        st.session_state.messages.append({"role": "assistant", "content": response})

    journal_update_prompt = f"Concisely summarize the key points from this exchange for a journal. User: '{prompt}'. Advisor: '{response}'"
    journal_messages = [{"role": "system", "content": journal_update_prompt}]
    summary = call_ai_api(journal_messages, model=Config.API_MODEL_CLASSIFY, api_key=st.session_state.api_key)
    st.session_state.session_journal += f"\n\nUser: {prompt}\nAdvisor: {summary}"

    st.session_state.dynamic_directive = get_prompt_improvement_suggestion(st.session_state.messages)
    
    st.rerun()
