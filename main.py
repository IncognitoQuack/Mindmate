# main.py - Professional Enhanced Version with Light Theme
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

# Import our new UI components
from ui_components import LightThemeUI, AnimationEffects, create_card, create_metric_row, show_toast
from community_features import render_community_tab

# --- Load Environment Variables ---
load_dotenv()

# --- Logging Configuration ---
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

# --- Apply Light Theme ---
ui = LightThemeUI()
ui.inject_custom_css()

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
        if "mood_history" not in st.session_state:
            st.session_state.mood_history = []
        if "achievements" not in st.session_state:
            st.session_state.achievements = []
        if "daily_streak" not in st.session_state:
            st.session_state.daily_streak = 0
        if "total_sessions" not in st.session_state:
            st.session_state.total_sessions = 1
            
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
            score = min(10, max(1, int(match.group())))
            # Track mood history
            st.session_state.mood_history.append(score)
            return score
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
    
    # Mood average
    if st.session_state.mood_history:
        metrics['avg_mood'] = sum(st.session_state.mood_history) / len(st.session_state.mood_history)
    else:
        metrics['avg_mood'] = 5.0
    
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

def check_achievements():
    """Check and unlock achievements"""
    achievements = []
    
    # First conversation
    if len(st.session_state.messages) >= 2:
        achievements.append({
            'id': 'first_chat',
            'title': 'First Steps',
            'description': 'Started your wellness journey',
            'icon': '🌱'
        })
    
    # Regular user
    if st.session_state.total_sessions >= 5:
        achievements.append({
            'id': 'regular_user',
            'title': 'Committed',
            'description': 'Completed 5 sessions',
            'icon': '⭐'
        })
    
    # Long conversation
    if len(st.session_state.messages) >= 20:
        achievements.append({
            'id': 'deep_talk',
            'title': 'Deep Conversation',
            'description': 'Engaged in meaningful dialogue',
            'icon': '💬'
        })
    
    # Check for new achievements
    for achievement in achievements:
        if achievement['id'] not in [a['id'] for a in st.session_state.achievements]:
            st.session_state.achievements.append(achievement)
            show_toast(f"🎉 Achievement Unlocked: {achievement['title']}", "success")
            AnimationEffects.celebration_effect()

# --- UI Components ---
def render_header():
    """Render animated header with light theme"""
    st.markdown(ui.render_animated_header(
        "🧠 Mindmate AI",
        "Your trusted mental health companion - Here to listen and support"
    ), unsafe_allow_html=True)

