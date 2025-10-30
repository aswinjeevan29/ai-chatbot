from transformers import pipeline

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

# Test various emotions
test_messages = [
    "I can’t handle this anymore!",
    "People just don’t listen to me!",
    "That movie made my day, it was so good!",
    "I'm angry about what happened!",
    "I miss my best friend so much.",
    "Everything is perfect today!"
]

for msg in test_messages:
    emotion = analyze_emotion(msg)
    print(f"Message: '{msg}' -> Detected Emotion: {emotion}")
