import requests
import json

def emotion_detector(text_to_analyze):
    """
    Detects emotions from the given text using Watson NLP EmotionPredict.

    Handles:
    - Blank input
    - Server errors (status_code = 400)
    - Network or parsing errors

    Returns:
        dict: {
            'anger': float or None,
            'disgust': float or None,
            'fear': float or None,
            'joy': float or None,
            'sadness': float or None,
            'dominant_emotion': str or None
        }
    """
    # Default "empty" response for errors or blank input
    empty_result = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    # Handle blank input
    if not text_to_analyze or text_to_analyze.strip() == "":
        return empty_result

    # Prepare request
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    payload = { "raw_document": { "text": text_to_analyze } }

    try:
        response = requests.post(url, headers=headers, json=payload)
    except requests.RequestException:
        # Network error
        return empty_result

    # Handle server error (e.g., blank input processed by server)
    if response.status_code == 400:
        return empty_result

    # Parse response JSON
    try:
        data = response.json()
    except json.JSONDecodeError:
        return empty_result

    # Extract emotions
    emotions = data.get('text', {}).get('emotion', {})
    anger = emotions.get('anger', 0)
    disgust = emotions.get('disgust', 0)
    fear = emotions.get('fear', 0)
    joy = emotions.get('joy', 0)
    sadness = emotions.get('sadness', 0)

    # Determine dominant emotion
    emotion_scores = {
        'anger': anger,
        'disgust': disgust,
        'fear': fear,
        'joy': joy,
        'sadness': sadness
    }
    dominant_emotion = max(emotion_scores, key=emotion_scores.get)

    # Return final dictionary
    result = emotion_scores
    result['dominant_emotion'] = dominant_emotion
    return result