def render_chat_view():
    """Render chat interface with light theme"""
    if not st.session_state.messages:
        st.markdown(ui.render_welcome_animation(), unsafe_allow_html=True)
        st.markdown(ui.render_info_card(
            "Welcome to Mindmate!",
            "I'm here to listen and support you. Feel free to share what's on your mind. Your conversation is private and secure.",
            "👋"
        ), unsafe_allow_html=True)
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def render_dashboard():
    """Render analytics dashboard with light theme"""
    st.markdown('<h2 class="gradient-text" style="font-size: 1.75rem;">📊 Session Analytics</h2>', unsafe_allow_html=True)
    
    # Calculate real metrics
    metrics = calculate_session_metrics()
    
    # Display metrics in grid
    create_metric_row([
        {'label': 'Messages', 'value': str(metrics['total_messages']), 'icon': '💬'},
        {'label': 'Duration', 'value': metrics['session_duration'], 'icon': '⏱️'},
        {'label': 'Mood Average', 'value': f"{metrics['avg_mood']:.1f}/10", 'icon': '😊'},
        {'label': 'Streak', 'value': f"{st.session_state.daily_streak} days", 'icon': '🔥'}
    ])
    
    # Mood chart with light theme
    if st.session_state.mood_history:
        st.markdown('<h3 class="gradient-text" style="margin-top: 2rem;">Emotional Journey</h3>', unsafe_allow_html=True)
        labels = [f"Message {i+1}" for i in range(len(st.session_state.mood_history))]
        fig = ui.create_mood_gradient_chart(st.session_state.mood_history, labels)
        st.plotly_chart(fig, use_container_width=True)
    
    # Achievements section
    st.markdown('<h3 class="gradient-text" style="margin-top: 2rem;">🏆 Achievements</h3>', unsafe_allow_html=True)
    
    if st.session_state.achievements:
        cols = st.columns(3)
        for idx, achievement in enumerate(st.session_state.achievements[:6]):
            with cols[idx % 3]:
                st.markdown(ui.render_achievement_card(
                    achievement['title'],
                    achievement['description'],
                    achievement['icon'],
                    True
                ), unsafe_allow_html=True)
    else:
        st.info("Start chatting to unlock achievements! 🎯")
    
    # Generate insights button
    if st.button("🔍 Generate Session Insights", key="generate_insights", use_container_width=True):
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
            st.markdown(create_card(
                f"<div style='text-align: center;'><h4 class='gradient-text'>Overall Sentiment</h4><p style='font-size: 1.2rem; margin-top: 1rem;'>{insights.get('sentiment', 'Analyzing...')}</p></div>",
                ""
            ), unsafe_allow_html=True)
        
        with col2:
            themes_html = "<h4 class='gradient-text'>Key Themes</h4><ul style='margin-top: 1rem;'>"
            for theme in insights.get('themes', []):
                themes_html += f"<li style='margin: 0.5rem 0;'>{theme}</li>"
            themes_html += "</ul>"
            st.markdown(create_card(themes_html, ""), unsafe_allow_html=True)
        
        st.markdown('<h4 class="gradient-text" style="margin-top: 1.5rem;">💡 Personalized Recommendations</h4>', unsafe_allow_html=True)
        
        for rec in insights.get('recommendations', []):
            if isinstance(rec, dict):
                st.markdown(ui.render_info_card(
                    rec.get('suggestion', ''),
                    rec.get('reason', ''),
                    '💡'
                ), unsafe_allow_html=True)

