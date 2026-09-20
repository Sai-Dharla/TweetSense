import unittest
import json
from app import app
import sentiment

class TweetSenseTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_homepage(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sentiment Analysis on Twitter Data', response.data)
        self.assertIn(b'TweetSense', response.data)

    def test_sentiment_cases(self):
        cases = [
            ("I absolutely love this product!", "Positive"),
            ("This is terrible and completely disappointing.", "Negative"),
            ("The meeting starts at 10 AM.", "Neutral"),
            ("I don't like this.", "Negative"),
            ("Wow!!! This is amazing!!!", "Positive"),
            ("Worst experience ever!!!", "Negative"),
            ("The product arrived today.", "Neutral"),
            ("Check out this link https://example.com @user #awesome", "Positive"),
        ]

        for text, expected_sentiment in cases:
            res = self.app.post('/analyze',
                                data=json.dumps({'text': text}),
                                content_type='application/json')
            self.assertEqual(res.status_code, 200)
            data = res.get_json()
            self.assertEqual(data['sentiment'], expected_sentiment, f"Failed on: {text}")
            self.assertIn('compound', data)

    def test_empty_and_whitespace_input(self):
        # Empty text
        res = self.app.post('/analyze',
                            data=json.dumps({'text': ''}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 400)

        # Whitespace-only text
        res = self.app.post('/analyze',
                            data=json.dumps({'text': '   \n\t  '}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_invalid_requests(self):
        res = self.app.post('/analyze', data="Not JSON", content_type='text/plain')
        self.assertEqual(res.status_code, 400)

        res = self.app.post('/analyze',
                            data=json.dumps({'other': 'value'}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_280_limit_and_truncation(self):
        text_280 = "a" * 280
        res = self.app.post('/analyze',
                            data=json.dumps({'text': text_280}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)

        text_over = "a" * 300
        res = self.app.post('/analyze',
                            data=json.dumps({'text': text_over}),
                            content_type='application/json')
        self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
    unittest.main()

