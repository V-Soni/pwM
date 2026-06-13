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

