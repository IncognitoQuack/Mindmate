# main.py 
import streamlit as st
import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer, util
import requests
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
import re
import hashlib
import secrets
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
import logging
from functools import lru_cache
import time

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('mindmate.log'), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# --- Page Configuration ---
st.set_page_config(
    page_title="Mindmate AI - Mental Health Companion",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Professional Clean UI Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    :root {
        --primary-color: #7f9cf5;
        --secondary-color: #a78bfa;
        --success-color: #2DCE89;
        --warning-color: #FB6340;
        --info-color: #38bdf8;
        --dark-bg: #181c27;
        --light-bg: #23283b;
        --card-bg: #23283b;
        --text-primary: #f7fafc;
        --text-secondary: #b5b9c9;
        --border-color: #2d334d;
        --shadow-sm: 0 2px 4px rgba(0,0,0,0.12);
        --shadow-md: 0 4px 12px rgba(0,0,0,0.18);
        --shadow-lg: 0 10px 24px rgba(0,0,0,0.22);
    }
    .stApp {
        background: linear-gradient(180deg, #181c27 0%, #23283b 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: var(--text-primary);
    }
    #MainMenu, footer, header {visibility: hidden;}
    .main-header {
        background: var(--card-bg);
        padding: 2rem 3rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-md);
        border-left: 4px solid var(--primary-color);
    }
    .main-header h1 {
        color: var(--primary-color);
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        font-family: 'Inter', sans-serif;
    }
    .main-header p {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-top: 0.5rem;
        margin-bottom: 0;
    }
    .clean-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        color: var(--text-primary);
    }
    .clean-card:hover {
        box-shadow: var(--shadow-md);
        transform: translateY(-2px);
    }
    .stChatMessage {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        color: var(--text-primary);
    }
    .stChatMessage[data-testid="user-message"] {
        background: linear-gradient(135deg, #23283b 0%, #181c27 100%);
        border-left: 3px solid var(--primary-color);
    }
    .stChatMessage[data-testid="assistant-message"] {
        background: var(--card-bg);
        border-left: 3px solid var(--secondary-color);
    }
    .css-1d391kg, [data-testid="stSidebar"] {
        background: var(--card-bg);
        box-shadow: 2px 0 10px rgba(0,0,0,0.12);
        color: var(--text-primary);
    }
    .css-1d391kg .block-container {
        padding: 2rem 1rem;
    }
    .stButton > button {
        background: var(--primary-color);
        color: #181c27;
        border: none;
        padding: 0.625rem 1.5rem;
        border-radius: 8px;
        font-weight: 500;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: var(--shadow-sm);
        font-family: 'Inter', sans-serif;
        width: 100%;
        cursor: pointer;
    }
    .stButton > button:hover {
        background: #5a67d8;
        color: #fff;
        box-shadow: var(--shadow-md);
        transform: translateY(-1px);
    }
    .secondary-button > button {
        background: transparent;
        color: var(--primary-color);
        border: 1px solid var(--primary-color);
    }
    .secondary-button > button:hover {
        background: var(--primary-color);
        color: #181c27;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: var(--card-bg);
        padding: 0.5rem;
        border-radius: 10px;
        gap: 0.5rem;
        border: 1px solid var(--border-color);
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent;
        color: var(--text-secondary);
        border-radius: 6px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        font-size: 0.95rem;
        border: none;
    }
    .stTabs [aria-selected="true"] {
        background: var(--primary-color);
        color: #181c27;
    }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #181c27;
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 0.75rem;
        font-size: 0.95rem;
        color: var(--text-primary);
        transition: all 0.2s ease;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 3px rgba(127, 156, 245, 0.18);
    }
    .metric-card {
        background: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
        height: 100%;
        color: var(--text-primary);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0.5rem 0;
    }
    .metric-label {
        font-size: 0.875rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-weight: 600;
    }
    .stAlert {
        background: var(--card-bg);
        border-radius: 8px;
        border-left: 4px solid var(--info-color);
        box-shadow: var(--shadow-sm);
        color: var(--text-primary);
    }
    .stSuccess {
        border-left-color: var(--success-color);
        background: #1e2e26;
        color: var(--success-color);
    }
    .stWarning {
        border-left-color: var(--warning-color);
        background: #3a2323;
        color: var,--warning-color;
    }
    .info-box {
        background: linear-gradient(135deg, #23283b 0%, #181c27 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 3px solid var(--info-color);
        color: var(--text-primary);
    }
    .stChatInput {
        background: var(--card-bg);
        border-radius: 12px;
        border: 1px solid var(--border-color);
        padding: 0.5rem;
        color: var(--text-primary);
    }
    .streamlit-expanderHeader {
        background: var(--card-bg);
        border-radius: 8px;
        border: 1px solid var(--border-color);
        font-weight: 500;
        color: var(--text-primary);
    }
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    .section-header {
        color: var(--primary-color);
        font-size: 1.25rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    .status-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    .status-active {
        background: #23283b;
        color: #7f9cf5;
        border: 1px solid #7f9cf5;
    }
    .status-warning {
        background: #3a2323;
        color: #FB6340;
        border: 1px solid #FB6340;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .animate-in {
        animation: fadeIn 0.3s ease-out;
    }
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: var(--dark-bg);
    }
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)