def render_wellness_activities():
    """Render wellness activities and mini-games"""
    st.markdown('<h2 class="gradient-text" style="font-size: 1.75rem;">🎯 Wellness Activities</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(create_card("""
            <h3>🧘 Breathing Exercise</h3>
            <p>Take a moment to relax with guided breathing</p>
        """), unsafe_allow_html=True)
        
        if st.button("Start Breathing Exercise", key="breathing", use_container_width=True):
            placeholder = st.empty()
            for phase, duration in [("Inhale... 🫁", 4), ("Hold... ⏸️", 7), ("Exhale... 💨", 8)]:
                for i in range(duration):
                    placeholder.markdown(f"""
                        <div style='text-align: center; padding: 2rem;'>
                            <h2>{phase}</h2>
                            {ui.render_progress_bar((i+1)/duration * 100)}
                        </div>
                    """, unsafe_allow_html=True)
                    time.sleep(1)
            placeholder.markdown(ui.render_info_card("Great job!", "You've completed the breathing exercise", "✅"), unsafe_allow_html=True)
            AnimationEffects.success_animation()
    
    with col2:
        st.markdown(create_card("""
            <h3>📝 Gratitude Journal</h3>
            <p>Write three things you're grateful for today</p>
        """), unsafe_allow_html=True)
        
        gratitude_input = st.text_area("What are you grateful for?", height=100, key="gratitude")
        if st.button("Save Entry", key="save_gratitude", use_container_width=True):
            if gratitude_input:
                show_toast("Gratitude entry saved! Keep up the positive thinking! 🌟", "success")
                st.session_state.daily_streak += 1
                check_achievements()

def render_sidebar():
    """Render sidebar with light theme"""
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        # API Key Status with light theme
        if SecureSessionManager.has_valid_keys():
            st.success("✅ API Keys Configured")
            st.markdown(ui.render_status_badge("Active", "active"), unsafe_allow_html=True)
        else:
            st.warning("⚠️ API Keys Required")
        
        # API Key Input (secure)
        with st.expander("🔐 API Key Settings"):
            st.info("Enter your API keys. Keys are encrypted and never displayed.")
            
            new_primary_key = st.text_input(
                "Primary API Key",
                type="password",
                placeholder="sk-or-v1-...",
                key="primary_key_input",
                help="Your primary API key"
            )
            
            new_dashboard_key = st.text_input(
                "Secondary API Key (Optional)",
                type="password",
                placeholder="sk-or-v1-...",
                key="dashboard_key_input",
                help="Secondary key for higher rate limits"
            )
            
            if st.button("Update API Keys", key="update_keys", use_container_width=True):
                if new_primary_key:
                    SecureSessionManager.set_api_keys(new_primary_key, new_dashboard_key)
                    show_toast("✅ API keys updated securely", "success")
                    st.rerun()
                else:
                    st.error("Primary API key is required")
        
        # Session Management
        st.markdown("### 📊 Session Management")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🔄 New Session", key="clear_chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.session_journal = f"Session started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                st.session_state.dynamic_directive = ""
                st.session_state.severity_warning_shown = False
                st.session_state.session_start_time = datetime.now()
                st.session_state.api_call_count = 0
                st.session_state.mood_history = []
                st.session_state.total_sessions += 1
                if 'dashboard_insights' in st.session_state:
                    del st.session_state['dashboard_insights']
                st.rerun()
        
        with col2:
            if st.button("💾 Export", key="export_chat", use_container_width=True):
                if st.session_state.messages:
                    chat_export = {
                        'session_date': datetime.now().isoformat(),
                        'messages': st.session_state.messages,
                        'metrics': calculate_session_metrics(),
                        'achievements': st.session_state.achievements
                    }
                    st.download_button(
                        label="Download JSON",
                        data=json.dumps(chat_export, indent=2),
                        file_name=f"mindmate_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json",
                        use_container_width=True
                    )
        
        # Quick Stats
        st.markdown("### 📈 Quick Stats")
        metrics = calculate_session_metrics()
        st.markdown(f"""
        <div class="clean-card" style="text-align: center;">
            <div style="display: flex; justify-content: space-around; align-items: center;">
                <div>
                    <div class="metric-value" style="font-size: 1.5rem;">{metrics['total_messages']}</div>
                    <div class="metric-label">Messages</div>
                </div>
                <div>
                    <div class="metric-value" style="font-size: 1.5rem;">{st.session_state.daily_streak}</div>
                    <div class="metric-label">Day Streak</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
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
    
    # Load environment variables securely
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
    
    # Main tabs with icons
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat", "📊 Dashboard", "🎯 Wellness", "📝 Journal", "🤝 Community"])
    
    with tab1:
        render_chat_view()
        
        # Chat input
        if prompt := st.chat_input("What's on your mind today? 💭"):
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
                st.warning("I notice you're going through something difficult. Remember that professional support is available if you need it. 💙")
            
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
                
                # Check achievements
                check_achievements()
            
            st.rerun()
    
    with tab2:
        render_dashboard()
    
    with tab3:
        render_wellness_activities()
    
    with tab4:
        st.markdown('<h2 class="gradient-text" style="font-size: 1.75rem;">📝 Session Journal</h2>', unsafe_allow_html=True)
        
        # Display journal with light theme
        st.text_area(
            "Session Transcript",
            value=st.session_state.session_journal,
            height=400,
            disabled=True,
            key="journal_display"
        )
        
        # Export journal
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📥 Export Journal", use_container_width=True):
                st.download_button(
                    label="Download Journal",
                    data=st.session_state.session_journal,
                    file_name=f"mindmate_journal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                    mime="text/plain",
                    use_container_width=True
                )
        with col2:
            if st.button("📧 Email to Self", use_container_width=True):
                show_toast("Email feature coming soon!", "info")
    
    with tab5:
        render_community_tab()

    # Render sidebar
    render_sidebar()

    # Footer with animation
    st.markdown("""
    <div style="margin-top: 3rem; padding: 2rem; text-align: center; border-top: 1px solid var(--border-color);">
        <p class="gradient-text" style="font-size: 1rem; font-weight: 600;">
            Crafted with care by <b>Team BinaryDuo</b> 💜
        </p>
        <p style="color: var(--text-tertiary); font-size: 0.875rem; margin-top: 0.5rem;">
            Your mental health matters • Available 24/7 • Always here to listen
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()