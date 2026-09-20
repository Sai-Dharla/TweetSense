document.addEventListener('DOMContentLoaded', () => {
    const tweetInput = document.getElementById('tweetInput');
    const charCount = document.getElementById('charCount');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const spinner = document.getElementById('spinner');

    const resultBox = document.getElementById('resultBox');
    const initialState = document.getElementById('initialState');
    const resultContent = document.getElementById('resultContent');
    const errorContent = document.getElementById('errorContent');
    const sentimentValue = document.getElementById('sentimentValue');
    const compoundValue = document.getElementById('compoundValue');
    const errorMessage = document.getElementById('errorMessage');

    // Live character counter
    tweetInput.addEventListener('input', () => {
        const length = tweetInput.value.length;
        charCount.textContent = `${length}/280`;

        if (length >= 280) {
            charCount.classList.add('limit-reached');
        } else {
            charCount.classList.remove('limit-reached');
        }
    });

    // Submit handler
    analyzeBtn.addEventListener('click', async () => {
        const text = tweetInput.value.trim();

        if (!text) {
            showError('Please enter a tweet to analyze.');
            return;
        }

        setLoading(true);

        try {
            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: tweetInput.value })
            });

            const data = await response.json();

            if (!response.ok) {
                showError(data.error || 'Failed to analyze tweet.');
            } else {
                showResult(data.sentiment, data.compound);
            }
        } catch (err) {
            showError('Server connection error. Please try again.');
        } finally {
            setLoading(false);
        }
    });

    function setLoading(isLoading) {
        analyzeBtn.disabled = isLoading;
        if (isLoading) {
            btnText.textContent = 'Analyzing...';
            spinner.classList.remove('hidden');
        } else {
            btnText.textContent = 'Analyze Sentiment';
            spinner.classList.add('hidden');
        }
    }

    function showResult(sentiment, compound) {
        initialState.classList.add('hidden');
        errorContent.classList.add('hidden');
        resultContent.classList.remove('hidden');

        sentimentValue.textContent = sentiment;
        sentimentValue.className = 'sentiment-badge';

        if (sentiment === 'Positive') {
            sentimentValue.classList.add('positive');
        } else if (sentiment === 'Negative') {
            sentimentValue.classList.add('negative');
        } else {
            sentimentValue.classList.add('neutral');
        }

        // Format compound score to 4 decimal places
        compoundValue.textContent = Number(compound).toFixed(4);
    }

    function showError(msg) {
        initialState.classList.add('hidden');
        resultContent.classList.add('hidden');
        errorContent.classList.remove('hidden');
        errorMessage.textContent = msg;
    }
});

