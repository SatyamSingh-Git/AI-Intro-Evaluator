from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class SentimentAnalyzer:
    def __init__(self, text):
        self.text = text
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self):
        """
        Analyzes sentiment using VADER.
        Returns a dictionary with scores and a label.
        """
        scores = self.analyzer.polarity_scores(self.text)
        # Use compound score as it represents overall normalized sentiment
        # Compound score ranges from -1 to 1, we treat positive values (0 to 1) as positivity
        compound_score = scores['compound']
        
        # For negative compound scores, treat as low positivity
        positivity_score = max(0, compound_score)
        
        score = 0
        if positivity_score >= 0.9:
            score = 15
        elif 0.7 <= positivity_score <= 0.89:
            score = 12
        elif 0.5 <= positivity_score <= 0.69:
            score = 9
        elif 0.3 <= positivity_score <= 0.49:
            score = 6
        else: # < 0.3
            score = 3
            
        return {
            "scores": scores,
            "positivity_score": positivity_score,
            "score": score
        }


