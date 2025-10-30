from flask import Flask, request, jsonify, render_template
from transformers import pipeline
import random

app = Flask(__name__)

# Load emotion detection model (works offline after first load)
emotion_classifier = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")

def analyze_emotion(text):
    result = emotion_classifier(text)[0]['label']
    # Map to general categories
    mapping = {
        "joy": "Happy",
        "sadness": "Sad",
        "anger": "Angry",
        "fear": "Fear",
        "surprise": "Surprise",
        "disgust": "Disgust",
        "neutral": "Neutral"
    }
    return mapping.get(result.lower(), "Neutral")

def get_response(emotion):
    responses = {
        'Happy': {
            'messages': [
                "That's awesome! Keep that positive energy going!",
                "I'm so happy to hear that! You deserve every bit of joy.",
                "Yay! That’s great news — let’s celebrate this moment!"
            ],
            'emoji': '😄',
            'color': '#FFD700'
        },
        'Sad': {
            'messages': [
                "I'm really sorry you're feeling this way. You’re not alone — want me to cheer you up?",
                "It’s okay to feel sad sometimes. Things will get better, I promise.",
                "Tough times don’t last forever. I’m here with you, always."
            ],
            'emoji': '😢',
            'color': '#4169E1'
        },
        'Angry': {
            'messages': [
                "I get it — things can be really frustrating sometimes. Let’s take a deep breath together.",
                "You have every right to feel upset. Do you want to talk about what made you feel this way?",
                "I understand your anger. Let’s try to cool down and find a calm way forward."
            ],
            'emoji': '😡',
            'color': '#DC143C'
        },
        'Fear': {
            'messages': [
                "I know things can be scary, but you’re stronger than you think.",
                "It’s okay to feel afraid — everyone does. I’m right here with you.",
                "Try to breathe slowly. You’ve got this — I believe in you!"
            ],
            'emoji': '😨',
            'color': '#8A2BE2'
        },
        'Surprise': {
            'messages': [
                "Wow! That sounds unexpected! What happened exactly?",
                "Whoa, that must have been a surprise! Tell me more!",
                "Life’s full of surprises, isn’t it?"
            ],
            'emoji': '😲',
            'color': '#FFA500'
        },
        'Disgust': {
            'messages': [
                "That sounds really unpleasant. Do you want to talk about it?",
                "I get why you feel that way — sometimes things can be disappointing.",
                "That must’ve been tough to experience. Want to vent a little?"
            ],
            'emoji': '🤢',
            'color': '#32CD32'
        },
        'Neutral': {
            'messages': [
                "Alright, I’m here if you want to talk about anything.",
                "Got it! Tell me more about what’s on your mind.",
                "I’m listening — how’s your day going?"
            ],
            'emoji': '😐',
            'color': '#808080'
        }
    }
    response_data = responses.get(emotion, responses['Neutral'])
    response_data['message'] = random.choice(response_data['messages'])
    return response_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '')
        if not user_message or not user_message.strip():
            return jsonify({
                'emotion': 'Neutral',
                'message': "Please say something! I'm here to listen.",
                'emoji': '😐',
                'color': '#808080'
            }), 400
        emotion = analyze_emotion(user_message)
        response_data = get_response(emotion)
        return jsonify({
            'emotion': emotion,
            'message': response_data['message'],
            'emoji': response_data['emoji'],
            'color': response_data['color']
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            'emotion': 'Neutral',
            'message': "Sorry, something went wrong. Please try again.",
            'emoji': '😔',
            'color': '#808080'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)
