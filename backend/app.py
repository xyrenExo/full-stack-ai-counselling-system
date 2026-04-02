import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from models.emotion import emotion_detector
from models.crisis import crisis_detector
from models.empathy import empathy_refiner
from services.gemini import generate_response, get_music_suggestion, get_breathing_exercise, get_mental_exercise

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.getenv("FRONTEND_URL", "http://localhost:3000")}})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

mood_history = []

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
        
        user_input = data['message'].strip()
        if not user_input:
            return jsonify({"error": "Empty message"}), 400
        
        logger.info(f"Received message: {user_input[:50]}...")
        
        emotion_data = emotion_detector.detect(user_input)
        logger.info(f"Detected emotion: {emotion_data['primary_emotion']}")
        
        crisis_data = crisis_detector.detect(user_input, emotion_data)
        logger.info(f"Crisis level: {crisis_data['level']}")
        
        initial_response = generate_response(user_input, emotion_data, crisis_data)
        
        refined_response = empathy_refiner.refine(user_input, initial_response, emotion_data)
        
        final_response = _add_optional_features(refined_response, emotion_data, crisis_data)
        
        empathy_refiner.add_to_history(user_input, final_response)
        
        mood_history.append({
            "timestamp": datetime.now().isoformat(),
            "emotion": emotion_data['primary_emotion'],
            "intensity": emotion_data['intensity']
        })
        if len(mood_history) > 10:
            mood_history.pop(0)
        
        return jsonify({
            "response": final_response,
            "emotion": emotion_data['primary_emotion'],
            "secondary_emotion": emotion_data.get('secondary_emotion'),
            "intensity": emotion_data['intensity'],
            "crisis": crisis_data['crisis'],
            "crisis_level": crisis_data['level'],
            "mood_history": mood_history[-5:]
        })
    
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "response": "I'm having trouble processing that right now. Please try again."
        }), 500

@app.route('/mood', methods=['GET'])
def get_mood_history():
    return jsonify({"mood_history": mood_history})

@app.route('/reset', methods=['POST'])
def reset_conversation():
    empathy_refiner.clear_history()
    mood_history.clear()
    return jsonify({"message": "Conversation reset"})

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

def _add_optional_features(response: str, emotion_data: dict, crisis_data: dict) -> str:
    parts = [response]
    
    if crisis_data.get("level") in ["high", "medium"]:
        help_text = (
            "\n\nIf you're struggling, please consider reaching out to a professional. "
            "You can call 988 (US) or your local crisis hotline. You don't have to face this alone."
        )
        parts.append(help_text)
    
    music = get_music_suggestion(emotion_data.get("primary_emotion", "neutral"))
    parts.append(f"\n\nMusic suggestion: {', '.join(music)}")
    
    if crisis_data.get("level") == "high":
        exercise = get_breathing_exercise()
        parts.append(f"\n\nTry this: {exercise}")
    elif crisis_data.get("level") == "none":
        exercise = get_mental_exercise()
        parts.append(f"\n\nGrounding exercise: {exercise}")
    
    return "".join(parts)

if __name__ == '__main__':
    port = int(os.getenv("FLASK_PORT", 5000))
    print(f"\n=== AI Counselling System Backend ===")
    print(f"Starting on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)