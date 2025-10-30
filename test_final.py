import requests
import json

messages = [
    "I am so happy today!",
    "I feel really sad about this.",
    "This makes me angry!",
    "I'm scared of what's happening.",
    "Wow, that's surprising!",
    "This is disgusting.",
    "I trust you completely.",
    "I'm excited for the future.",
    "Everything is fine."
]

for msg in messages:
    response = requests.post('http://localhost:5000/chat', json={'message': msg})
    if response.status_code == 200:
        data = response.json()
        print(f"Message: '{msg}'")
        print(f"Detected Emotion: {data['emotion']}")
        print(f"Response: {data['message']}")
        print(f"Emoji: {data['emoji']}")
        print(f"Color: {data['color']}")
        print("---")
    else:
        print(f"Error for message '{msg}': {response.status_code} - {response.text}")
