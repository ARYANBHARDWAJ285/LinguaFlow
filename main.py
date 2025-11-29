import os
import streamlit as st
from dotenv import load_dotenv
import streamlit as st
from streamlit_mic_recorder import speech_to_text
import google.generativeai as genai
from gtts import gTTS
import base64
import time

# ==========================================
# 1. BRAIN SETUP (The Logic)
# ==========================================
# Load API key from .env file (do NOT hard-code it)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))
GOOGLE_API_KEY = os.getenv("PASTE_YOUR_KEY_HERE")

if not GOOGLE_API_KEY:
    st.error("⚠️ ERROR: No GOOGLE_API_KEY found. Create a .env file in d:\\Pyhton\\Agent with GOOGLE_API_KEY=YOUR_KEY")
    st.stop()

genai.configure(api_key="PASTE_YOUR_KEY_HERE")              // I hide my google API for security purpoase
model = genai.GenerativeModel('gemini-1.5-flash')

# Page Config
st.set_page_config(page_title="LinguaFlow", layout="wide", page_icon="📹")

# ==========================================
# 2. THE DESIGN (CSS Injection)
# ==========================================
# This makes Python look like your Figma Design
st.markdown("""
<style>
    /* 1. DARK THEME & BACKGROUND */
    .stApp { background-color: #0f1014; }
    
    /* 2. GLASSMORPHISM PANELS */
    .glass-panel {
        background: rgba(30, 32, 38, 0.95);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 20px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
    }

    /* 3. VIDEO FRAMES */
    .video-frame {
        border-radius: 24px;
        border: 4px solid #333;
        overflow: hidden;
        position: relative;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
    }
    .video-frame:hover { transform: scale(1.02); }
    
    .name-tag {
        position: absolute;
        bottom: 20px; left: 20px;
        background: rgba(0,0,0,0.8);
        color: white;
        padding: 5px 15px;
        border-radius: 10px;
        font-weight: bold;
    }

    /* 4. CHAT BOX */
    .chat-bubble-user {
        background-color: #2563eb;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0 15px;
        margin-bottom: 10px;
        text-align: right;
    }
    .chat-bubble-ai {
        background-color: #374151;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 15px 0;
        margin-bottom: 10px;
        text-align: left;
    }

    /* 5. HIDE DEFAULT STREAMLIT ELEMENTS */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stButton>button {
        border-radius: 50px;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HELPER FUNCTIONS
# ==========================================
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    md = f"""
        <audio autoplay="true">
        <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
        </audio>
        """
    st.markdown(md, unsafe_allow_html=True)

# Initialize Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "ai", "content": "Hi! I am Sarah. Ready to practice English?"}
    ]

# ==========================================
# 4. THE LAYOUT (Header & Grid)
# ==========================================

# --- HEADER ---
c1, c2, c3 = st.columns([1, 6, 1])
with c1:
    st.markdown('<div class="glass-panel" style="text-align:center; padding:10px;">🇬🇧 English (US)</div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="glass-panel" style="text-align:center; padding:10px;">⏱️ 45:00 / 60:00</div>', unsafe_allow_html=True)

st.write("") # Spacer

# --- MAIN VIDEO GRID ---
col_user, col_ai = st.columns(2)

with col_user:
    st.markdown("""
    <div class="video-frame">
        <img src="https://images.unsplash.com/photo-1548142813-c348350df52b?w=800&q=80" style="width:100%; display:block;">
        <div class="name-tag">👤 You</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    st.info("👇 Click below to speak")
    
    # THE MICROPHONE (Real Logic)
    # This button connects to your microphone
    user_voice_input = speech_to_text(
        language='en',
        start_prompt="🎤 START SPEAKING",
        stop_prompt="⏹️ STOP & SEND",
        just_once=False,
        key='STT'
    )

with col_ai:
    st.markdown("""
    <div class="video-frame">
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=800&q=80" style="width:100%; display:block;">
        <div class="name-tag">🤖 Sarah (AI Tutor) <span style="color:#4ade80">● Live</span></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Audio Player Placeholder
    audio_container = st.empty()

# ==========================================
# 5. THE BRAIN LOGIC (Processing)
# ==========================================
if user_voice_input:
    # 1. Add User Message to Chat
    st.session_state.messages.append({"role": "user", "content": user_voice_input})
    
    # 2. AI Thinks (Gemini)
    prompt = f"""
    You are Sarah, a friendly English tutor.
    User said: "{user_voice_input}"
    
    Task:
    1. Reply naturally (max 2 sentences).
    2. If grammar is bad, fix it gently at the end in parentheses ().
    """
    
    try:
        response = model.generate_content(prompt)
        ai_reply = response.text
        
        # 3. Add AI Message to Chat
        st.session_state.messages.append({"role": "ai", "content": ai_reply})
        
        # 4. Generate Audio (Voice)
        tts = gTTS(text=ai_reply, lang='en')
        tts.save("reply.mp3")
        
        # 5. Play Audio Automatically
        autoplay_audio("reply.mp3")
        
    except Exception as e:
        st.error(f"Connection Error: {e}")

# ==========================================
# 6. CHAT HISTORY & CONTROLS (Bottom)
# ==========================================
st.write("---")
c_chat, c_controls = st.columns([1, 1])

with c_chat:
    st.subheader("💬 Conversation History")
    chat_container = st.container(height=300)
    with chat_container:
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai">🤖 {msg["content"]}</div>', unsafe_allow_html=True)

with c_controls:
    st.subheader("🎛️ Controls")
    
    # Volume Slider (Functional)
    vol = st.slider("Volume Boost", 0, 200, 100)
    
    # Reactions (Visual Only for now)
    rc1, rc2, rc3 = st.columns(3)
    if rc1.button("👍"):
        st.toast("You sent a Thumbs Up!")
    if rc2.button("👎"):
        st.toast("You sent a Thumbs Down!")
    if rc3.button("🔥"):
        st.toast("You sent Fire!")
        
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔴 END CALL", type="primary", use_container_width=True):
        st.warning("Session Ended. Great job practicing!")
        st.stop()
