# community_features.py - Lightweight, innovative community features without external dependencies
import streamlit as st
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
import re

class MindmateCommunity:
    """Lightweight, self-contained community features with innovative approaches"""
    
    def __init__(self):
        self.initialize_community_state()
        self.affirmations = self._get_affirmations_pool()
        self.wisdom_quotes = self._get_wisdom_quotes()
        self.support_templates = self._get_support_templates()
    
    def initialize_community_state(self):
        """Initialize community session state - no external files needed"""
        if "community_messages" not in st.session_state:
            # Store messages in session - ephemeral but perfect for mental health privacy
            st.session_state.community_messages = self._get_sample_messages()
        
        if "user_avatar" not in st.session_state:
            # Generate anonymous avatar
            st.session_state.user_avatar = self._generate_avatar()
        
        if "support_given" not in st.session_state:
            st.session_state.support_given = 0
        
        if "support_received" not in st.session_state:
            st.session_state.support_received = 0
        
        if "daily_affirmation" not in st.session_state:
            st.session_state.daily_affirmation = None
        
        if "mood_room" not in st.session_state:
            st.session_state.mood_room = "general"
        
        if "anonymous_id" not in st.session_state:
            st.session_state.anonymous_id = self._generate_anonymous_id()
    
    def _generate_anonymous_id(self) -> str:
        """Generate anonymous but consistent ID for the session"""
        timestamp = str(datetime.now().timestamp())
        return hashlib.md5(timestamp.encode()).hexdigest()[:8]
    
    def _generate_avatar(self) -> Dict:
        """Generate random anonymous avatar with emoji and color"""
        avatars = ["🦋", "🌟", "🌈", "🌸", "🍀", "🦄", "🐨", "🦉", "🐢", "🦊", "🌺", "🌙"]
        colors = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FECA57", "#DDA0DD", "#98D8C8", "#FFB6C1"]
        names = ["Hopeful", "Peaceful", "Brave", "Gentle", "Caring", "Strong", "Wise", "Kind", "Calm", "Bright"]
        animals = ["Butterfly", "Star", "Rainbow", "Flower", "Clover", "Unicorn", "Koala", "Owl", "Turtle", "Fox"]
        
        return {
            "emoji": random.choice(avatars),
            "color": random.choice(colors),
            "name": f"{random.choice(names)} {random.choice(animals)}"
        }
    
    def _get_sample_messages(self) -> List[Dict]:
        """Get sample supportive messages to populate community"""
        return [
            {
                "id": "msg1",
                "avatar": {"emoji": "🦋", "color": "#FF6B6B", "name": "Hopeful Butterfly"},
                "content": "Remember that it's okay to take things one day at a time. You're doing better than you think! 💪",
                "timestamp": datetime.now() - timedelta(hours=2),
                "supports": 12,
                "room": "encouragement",
                "replies": []
            },
            {
                "id": "msg2",
                "avatar": {"emoji": "🌟", "color": "#4ECDC4", "name": "Peaceful Star"},
                "content": "Just completed my 5-minute breathing exercise. Feeling so much calmer. Small steps matter! 🧘",
                "timestamp": datetime.now() - timedelta(hours=5),
                "supports": 8,
                "room": "victories",
                "replies": []
            },
            {
                "id": "msg3",
                "avatar": {"emoji": "🌈", "color": "#45B7D1", "name": "Brave Rainbow"},
                "content": "Having a tough day but choosing to be grateful for the small things. What are you grateful for today?",
                "timestamp": datetime.now() - timedelta(hours=8),
                "supports": 15,
                "room": "gratitude",
                "replies": []
            }
        ]
    
    def _get_affirmations_pool(self) -> List[str]:
        """Pool of positive affirmations"""
        return [
            "You are stronger than you know 💪",
            "Every small step forward is progress 🌱",
            "You deserve kindness, especially from yourself 💝",
            "Your feelings are valid and temporary 🌈",
            "You've survived 100% of your bad days 🌟",
            "It's okay to rest and recharge 🔋",
            "You are worthy of love and respect 💖",
            "Today is a new opportunity to grow 🌸",
            "Your presence makes a difference 🦋",
            "You are not alone in this journey 🤝",
            "Healing is not linear, be patient with yourself 🌊",
            "You have the power to write your story 📖",
            "Every breath is a new beginning 🌬️",
            "You are exactly where you need to be 🧭",
            "Your best is enough, always 🌺"
        ]
    
    def _get_wisdom_quotes(self) -> List[Dict]:
        """Curated wisdom quotes with authors"""
        return [
            {"quote": "The only way out is through.", "author": "Robert Frost"},
            {"quote": "You are not your thoughts.", "author": "Eckhart Tolle"},
            {"quote": "This too shall pass.", "author": "Persian Proverb"},
            {"quote": "Be yourself; everyone else is already taken.", "author": "Oscar Wilde"},
            {"quote": "The wound is the place where the Light enters you.", "author": "Rumi"},
            {"quote": "What we resist, persists.", "author": "Carl Jung"},
            {"quote": "The present moment is all we ever have.", "author": "Thich Nhat Hanh"},
            {"quote": "Happiness is not by chance, but by choice.", "author": "Jim Rohn"}
        ]
    
    def _get_support_templates(self) -> List[str]:
        """Quick support message templates"""
        return [
            "You've got this! 💪",
            "Sending you positive vibes ✨",
            "Thank you for sharing 💝",
            "I hear you and you're valid 🤗",
            "Keep going, you're amazing! 🌟",
            "Your strength inspires me 🦋",
            "Together we're stronger 🤝",
            "Proud of you! 🎉",
            "One step at a time 👣",
            "You matter! 💖"
        ]
    
    def render_community_hub(self):
        """Main community interface"""
        st.markdown("""
        <style>
            .mood-room-card {
                background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
                border-radius: 15px;
                padding: 1.5rem;
                color: white;
                text-align: center;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 1rem;
            }
            .mood-room-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            }
            .message-bubble {
                background: #F8F9FA;
                border-radius: 15px;
                padding: 1.25rem;
                margin-bottom: 1rem;
                border-left: 4px solid var(--primary-color);
                box-shadow: 0 2px 10px rgba(0,0,0,0.05);
                transition: all 0.3s ease;
            }
            .message-bubble:hover {
                transform: translateX(5px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            }
            .support-btn {
                background: linear-gradient(135deg, #FFB6C1 0%, #FFC0CB 100%);
                border: none;
                padding: 0.5rem 1rem;
                border-radius: 20px;
                color: #C71585;
                font-weight: bold;
                cursor: pointer;
                transition: all 0.3s ease;
            }
            .support-btn:hover {
                transform: scale(1.05);
                box-shadow: 0 5px 15px rgba(255,182,193,0.4);
            }
            .avatar-circle {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                font-size: 1.5rem;
                margin-right: 0.75rem;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Header with user's anonymous avatar
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"""
            <div style="display: flex; align-items: center;">
                <div class="avatar-circle" style="background: {st.session_state.user_avatar['color']};">
                    {st.session_state.user_avatar['emoji']}
                </div>
                <div>
                    <h3 style="margin: 0;">Welcome, {st.session_state.user_avatar['name']}</h3>
                    <p style="margin: 0; color: #6C757D;">Your safe space to connect</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.metric("💝 Support Given", st.session_state.support_given)
        
        with col3:
            st.metric("🤗 Support Received", st.session_state.support_received)
        
        # Main tabs
        tab1, tab2, tab3, tab4 = st.tabs(["🏠 Mood Rooms", "💬 Peer Support", "✨ Daily Wisdom", "🎯 Wellness Buddy"])
        
        with tab1:
            self.render_mood_rooms()
        
        with tab2:
            self.render_peer_support()
        
        with tab3:
            self.render_daily_wisdom()
        
        with tab4:
            self.render_wellness_buddy()
    
    def render_mood_rooms(self):
        """Themed rooms for different emotional states"""
        st.markdown("### 🏠 Choose Your Mood Room")
        st.info("Connect with others experiencing similar feelings in a safe, anonymous space")
        
        rooms = [
            {"id": "gratitude", "name": "Gratitude Garden", "emoji": "🌻", "desc": "Share what you're thankful for", "color": "#FFD700"},
            {"id": "encouragement", "name": "Encouragement Corner", "emoji": "💪", "desc": "Give and receive motivation", "color": "#FF69B4"},
            {"id": "victories", "name": "Small Victories", "emoji": "🎉", "desc": "Celebrate your wins, big or small", "color": "#98D8C8"},
            {"id": "mindful", "name": "Mindful Moments", "emoji": "🧘", "desc": "Share mindfulness experiences", "color": "#DDA0DD"},
            {"id": "creative", "name": "Creative Outlet", "emoji": "🎨", "desc": "Express through creativity", "color": "#87CEEB"},
            {"id": "night", "name": "Night Owls", "emoji": "🌙", "desc": "Late night support", "color": "#483D8B"}
        ]
        
        cols = st.columns(3)
        for idx, room in enumerate(rooms):
            with cols[idx % 3]:
                if st.button(
                    f"{room['emoji']} {room['name']}\n{room['desc']}", 
                    key=f"room_{room['id']}", 
                    use_container_width=True
                ):
                    st.session_state.mood_room = room['id']
                    st.rerun()
        
        # Show messages from selected room
        current_room = st.session_state.mood_room
        st.markdown(f"### 💬 Messages in {[r['name'] for r in rooms if r['id'] == current_room][0] if current_room != 'general' else 'General Room'}")
        
        # Filter messages by room
        room_messages = [m for m in st.session_state.community_messages if m.get('room', 'general') == current_room]
        
        if room_messages:
            for msg in sorted(room_messages, key=lambda x: x['timestamp'], reverse=True):
                self.render_message(msg)
        else:
            st.info("Be the first to share in this room! 🌟")
        
        # Quick share box
        with st.expander("✍️ Share Your Thoughts"):
            new_message = st.text_area("What's on your mind? (Anonymous)", max_chars=280)
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("Share Anonymously 🦋", use_container_width=True):
                    if new_message:
                        self.add_community_message(new_message, current_room)
                        st.success("Your message has been shared! Thank you for contributing 💝")
                        st.rerun()
            with col2:
                if st.button("Add Emoji", use_container_width=True):
                    emojis = ["💪", "🌈", "✨", "🤗", "💝", "🌟", "🦋", "🌸"]
                    new_message += random.choice(emojis)
    
    def render_message(self, message: Dict):
        """Render a single community message"""
        time_ago = self.get_time_ago(message['timestamp'])
        
        st.markdown(f"""
        <div class="message-bubble">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div style="display: flex; align-items: center;">
                    <div class="avatar-circle" style="background: {message['avatar']['color']};">
                        {message['avatar']['emoji']}
                    </div>
                    <div>
                        <strong>{message['avatar']['name']}</strong>
                        <span style="color: #6C757D; font-size: 0.85rem; margin-left: 0.5rem;">{time_ago}</span>
                    </div>
                </div>
            </div>
            <p style="margin: 0.75rem 0; color: #333;">{message['content']}</p>
            <div style="display: flex; gap: 1rem; align-items: center;">
                <span style="color: #E91E63;">💝 {message['supports']} supports</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 3])
        with col1:
            if st.button("💝 Support", key=f"support_{message['id']}"):
                message['supports'] += 1
                st.session_state.support_given += 1
                st.rerun()
        
        with col2:
            if st.button("💬 Reply", key=f"reply_{message['id']}"):
                st.session_state[f"replying_to_{message['id']}"] = True
        
        # Quick reply templates
        if st.session_state.get(f"replying_to_{message['id']}", False):
            with st.container():
                st.markdown("**Quick Support:**")
                cols = st.columns(4)
                for idx, template in enumerate(self.support_templates[:4]):
                    with cols[idx]:
                        if st.button(template, key=f"template_{message['id']}_{idx}"):
                            self.add_reply(message['id'], template)
                            st.session_state[f"replying_to_{message['id']}"] = False
                            st.rerun()
    
    def render_peer_support(self):
        """Anonymous peer support system"""
        st.markdown("### 🤝 Peer Support Circle")
        st.info("Connect with a random peer for mutual support - completely anonymous")
        
        # Peer matching system
        if st.button("🔄 Find Support Buddy", use_container_width=True):
            # Simulate finding a peer
            peer = self._generate_avatar()
            st.success(f"Matched with {peer['name']} {peer['emoji']}")
            
            # Generate conversation starter
            starters = [
                "What's one thing you're grateful for today?",
                "What small victory did you have this week?",
                "What's helping you cope lately?",
                "What self-care activity do you enjoy?",
                "What's one kind thing you did for yourself today?"
            ]
            
            st.markdown(f"""
            <div style="background: #E8F5E9; padding: 1.5rem; border-radius: 10px; margin: 1rem 0;">
                <h4>Conversation Starter:</h4>
                <p style="font-size: 1.1rem; color: #2E7D32;">"{random.choice(starters)}"</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Support exchange
        st.markdown("#### 💌 Support Exchange")
        support_type = st.radio(
            "What kind of support are you looking for?",
            ["Just need someone to listen", "Seeking encouragement", "Want to share a victory", "Looking for coping tips"]
        )
        
        if st.button("Post Support Request", use_container_width=True):
            st.success("Your request has been posted anonymously. Someone will respond soon! 💝")
            st.session_state.support_received += 1
        
        # Show recent support exchanges
        st.markdown("#### Recent Support Exchanges")
        exchanges = [
            {"type": "encouragement", "given": 5, "received": 8},
            {"type": "listening", "given": 3, "received": 4},
            {"type": "tips", "given": 7, "received": 6}
        ]
        
        for exchange in exchanges:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(f"**{exchange['type'].title()}**")
            with col2:
                st.write(f"Given: {exchange['given']}")
            with col3:
                st.write(f"Received: {exchange['received']}")
    
    def render_daily_wisdom(self):
        """Daily affirmations and wisdom sharing"""
        st.markdown("### ✨ Daily Wisdom & Affirmations")
        
        # Daily affirmation
        today = datetime.now().date()
        if st.session_state.daily_affirmation is None or st.session_state.get('affirmation_date') != today:
            st.session_state.daily_affirmation = random.choice(self.affirmations)
            st.session_state.affirmation_date = today
        
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
            padding: 2rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
        ">
            <h2 style="margin: 0;">Today's Affirmation</h2>
            <p style="font-size: 1.3rem; margin: 1rem 0;">"{st.session_state.daily_affirmation}"</p>
            <p style="font-size: 0.9rem; opacity: 0.9;">Repeat this to yourself today 💫</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Wisdom quote
        quote = random.choice(self.wisdom_quotes)
        st.markdown(f"""
        <div style="
            background: #F8F9FA;
            padding: 1.5rem;
            border-radius: 10px;
            border-left: 4px solid #6366F1;
            margin: 1rem 0;
        ">
            <p style="font-style: italic; font-size: 1.1rem; margin: 0;">"{quote['quote']}"</p>
            <p style="text-align: right; color: #6C757D; margin: 0.5rem 0 0 0;">— {quote['author']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Community affirmation wall
        st.markdown("#### 🌟 Community Affirmation Wall")
        st.info("Share an affirmation that helps you")
        
        user_affirmation = st.text_input("Add your affirmation to the wall:")
        if st.button("Add to Wall 🌟", use_container_width=True):
            if user_affirmation:
                st.success("Your affirmation has been added to the wall! 💝")
                self.affirmations.append(user_affirmation)
        
        # Display affirmation wall
        st.markdown("#### 💫 Affirmations from the Community")
        cols = st.columns(2)
        for idx, affirmation in enumerate(random.sample(self.affirmations, min(6, len(self.affirmations)))):
            with cols[idx % 2]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #FFE0EC 0%, #FFC0CB 100%);
                    padding: 1rem;
                    border-radius: 10px;
                    margin-bottom: 0.5rem;
                    text-align: center;
                ">
                    <p style="margin: 0; color: #C71585;">{affirmation}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_wellness_buddy(self):
        """AI-powered wellness buddy for personalized support"""
        st.markdown("### 🎯 Your Wellness Buddy")
        st.info("Get personalized wellness suggestions based on community wisdom")
        
        # Mood-based recommendations
        st.markdown("#### How are you feeling right now?")
        mood_cols = st.columns(5)
        moods = ["😊 Great", "🙂 Good", "😐 Okay", "😔 Low", "😰 Anxious"]
        
        selected_mood = None
        for idx, mood in enumerate(moods):
            with mood_cols[idx]:
                if st.button(mood, key=f"buddy_mood_{idx}", use_container_width=True):
                    selected_mood = mood
                    
                    # Generate personalized recommendations
                    recommendations = self.get_mood_recommendations(mood)
                    
                    st.markdown("#### 💡 Personalized Suggestions")
                    for rec in recommendations:
                        st.markdown(f"""
                        <div style="
                            background: #E8F5E9;
                            padding: 1rem;
                            border-radius: 10px;
                            margin-bottom: 0.5rem;
                            border-left: 3px solid #4CAF50;
                        ">
                            <strong>{rec['activity']}</strong>
                            <p style="margin: 0.5rem 0 0 0; color: #555;">{rec['benefit']}</p>
                        </div>
                        """, unsafe_allow_html=True)
        
        # Wellness challenges from community
        st.markdown("#### 🏆 Community Wellness Challenges")
        challenges = [
            {"name": "Gratitude Chain", "participants": 47, "desc": "Share 3 things you're grateful for"},
            {"name": "Mindful Minutes", "participants": 32, "desc": "5 minutes of mindfulness daily"},
            {"name": "Kindness Ripple", "participants": 28, "desc": "One act of self-kindness daily"}
        ]
        
        for challenge in challenges:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{challenge['name']}** - {challenge['desc']}")
                st.caption(f"👥 {challenge['participants']} participants")
            with col2:
                if st.button("Join", key=f"join_{challenge['name']}", use_container_width=True):
                    st.success(f"You've joined {challenge['name']}! 🎉")
        
        # Community insights
        st.markdown("#### 📊 Community Wellness Insights")
        insights = {
            "Most helpful activity": "Deep breathing (78% found helpful)",
            "Popular time for self-care": "Evening (6-8 PM)",
            "Average mood improvement": "+2.3 points after activities",
            "Top coping strategy": "Journaling and gratitude practice"
        }
        
        for key, value in insights.items():
            st.metric(key, value)
    
    def get_mood_recommendations(self, mood: str) -> List[Dict]:
        """Get personalized recommendations based on mood"""
        recommendations = {
            "😊 Great": [
                {"activity": "Share your joy", "benefit": "Spreading positivity helps others"},
                {"activity": "Gratitude journal", "benefit": "Amplify positive feelings"},
                {"activity": "Help someone", "benefit": "Kindness boosts happiness"}
            ],
            "🙂 Good": [
                {"activity": "Mindful walking", "benefit": "Maintain your positive state"},
                {"activity": "Creative expression", "benefit": "Channel good energy creatively"},
                {"activity": "Connect with friends", "benefit": "Share your good vibes"}
            ],
            "😐 Okay": [
                {"activity": "Gentle stretching", "benefit": "Activate your body gently"},
                {"activity": "Listen to music", "benefit": "Shift your emotional state"},
                {"activity": "Small accomplishment", "benefit": "Build momentum"}
            ],
            "😔 Low": [
                {"activity": "Self-compassion break", "benefit": "Be kind to yourself"},
                {"activity": "Reach out to someone", "benefit": "Connection helps healing"},
                {"activity": "Comfort activity", "benefit": "It's okay to rest"}
            ],
            "😰 Anxious": [
                {"activity": "4-7-8 breathing", "benefit": "Activate calm response"},
                {"activity": "Grounding exercise", "benefit": "Return to present moment"},
                {"activity": "Progressive relaxation", "benefit": "Release physical tension"}
            ]
        }
        
        return recommendations.get(mood, [])
    
    def add_community_message(self, content: str, room: str):
        """Add a new message to the community"""
        new_message = {
            "id": f"msg_{len(st.session_state.community_messages) + 1}",
            "avatar": st.session_state.user_avatar,
            "content": content,
            "timestamp": datetime.now(),
            "supports": 0,
            "room": room,
            "replies": []
        }
        st.session_state.community_messages.append(new_message)
    
    def add_reply(self, message_id: str, reply_content: str):
        """Add a reply to a message"""
        for msg in st.session_state.community_messages:
            if msg['id'] == message_id:
                msg['replies'].append({
                    "avatar": st.session_state.user_avatar,
                    "content": reply_content,
                    "timestamp": datetime.now()
                })
                break
    
    def get_time_ago(self, timestamp: datetime) -> str:
        """Convert timestamp to 'time ago' format"""
        now = datetime.now()
        diff = now - timestamp
        
        if diff.days > 0:
            return f"{diff.days}d ago"
        elif diff.seconds > 3600:
            return f"{diff.seconds // 3600}h ago"
        elif diff.seconds > 60:
            return f"{diff.seconds // 60}m ago"
        else:
            return "just now"

# Helper function for main app integration
def render_community_tab():
    """Main function to render community features in a tab"""
    community = MindmateCommunity()
    community.render_community_hub()

# Quick access widgets for sidebar
def get_daily_affirmation() -> str:
    """Get today's affirmation for sidebar widget"""
    community = MindmateCommunity()
    if st.session_state.daily_affirmation is None:
        st.session_state.daily_affirmation = random.choice(community.affirmations)
    return st.session_state.daily_affirmation

def get_community_stats() -> Dict:
    """Get community statistics for display"""
    return {
        "active_members": random.randint(150, 300),  # Simulated for privacy
        "support_given_today": random.randint(50, 150),
        "messages_shared": len(st.session_state.get('community_messages', [])),
        "mood_rooms_active": 6
    }

def quick_support_widget():
    """Quick support widget for sidebar"""
    st.markdown("### 💝 Quick Support")
    templates = ["You've got this! 💪", "Sending love 💖", "Stay strong 🌟"]
    for template in templates:
        if st.button(template, key=f"quick_{template}", use_container_width=True):
            st.success("Support sent to community!")
            if "support_given" in st.session_state:
                st.session_state.support_given += 1