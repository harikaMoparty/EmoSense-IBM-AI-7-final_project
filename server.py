"""
server.py

Flask application for Emotion Detection.

Provides two routes:
- "/" renders the main page.
- "/emotionDetector" accepts POST requests with text and returns emotion analysis.
"""

import sys
import os

# pylint: disable=wrong-import-position
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, render_template, request, jsonify
from emotion_detection.emotion_detection import emotion_detector  # noqa: E402

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    """
    Render the main index page.

    Returns:
        Response object rendering 'index.html' template.
    """
    return render_template("index.html")


@app.route("/emotionDetector", methods=["POST"])
def emotion_detector_route():
    """
    Handle emotion detection requests.

    Extracts 'text' from JSON request data, calls emotion_detector,
    and returns JSON response with emotion scores and dominant emotion.
    If the dominant emotion is None (blank or invalid input), returns
    a message prompting the user to try again.

    Returns:
        JSON response containing emotion scores, dominant emotion,
        and a display text message.
    """
    data = request.get_json()
    text = data.get("text", "")

    result = emotion_detector(text)

    if result.get("dominant_emotion") is None:
        # Handle blank or invalid input
        result["display_text"] = "Invalid text! Please try again!"
    else:
        # Prepare formatted display text
        result["display_text"] = (
            f"For the given statement, the system response is "
            f"'anger': {result['anger']}, "
            f"'disgust': {result['disgust']}, "
            f"'fear': {result['fear']}, "
            f"'joy': {result['joy']} and "
            f"'sadness': {result['sadness']}. "
            f"The dominant emotion is {result['dominant_emotion']}."
        )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
