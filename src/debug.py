"""
Debug script to inspect Grammar errors and VADER sentiment scores in detail
"""
import sys
import language_tool_python
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from src.utils.text_utils import clean_text

def debug_grammar(file_path):
    """Inspect grammar errors in detail"""
    print("=" * 80)
    print("GRAMMAR ERROR ANALYSIS")
    print("=" * 80)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned_text = clean_text(text)
    tool = language_tool_python.LanguageTool('en-US')
    matches = tool.check(cleaned_text)
    
    print(f"\nTotal errors found: {len(matches)}")
    print(f"Word count: {len(cleaned_text.split())}")
    
    errors_per_100 = (len(matches) / len(cleaned_text.split())) * 100
    g_index = 1 - min(errors_per_100 / 10, 1)
    
    print(f"Errors per 100 words: {errors_per_100:.2f}")
    print(f"G-Index: {g_index:.2f}")
    
    if g_index >= 0.9:
        score = 10
    elif 0.7 <= g_index <= 0.89:
        score = 8
    elif 0.5 <= g_index <= 0.69:
        score = 6
    else:
        score = 4
    
    print(f"Grammar Score: {score}/10")
    
    print("\n" + "-" * 80)
    print("DETAILED ERROR LIST:")
    print("-" * 80)
    
    for i, match in enumerate(matches, 1):
        print(f"\nError {i}:")
        print(f"  Type: {match.rule_id}")
        print(f"  Category: {match.category}")
        print(f"  Message: {match.message}")
        print(f"  Context: ...{match.context}...")
        print(f"  Suggestions: {match.replacements[:3] if match.replacements else 'None'}")
    
    tool.close()
    print("\n" + "=" * 80)

def debug_sentiment(file_path):
    """Inspect VADER sentiment scores in detail"""
    print("=" * 80)
    print("SENTIMENT ANALYSIS")
    print("=" * 80)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned_text = clean_text(text)
    analyzer = SentimentIntensityAnalyzer()
    scores = analyzer.polarity_scores(cleaned_text)
    
    print(f"\nVADER Scores:")
    print(f"  Positive (pos): {scores['pos']:.4f}")
    print(f"  Neutral (neu): {scores['neu']:.4f}")
    print(f"  Negative (neg): {scores['neg']:.4f}")
    print(f"  Compound: {scores['compound']:.4f}")
    
    # Calculate using pos score
    pos_score = scores['pos']
    if pos_score >= 0.9:
        pos_based_score = 15
    elif 0.7 <= pos_score <= 0.89:
        pos_based_score = 12
    elif 0.5 <= pos_score <= 0.69:
        pos_based_score = 9
    elif 0.3 <= pos_score <= 0.49:
        pos_based_score = 6
    else:
        pos_based_score = 3
    
    # Calculate using compound score
    compound_score = max(0, scores['compound'])
    if compound_score >= 0.9:
        compound_based_score = 15
    elif 0.7 <= compound_score <= 0.89:
        compound_based_score = 12
    elif 0.5 <= compound_score <= 0.69:
        compound_based_score = 9
    elif 0.3 <= compound_score <= 0.49:
        compound_based_score = 6
    else:
        compound_based_score = 3
    
    # Calculate using pos/(pos+neg)
    if scores['pos'] + scores['neg'] > 0:
        pos_ratio = scores['pos'] / (scores['pos'] + scores['neg'])
    else:
        pos_ratio = 0
    
    if pos_ratio >= 0.9:
        ratio_based_score = 15
    elif 0.7 <= pos_ratio <= 0.89:
        ratio_based_score = 12
    elif 0.5 <= pos_ratio <= 0.69:
        ratio_based_score = 9
    elif 0.3 <= pos_ratio <= 0.49:
        ratio_based_score = 6
    else:
        ratio_based_score = 3
    
    print(f"\n" + "-" * 80)
    print("SCORE CALCULATIONS:")
    print("-" * 80)
    print(f"Using pos score ({pos_score:.4f}): {pos_based_score}/15")
    print(f"Using compound score ({compound_score:.4f}): {compound_based_score}/15")
    print(f"Using pos/(pos+neg) ratio ({pos_ratio:.4f}): {ratio_based_score}/15")
    print(f"\nSample expected score: 12/15 (positivity 0.7-0.89)")
    
    print("\n" + "=" * 80)

def debug_keywords(file_path):
    """Inspect keyword matches in detail"""
    from src.config import KEYWORDS
    
    print("=" * 80)
    print("KEYWORD ANALYSIS")
    print("=" * 80)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    cleaned_text = clean_text(text).lower()
    
    print("\nMUST HAVE Keywords (4 points each, max 20):")
    print("-" * 80)
    must_have_score = 0
    for topic, phrases in KEYWORDS["Must Have"].items():
        found = False
        matched_phrase = None
        for phrase in phrases:
            if phrase in cleaned_text:
                found = True
                matched_phrase = phrase
                break
        
        status = "✓" if found else "✗"
        print(f"{status} {topic}: {matched_phrase if found else 'Not found'}")
        if found:
            must_have_score += 4
    
    print(f"\nMust Have Score: {must_have_score}/20")
    
    print("\n" + "-" * 80)
    print("GOOD TO HAVE Keywords (2 points each, max 10):")
    print("-" * 80)
    good_to_have_score = 0
    for topic, phrases in KEYWORDS["Good to Have"].items():
        found = False
        matched_phrase = None
        for phrase in phrases:
            if phrase in cleaned_text:
                found = True
                matched_phrase = phrase
                break
        
        status = "✓" if found else "✗"
        print(f"{status} {topic}: {matched_phrase if found else 'Not found'}")
        if found:
            good_to_have_score += 2
    
    print(f"\nGood to Have Score: {good_to_have_score}/10")
    print(f"Total Keyword Score: {must_have_score + good_to_have_score}/30")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    # Use the sample text file
    file_path = r"e:\AI Intro Evaluator\Docs\Sample text for case study.txt"
    
    print("\n\n")
    debug_keywords(file_path)
    print("\n\n")
    debug_grammar(file_path)
    print("\n\n")
    debug_sentiment(file_path)
