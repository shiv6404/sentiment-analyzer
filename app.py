"""
Flask web app for the AI-Based Sentiment Analyzer.
Run with: python app.py
Then open http://127.0.0.1:5000 in your browser.
"""

from flask import Flask, render_template, request
from sentiment_engine import analyze_sentiment, analyze_batch

app = Flask(__name__)

# In-memory history of analyzed texts (resets when server restarts)
HISTORY = []


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        text = request.form.get("text", "").strip()
        if text:
            result = analyze_sentiment(text)
            HISTORY.append(result)

    summary = {"Positive": 0, "Negative": 0, "Neutral": 0}
    for r in HISTORY:
        summary[r["label"]] += 1

    return render_template("index.html", result=result, history=list(reversed(HISTORY)), summary=summary)


@app.route("/batch", methods=["POST"])
def batch():
    raw = request.form.get("batch_text", "")
    lines = [l.strip() for l in raw.split("\n") if l.strip()]
    results, summary = analyze_batch(lines)
    HISTORY.extend(results)
    return render_template("index.html", result=None, history=list(reversed(HISTORY)), summary=summary)


if __name__ == "__main__":
    app.run(debug=True)
