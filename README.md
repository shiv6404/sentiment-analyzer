# AI-Based Sentiment Analyzer

A lightweight, fully offline sentiment analysis tool that classifies text
(reviews, comments, social media posts) as **Positive**, **Negative**, or
**Neutral**, with a confidence score and a visualized summary chart.

## Features
- Lexicon-based sentiment scoring engine (handles negation and intensifiers, e.g. "not bad", "extremely good")
- Single-text and batch (multi-line) analysis
- Dark-themed web dashboard built with Flask
- Live doughnut chart summarizing sentiment distribution (Chart.js)
- Analysis history table
- No external API keys or internet connection required

## Tech Stack
Python, Flask, Chart.js (CDN), HTML/CSS

## Project Structure
```
sentiment-analyzer/
├── app.py                 # Flask routes
├── sentiment_engine.py    # Core sentiment scoring logic
├── templates/
│   └── index.html         # Dashboard UI
├── requirements.txt
└── README.md
```

## Setup & Run
```bash
pip install -r requirements.txt
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

## How it works
1. Text is tokenized and checked against curated positive/negative word
   lexicons.
2. Negation words ("not", "never", etc.) flip the polarity of nearby words.
3. Intensifiers ("very", "extremely") boost the weight of nearby words.
4. A final score determines the label and a normalized confidence value.

## Example
```python
from sentiment_engine import analyze_sentiment

result = analyze_sentiment("Not bad at all, actually quite impressive!")
print(result)
# {'label': 'Positive', 'score': 0.4, 'confidence': 0.04, ...}
```

## Future Improvements
- Swap in a transformer-based model (e.g. Hugging Face) for higher accuracy
- Persist history to a database instead of in-memory storage
- Add CSV upload for bulk review analysis

---
Built as part of a Data Science Internship project.
