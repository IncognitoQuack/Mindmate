# ui_components.py - Professional Light Theme UI Components with Animations
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime
import json
import random
import time
from typing import Dict, List, Optional


class LightThemeUI:
    """Professional light theme with smooth animations and positive vibes"""
    
    @staticmethod
    def inject_custom_css():
        """Inject professional light theme CSS with animations"""
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&display=swap');
            
            :root {
                --primary-color: #6366F1;
                --primary-light: #818CF8;
                --primary-dark: #4F46E5;
                --secondary-color: #14B8A6;
                --accent-color: #F59E0B;
                --success-color: #10B981;
                --warning-color: #F59E0B;
                --error-color: #EF4444;
                --bg-primary: #FFFFFF;
                --bg-secondary: #F9FAFB;
                --bg-tertiary: #F3F4F6;
                --card-bg: #FFFFFF;
                --text-primary: #111827;
                --text-secondary: #6B7280;
                --text-tertiary: #9CA3AF;
                --border-color: #E5E7EB;
                --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
                --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
                --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
                --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
                --gradient-primary: linear-gradient(135deg, #667EEA 0%, #764BA2 100%);
                --gradient-secondary: linear-gradient(135deg, #F093FB 0%, #F5576C 100%);
                --gradient-success: linear-gradient(135deg, #11998E 0%, #38EF7D 100%);
            }
            
            /* Main App Styling */
            .stApp {
                background: linear-gradient(135deg, #F5F7FA 0%, #C3CFE2 100%);
                font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
                color: var(--text-primary);
            }
            
            /* Hide Streamlit Elements */
            #MainMenu, footer, header {visibility: hidden;}
            
            /* Animated Header */
            .main-header {
                background: var(--card-bg);
                padding: 2.5rem;
                border-radius: 20px;
                margin-bottom: 2rem;
                box-shadow: var(--shadow-lg);
                border: 1px solid var(--border-color);
                position: relative;
                overflow: hidden;
                animation: slideDown 0.6s ease-out;
            }
            
            .main-header::before {
                content: '';
                position: absolute;
                top: 0;
                left: -100%;
                width: 100%;
                height: 3px;
                background: var(--gradient-primary);
                animation: slideAcross 3s ease-in-out infinite;
            }
            
            .main-header h1 {
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
                font-family: 'Poppins', sans-serif;
                animation: fadeInUp 0.8s ease-out;
            }
            
            .main-header p {
                color: var(--text-secondary);
                font-size: 1.1rem;
                margin-top: 0.5rem;
                animation: fadeInUp 0.8s ease-out 0.2s both;
            }
            
            /* Card Styling with Hover Effects */
            .clean-card {
                background: var(--card-bg);
                border-radius: 16px;
                padding: 1.75rem;
                margin-bottom: 1.5rem;
                box-shadow: var(--shadow-md);
                border: 1px solid var(--border-color);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;
                animation: fadeInUp 0.5s ease-out;
            }
            
            .clean-card:hover {
                box-shadow: var(--shadow-xl);
                transform: translateY(-4px);
                border-color: var(--primary-light);
            }
            
            .clean-card::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.05), transparent);
                transform: translateX(-100%);
                transition: transform 0.6s;
            }
            
            .clean-card:hover::after {
                transform: translateX(100%);
            }
            
            /* Chat Messages with Animation */
            .stChatMessage {
                background: var(--card-bg);
                border-radius: 16px;
                padding: 1.25rem;
                margin-bottom: 1rem;
                box-shadow: var(--shadow-md);
                border: 1px solid var(--border-color);
                animation: messageSlide 0.4s ease-out;
                transition: all 0.3s ease;
            }
            
            .stChatMessage:hover {
                box-shadow: var(--shadow-lg);
                transform: translateX(4px);
            }
            
            .stChatMessage[data-testid="user-message"] {
                background: linear-gradient(135deg, #E0E7FF 0%, #C7D2FE 100%);
                border-left: 3px solid var(--primary-color);
                margin-left: 2rem;
            }
            
            .stChatMessage[data-testid="assistant-message"] {
                background: linear-gradient(135deg, #F0F9FF 0%, #E0F2FE 100%);
                border-left: 3px solid var(--secondary-color);
                margin-right: 2rem;
            }
            
            /* Sidebar Styling */
            .css-1d391kg, [data-testid="stSidebar"] {
                background: linear-gradient(180deg, #FFFFFF 0%, #F9FAFB 100%);
                box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
                border-right: 1px solid var(--border-color);
            }
            
            /* Button Animations */
            .stButton > button {
                background: var(--gradient-primary);
                color: white;
                border: none;
                padding: 0.75rem 1.75rem;
                border-radius: 12px;
                font-weight: 600;
                font-size: 1rem;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                box-shadow: var(--shadow-md);
                font-family: 'Inter', sans-serif;
                cursor: pointer;
                position: relative;
                overflow: hidden;
            }
            
            .stButton > button::before {
                content: '';
                position: absolute;
                top: 50%;
                left: 50%;
                width: 0;
                height: 0;
                border-radius: 50%;
                background: rgba(255, 255, 255, 0.3);
                transform: translate(-50%, -50%);
                transition: width 0.6s, height 0.6s;
            }
            
            .stButton > button:hover::before {
                width: 300px;
                height: 300px;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: var(--shadow-xl);
            }
            
            /* Secondary Button Style */
            .secondary-button > button {
                background: transparent;
                color: var(--primary-color);
                border: 2px solid var(--primary-color);
            }
            
            .secondary-button > button:hover {
                background: var(--primary-color);
                color: white;
            }
            
            /* Tabs with Animation */
            .stTabs [data-baseweb="tab-list"] {
                background: var(--bg-secondary);
                padding: 0.5rem;
                border-radius: 12px;
                gap: 0.5rem;
                border: 1px solid var(--border-color);
                box-shadow: var(--shadow-sm);
            }
            
            .stTabs [data-baseweb="tab"] {
                background: transparent;
                color: var(--text-secondary);
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
                font-size: 0.95rem;
                border: none;
                transition: all 0.3s ease;
            }
            
            .stTabs [aria-selected="true"] {
                background: var(--gradient-primary);
                color: white;
                box-shadow: var(--shadow-md);
                animation: tabActivate 0.3s ease;
            }
            
            /* Input Fields */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                background: var(--bg-secondary);
                border: 2px solid var(--border-color);
                border-radius: 10px;
                padding: 0.75rem 1rem;
                font-size: 0.95rem;
                color: var(--text-primary);
                transition: all 0.3s ease;
            }
            
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {
                border-color: var(--primary-color);
                box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
                background: white;
            }
            
            /* Metric Cards with Animation */
            .metric-card {
                background: var(--card-bg);
                border-radius: 16px;
                padding: 1.75rem;
                text-align: center;
                box-shadow: var(--shadow-md);
                border: 1px solid var(--border-color);
                height: 100%;
                transition: all 0.3s ease;
                position: relative;
                overflow: hidden;
            }
            
            .metric-card::before {
                content: '';
                position: absolute;
                top: -50%;
                left: -50%;
                width: 200%;
                height: 200%;
                background: radial-gradient(circle, rgba(99, 102, 241, 0.05) 0%, transparent 70%);
                animation: pulse 3s ease-in-out infinite;
            }
            
            .metric-card:hover {
                transform: translateY(-5px);
                box-shadow: var(--shadow-xl);
                border-color: var(--primary-light);
            }
            
            .metric-value {
                font-size: 2.5rem;
                font-weight: 700;
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                margin: 0.5rem 0;
                animation: countUp 1s ease-out;
            }
            
            .metric-label {
                font-size: 0.875rem;
                color: var(--text-tertiary);
                text-transform: uppercase;
                letter-spacing: 1px;
                font-weight: 600;
            }
            
            /* Alert Styling */
            .stAlert {
                background: var(--bg-secondary);
                border-radius: 12px;
                border-left: 4px solid var(--info-color);
                box-shadow: var(--shadow-sm);
                animation: slideIn 0.3s ease-out;
            }
            
            .stSuccess {
                background: #ECFDF5;
                border-left-color: var(--success-color);
                color: var(--success-color);
            }
            
            .stWarning {
                background: #FFFBEB;
                border-left-color: var(--warning-color);
                color: var(--warning-color);
            }
            
            .stError {
                background: #FEF2F2;
                border-left-color: var(--error-color);
                color: var(--error-color);
            }
            
            /* Info Box */
            .info-box {
                background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%);
                border-radius: 12px;
                padding: 1.25rem;
                margin: 1rem 0;
                border-left: 3px solid var(--primary-color);
                box-shadow: var(--shadow-sm);
                animation: fadeInUp 0.5s ease-out;
            }
            
            /* Status Badge */
            .status-badge {
                display: inline-block;
                padding: 0.375rem 0.875rem;
                border-radius: 9999px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                animation: badgePop 0.3s ease;
            }
            
            .status-active {
                background: linear-gradient(135deg, #D1FAE5 0%, #A7F3D0 100%);
                color: #065F46;
                border: 1px solid #10B981;
            }
            
            .status-warning {
                background: linear-gradient(135deg, #FEF3C7 0%, #FDE68A 100%);
                color: #92400E;
                border: 1px solid #F59E0B;
            }
            
            /* Celebration Effect */
            .celebration {
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                pointer-events: none;
                z-index: 9999;
            }
            
            .confetti {
                position: absolute;
                width: 10px;
                height: 10px;
                background: var(--primary-color);
                animation: confettiFall 3s ease-out forwards;
            }
            
            /* Progress Bar Animation */
            .progress-bar {
                width: 100%;
                height: 8px;
                background: var(--bg-tertiary);
                border-radius: 4px;
                overflow: hidden;
                position: relative;
            }
            
            .progress-fill {
                height: 100%;
                background: var(--gradient-primary);
                border-radius: 4px;
                transition: width 0.6s ease;
                position: relative;
                overflow: hidden;
            }
            
            .progress-fill::after {
                content: '';
                position: absolute;
                top: 0;
                left: 0;
                bottom: 0;
                right: 0;
                background: linear-gradient(
                    90deg,
                    transparent,
                    rgba(255, 255, 255, 0.3),
                    transparent
                );
                animation: shimmer 2s infinite;
            }
            
            /* Floating Action Button */
            .fab {
                position: fixed;
                bottom: 2rem;
                right: 2rem;
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: var(--gradient-primary);
                box-shadow: var(--shadow-xl);
                display: flex;
                align-items: center;
                justify-content: center;
                cursor: pointer;
                transition: all 0.3s ease;
                z-index: 1000;
                animation: fabEntrance 0.5s ease-out;
            }
            
            .fab:hover {
                transform: scale(1.1) rotate(90deg);
                box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
            }
            
            /* Animations */
            @keyframes slideDown {
                from {
                    opacity: 0;
                    transform: translateY(-30px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes slideAcross {
                0% { left: -100%; }
                50% { left: 100%; }
                100% { left: 100%; }
            }
            
            @keyframes fadeInUp {
                from {
                    opacity: 0;
                    transform: translateY(20px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            @keyframes messageSlide {
                from {
                    opacity: 0;
                    transform: translateX(-20px);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes tabActivate {
                0% {
                    transform: scale(0.95);
                }
                50% {
                    transform: scale(1.05);
                }
                100% {
                    transform: scale(1);
                }
            }
            
            @keyframes pulse {
                0%, 100% {
                    transform: scale(1);
                    opacity: 0.5;
                }
                50% {
                    transform: scale(1.1);
                    opacity: 0.8;
                }
            }
            
            @keyframes countUp {
                from {
                    opacity: 0;
                    transform: scale(0.5);
                }
                to {
                    opacity: 1;
                    transform: scale(1);
                }
            }
            
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateX(-100%);
                }
                to {
                    opacity: 1;
                    transform: translateX(0);
                }
            }
            
            @keyframes badgePop {
                0% {
                    transform: scale(0);
                }
                50% {
                    transform: scale(1.2);
                }
                100% {
                    transform: scale(1);
                }
            }
            
            @keyframes confettiFall {
                0% {
                    transform: translateY(0) rotate(0deg);
                    opacity: 1;
                }
                100% {
                    transform: translateY(300px) rotate(720deg);
                    opacity: 0;
                }
            }
            
            @keyframes shimmer {
                0% {
                    transform: translateX(-100%);
                }
                100% {
                    transform: translateX(100%);
                }
            }
            
            @keyframes fabEntrance {
                from {
                    transform: scale(0) rotate(-180deg);
                }
                to {
                    transform: scale(1) rotate(0);
                }
            }
            
            /* Smooth Scrollbar */
            ::-webkit-scrollbar {
                width: 10px;
                height: 10px;
            }
            
            ::-webkit-scrollbar-track {
                background: var(--bg-secondary);
                border-radius: 5px;
            }
            
            ::-webkit-scrollbar-thumb {
                background: var(--primary-light);
                border-radius: 5px;
                transition: background 0.3s ease;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: var(--primary-color);
            }
            
            /* Loading Animation */
            .loading-dots {
                display: inline-flex;
                gap: 4px;
            }
            
            .loading-dot {
                width: 8px;
                height: 8px;
                border-radius: 50%;
                background: var(--primary-color);
                animation: dotPulse 1.4s ease-in-out infinite;
            }
            
            .loading-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .loading-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes dotPulse {
                0%, 80%, 100% {
                    transform: scale(0.8);
                    opacity: 0.5;
                }
                40% {
                    transform: scale(1.2);
                    opacity: 1;
                }
            }
            
            /* Tooltip */
            .tooltip {
                position: relative;
                display: inline-block;
            }
            
            .tooltip .tooltiptext {
                visibility: hidden;
                width: 200px;
                background: var(--text-primary);
                color: white;
                text-align: center;
                border-radius: 8px;
                padding: 8px 12px;
                position: absolute;
                z-index: 1;
                bottom: 125%;
                left: 50%;
                margin-left: -100px;
                opacity: 0;
                transition: opacity 0.3s;
                font-size: 0.875rem;
                box-shadow: var(--shadow-lg);
            }
            
            .tooltip:hover .tooltiptext {
                visibility: visible;
                opacity: 1;
            }
            
            /* Gradient Text */
            .gradient-text {
                background: var(--gradient-primary);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                font-weight: 600;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .main-header h1 {
                    font-size: 2rem;
                }
                
                .stChatMessage[data-testid="user-message"],
                .stChatMessage[data-testid="assistant-message"] {
                    margin-left: 0;
                    margin-right: 0;
                }
                
                .metric-card {
                    padding: 1.25rem;
                }
                
                .metric-value {
                    font-size: 2rem;
                }
            }
            
            /* Force black text in chat area and sidebar */
            .stChatMessage,
            .stChatMessage * {
                color: #111827 !important;
            }
            .css-1d391kg, [data-testid="stSidebar"], .css-1d391kg *, [data-testid="stSidebar"] * {
                color: #111827 !important;
            }
            
            /* Force black text in all text areas/inputs (Session Journal, etc) */
            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea {
                color: #111827 !important;
                background: #FFFFFF !important;
            }
            
            /* Sidebar headings and info cards: keep background white and text visible */
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] h4,
            [data-testid="stSidebar"] h5,
            [data-testid="stSidebar"] h6,
            [data-testid="stSidebar"] .info-box,
            [data-testid="stSidebar"] .clean-card {
                background: #FFFFFF !important;
                color: #111827 !important;
            }
            
            /* Prevent black background on extended/focused fields */
            .stTextInput > div > div > input:focus,
            .stTextArea > div > div > textarea:focus {
                background: #FFFFFF !important;
                color: #111827 !important;
                border-color: var(--primary-color) !important;
            }
        </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_animated_header(title: str, subtitle: str = ""):
        """Render animated header with gradient text"""
        return f"""
        <div class="main-header animate-in">
            <h1>{title}</h1>
            {f'<p>{subtitle}</p>' if subtitle else ''}
        </div>
        """
    
    @staticmethod
    def render_metric_card(label: str, value: str, icon: str = ""):
        """Render animated metric card"""
        return f"""
        <div class="metric-card">
            {f'<div style="font-size: 2rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''}
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
        """
    
    @staticmethod
    def render_progress_bar(progress: float, label: str = ""):
        """Render animated progress bar"""
        progress = min(100, max(0, progress))
        return f"""
        <div style="margin: 1rem 0;">
            {f'<div style="margin-bottom: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">{label}</div>' if label else ''}
            <div class="progress-bar">
                <div class="progress-fill" style="width: {progress}%;"></div>
            </div>
            <div style="margin-top: 0.25rem; font-size: 0.75rem; color: var(--text-tertiary);">{progress:.0f}%</div>
        </div>
        """
    
    @staticmethod
    def render_status_badge(status: str, type: str = "active"):
        """Render animated status badge"""
        badge_class = f"status-{type}"
        return f'<span class="status-badge {badge_class}">{status}</span>'
    
    @staticmethod
    def render_info_card(title: str, content: str, icon: str = "ℹ️"):
        """Render info card with animation"""
        return f"""
        <div class="info-box">
            <div style="display: flex; align-items: center; gap: 0.75rem; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{icon}</span>
                <strong style="font-size: 1.1rem; color: var(--text-primary);">{title}</strong>
            </div>
            <p style="margin: 0; color: var(--text-secondary);">{content}</p>
        </div>
        """
    
    @staticmethod
    def render_celebration_effect():
        """Render celebration animation for achievements"""
        confetti_colors = ['#6366F1', '#14B8A6', '#F59E0B', '#EF4444', '#8B5CF6']
        confetti_html = ""
        for i in range(20):
            color = random.choice(confetti_colors)
            left = random.randint(-200, 200)
            delay = random.random() * 2
            confetti_html += f"""
            <div class="confetti" style="
                background: {color};
                left: {left}px;
                animation-delay: {delay}s;
                transform: rotate({random.randint(0, 360)}deg);
            "></div>
            """
        
        return f"""
        <div class="celebration">
            {confetti_html}
        </div>
        """
    
    @staticmethod
    def render_loading_animation():
        """Render loading dots animation"""
        return """
        <div class="loading-dots">
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
            <div class="loading-dot"></div>
        </div>
        """
    
    @staticmethod
    def create_mood_gradient_chart(mood_data: List[int], labels: List[str]) -> go.Figure:
        """Create beautiful gradient mood chart"""
        fig = go.Figure()
        
        # Add gradient area chart
        fig.add_trace(go.Scatter(
            x=labels,
            y=mood_data,
            mode='lines+markers',
            name='Mood Journey',
            line=dict(
                color='#6366F1',
                width=3,
                shape='spline'
            ),
            marker=dict(
                size=10,
                color=mood_data,
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(
                    title="Mood Level",
                    thickness=15,
                    len=0.7
                ),
                line=dict(color='white', width=2)
            ),
            fill='tozeroy',
            fillcolor='rgba(99, 102, 241, 0.1)',
            hovertemplate='%{y}<extra></extra>'
        ))
        
        # Update layout with light theme
        fig.update_layout(
            title={
                'text': 'Your Emotional Journey',
                'font': {'size': 20, 'color': '#111827', 'family': 'Inter'}
            },
            xaxis=dict(
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                color='#6B7280'
            ),
            yaxis=dict(
                range=[0, 10],
                showgrid=True,
                gridcolor='rgba(0,0,0,0.05)',
                color='#6B7280',
                title='Mood Level'
            ),
            paper_bgcolor='rgba(255,255,255,0.9)',
            plot_bgcolor='rgba(249,250,251,0.5)',
            height=350,
            margin=dict(l=20, r=20, t=60, b=20),
            hovermode='x unified',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def render_welcome_animation():
        """Render welcome animation for new users"""
        return """
        <div style="text-align: center; padding: 2rem; animation: fadeInUp 1s ease-out;">
            <div style="font-size: 4rem; margin-bottom: 1rem; animation: pulse 2s ease-in-out infinite;">
                🧠
            </div>
            <h2 class="gradient-text" style="font-size: 2rem; margin-bottom: 0.5rem;">
                Welcome to Mindmate AI
            </h2>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Your compassionate companion for mental wellness
            </p>
        </div>
        """
    
    @staticmethod
    def render_achievement_card(title: str, description: str, icon: str, unlocked: bool = False):
        """Render achievement/badge card"""
        opacity = "1" if unlocked else "0.4"
        border = "2px solid var(--primary-color)" if unlocked else "2px solid var(--border-color)"
        
        return f"""
        <div class="clean-card" style="
            opacity: {opacity};
            border: {border};
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
        ">
            <div style="font-size: 3rem; margin-bottom: 0.75rem;">
                {icon}
            </div>
            <h4 style="color: var(--text-primary); margin: 0.5rem 0; font-size: 1.1rem;">
                {title}
            </h4>
            <p style="color: var(--text-secondary); font-size: 0.875rem; margin: 0;">
                {description}
            </p>
            {f'<div class="status-badge status-active" style="margin-top: 0.75rem;">UNLOCKED</div>' if unlocked else ''}
        </div>
        """
    
    @staticmethod
    def render_floating_action_button(icon: str = "💬"):
        """Render floating action button"""
        return f"""
        <div class="fab">
            <span style="font-size: 1.5rem; color: white;">{icon}</span>
        </div>
        """

class AnimationEffects:
    """Collection of animation effects for different interactions"""
    
    @staticmethod
    def success_animation():
        """Show success animation"""
        st.balloons()
    
    @staticmethod
    def celebration_effect():
        """Show celebration for achievements"""
        st.snow()
    
    @staticmethod
    def typing_effect(text: str, placeholder):
        """Create typing effect for text"""
        typed_text = ""
        for char in text:
            typed_text += char
            placeholder.markdown(typed_text)
            time.sleep(0.02)

# Helper functions for quick UI components
def create_card(content: str, title: str = "", type: str = "default"):
    """Quick function to create a styled card"""
    title_html = f"<h3 style='margin-top: 0;'>{title}</h3>" if title else ""
    return f"""
    <div class="clean-card">
        {title_html}
        {content}
    </div>
    """

def create_metric_row(metrics: List[Dict]):
    """Create a row of metrics"""
    cols = st.columns(len(metrics))
    for col, metric in zip(cols, metrics):
        with col:
            st.markdown(
                LightThemeUI.render_metric_card(
                    metric.get('label', ''),
                    metric.get('value', ''),
                    metric.get('icon', '')
                ),
                unsafe_allow_html=True
            )

def show_toast(message: str, type: str = "success"):
    """Show toast notification"""
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    else:
        st.info(message)