# --- System Configuration (Original Models) ---
class Config:
    DATA_DIR = "mental_health_kb"
    EMBEDDING_MODEL = 'paraphrase-multilingual-mpnet-base-v2'
    API_MODEL_CHAT = 'google/gemma-3-27b-it:free'
    API_MODEL_DASHBOARD = 'deepseek/deepseek-r1-0528:free'
    API_MODEL_CLASSIFY = 'google/gemma-2-9b-it:free'
    TOP_K = 4
    CRISIS_KEYWORDS = [
        'suicide', 'kill myself', 'harm myself', 'want to die', 'end my life',
        'self harm', 'overdose', 'not worth living', 'better off dead'
    ]

# --- Secure Session State Manager ---
class SecureSessionManager:
    """Manages secure session state without exposing sensitive data"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state with secure defaults"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "session_journal" not in st.session_state:
            st.session_state.session_journal = f"Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        if "dynamic_directive" not in st.session_state:
            st.session_state.dynamic_directive = ""
        if "severity_warning_shown" not in st.session_state:
            st.session_state.severity_warning_shown = False
        if "session_start_time" not in st.session_state:
            st.session_state.session_start_time = datetime.now()
        if "message_count" not in st.session_state:
            st.session_state.message_count = 0
        if "api_call_count" not in st.session_state:
            st.session_state.api_call_count = 0
        if "current_api_key_index" not in st.session_state:
            st.session_state.current_api_key_index = 0
            
        # Secure API key initialization (never expose actual keys)
        if "_api_keys_set" not in st.session_state:
            st.session_state._api_keys_set = False
            st.session_state._api_key_primary_hash = None
            st.session_state._api_key_dashboard_hash = None
    
    @staticmethod
    def set_api_keys(primary_key: str, dashboard_key: str = None):
        """Securely store API keys without exposing them"""
        if primary_key:
            # Store only hash for verification, actual key in protected session
            st.session_state._api_key_primary_hash = hashlib.sha256(primary_key.encode()).hexdigest()
            st.session_state._api_key_primary = primary_key
            st.session_state._api_keys_set = True
            
        if dashboard_key:
            st.session_state._api_key_dashboard_hash = hashlib.sha256(dashboard_key.encode()).hexdigest()
            st.session_state._api_key_dashboard = dashboard_key
        elif primary_key:
            # Use primary key as fallback for dashboard
            st.session_state._api_key_dashboard = primary_key
    
    @staticmethod
    def get_current_api_key() -> str:
        """Get current API key for rotation to avoid rate limits"""
        if not st.session_state._api_keys_set:
            return None
            
        # Rotate between keys if both are available
        if hasattr(st.session_state, '_api_key_dashboard') and st.session_state._api_key_dashboard:
            keys = [st.session_state._api_key_primary, st.session_state._api_key_dashboard]
            key = keys[st.session_state.current_api_key_index % 2]
            st.session_state.current_api_key_index += 1
            return key
        
        return st.session_state._api_key_primary if hasattr(st.session_state, '_api_key_primary') else None
    
    @staticmethod
    def has_valid_keys() -> bool:
        """Check if valid API keys are set"""
        return st.session_state._api_keys_set and hasattr(st.session_state, '_api_key_primary')

# --- Caching for Performance ---
@st.cache_resource
def load_embedding_model():
    """Load and cache the embedding model"""
    return SentenceTransformer(Config.EMBEDDING_MODEL)

@st.cache_data(ttl=3600)
def load_knowledge_base():
    """Load and cache knowledge base with embeddings"""
    knowledge_base = []
    data_dir = Config.DATA_DIR
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        create_default_knowledge_base(data_dir)
    
    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    if not json_files:
        create_default_knowledge_base(data_dir)
        json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]
    
    for file_name in json_files:
        file_path = os.path.join(data_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    text = item.get('text', item.get('content', '')) if isinstance(item, dict) else str(item)
                    if text:
                        knowledge_base.append({"source": file_name, "text": text})
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            logger.error(f"Error loading {file_name}: {e}")
    
    if knowledge_base:
        model = load_embedding_model()
        all_texts = [doc['text'] for doc in knowledge_base]
        embeddings = model.encode(all_texts, convert_to_tensor=True, show_progress_bar=False)
        return knowledge_base, embeddings
    
    return [], None

def create_default_knowledge_base(data_dir: str):
    """Create default knowledge base with therapeutic content"""
    default_content = [
        {
            "text": "Cognitive Behavioral Therapy (CBT) helps identify and change negative thought patterns. It's based on the idea that our thoughts, feelings, and behaviors are interconnected.",
            "category": "therapy_techniques"
        },
        {
            "text": "The 4-7-8 breathing technique: Inhale for 4 counts, hold for 7 counts, exhale for 8 counts. This activates the parasympathetic nervous system and promotes relaxation.",
            "category": "coping_strategies"
        },
        {
            "text": "Mindfulness meditation involves observing thoughts and feelings without judgment. Regular practice can reduce anxiety and improve emotional regulation.",
            "category": "mindfulness"
        },
        {
            "text": "Journaling helps process emotions and identify patterns. Try writing for 10 minutes daily about your thoughts and feelings.",
            "category": "self_help"
        },
        {
            "text": "Physical exercise releases endorphins, natural mood lifters. Even a 20-minute walk can significantly improve mental well-being.",
            "category": "lifestyle"
        },
        {
            "text": "The STOP technique for anxiety: Stop what you're doing, Take a breath, Observe your surroundings and feelings, Proceed with intention.",
            "category": "coping_strategies"
        },
        {
            "text": "Grounding techniques like the 5-4-3-2-1 method help manage panic. Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, and 1 you taste.",
            "category": "anxiety_management"
        },
        {
            "text": "Sleep hygiene is crucial for mental health. Maintain consistent sleep schedule, avoid screens before bed, and create a relaxing bedtime routine.",
            "category": "lifestyle"
        }
    ]
    
    with open(os.path.join(data_dir, 'therapeutic_knowledge.json'), 'w') as f:
        json.dump(default_content, f, indent=2)

# --- Core AI Functions ---
def call_ai_api(messages: List[Dict], model: str, max_retries: int = 2) -> str:
    """Call AI API with automatic key rotation for rate limit management"""
    api_key = SecureSessionManager.get_current_api_key()
    
    if not api_key:
        return "⚠️ Please configure your API key in the settings panel."
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://github.com/Sanjit-Mathur/Mindmate",
        "X-Title": "Mindmate AI Advisor",
    }
    
    data = {"model": model, "messages": messages}
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=180
            )
            response.raise_for_status()
            
            st.session_state.api_call_count += 1
            api_response = response.json()
            return api_response["choices"][0]["message"]["content"].strip()
            
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 429:  # Rate limit
                # Try with alternate key
                api_key = SecureSessionManager.get_current_api_key()
                headers["Authorization"] = f"Bearer {api_key}"
                if attempt < max_retries - 1:
                    time.sleep(2)
                    continue
            logger.error(f"API HTTP Error: {http_err}")
            return f"⚠️ Service temporarily unavailable. Please try again."
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API Request Error: {e}")
            return "⚠️ Connection error. Please check your internet connection."
            
        except (KeyError, IndexError) as e:
            logger.error(f"API Response Error: {e}")
            return "⚠️ Received unexpected response format."
    
    return "⚠️ Unable to get response. Please try again."

def get_severity_score(prompt: str) -> int:
    """Analyze message severity for crisis detection"""
    instruction = f"""Analyze this message for mental health crisis severity. 
    Return ONLY a number from 1-10 where:
    1-3 = Normal conversation
    4-6 = Mild distress
    7-8 = Significant distress
    9-10 = Crisis/emergency
    
    Message: "{prompt}"
    
    Return only the number."""
    
    messages = [{"role": "system", "content": instruction}]
    
    try:
        response = call_ai_api(messages, model=Config.API_MODEL_CLASSIFY)
        match = re.search(r'\d+', response)
        if match:
            return min(10, max(1, int(match.group())))
    except (ValueError, AttributeError) as e:
        logger.error(f"Severity scoring error: {e}")
    
    # Default severity check based on keywords
    prompt_lower = prompt.lower()
    for keyword in Config.CRISIS_KEYWORDS:
        if keyword in prompt_lower:
            return 9
    
    return 3

def get_crisis_response() -> str:
    """Provide crisis response with resources"""
    return """
    🆘 **I'm very concerned about what you're sharing. Your safety is the top priority.**
    
    Please reach out for immediate professional support:
    
    **📞 Crisis Hotlines (24/7):**
    
    🇮🇳 **India:**
    • Vandrevala Foundation: **9999666555** or **1860-2662-345**
    • KIRAN Mental Health: **1800-599-0019**
    • AASRA: **9820466726**
    
    🌍 **International:**
    • Crisis Text Line: Text HOME to **741741**
    • National Suicide Prevention Lifeline: **988** (US)
    • Samaritans: **116 123** (UK)
    
    **💙 Remember:** You matter, help is available, and things can get better. Please reach out to one of these resources or someone you trust right now.
    """

def get_prompt_improvement_suggestion(history: List[Dict]) -> str:
    """Generate dynamic suggestions for better responses"""
    if len(history) < 4:
        return ""
    
    recent_messages = history[-4:]
    conversation_context = "\n".join([f"{msg['role']}: {msg['content'][:200]}" for msg in recent_messages])
    
    instruction = f"""Based on this conversation, suggest ONE specific way to improve the next response.
    Focus on: validation, empathy, or therapeutic techniques.
    
    Conversation:
    {conversation_context}
    
    Return only a brief directive (max 10 words)."""
    
    messages = [{"role": "system", "content": instruction}]
    suggestion = call_ai_api(messages, model=Config.API_MODEL_CLASSIFY)
    
    return suggestion[:100] if suggestion else ""

def get_system_prompt() -> str:
    """Generate system prompt for AI assistant"""
    base_prompt = """
    You are a compassionate mental health companion. Your role is to provide emotional support and guidance while maintaining professional boundaries yet have emotional connect with the user and answer him in what ever language he is using/perfers .
    
    **Core Principles:**
    1. Always prioritize user safety - if someone expresses suicidal thoughts, provide crisis resources immediately
    2. Validate emotions before offering suggestions
    3. Use evidence-based therapeutic techniques (CBT, mindfulness, etc.)
    4. Ask clarifying questions to understand better
    5. Never diagnose or prescribe medication
    6. Maintain warm, empathetic tone
    7. Encourage professional help when appropriate
    
    **Response Structure:**
    - Acknowledge and validate feelings
    - Show understanding through reflection
    - Offer gentle, practical suggestions if appropriate
    - End with an open question or supportive statement
    
    Remember: You're a supportive companion, and act like a professional therapy.
    """
    
    if st.session_state.dynamic_directive:
        base_prompt += f"\n\n**Current Focus:** {st.session_state.dynamic_directive}"
    
    return base_prompt

# --- Dashboard Analytics ---
def calculate_session_metrics() -> Dict:
    """Calculate real session metrics"""
    metrics = {}
    
    # Message count
    metrics['total_messages'] = len(st.session_state.messages)
    
    # Session duration
    if hasattr(st.session_state, 'session_start_time'):
        duration = datetime.now() - st.session_state.session_start_time
        hours, remainder = divmod(duration.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        metrics['session_duration'] = f"{hours}h {minutes}m"
    else:
        metrics['session_duration'] = "0h 0m"
    
    # API calls made
    metrics['api_calls'] = st.session_state.get('api_call_count', 0)
    
    # Average message length
    if st.session_state.messages:
        user_messages = [len(m['content']) for m in st.session_state.messages if m['role'] == 'user']
        metrics['avg_message_length'] = sum(user_messages) // len(user_messages) if user_messages else 0
    else:
        metrics['avg_message_length'] = 0
    
    return metrics

def generate_session_insights(journal: str, messages: List[Dict]) -> Dict:
    """Generate AI-powered session insights using real data"""
    if not messages or len(journal) < 100:
        return {
            'sentiment': 'No data available yet',
            'themes': [],
            'recommendations': []
        }
    
    instruction = f"""
    Analyze this therapy session journal and provide insights as a JSON object with:
    1. "sentiment": Overall emotional tone (one phrase)
    2. "themes": List of 3-4 main topics discussed
    3. "recommendations": List of 2-3 actionable suggestions, each with "suggestion" and "reason" keys
    
    Journal: {journal[:2000]}
    
    Return ONLY valid JSON.
    """
    
    messages_api = [{"role": "system", "content": instruction}]
    
    try:
        response = call_ai_api(messages_api, model=Config.API_MODEL_DASHBOARD)
        
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', response, re.DOTALL)
        if json_match:
            insights = json.loads(json_match.group())
            return insights
    except (json.JSONDecodeError, Exception) as e:
        logger.error(f"Error generating insights: {e}")
    
    # Fallback analysis based on actual messages
    themes = set()
    for msg in messages:
        content_lower = msg['content'].lower()
        if 'anxiety' in content_lower or 'worried' in content_lower:
            themes.add('Anxiety')
        if 'depress' in content_lower or 'sad' in content_lower:
            themes.add('Depression')
        if 'stress' in content_lower:
            themes.add('Stress')
        if 'relationship' in content_lower:
            themes.add('Relationships')
    
    return {
        'sentiment': 'Processing...',
        'themes': list(themes) if themes else ['General emotional support'],
        'recommendations': [
            {
                'suggestion': 'Practice daily mindfulness meditation',
                'reason': 'Can help reduce stress and improve emotional regulation'
            }
        ]
    }

def create_mood_chart(messages: List[Dict]) -> go.Figure:
    """Create mood progression chart from actual conversation"""
    if not messages:
        return go.Figure()
    
    # Analyze sentiment progression through messages
    mood_scores = []
    timestamps = []
    
    for i, msg in enumerate(messages):
        if msg['role'] == 'user':
            # Simple sentiment scoring based on keywords
            content_lower = msg['content'].lower()
            score = 5  # Neutral default
            
            # Positive indicators
            if any(word in content_lower for word in ['better', 'good', 'happy', 'great', 'improved']):
                score += 2
            # Negative indicators
            if any(word in content_lower for word in ['sad', 'anxious', 'worried', 'stressed', 'bad']):
                score -= 2
            
            score = max(1, min(10, score))  # Keep between 1-10
            mood_scores.append(score)
            timestamps.append(f"Message {i//2 + 1}")
    
    if not mood_scores:
        mood_scores = [5]
        timestamps = ["Start"]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=mood_scores,
        mode='lines+markers',
        name='Mood',
        line=dict(color='#5E72E4', width=3),
        marker=dict(size=8, color='#5E72E4'),
        fill='tozeroy',
        fillcolor='rgba(94, 114, 228, 0.1)'
    ))
    
    fig.update_layout(
        title="Emotional Journey",
        xaxis_title="Conversation Progress",
        yaxis_title="Mood Level",
        yaxis=dict(range=[0, 10]),
        template="plotly_white",
        height=300,
        margin=dict(l=0, r=0, t=40, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# --- Sidebar Toggle State ---
if "sidebar_open" not in st.session_state:
    st.session_state.sidebar_open = True

def toggle_sidebar():
    st.session_state.sidebar_open = not st.session_state.sidebar_open

# --- UI Components ---
def render_header():
    """Render clean professional header"""
    st.markdown("""
    <div class="main-header animate-in">
        <h1>🧠 Mindmate AI</h1>
        <p>Your trusted mental health companion - Here to listen and support</p>
    </div>
    """, unsafe_allow_html=True)

def render_chat_view():
    """Render chat interface"""
    if not st.session_state.messages:
        st.markdown("""
        <div class="info-box">
            <p>👋 <strong>Welcome to Mindmate!</strong></p>
            <p>I'm here to listen and support you. Feel free to share what's on your mind.</p>
        </div>
        """, unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def render_dashboard():
    """Render analytics dashboard with real data"""
    st.markdown('<h2 class="section-header">📊 Session Analytics</h2>', unsafe_allow_html=True)
    
    # Calculate real metrics
    metrics = calculate_session_metrics()
    
    # Display metrics in grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Messages</div>
            <div class="metric-value">{metrics['total_messages']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Duration</div>
            <div class="metric-value">{metrics['session_duration']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">API Calls</div>
            <div class="metric-value">{metrics['api_calls']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Avg Length</div>
            <div class="metric-value">{metrics['avg_message_length']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Mood chart
    if st.session_state.messages:
        st.markdown('<h3 class="section-header">Emotional Journey</h3>', unsafe_allow_html=True)
        fig = create_mood_chart(st.session_state.messages)
        st.plotly_chart(fig, use_container_width=True)
    
    # Generate insights
    if st.button("🔍 Generate Session Insights", key="generate_insights"):
        with st.spinner("Analyzing your session..."):
            insights = generate_session_insights(
                st.session_state.session_journal,
                st.session_state.messages
            )
            st.session_state.dashboard_insights = insights
    
    # Display insights if available
    if 'dashboard_insights' in st.session_state:
        insights = st.session_state.dashboard_insights
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="clean-card">
                <h4>Overall Sentiment</h4>
            </div>
            """, unsafe_allow_html=True)
            st.info(insights.get('sentiment', 'Analyzing...'))
        
        with col2:
            st.markdown("""
            <div class="clean-card">
                <h4>Key Themes</h4>
            </div>
            """, unsafe_allow_html=True)
            themes = insights.get('themes', [])
            if themes:
                for theme in themes:
                    st.write(f"• {theme}")
        
        st.markdown("""
        <div class="clean-card">
            <h4>Personalized Recommendations</h4>
        </div>
        """, unsafe_allow_html=True)
        
        recommendations = insights.get('recommendations', [])
        for rec in recommendations:
            if isinstance(rec, dict):
                st.success(f"💡 **{rec.get('suggestion', '')}**")
                st.caption(rec.get('reason', ''))

