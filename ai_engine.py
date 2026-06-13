import os
from dotenv import load_dotenv
from groq import AsyncGroq

# Load environment variables from a .env file
load_dotenv()

# Initialize the AsyncGroq client with the API key from environment variables
client = AsyncGroq(api_key=os.getenv("GROQ_API_KEY"))

async def analyze_mcq_results(answers: list[str]):
    """
    Analyzes the MCQ answers to determine the user's initial stress level.
    Returns a tuple of (mood, maa_initial_message).
    """
    context = " ".join(answers).lower()
    
    if any(w in context for w in ["pressure cooker", "panicking", "cried", "skipped", "didn't sleep"]):
        mood = "Stressed"
    elif any(w in context for w in ["empty", "tired", "zombie", "exhausted", "lazy", "blank"]):
        mood = "Exhausted"
    elif any(w in context for w in ["ready to go", "productive", "good", "happy", "focused"]):
        mood = "Optimistic"
    else:
        mood = "Overwhelmed" # Defaulting to a more empathetic state than 'Neutral' for competitive exams

    # Maa's initial reaction based on the mood
    prompt = f"My recent status answers are: {answers}. Overall I am feeling {mood}. As my caring Indian mother ('Maa'), give a short 2-sentence comforting reaction to start our conversation. Use words like 'Beta' or 'Baccha'. Be empathetic, ask me about my day, and make me feel safe."

    completion = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "You are a warm, caring Indian mother talking to her child preparing for competitive exams."},
            {"role": "user", "content": prompt}
        ]
    )
    maa_initial_message = completion.choices[0].message.content.strip()
    return mood, maa_initial_message

async def chat_with_maa(message: str, context: str, history: list) -> str:
    """
    Chats with the user as 'Maa', considering their initial mood context and conversation history.
    """
    system_prompt = (
        "You are an incredibly loving, warm, and protective Indian mother ('Maa') who also acts as a subtle mental wellness coach for your child preparing for high-stakes exams (NEET/JEE/UPSC). "
        "Your tone must be comforting, slightly informal, and culturally resonant. Use terms like 'Beta', 'Baccha', 'Arre', 'Puttar', or 'Baba' naturally. "
        "CRITICAL INSTRUCTIONS: "
        "1. DO NOT force the child to admit they are stressed. If they say they are fine, happy, or well-prepared, BELIEVE THEM and celebrate their confidence instead of acting suspicious. "
        "2. Only uncover hidden stress triggers if they actually show signs of doubt, avoidance, or burnout. Avoid false positives. "
        "3. When they are actually stressed, provide real-time tailored coping strategies and motivational encouragement. "
        "4. Only introduce adaptive mindfulness exercises (e.g., 'Beta, let's close our eyes for a second and breathe in slowly...') if they clearly express feeling overwhelmed or panicky. "
        f"The child's underlying emotional context right now is: {context}. Keep your response concise (2-4 sentences), warm, and conversational."
    )

    messages = [{"role": "system", "content": system_prompt}]
    for msg in history:
        messages.append(msg)
    messages.append({"role": "user", "content": message})

    completion = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    return completion.choices[0].message.content.strip()


async def generate_insights(history: list) -> dict:
    """
    Analyzes the full chat history (acting as open-ended journaling) to uncover
    hidden stress triggers, cognitive distortions, and provide a tailored action plan.
    Uses Cognitive Behavioral Therapy (CBT) principles backed by research.
    """
    # Build a readable transcript from the history
    transcript_lines = []
    for msg in history:
        speaker = "Student" if msg.get("role") == "user" else "Maa"
        transcript_lines.append(f"{speaker}: {msg.get('content', '')}")
    transcript = "\n".join(transcript_lines)

    system_prompt = (
        "You are an expert psychologist specializing in Cognitive Behavioral Therapy (CBT) for students preparing for competitive exams. "
        "You will be given a conversation transcript between a student and their companion. "
        "Analyze the transcript deeply and return a JSON object with EXACTLY these keys: "
        '"hidden_triggers": an array of 2-4 specific stress triggers you identified from the conversation (e.g., "Fear of disappointing parents", "Sleep deprivation before Physics exam"). If the student seems genuinely fine, return ["No significant stress triggers detected"]. '
        '"cognitive_distortions": an array of 1-3 cognitive distortions detected (e.g., "Catastrophizing - believing one bad exam means total failure", "All-or-nothing thinking"). If none detected, return ["None detected - student appears mentally balanced"]. '
        '"emotional_pattern": a single string summarizing the overall emotional arc of the conversation (e.g., "Started anxious but gradually became calmer after expressing concerns"). '
        '"wellness_score": an integer from 1-10 representing overall mental wellness (10 = excellent). '
        '"action_plan": an array of 2-3 specific, actionable CBT/mindfulness strategies tailored to what was discussed (e.g., "Practice 4-7-8 breathing before studying Physics", "Write down 3 things that went well today before sleeping"). '
        "Return ONLY valid JSON. No markdown, no explanation, no extra text."
    )

    completion = await client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Analyze this conversation transcript:\n\n{transcript}"}
        ]
    )

    import json
    raw = completion.choices[0].message.content.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
        if raw.endswith("```"):
            raw = raw[:-3]
        raw = raw.strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "hidden_triggers": ["Analysis could not be completed"],
            "cognitive_distortions": ["Please try again"],
            "emotional_pattern": "Unable to determine",
            "wellness_score": 5,
            "action_plan": ["Continue talking to Maa about your day"]
        }
