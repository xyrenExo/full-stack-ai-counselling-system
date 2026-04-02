import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel('gemini-pro')
else:
    gemini_model = None
    print("WARNING: GEMINI_API_KEY not set. Using fallback responses.")

MUSIC_SUGGESTIONS = {
    "anxiety": ["ambient piano", "nature sounds"],
    "sadness": ["warm acoustic", "comforting melodies"],
    "stress": ["meditation music", "ocean waves"],
    "anger": ["slow ambient", "peaceful instrumentals"],
    "fear": ["calming instrumental", "soft classical"],
    "joy": ["uplifting acoustic", "bright instrumental"],
    "neutral": ["ambient music", "nature sounds"]
}

BREATHING_EXERCISES = [
    "4-7-8 Breathing: Inhale for 4s, hold for 7s, exhale for 8s",
    "Box Breathing: Inhale 4s, hold 4s, exhale 4s, hold 4s",
    "Diaphragmatic Breathing: Breathe deeply into belly, exhale slowly"
]

MENTAL_EXERCISES = [
    "5-4-3-2-1 Grounding: Name 5 things you see, 4 you hear, 3 you feel, 2 you smell, 1 you taste",
    "Body Scan: Focus attention on each body part, from toes to head",
    "Color Shift: Look around and name items by color, focusing on details"
]

HOTLINES = {
    "US": "988 (Suicide & Crisis Lifeline)",
    "UK": "116 123 (Samaritans)",
    "CANADA": "988",
    "AUSTRALIA": "13 11 14 (Lifeline)",
    "INDIA": "iCall: 9152987821"
}

def generate_response(user_input: str, emotion_data: dict, crisis_data: dict) -> str:
    prompt = _build_prompt(user_input, emotion_data, crisis_data)
    
    if gemini_model:
        try:
            response = gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini error: {e}")
            return _fallback_response(emotion_data, crisis_data)
    else:
        return _fallback_response(emotion_data, crisis_data)

def _build_prompt(user_input: str, emotion_data: dict, crisis_data: dict) -> str:
    primary = emotion_data.get("primary_emotion", "unknown")
    secondary = emotion_data.get("secondary_emotion", "unknown")
    intensity = emotion_data.get("intensity", "unknown")
    crisis = crisis_data.get("crisis", False)
    crisis_level = crisis_data.get("level", "none")
    
    prompt = f"""You are an empathetic AI counselling assistant. Your task is to help users express emotions freely and provide emotional support.

USER INPUT: {user_input}

EMOTION ANALYSIS:
- Primary Emotion: {primary}
- Secondary Emotion: {secondary}
- Intensity: {intensity}

CRISIS DETECTION:
- Crisis: {crisis}
- Level: {crisis_level}

TONE REQUIREMENTS:
- Human-like, warm, calm
- Use phrases like "It sounds like...", "I understand...", "That must feel..."
- Keep responses clear and not overwhelming
- Always validate feelings first, never judge

RESPONSE STRUCTURE:
1. Emotional Validation (acknowledge their feelings)
2. Emotional Reflection (reflect back what you understand)
3. Gentle Guidance (1-2 suggestions only)
4. Optional Support (music/breathing/mental exercises if appropriate)
5. Professional Help (if crisis detected or needed)

IMPORTANT RULES:
- Never diagnose or prescribe
- If crisis=true, respond with urgency and provide hotline guidance
- Keep response supportive and encouraging
- Return ONLY the final response to the user, no analysis or system data

Generate a caring, supportive response:"""

    return prompt

def _fallback_response(emotion_data: dict, crisis_data: dict) -> str:
    primary = emotion_data.get("primary_emotion", "that emotion")
    crisis = crisis_data.get("crisis", False)
    crisis_level = crisis_data.get("level", "none")
    
    if crisis:
        if crisis_level == "high":
            return (
                "I'm really concerned about you right now. Your safety is so important to me. "
                "Please reach out to a crisis hotline (call 988 in the US) or talk to someone "
                "who can be with you right away. You don't have to face this alone."
            )
        else:
            return (
                "I want to make sure you're okay. What you're going through matters. "
                "Please consider talking to a trusted person or professional. "
                "I'm here to listen and support you."
            )
    
    responses = {
        "sadness": "I hear you, and it sounds like you're going through something difficult right now. "
                   "It's okay to feel sad - those feelings are valid. I'm here with you.",
        "anxiety": "It sounds like things feel overwhelming right now. Let's take a breath together. "
                   "Anxiety can be really hard, but you're not alone in this.",
        "fear": "You're feeling scared, and that's completely understandable. "
                "Take your time - I'm here to listen without judgment.",
        "anger": "I hear that you're frustrated or angry. It's okay to feel that way. "
                 "Let's work through this together, at your own pace.",
        "joy": "That's wonderful! I'm so glad you're sharing something positive. "
               "Keep holding onto those good feelings!"
    }
    
    return responses.get(primary, "Thank you for sharing that with me. I'm here to listen and support you.")

def get_music_suggestion(emotion: str) -> list:
    return MUSIC_SUGGESTIONS.get(emotion.lower(), MUSIC_SUGGESTIONS["neutral"])

def get_breathing_exercise() -> str:
    import random
    return random.choice(BREATHING_EXERCISES)

def get_mental_exercise() -> str:
    import random
    return random.choice(MENTAL_EXERCISES)

def get_hotline_info(country: str = "US") -> str:
    return HOTLINES.get(country, "988")