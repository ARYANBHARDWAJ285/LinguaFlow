# 🗣️ LinguaFlow: The Judgment-Free AI Tutor

> **Winner of "Agents for Good" Track (Submission)** > *Helping millions of students bridge the "English Confidence Gap" via AI.*

## 🧐 The Problem
In Tier-2/3 cities in India, students struggle with spoken English not because of a lack of knowledge, but a lack of **environment**. They fear social embarrassment if they make mistakes. This "Confidence Gap" leads to unemployment for otherwise talented engineers.

## 💡 The Solution
LinguaFlow is a voice-first AI Agent that acts as a supportive, non-judgmental English tutor named "Sarah".
* **Safe Sandbox:** Speak without fear of mockery.
* **Real-time Correction:** Get instant feedback on grammar.
* **Video Interface:** Simulates a real video call for immersion.

## ⚙️ Architecture
1.  **Frontend:** Streamlit (with Custom CSS for Glassmorphism UI).
2.  **Audio In:** `streamlit-mic-recorder` bridges Browser Audio -> Python Server.
3.  **The Brain:** **Google Gemini 1.5 Flash API** handles conversation & grammar logic.
4.  **Audio Out:** `gTTS` (Google Text-to-Speech) converts AI text to speech.


