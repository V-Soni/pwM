# Maa - Your Desi Mental Wellness Companion

*Submission for PromptWars Mumbai*

**Theme Challenge**: Mental Wellness Tracker for Students preparing for High-Stakes Exams (NEET, JEE, UPSC, etc.)

## The Problem
Students preparing for competitive exams face immense burnout and stress. However, traditional "Mental Health Trackers" or "Journal Apps" often feel clinical, intimidating, and feel like "extra work" for an already exhausted student. They don't want a psychologist; they want comfort.

## The Solution: The "Maa" Persona
We built a Generative AI-powered web app that adopts the persona of a warm, caring Indian Mother ("Maa"). 
- **Cultural Resonance**: "Maa" doesn't use clinical jargon. She asks if you've eaten, tells you to sleep, and subtly assesses your stress levels through natural conversation.
- **Low-Friction Onboarding (The MCQ Game)**: Instead of staring at a blank journal page, users start with a 3-question MCQ "check-in" (e.g., "Did you eat properly today?"). This takes 5 seconds, feels like a game, but provides the AI with critical context about the user's physical and mental state.
- **Contextual Chat with Memory**: The chat interface uses the MCQ results as an underlying system prompt context and maintains full conversation history, allowing "Maa" to reference earlier messages and provide continuous, contextual support.
- **Maa's Diary (Insight Engine)**: After chatting, users can click "Maa's Diary" to get a deep CBT-based analysis of their conversation. This uncovers **hidden stress triggers**, detects **cognitive distortions** (e.g., catastrophizing, all-or-nothing thinking), and generates a **personalized action plan** with tailored coping strategies and adaptive mindfulness exercises — fulfilling the core requirement of uncovering emotional patterns that standard trackers miss.

## Research Foundation
Our approach is grounded in evidence-based mental wellness interventions:
- **Cognitive Behavioral Therapy (CBT)**: The Insight Engine identifies cognitive distortions (irrational fears like "If I fail this exam, my life is over") and provides restructuring strategies.
- **Mindfulness-Based Interventions (MBIs)**: Research shows that even brief mindfulness training significantly reduces test anxiety. Maa seamlessly introduces breathing exercises and grounding techniques when stress is detected.
- **Holistic Wellness**: The MCQ check-in addresses the research-backed pillars of sleep, nutrition, and study preparedness — all critical protective factors for student mental health.

## How It Works Technically
1. **Frontend**: Built with HTML5, Tailwind CSS, and Vanilla JavaScript for a lightweight, fast, single-page application. We used a warm, comforting color palette (terracotta, amber) to reflect the homey persona.
2. **Backend**: FastAPI handles asynchronous API routing (`/api/mcq-submit`, `/api/chat`, and `/api/insights`).
3. **AI Engine**: Powered by Groq's ultra-fast inference and `llama-3.3-70b-versatile`. The engine dynamically constructs system prompts based on the MCQ choices to ensure high context retention and strict persona adherence.
4. **Insight Engine**: A separate CBT-specialist prompt analyzes the full conversation transcript to extract structured psychological insights as JSON.

## Running Locally
1. Create a virtual environment and activate it.
2. `pip install -r requirements.txt`
3. Create a `.env` file with `GROQ_API_KEY=your_key`.
4. Run `fastapi dev main.py`.

## Deployment
This project is configured to be deployed natively on **FastAPI Cloud** via the `fastapi deploy` command.

## Assumptions Made
- The target audience responds better to informal, culturally resonant (Indian household) comfort rather than clinical psychological advice.
- Users are English speakers who understand common Indian affectionate terms (Beta, Baccha, etc.).
- The user will have an internet connection to reach the Groq API.