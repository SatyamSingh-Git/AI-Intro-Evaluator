import language_tool_python
from src.config import FILLER_WORDS
from src.utils.text_utils import clean_text, tokenize_text

class GrammarAnalyzer:
    def __init__(self, text):
        self.text = clean_text(text)
        try:
            self.tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            print(f"Warning: Could not initialize LanguageTool: {e}")
            self.tool = None

    def count_grammar_errors(self):
        """
        Counts grammar errors and calculates score.
        Filters out proper name spelling errors (MORFOLOGIK_RULE_EN_US).
        """
        if not self.tool:
            return {"count": 0, "matches": [], "score": 0}
        
        all_matches = self.tool.check(self.text)
        
        # Filter out proper name spelling errors (these are often false positives)
        matches = [m for m in all_matches if m.rule_id != 'MORFOLOGIK_RULE_EN_US']
        error_count = len(matches)
        
        words = tokenize_text(self.text)
        word_count = len(words)
        
        if word_count == 0:
            return {"count": error_count, "matches": matches, "score": 0}

        # Formula: Grammar Score = 1 - min(errors per 100 words / 10, 1)
        errors_per_100 = (error_count / word_count) * 100
        g_index = 1 - min(errors_per_100 / 10, 1)
        
        score = 0
        if g_index > 0.9:
            score = 10
        elif 0.7 <= g_index <= 0.89:
            score = 8
        elif 0.5 <= g_index <= 0.69:
            score = 6
        elif 0.3 <= g_index <= 0.49:
            score = 4
        else: # < 0.3
            score = 2
            
        return {"count": error_count, "matches": matches, "score": score, "g_index": g_index}

    def count_filler_words(self):
        """
        Counts filler words and calculates score.
        """
        words = tokenize_text(self.text)
        count = 0
        found_fillers = []
        
        # Check for single word fillers
        for word in words:
            if word in FILLER_WORDS:
                count += 1
                found_fillers.append(word)
                
        # Also check for multi-word fillers like "you know"
        text_lower = self.text.lower()
        for filler in FILLER_WORDS:
            if " " in filler:
                matches = text_lower.count(filler)
                if matches > 0:
                    count += matches
                    found_fillers.extend([filler] * matches)
                    
        # Calculate rate (fillers per 100 words)
        total_words = len(words)
        rate = (count / total_words * 100) if total_words > 0 else 0
        
        score = 0
        if 0 <= rate <= 3:
            score = 15
        elif 4 <= rate <= 6:
            score = 12
        elif 7 <= rate <= 9:
            score = 9
        elif 10 <= rate <= 12:
            score = 6
        else: # 13 and above
            score = 3
        
        return {"count": count, "rate": rate, "fillers": found_fillers, "score": score}


