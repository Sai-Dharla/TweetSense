import os
import re
from pathlib import Path
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Configure NLTK to use bundled nltk_data directory
PROJECT_ROOT = Path(__file__).resolve().parent
NLTK_DATA_DIR = str(PROJECT_ROOT / "nltk_data")

if NLTK_DATA_DIR not in nltk.data.path:
    nltk.data.path.insert(0, NLTK_DATA_DIR)

# Initialize SentimentIntensityAnalyzer instance
_sia = None

def get_analyzer():
    global _sia
    if _sia is None:
        _sia = SentimentIntensityAnalyzer()
    return _sia

def preprocess_tweet(text: str) -> str:
    """
    Lightweight preprocessing suitable for social-media text.
    Handles URLs, @mentions, whitespace, but preserves hashtags,
    emojis, punctuation, and capitalization for VADER sentiment signals.
    """
    if not text:
        return ""
    
    # Remove URLs (http/https/ftp/www)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove @mentions
    text = re.sub(r'@\w+', '', text)
    
    # Strip hashtag symbol '#' but keep the word for sentiment context
    text = re.sub(r'#(\w+)', r'\1', text)
    
    # Normalize multiple whitespace characters
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def analyze_tweet_sentiment(text: str) -> dict:
    """
    Analyzes sentiment of tweet text using NLTK VADER.
    Returns dictionary with 'sentiment' (Positive/Negative/Neutral) and 'compound' score.
    """
    cleaned_text = preprocess_tweet(text)
    
    if not cleaned_text:
        # If text had only URLs or mentions, analyze original trimmed text if non-empty, else neutral 0.0
        cleaned_text = text.strip() if text else ""
        if not cleaned_text:
            return {"sentiment": "Neutral", "compound": 0.0}

    analyzer = get_analyzer()
    scores = analyzer.polarity_scores(cleaned_text)
    compound = round(scores.get('compound', 0.0), 4)

    # Classification rules:
    # compound >= 0.05 -> Positive
    # compound <= -0.05 -> Negative
    # otherwise -> Neutral
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "compound": compound
    }

