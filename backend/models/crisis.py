CRISIS_KEYWORDS = [
    "suicide", "kill myself", "end my life", "want to die", "better off dead",
    "self-harm", "hurt myself", "cut myself", "overdose", "no reason to live",
    "hopeless", "can't go on", "end it all", "never wake up"
]

CRISIS_INDICATORS = {
    "high": ["suicide", "kill myself", "end my life", "want to die", "self-harm", "hurt myself"],
    "medium": ["hopeless", "can't go on", "better without me", "nobody cares", "alone forever"]
}

class CrisisDetector:
    def __init__(self):
        self.crisis_keywords = CRISIS_KEYWORDS
        self.crisis_indicators = CRISIS_INDICATORS
    
    def detect(self, text: str, emotion_data: dict = None) -> dict:
        text_lower = text.lower()
        crisis_found = False
        crisis_level = "none"
        
        for keyword in self.crisis_keywords:
            if keyword in text_lower:
                crisis_found = True
                if keyword in self.crisis_indicators["high"]:
                    crisis_level = "high"
                    break
                elif crisis_level != "high":
                    crisis_level = "medium"
        
        if emotion_data and not crisis_found:
            if emotion_data.get("intensity") == "high":
                high_distress_emotions = ["sadness", "fear", "anger", "disgust"]
                if emotion_data.get("primary_emotion", "").lower() in high_distress_emotions:
                    crisis_found = True
                    crisis_level = "medium"
        
        return {
            "crisis": crisis_found,
            "level": crisis_level,
            "requires_immediate_action": crisis_level == "high"
        }

crisis_detector = CrisisDetector()