import os
import sys

# Add the src directory to the python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.analyzers.content import ContentAnalyzer
from src.analyzers.grammar import GrammarAnalyzer
from src.analyzers.sentiment import SentimentAnalyzer
from src.analyzers.metrics import MetricsAnalyzer

def main():
    print("AI Intro Evaluator - Starting Analysis...")
    
    input_path = os.path.join("data", "input", "sample.txt")
    output_path = os.path.join("data", "output", "evaluation_report.txt")
    
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"Analyzing text from: {input_path}")
    print("-" * 50)

    # 1. Content Analysis
    content_analyzer = ContentAnalyzer(text)
    keywords_result = content_analyzer.check_keywords()
    flow_result = content_analyzer.check_flow()
    salutation_result = content_analyzer.check_salutation()

    # 2. Grammar Analysis
    grammar_analyzer = GrammarAnalyzer(text)
    grammar_result = grammar_analyzer.count_grammar_errors()
    filler_result = grammar_analyzer.count_filler_words()
    
    # Debug Grammar
    print("\nDEBUG: Grammar Matches:")
    for match in grammar_result['matches']:
        print(f"- {match.rule_id}: {match.message} (Context: {match.context})")

    # 3. Sentiment Analysis
    sentiment_analyzer = SentimentAnalyzer(text)
    sentiment_result = sentiment_analyzer.analyze_sentiment()
    print(f"\nDEBUG: Sentiment Scores: {sentiment_result['scores']}")


    # 4. Metrics Analysis
    metrics_analyzer = MetricsAnalyzer(text)
    # Assuming 1 minute for calculation as we don't have audio duration
    wpm_result = metrics_analyzer.calculate_speech_rate(duration_minutes=1) 
    vocab_result = metrics_analyzer.calculate_vocabulary_richness()

    # Generate Report
    report = []
    report.append("AI Intro Evaluator Report")
    report.append("=" * 30)
    report.append(f"Input Text:\n{text}\n")
    report.append("=" * 30)
    
    total_score = 0
    
    # 1. Content & Structure
    report.append("\n1. Content & Structure (Total 30)")
    report.append("-" * 30)
    
    report.append("  a) Salutation Level (Max 5)")
    report.append(f"     Present: {salutation_result['present']}")
    report.append(f"     Type: {salutation_result['type']}")
    report.append(f"     Score: {salutation_result['score']}")
    total_score += salutation_result['score']
    
    report.append("\n  b) Keyword Presence (Max 30)")
    report.append("     Must Have (Max 20):")
    for topic, found in keywords_result["topics"].items():
        if topic in ["Name", "Age", "Class_School", "Family", "Hobbies"]:
            status = "Found" if found else "Not Found"
            report.append(f"       - {topic}: {status}")
    
    report.append("     Good to Have (Max 10):")
    for topic, found in keywords_result["topics"].items():
        if topic not in ["Name", "Age", "Class_School", "Family", "Hobbies"]:
            status = "Found" if found else "Not Found"
            report.append(f"       - {topic}: {status}")
            
    report.append(f"     Score: {keywords_result['score']}")
    total_score += keywords_result['score']

    report.append("\n  c) Flow Analysis (Max 5)")
    report.append(f"     Valid Order: {flow_result['valid_order']}")
    if flow_result['feedback']:
        report.append("     Feedback:")
        for fb in flow_result['feedback']:
            report.append(f"       - {fb}")
    report.append(f"     Score: {flow_result['score']}")
    total_score += flow_result['score']

    # 2. Speech Rate
    report.append("\n2. Speech Rate (Total 10)")
    report.append("-" * 30)
    report.append(f"  Word Count: {len(metrics_analyzer.words)}")
    report.append(f"  Speech Rate (assuming 1 min): {wpm_result['wpm']:.2f} WPM")
    report.append(f"  Score: {wpm_result['score']}")
    total_score += wpm_result['score']

    # 3. Language & Grammar
    report.append("\n3. Language & Grammar (Total 20)")
    report.append("-" * 30)
    
    report.append("  a) Grammar Errors (Max 10)")
    report.append(f"     Errors Found: {grammar_result['count']}")
    report.append(f"     G-Index: {grammar_result.get('g_index', 0):.2f}")
    report.append(f"     Score: {grammar_result['score']}")
    total_score += grammar_result['score']
    
    report.append("\n  b) Vocabulary Richness (Max 10)")
    report.append(f"     TTR: {vocab_result['ttr']:.2f}")
    report.append(f"     Score: {vocab_result['score']}")
    total_score += vocab_result['score']

    # 4. Clarity
    report.append("\n4. Clarity (Total 15)")
    report.append("-" * 30)
    report.append("  Filler Word Rate (Max 15)")
    report.append(f"     Count: {filler_result['count']}")
    report.append(f"     Rate: {filler_result['rate']:.2f}%")
    report.append(f"     Fillers: {', '.join(filler_result['fillers'])}")
    report.append(f"     Score: {filler_result['score']}")
    total_score += filler_result['score']

    # 5. Engagement
    report.append("\n5. Engagement (Total 15)")
    report.append("-" * 30)
    report.append("  Sentiment/Positivity (Max 15)")
    report.append(f"     Positivity Score: {sentiment_result['positivity_score']:.2f}")
    report.append(f"     Score: {sentiment_result['score']}")
    total_score += sentiment_result['score']

    report.append("=" * 30)
    report.append(f"TOTAL SCORE: {total_score} / 100")
    report.append("=" * 30)

    # Print and Save
    report_text = "\n".join(report)
    print(report_text)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(report_text)
    
    print("-" * 50)
    print(f"Report saved to: {output_path}")

if __name__ == "__main__":
    main()

