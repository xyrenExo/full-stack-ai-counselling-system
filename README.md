# AI Counselling System - Full Stack

A complete AI-powered emotional support chatbot built with Flask (backend) and Next.js (frontend).

## Architecture

```
┌─────────────┐     POST /chat     ┌─────────────────────────────────────┐
│   Next.js   │ ──────────────────► │           Flask Backend             │
│  Frontend   │ ◄────────────────── │                                     │
│   (React)   │    JSON Response    │  RoBERTa → Crisis → Gemini → DialoGPT│
└─────────────┘                     └─────────────────────────────────────┘
```

## Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Flask (Python) |
| Frontend | Next.js 14 (React) |
| Emotion Detection | SamLowe/roberta-base-go_emotions |
| Empathy Refinement | AliiaR/DialoGPT-medium-empathetic-dialogues |
| Response Generation | Gemini API |

## Folder Structure

```
AI_Counselling_System_Fullstack/
├── backend/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment template
│   ├── models/
│   │   ├── emotion.py         # RoBERTa emotion detector
│   │   ├── crisis.py          # Crisis detection logic
│   │   └── empathy.py         # DialoGPT empathy refiner
│   └── services/
│       └── gemini.py          # Gemini API integration
├── frontend/
│   ├── package.json
│   ├── next.config.js
│   ├── .env.local.example
│   ├── app/
│   │   ├── layout.js          # Root layout
│   │   └── page.js            # Main page
│   └── components/
│       └── ChatBox.js         # Chat UI component
└── README.md
```

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

pip install -r requirements.txt
python app.py
```

The backend will start on `http://localhost:5000`.

### 2. Frontend Setup

```bash
cd frontend
copy .env.local.example .env.local
npm install
npm run dev
```

The frontend will start on `http://localhost:3000`.

### 3. Get Gemini API Key

1. Go to https://aistudio.google.com/app/apikey
2. Create an API key
3. Add it to `backend/.env`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Send message and get AI response |
| `/mood` | GET | Get mood history |
| `/reset` | POST | Reset conversation |
| `/health` | GET | Health check |

### Request Format

```json
POST /chat
{
  "message": "I'm feeling really stressed about work"
}
```

### Response Format

```json
{
  "response": "AI empathetic response...",
  "emotion": "stress",
  "secondary_emotion": "anxiety",
  "intensity": "high",
  "crisis": false,
  "crisis_level": "none",
  "mood_history": [...]
}
```

## Features

- **Emotion Detection** - Real-time emotion analysis using RoBERTa
- **Crisis Detection** - Automatic detection of crisis situations
- **Empathetic Responses** - Gemini-powered responses refined by DialoGPT
- **Music Suggestions** - Calming music recommendations based on emotion
- **Breathing Exercises** - Guided breathing techniques for crisis situations
- **Mental Exercises** - Grounding exercises for emotional regulation
- **Mood Tracking** - Tracks emotional history across conversations
- **Crisis Support** - Hotline suggestions and urgent care guidance

### Note
## I replaced the torch ~2Gb+ version with 200Mb version for compatible wit Railway free Build
This system provides emotional support but is NOT a replacement for professional mental health care. If you're in crisis, please contact emergency services or a crisis hotline immediately.