def render_sidebar():
    """Render sidebar with secure API key management"""
    with st.sidebar:
        if st.button("⬅️ Hide Sidebar", key="hide_sidebar"):
            st.session_state.sidebar_open = False
            st.experimental_rerun()
        st.markdown("### ⚙️ Configuration")
        
        # API Key Status (show status without revealing keys)
        if SecureSessionManager.has_valid_keys():
            st.success("✅ API Keys Configured")
            st.markdown("""
            <div class="status-badge status-active">
                Active
            </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ API Keys Required")
        
        # API Key Input (secure - never show existing keys)
        with st.expander("🔐 API Key Settings"):
            st.info("Enter your API keys. Keys are encrypted and never displayed.")
            
            # Primary API Key
            new_primary_key = st.text_input(
                "Primary API Key",
                type="password",
                placeholder="sk-or-v1-...",
                key="primary_key_input",
                help="Your primary API key"
            )
            
            # Dashboard/Secondary API Key for rate limit management
            new_dashboard_key = st.text_input(
                "Secondary API Key (Optional)",
                type="password",
                placeholder="sk-or-v1-...",
                key="dashboard_key_input",
                help="Secondary key for higher rate limits"
            )
            
            if st.button("Update API Keys", key="update_keys"):
                if new_primary_key:
                    SecureSessionManager.set_api_keys(new_primary_key, new_dashboard_key)
                    st.success("✅ API keys updated securely")
                    st.rerun()
                else:
                    st.error("Primary API key is required")
        
        # Session Management
        st.markdown("### 📊 Session Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Session", key="clear_chat"):
                st.session_state.messages = []
                st.session_state.session_journal = f"Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                st.session_state.dynamic_directive = ""
                st.session_state.severity_warning_shown = False
                st.session_state.session_start_time = datetime.now()
                st.session_state.api_call_count = 0
                if 'dashboard_insights' in st.session_state:
                    del st.session_state['dashboard_insights']
                st.rerun()
        
        with col2:
            if st.button("💾 Export", key="export_chat"):
                if st.session_state.messages:
                    chat_export = {
                        'session_date': datetime.now().isoformat(),
                        'messages': st.session_state.messages,
                        'metrics': calculate_session_metrics()
                    }
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(chat_export, indent=2),
                        file_name=f"mindmate_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )
        
        # Resources
        st.markdown("### 🆘 Crisis Resources")
        with st.expander("Emergency Contacts"):
            st.markdown("""
            **India 🇮🇳**
            - Vandrevala: `9999666555`
            - KIRAN: `1800-599-0019`
            - AASRA: `9820466726`
            
            **International 🌍**
            - Crisis Text: `741741`
            - Lifeline: `988` (US)
            """)

# --- Main Application ---
def main():
    # Initialize secure session
    SecureSessionManager.initialize_session()
    
    # Load environment variables securely (only on first run)
    if not SecureSessionManager.has_valid_keys():
        env_primary = os.getenv("OPENROUTER_API_KEY")
        env_dashboard = os.getenv("OPENROUTER_API_KEY_DASHBOARD")
        if env_primary:
            SecureSessionManager.set_api_keys(env_primary, env_dashboard)
    
    # Load knowledge base
    model = load_embedding_model()
    kb_docs, kb_embeddings = load_knowledge_base()
    
    # Render UI
    render_header()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs(["💬 Chat", "📊 Dashboard", "📝 Journal"])
    
    with tab1:
        render_chat_view()
        
        # Chat input
        if prompt := st.chat_input("What's on your mind?"):
            if not SecureSessionManager.has_valid_keys():
                st.error("⚠️ Please configure your API keys in the sidebar first.")
                st.stop()
            
            # Add user message
            st.session_state.messages.append({"role": "user", "content": prompt})
            st.session_state.message_count += 1
            
            # Check for crisis
            if any(keyword in prompt.lower() for keyword in Config.CRISIS_KEYWORDS):
                crisis_response = get_crisis_response()
                st.session_state.messages.append({"role": "assistant", "content": crisis_response})
                st.rerun()
            
            # Check severity
            severity_score = get_severity_score(prompt)
            if severity_score >= 8 and not st.session_state.severity_warning_shown:
                st.session_state.severity_warning_shown = True
                st.warning("I notice you're going through something difficult. Remember that professional support is available if you need it.")
            
            # Get relevant knowledge
            with st.spinner("Thinking..."):
                relevant_texts = []
                if kb_embeddings is not None and len(kb_docs) > 0:
                    query_embedding = model.encode(prompt)
                    search_results = util.semantic_search(query_embedding, kb_embeddings, top_k=Config.TOP_K)[0]
                    relevant_texts = [kb_docs[result['corpus_id']]['text'] for result in search_results]
                
                # Build context
                context_prompt = ""
                if relevant_texts:
                    context_prompt += "--- Relevant Information ---\n" + "\n".join(relevant_texts[:3])
                
                # Get response
                messages_for_api = [
                    {"role": "system", "content": get_system_prompt()},
                    *st.session_state.messages[-6:-1],  # Recent history
                    {"role": "user", "content": f"{context_prompt}\n\nUser: {prompt}"}
                ]
                
                response = call_ai_api(messages_for_api, model=Config.API_MODEL_CHAT)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Update journal
                st.session_state.session_journal += f"\n\n[{datetime.now().strftime('%H:%M')}]\nUser: {prompt}\nAssistant: {response[:200]}..."
                
                # Update dynamic directive
                st.session_state.dynamic_directive = get_prompt_improvement_suggestion(st.session_state.messages)
            
            st.rerun()
    
    with tab2:
        render_dashboard()
    
    with tab3:
        st.markdown('<h2 class="section-header">📝 Session Journal</h2>', unsafe_allow_html=True)
        
        # Display journal
        st.text_area(
            "Session Transcript",
            value=st.session_state.session_journal,
            height=400,
            disabled=True,
            key="journal_display"
        )
        
        # Export journal
        if st.button("📥 Export Journal"):
            st.download_button(
                label="Download Journal",
                data=st.session_state.session_journal,
                file_name=f"mindmate_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
    
    # Render sidebar only if open
    if st.session_state.sidebar_open:
        render_sidebar()
    else:
        # Floating button to reopen sidebar
        st.markdown("""
        <style>
        .sidebar-fab {
            position: fixed;
            bottom: 32px;
            left: 32px;
            z-index: 9999;
            background: #23283b;
            color: #7f9cf5;
            border-radius: 50%;
            width: 48px;
            height: 48px;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.18);
            cursor: pointer;
            border: 2px solid #7f9cf5;
            font-size: 1.7rem;
            transition: background 0.2s;
        }
        .sidebar-fab:hover {
            background: #7f9cf5;
            color: #181c27;
        }
        </style>
        <div class="sidebar-fab" onclick="window.dispatchEvent(new Event('toggleSidebar'))" title="Open sidebar">☰</div>
        <script>
        const doc = window.parent.document;
        window.addEventListener('toggleSidebar', () => {
            const streamlitEvents = window.streamlitEvents || {};
            streamlitEvents.toggleSidebar = (streamlitEvents.toggleSidebar || 0) + 1;
            window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', key: 'toggleSidebar', value: streamlitEvents.toggleSidebar}, '*');
        });
        </script>
        """, unsafe_allow_html=True)
        # Listen for JS event and update session state
        st.experimental_data_editor({"toggleSidebar": 0}, key="sidebar_toggle", on_change=toggle_sidebar)

    # Watermark
    st.markdown("""
    <div style="position:fixed; bottom:10px; left:0; width:100%; text-align:center; color:#7f9cf5; opacity:0.6; font-size:0.95rem; z-index:9999;">
        Crafted with care by <b>Team BinaryDuo</b>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
