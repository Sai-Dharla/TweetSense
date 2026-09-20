# TweetSense

Sentiment Analysis on Twitter Data powered by Python, Flask, and NLTK VADER.

## Features
- Clean single-page interface fitted to a single desktop viewport (no scrolling).
- Real-time 280-character count tracker.
- Rule-based sentiment analysis using NLTK VADER.
- Social media preprocessing preserving emojis, capitalization, and punctuation sentiment signals.
- Classification into Positive, Negative, or Neutral with exact compound scores.

## Setup & Local Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run tests:
```bash
python test_app.py
```

3. Start local development server:
```bash
python app.py
```

4. Start production server (using Gunicorn):
```bash
gunicorn app:app
```

