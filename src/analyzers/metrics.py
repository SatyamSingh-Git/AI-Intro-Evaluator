from src.utils.text_utils import tokenize_text

class MetricsAnalyzer:
    def __init__(self, text):
        self.text = text
        self.words = tokenize_text(text)

    def calculate_speech_rate(self, duration_minutes=1):
        """
        Calculates Words Per Minute (WPM) and returns score.
        """
        word_count = len(self.words)
        if duration_minutes <= 0:
            wpm = 0
        else:
            wpm = word_count / duration_minutes
            
        score = 0
        if wpm > 161:
            score = 2
        elif 141 <= wpm <= 160:
            score = 6
        elif 111 <= wpm <= 140:
            score = 10
        elif 81 <= wpm <= 110:
            score = 6
        else: # < 80
            score = 2
            
        return {"wpm": wpm, "score": score}

    def calculate_vocabulary_richness(self):
        """
        Calculates Type-Token Ratio (TTR) and returns score.
        """
        if not self.words:
            return {"ttr": 0, "score": 2}
            
        unique_words = set(self.words)
        ttr = len(unique_words) / len(self.words)
        
        score = 0
        if 0.9 <= ttr <= 1.0:
            score = 10
        elif 0.7 <= ttr <= 0.89:
            score = 8
        elif 0.5 <= ttr <= 0.69:
            score = 6
        elif 0.3 <= ttr <= 0.49:
            score = 4
        else: # 0 - 0.29
            score = 2
        
        return {"ttr": ttr, "score": score}


