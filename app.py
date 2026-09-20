import os
from flask import Flask, render_template, request, jsonify
from sentiment import analyze_tweet_sentiment

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.get_json(silent=True)
        if not data or not isinstance(data, dict):
            return jsonify({"error": "Invalid JSON request"}), 400
        
        text = data.get("text", "")
        if not isinstance(text, str):
            return jsonify({"error": "Field 'text' must be a string"}), 400
        
        if not text.strip():
            return jsonify({"error": "Please enter a tweet to analyze."}), 400
        
        # Enforce max length of 280 characters if needed or handle it
        if len(text) > 280:
            text = text[:280]
            
        result = analyze_tweet_sentiment(text)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred during analysis: {str(e)}"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

