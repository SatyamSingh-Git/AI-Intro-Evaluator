import re

def clean_text(text):
    """
    Cleans the input text by removing extra whitespace and normalizing.
    """
    if not text:
        return ""
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def tokenize_text(text):
    """
    Splits text into words.
    """
    if not text:
        return []
    # Simple word tokenization (removing punctuation for counting)
    words = re.findall(r'\b\w+\b', text.lower())
    return words

def get_sentences(text):
    """
    Splits text into sentences.
    """
    if not text:
        return []
    # Simple sentence splitting
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

