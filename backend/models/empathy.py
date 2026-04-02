import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from huggingface_hub import login
import warnings
warnings.filterwarnings('ignore')

EMPATHY_MODEL_NAME = "AliiaR/DialoGPT-medium-empathetic-dialogues"

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)

class EmpathyRefiner:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.conversation_history = []
        self._load_model()
    
    def _load_model(self):
        print(f"Loading empathy refinement model: {EMPATHY_MODEL_NAME}...")
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(EMPATHY_MODEL_NAME)
            self.model = AutoModelForCausalLM.from_pretrained(EMPATHY_MODEL_NAME)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            if torch.cuda.is_available():
                self.model = self.model.to('cuda')
            print("Empathy refinement model loaded successfully!")
        except Exception as e:
            print(f"Warning: Could not load empathy model: {e}")
            self.model = None
    
    def refine(self, user_input: str, initial_response: str, emotion_data: dict = None) -> str:
        if not self.model or not self.tokenizer:
            return initial_response
        try:
            prompt = self._build_refinement_prompt(user_input, initial_response, emotion_data)
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            if torch.cuda.is_available():
                inputs = {k: v.to('cuda') for k, v in inputs.items()}
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=150,
                    temperature=0.7,
                    top_p=0.9,
                    do_sample=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            refined = response.replace(prompt, "").strip()
            return refined if refined and len(refined) > 10 else initial_response
        except Exception as e:
            print(f"Empathy refinement error: {e}")
            return initial_response
    
    def _build_refinement_prompt(self, user_input: str, initial_response: str, emotion_data: dict = None) -> str:
        emotion_info = f"\nUser's emotion: {emotion_data.get('primary_emotion', 'unknown')}" if emotion_data else ""
        prompt = f"Instruction: Provide an empathetic, supportive response to the user.{emotion_info}\n"
        prompt += f"User: {user_input}\n"
        prompt += f"Assistant: {initial_response}\n"
        prompt += "Refined response:"
        return prompt
    
    def clear_history(self):
        self.conversation_history = []
    
    def add_to_history(self, user_input: str, response: str):
        self.conversation_history.append({"user": user_input, "assistant": response})
        if len(self.conversation_history) > 5:
            self.conversation_history.pop(0)

empathy_refiner = EmpathyRefiner()