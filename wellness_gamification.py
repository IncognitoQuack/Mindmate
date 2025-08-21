# wellness_gamification.py - Gamification, Streaks, and Interactive Wellness Games
import streamlit as st
import json
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import os
import time
import math

class WellnessGamification:
    """Manages gamification, streaks, badges, and wellness challenges"""
    
    def __init__(self):
        self.initialize_gamification_state()
        self.badges_config = self._get_badges_config()
        self.challenges_config = self._get_challenges_config()
    
    def initialize_gamification_state(self):
        """Initialize gamification session state"""
        if "user_points" not in st.session_state:
            st.session_state.user_points = 0
        if "user_level" not in st.session_state:
            st.session_state.user_level = 1
        if "daily_streak" not in st.session_state:
            st.session_state.daily_streak = 0
        if "last_checkin" not in st.session_state:
            st.session_state.last_checkin = None
        if "badges_earned" not in st.session_state:
            st.session_state.badges_earned = []
        if "challenges_completed" not in st.session_state:
            st.session_state.challenges_completed = []
        if "wellness_stats" not in st.session_state:
            st.session_state.wellness_stats = {
                "meditation_minutes": 0,
                "journal_entries": 0,
                "breathing_sessions": 0,
                "mood_logs": 0,
                "gratitude_entries": 0
            }
        if "daily_mood_log" not in st.session_state:
            st.session_state.daily_mood_log = []
        if "weekly_progress" not in st.session_state:
            st.session_state.weekly_progress = {}
    
    def _get_badges_config(self) -> List[Dict]:
        """Define all available badges"""
        return [
            # Streak Badges
            {"id": "streak_3", "name": "Consistent", "desc": "3-day streak", "icon": "🔥", "requirement": {"type": "streak", "value": 3}, "points": 50},
            {"id": "streak_7", "name": "Dedicated", "desc": "7-day streak", "icon": "⭐", "requirement": {"type": "streak", "value": 7}, "points": 100},
            {"id": "streak_30", "name": "Committed", "desc": "30-day streak", "icon": "🏆", "requirement": {"type": "streak", "value": 30}, "points": 500},
            
            # Activity Badges
            {"id": "first_meditation", "name": "Mindful Beginner", "desc": "First meditation", "icon": "🧘", "requirement": {"type": "activity", "stat": "meditation_minutes", "value": 1}, "points": 25},
            {"id": "meditation_master", "name": "Zen Master", "desc": "100 minutes meditation", "icon": "🧘‍♂️", "requirement": {"type": "activity", "stat": "meditation_minutes", "value": 100}, "points": 200},
            {"id": "journal_starter", "name": "Self-Reflector", "desc": "5 journal entries", "icon": "📝", "requirement": {"type": "activity", "stat": "journal_entries", "value": 5}, "points": 75},
            {"id": "gratitude_guru", "name": "Gratitude Guru", "desc": "10 gratitude entries", "icon": "🙏", "requirement": {"type": "activity", "stat": "gratitude_entries", "value": 10}, "points": 100},
            
            # Mood Badges
            {"id": "mood_tracker", "name": "Mood Tracker", "desc": "Log mood 7 days", "icon": "📊", "requirement": {"type": "activity", "stat": "mood_logs", "value": 7}, "points": 80},
            {"id": "positive_vibes", "name": "Positive Vibes", "desc": "5 days of good mood", "icon": "😊", "requirement": {"type": "mood_streak", "value": 5}, "points": 150},
            
            # Level Badges
            {"id": "level_5", "name": "Rising Star", "desc": "Reach Level 5", "icon": "🌟", "requirement": {"type": "level", "value": 5}, "points": 200},
            {"id": "level_10", "name": "Wellness Warrior", "desc": "Reach Level 10", "icon": "⚔️", "requirement": {"type": "level", "value": 10}, "points": 500},
            
            # Special Badges
            {"id": "night_owl", "name": "Night Owl", "desc": "Late night session", "icon": "🦉", "requirement": {"type": "special", "condition": "night_session"}, "points": 30},
            {"id": "early_bird", "name": "Early Bird", "desc": "Morning session before 6 AM", "icon": "🐦", "requirement": {"type": "special", "condition": "early_session"}, "points": 30},
            {"id": "weekend_warrior", "name": "Weekend Warrior", "desc": "Weekend activity", "icon": "🎯", "requirement": {"type": "special", "condition": "weekend"}, "points": 40},
        ]
    
    def _get_challenges_config(self) -> List[Dict]:
        """Define daily and weekly challenges"""
        return [
            # Daily Challenges
            {"id": "daily_meditation", "name": "5-Minute Peace", "desc": "Meditate for 5 minutes", "type": "daily", "points": 20, "icon": "🧘"},
            {"id": "daily_gratitude", "name": "Grateful Heart", "desc": "Write 3 things you're grateful for", "type": "daily", "points": 15, "icon": "💝"},
            {"id": "daily_breathing", "name": "Breathe Deep", "desc": "Complete 3 breathing exercises", "type": "daily", "points": 15, "icon": "🌬️"},
            {"id": "daily_mood", "name": "Mood Check", "desc": "Log your mood 3 times", "type": "daily", "points": 10, "icon": "😊"},
            {"id": "daily_journal", "name": "Daily Reflection", "desc": "Write a journal entry", "type": "daily", "points": 25, "icon": "📔"},
            
            # Weekly Challenges
            {"id": "weekly_streak", "name": "Consistency King", "desc": "Maintain a 7-day streak", "type": "weekly", "points": 100, "icon": "👑"},
            {"id": "weekly_meditation", "name": "Meditation Week", "desc": "30 minutes total meditation", "type": "weekly", "points": 80, "icon": "🧘‍♀️"},
            {"id": "weekly_wellness", "name": "Wellness Champion", "desc": "Complete 10 wellness activities", "type": "weekly", "points": 120, "icon": "🏅"},
        ]
    
    def check_daily_streak(self) -> Tuple[bool, int]:
        """Check and update daily streak"""
        current_date = datetime.now().date()
        
        if st.session_state.last_checkin:
            last_checkin = datetime.fromisoformat(st.session_state.last_checkin).date()
            days_diff = (current_date - last_checkin).days
            
            if days_diff == 0:
                # Already checked in today
                return False, st.session_state.daily_streak
            elif days_diff == 1:
                # Consecutive day - increase streak
                st.session_state.daily_streak += 1
                st.session_state.last_checkin = current_date.isoformat()
                self.add_points(10, "Daily check-in streak!")
                return True, st.session_state.daily_streak
            else:
                # Streak broken - reset
                st.session_state.daily_streak = 1
                st.session_state.last_checkin = current_date.isoformat()
                return True, 1
        else:
            # First check-in
            st.session_state.daily_streak = 1
            st.session_state.last_checkin = current_date.isoformat()
            self.add_points(10, "First check-in!")
            return True, 1
    
    def add_points(self, points: int, reason: str = ""):
        """Add points and check for level up"""
        st.session_state.user_points += points
        
        # Check for level up (every 100 points = 1 level)
        new_level = (st.session_state.user_points // 100) + 1
        if new_level > st.session_state.user_level:
            st.session_state.user_level = new_level
            st.balloons()
            st.success(f"🎉 Level Up! You're now Level {new_level}!")
            self.check_badge_unlock("level", new_level)
        
        if reason:
            st.success(f"✨ +{points} points: {reason}")
    
    def update_wellness_stat(self, stat: str, value: int = 1):
        """Update wellness statistics"""
        if stat in st.session_state.wellness_stats:
            st.session_state.wellness_stats[stat] += value
            self.check_badge_unlock("activity", stat, st.session_state.wellness_stats[stat])
    
    def check_badge_unlock(self, requirement_type: str, stat: str = "", value: int = 0):
        """Check if any badges should be unlocked"""
        for badge in self.badges_config:
            if badge["id"] in st.session_state.badges_earned:
                continue
            
            req = badge["requirement"]
            unlocked = False
            
            if req["type"] == requirement_type:
                if requirement_type == "streak" and st.session_state.daily_streak >= req["value"]:
                    unlocked = True
                elif requirement_type == "level" and st.session_state.user_level >= req["value"]:
                    unlocked = True
                elif requirement_type == "activity" and stat == req.get("stat", "") and value >= req["value"]:
                    unlocked = True
                elif requirement_type == "special":
                    unlocked = self._check_special_condition(req["condition"])
            
            if unlocked:
                st.session_state.badges_earned.append(badge["id"])
                self.add_points(badge["points"], f"Badge unlocked: {badge['name']}!")
                st.balloons()
                return badge
        
        return None
    
    def _check_special_condition(self, condition: str) -> bool:
        """Check special badge conditions"""
        current_hour = datetime.now().hour
        current_day = datetime.now().weekday()
        
        if condition == "night_session" and (current_hour >= 22 or current_hour <= 2):
            return True
        elif condition == "early_session" and current_hour < 6:
            return True
        elif condition == "weekend" and current_day >= 5:
            return True
        
        return False
    
    def render_gamification_dashboard(self):
        """Render the main gamification dashboard"""
        st.markdown("""
        <style>
            .level-card {
                background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
                border-radius: 20px;
                padding: 2rem;
                color: white;
                text-align: center;
                box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                margin-bottom: 2rem;
            }
            .points-display {
                font-size: 3rem;
                font-weight: bold;
                margin: 1rem 0;
            }
            .level-progress {
                background: rgba(255,255,255,0.2);
                border-radius: 10px;
                height: 20px;
                overflow: hidden;
                margin: 1rem 0;
            }
            .level-progress-fill {
                background: linear-gradient(90deg, #FFD700, #FFA500);
                height: 100%;
                transition: width 0.5s ease;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Level and Points Card
        level_progress = (st.session_state.user_points % 100)
        st.markdown(f"""
        <div class="level-card">
            <h2 style="margin: 0;">Level {st.session_state.user_level} Wellness Warrior</h2>
            <div class="points-display">{st.session_state.user_points} Points</div>
            <div class="level-progress">
                <div class="level-progress-fill" style="width: {level_progress}%;"></div>
            </div>
            <p>{level_progress}/100 to next level</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Daily Streak Section
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔥 Current Streak", f"{st.session_state.daily_streak} days")
            if st.button("📅 Check In Today", use_container_width=True):
                checked_in, streak = self.check_daily_streak()
                if checked_in:
                    st.success(f"✅ Checked in! Streak: {streak} days")
                else:
                    st.info("Already checked in today!")
        
        with col2:
            st.metric("🏆 Badges Earned", len(st.session_state.badges_earned))
        
        with col3:
            st.metric("⭐ Total Activities", sum(st.session_state.wellness_stats.values()))
        
        # Tabs for different sections
        tab1, tab2, tab3, tab4 = st.tabs(["🎮 Challenges", "🏅 Badges", "🎯 Mini-Games", "📊 Stats"])
        
        with tab1:
            self.render_challenges()
        
        with tab2:
            self.render_badges()
        
        with tab3:
            self.render_mini_games()
        
        with tab4:
            self.render_stats()
    
    def render_challenges(self):
        """Render daily and weekly challenges"""
        st.markdown("### 🎯 Today's Challenges")
        
        daily_challenges = [c for c in self.challenges_config if c["type"] == "daily"]
        cols = st.columns(2)
        
        for idx, challenge in enumerate(daily_challenges):
            with cols[idx % 2]:
                completed = challenge["id"] in st.session_state.challenges_completed
                status = "✅" if completed else "⭕"
                
                st.markdown(f"""
                <div style="
                    background: {'linear-gradient(135deg, #D4EDDA 0%, #C3E6CB 100%)' if completed else 'linear-gradient(135deg, #F8F9FA 0%, #E9ECEF 100%)'};
                    padding: 1rem;
                    border-radius: 10px;
                    margin-bottom: 1rem;
                    border: 2px solid {'#28A745' if completed else '#DEE2E6'};
                ">
                    <h4>{status} {challenge['icon']} {challenge['name']}</h4>
                    <p style="margin: 0.5rem 0;">{challenge['desc']}</p>
                    <p style="margin: 0; color: #6C757D;">+{challenge['points']} points</p>
                </div>
                """, unsafe_allow_html=True)
                
                if not completed:
                    if st.button(f"Complete", key=f"complete_{challenge['id']}"):
                        st.session_state.challenges_completed.append(challenge["id"])
                        self.add_points(challenge["points"], f"Challenge completed: {challenge['name']}")
                        st.rerun()
    
    def render_badges(self):
        """Render badge collection"""
        st.markdown("### 🏅 Badge Collection")
        
        cols = st.columns(4)
        for idx, badge in enumerate(self.badges_config):
            with cols[idx % 4]:
                earned = badge["id"] in st.session_state.badges_earned
                opacity = "1" if earned else "0.3"
                
                st.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 1rem;
                    background: white;
                    border-radius: 15px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    opacity: {opacity};
                    transition: all 0.3s ease;
                    margin-bottom: 1rem;
                ">
                    <div style="font-size: 3rem;">{badge['icon']}</div>
                    <h5 style="margin: 0.5rem 0;">{badge['name']}</h5>
                    <p style="font-size: 0.8rem; color: #6C757D; margin: 0;">{badge['desc']}</p>
                    <p style="font-size: 0.7rem; color: #28A745; margin: 0.25rem 0;">+{badge['points']} pts</p>
                    {'<span style="color: #28A745; font-weight: bold;">✓ EARNED</span>' if earned else '<span style="color: #6C757D;">LOCKED</span>'}
                </div>
                """, unsafe_allow_html=True)
    
    def render_mini_games(self):
        """Render interactive mini-games"""
        st.markdown("### 🎮 Wellness Mini-Games")
        
        game_col1, game_col2 = st.columns(2)
        
        with game_col1:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%); padding: 1.5rem; border-radius: 15px; color: white;">
                <h4>🎯 Mood Matcher</h4>
                <p>Match your mood with activities</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Play Mood Matcher", key="mood_matcher", use_container_width=True):
                self.play_mood_matcher()
        
        with game_col2:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #F093FB 0%, #F5576C 100%); padding: 1.5rem; border-radius: 15px; color: white;">
                <h4>🧩 Mindfulness Puzzle</h4>
                <p>Solve calming puzzles</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button("Play Mindfulness Puzzle", key="mindfulness_puzzle", use_container_width=True):
                self.play_mindfulness_puzzle()
        
        # Breathing Pattern Game
        st.markdown("#### 🌬️ Breathing Pattern Challenge")
        if st.button("Start Breathing Challenge", key="breathing_challenge", use_container_width=True):
            self.play_breathing_challenge()
        
        # Gratitude Bingo
        st.markdown("#### 🎲 Gratitude Bingo")
        self.render_gratitude_bingo()
    
    def play_mood_matcher(self):
        """Mood matching mini-game"""
        moods = ["😊 Happy", "😔 Sad", "😰 Anxious", "😤 Angry", "😴 Tired"]
        activities = ["Take a walk", "Deep breathing", "Call a friend", "Listen to music", "Journal"]
        
        st.markdown("### Match the mood with the best activity!")
        
        selected_mood = random.choice(moods)
        st.info(f"Mood: {selected_mood}")
        
        activity_choice = st.radio("Best activity for this mood:", activities, key="mood_match_choice")
        
        if st.button("Submit Answer", key="submit_mood_match"):
            # Simple scoring - any answer is correct (it's about reflection)
            self.add_points(5, "Great job reflecting on mood management!")
            self.update_wellness_stat("mood_logs", 1)
            st.success("Excellent! Every activity can help in its own way!")
    
    def play_mindfulness_puzzle(self):
        """Simple mindfulness word puzzle"""
        words = ["CALM", "PEACE", "BREATHE", "RELAX", "FOCUS", "PRESENT", "GRATEFUL", "SERENE"]
        word = random.choice(words)
        scrambled = ''.join(random.sample(word, len(word)))
        
        st.markdown(f"### Unscramble this mindfulness word:")
        st.markdown(f"# {scrambled}")
        
        answer = st.text_input("Your answer:", key="puzzle_answer").upper()
        
        if st.button("Check Answer", key="check_puzzle"):
            if answer == word:
                self.add_points(10, "Puzzle solved!")
                st.success(f"🎉 Correct! The word was {word}")
                st.balloons()
            else:
                st.error(f"Not quite. Hint: It starts with '{word[0]}'")
    
    def play_breathing_challenge(self):
        """Interactive breathing challenge"""
        st.markdown("### 🌬️ Follow the breathing pattern!")
        
        pattern = ["Inhale 4s", "Hold 4s", "Exhale 4s", "Hold 4s"]
        placeholder = st.empty()
        
        if st.button("Start Pattern", key="start_breathing_pattern"):
            for _ in range(3):  # 3 cycles
                for step in pattern:
                    with placeholder.container():
                        st.markdown(f"""
                        <div style="
                            text-align: center;
                            padding: 3rem;
                            background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
                            border-radius: 20px;
                            color: white;
                        ">
                            <h1>{step}</h1>
                            <div style="font-size: 4rem;">{'🫁' if 'Inhale' in step else '⏸️' if 'Hold' in step else '💨'}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    time.sleep(4)
            
            placeholder.success("🎉 Great breathing session!")
            self.add_points(15, "Breathing challenge completed!")
            self.update_wellness_stat("breathing_sessions", 1)
    
    def render_gratitude_bingo(self):
        """Gratitude bingo game"""
        bingo_items = [
            "Thank someone", "Appreciate nature", "Grateful for health",
            "Value friendship", "Love family", "Enjoy a meal",
            "Sunshine", "Good sleep", "Kind gesture"
        ]
        
        if "bingo_board" not in st.session_state:
            st.session_state.bingo_board = random.sample(bingo_items, 9)
            st.session_state.bingo_checked = [False] * 9
        
        st.markdown("Check off things you're grateful for today:")
        
        cols = st.columns(3)
        for i in range(9):
            with cols[i % 3]:
                checked = st.checkbox(
                    st.session_state.bingo_board[i],
                    key=f"bingo_{i}",
                    value=st.session_state.bingo_checked[i]
                )
                st.session_state.bingo_checked[i] = checked
        
        checked_count = sum(st.session_state.bingo_checked)
        if checked_count >= 5 and st.button("Claim Bingo Reward!", key="claim_bingo"):
            self.add_points(20, "Gratitude Bingo completed!")
            self.update_wellness_stat("gratitude_entries", checked_count)
            st.session_state.bingo_board = random.sample(bingo_items, 9)
            st.session_state.bingo_checked = [False] * 9
            st.balloons()
            st.rerun()
    
    def render_stats(self):
        """Render wellness statistics"""
        st.markdown("### 📊 Your Wellness Journey")
        
        # Statistics grid
        col1, col2 = st.columns(2)
        
        with col1:
            for stat, value in list(st.session_state.wellness_stats.items())[:3]:
                st.metric(
                    stat.replace("_", " ").title(),
                    value,
                    delta=f"+{random.randint(1, 5)} this week"  # Mock delta
                )
        
        with col2:
            for stat, value in list(st.session_state.wellness_stats.items())[3:]:
                st.metric(
                    stat.replace("_", " ").title(),
                    value,
                    delta=f"+{random.randint(1, 5)} this week"  # Mock delta
                )
        
        # Mood trend chart
        if st.session_state.daily_mood_log:
            st.markdown("#### Mood Trend")
            mood_chart_data = {
                "Day": [f"Day {i+1}" for i in range(len(st.session_state.daily_mood_log))],
                "Mood": st.session_state.daily_mood_log
            }
            st.line_chart(mood_chart_data, x="Day", y="Mood", height=300)
        
        # Achievement progress
        total_badges = len(self.badges_config)
        earned_badges = len(st.session_state.badges_earned)
        progress = (earned_badges / total_badges) * 100
        
        st.markdown(f"""
        <div style="margin-top: 2rem;">
            <h4>Achievement Progress</h4>
            <div style="background: #E9ECEF; border-radius: 10px; height: 30px; overflow: hidden;">
                <div style="
                    background: linear-gradient(90deg, #28A745, #20C997);
                    height: 100%;
                    width: {progress}%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                ">
                    {earned_badges}/{total_badges} Badges
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

class MoodTracker:
    """Interactive mood tracking with visualization"""
    
    @staticmethod
    def render_mood_check_in():
        """Render mood check-in interface"""
        st.markdown("### 🎭 How are you feeling?")
        
        moods = {
            "😊": ("Great", 9),
            "🙂": ("Good", 7),
            "😐": ("Okay", 5),
            "😔": ("Down", 3),
            "😢": ("Struggling", 1)
        }
        
        cols = st.columns(5)
        selected_mood = None
        
        for idx, (emoji, (label, score)) in enumerate(moods.items()):
            with cols[idx]:
                if st.button(f"{emoji}\n{label}", key=f"mood_{label}", use_container_width=True):
                    selected_mood = score
                    st.session_state.daily_mood_log.append(score)
                    return score
        
        return None
    
    @staticmethod
    def render_mood_booster():
        """Suggest activities based on mood"""
        st.markdown("### 💫 Mood Boosters")
        
        boosters = [
            {"name": "5-Minute Walk", "icon": "🚶", "desc": "Fresh air and movement"},
            {"name": "Favorite Song", "icon": "🎵", "desc": "Music therapy"},
            {"name": "Deep Breaths", "icon": "🌬️", "desc": "Instant calm"},
            {"name": "Call a Friend", "icon": "📞", "desc": "Social connection"},
            {"name": "Gratitude List", "icon": "📝", "desc": "Positive focus"},
            {"name": "Funny Video", "icon": "😄", "desc": "Laughter therapy"}
        ]
        
        cols = st.columns(3)
        for idx, booster in enumerate(boosters):
            with cols[idx % 3]:
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #FFF5F5 0%, #FFE0E0 100%);
                    padding: 1rem;
                    border-radius: 10px;
                    text-align: center;
                    border: 1px solid #FFB3B3;
                    cursor: pointer;
                    transition: all 0.3s ease;
                ">
                    <div style="font-size: 2rem;">{booster['icon']}</div>
                    <h5 style="margin: 0.5rem 0;">{booster['name']}</h5>
                    <p style="font-size: 0.8rem; color: #666; margin: 0;">{booster['desc']}</p>
                </div>
                """, unsafe_allow_html=True)

class WellnessExercises:
    """Collection of interactive wellness exercises"""
    
    @staticmethod
    def render_meditation_timer():
        """Customizable meditation timer"""
        st.markdown("### 🧘 Meditation Timer")
        
        duration = st.slider("Duration (minutes)", 1, 30, 5)
        
        if st.button("Start Meditation", key="start_meditation", use_container_width=True):
            placeholder = st.empty()
            
            # Meditation phases
            phases = [
                ("Settling in...", 10),
                ("Focus on breath...", duration * 60 - 20),
                ("Returning to awareness...", 10)
            ]
            
            for phase_text, phase_duration in phases:
                with placeholder.container():
                    st.markdown(f"""
                    <div style="
                        text-align: center;
                        padding: 4rem;
                        background: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
                        border-radius: 20px;
                        color: white;
                    ">
                        <h2>{phase_text}</h2>
                        <div style="font-size: 5rem; margin: 2rem 0;">🧘</div>
                    </div>
                    """, unsafe_allow_html=True)
                time.sleep(min(phase_duration, 3))  # Cap at 3 seconds for demo
            
            placeholder.success(f"🎉 {duration} minute meditation completed!")
            
            # Update stats
            if "wellness_stats" in st.session_state:
                st.session_state.wellness_stats["meditation_minutes"] += duration
            
            return duration
        
        return 0
    
    @staticmethod
    def render_progressive_relaxation():
        """Progressive muscle relaxation guide"""
        st.markdown("### 💆 Progressive Muscle Relaxation")
        
        muscle_groups = [
            "Toes and feet", "Calves", "Thighs", "Abdomen",
            "Hands", "Arms", "Shoulders", "Neck", "Face"
        ]
        
        if st.button("Start Relaxation", key="start_relaxation", use_container_width=True):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for idx, muscle in enumerate(muscle_groups):
                progress = (idx + 1) / len(muscle_groups)
                progress_bar.progress(progress)
                
                status_text.markdown(f"""
                <div style="
                    text-align: center;
                    padding: 2rem;
                    background: linear-gradient(135deg, #E0F2FE 0%, #BAE6FD 100%);
                    border-radius: 15px;
                    margin: 1rem 0;
                ">
                    <h3>Focus on: {muscle}</h3>
                    <p>Tense for 5 seconds... then release...</p>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(2)  # Shortened for demo
            
            status_text.success("✨ Complete relaxation achieved!")
            st.balloons()

# Helper function to integrate with main app
def render_wellness_gamification_tab():
    """Main function to render gamification in a tab"""
    gamification = WellnessGamification()
    gamification.render_gamification_dashboard()

# Quick access functions for main app
def quick_mood_check():
    """Quick mood check widget for sidebar"""
    tracker = MoodTracker()
    mood_score = tracker.render_mood_check_in()
    if mood_score:
        st.success(f"Mood logged: {mood_score}/10")
        if mood_score <= 3:
            st.info("Consider trying a mood booster activity!")
            tracker.render_mood_booster()
    return mood_score

def daily_wellness_check():
    """Daily wellness check-in"""
    gamification = WellnessGamification()
    checked_in, streak = gamification.check_daily_streak()
    return checked_in, streak