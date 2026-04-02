import os
import torch
from transformers import pipeline
from huggingface_hub import login

EMOTION_MODEL_NAME = "SamLowe/roberta-base-go_emotions"

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)

class EmotionDetector:
    def __init__(self):
        self.classifier = None
        self._load_model()
    
    def _load_model(self):
        print(f"Loading emotion detection model: {EMOTION_MODEL_NAME}...")
        self.classifier = pipeline(
            "text-classification",
            model=EMOTION_MODEL_NAME,
            top_k=None,
            device=0 if torch.cuda.is_available() else -1
        )
        print("Emotion detector loaded successfully!")
    
    def detect(self, text: str) -> dict:
        results = self.classifier(text)[0]
        sorted_emotions = sorted(results, key=lambda x: x['score'], reverse=True)
        
        return {
            "primary_emotion": sorted_emotions[0]['label'],
            "primary_confidence": round(sorted_emotions[0]['score'], 4),
            "secondary_emotion": sorted_emotions[1]['label'] if len(sorted_emotions) > 1 else None,
            "secondary_confidence": round(sorted_emotions[1]['score'], 4) if len(sorted_emotions) > 1 else None,
            "all_emotions": [
                {"label": e['label'], "score": round(e['score'], 4)} 
                for e in sorted_emotions[:5]
            ],
            "intensity": self._calculate_intensity(sorted_emotions[0]['score'])
        }
    
    def _calculate_intensity(self, confidence: float) -> str:
        if confidence >= 0.7:
            return "high"
        elif confidence >= 0.4:
            return "medium"
        else:
            return "low"

emotion_detector = EmotionDetector()