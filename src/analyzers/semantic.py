"""
Semantic Similarity Analyzer Module
Analyzes semantic relevance of sentences to introduction topics
"""

from sentence_transformers import SentenceTransformer, util
import streamlit as st

@st.cache_resource
def load_semantic_model():
    """Load the sentence transformer model (cached)"""
    return SentenceTransformer('all-MiniLM-L6-v2')

class SemanticAnalyzer:
    def __init__(self, text):
        self.text = text
        self.sentences = self._split_into_sentences(text)
        self.model = load_semantic_model()
        
    def _split_into_sentences(self, text):
        """Split text into sentences"""
        import re
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        return sentences
    
    def analyze_relevance(self):
        """
        Analyze semantic similarity of each sentence to introduction topics
        
        Returns:
            list of dict: Each dict contains sentence, score, and relevance level
        """
        # Define ideal introduction topics
        reference_topics = [
            "greeting and introduction",
            "personal name and identity",
            "age and school information",
            "family background and members",
            "hobbies interests and activities",
            "goals dreams and aspirations",
            "unique qualities and strengths"
        ]
        
        if not self.sentences:
            return []
        
        # Encode reference topics and sentences
        topic_embeddings = self.model.encode(reference_topics, convert_to_tensor=True)
        sentence_embeddings = self.model.encode(self.sentences, convert_to_tensor=True)
        
        results = []
        for i, sentence in enumerate(self.sentences):
            # Calculate similarity to all topics, take max
            similarities = util.cos_sim(sentence_embeddings[i], topic_embeddings)[0]
            max_similarity = float(similarities.max())
            
            # Determine relevance level
            if max_similarity >= 0.5:
                relevance = 'high'
                color = '#10B981'  # green
            elif max_similarity >= 0.3:
                relevance = 'medium'
                color = '#F59E0B'  # yellow
            else:
                relevance = 'low'
                color = '#EF4444'  # red
            
            results.append({
                'sentence': sentence,
                'score': max_similarity,
                'relevance': relevance,
                'color': color
            })
        
        return results
    
    def get_overall_score(self):
        """
        Calculate overall semantic coherence score
        
        Returns:
            float: Average relevance score (0-1)
        """
        results = self.analyze_relevance()
        if not results:
            return 0.0
        
        avg_score = sum(r['score'] for r in results) / len(results)
        return avg_score
    
    def get_highlighted_text(self):
        """
        Get HTML-highlighted text with color-coded sentences
        
        Returns:
            str: HTML string with colored sentences
        """
        results = self.analyze_relevance()
        
        html_parts = []
        for result in results:
            sentence = result['sentence']
            color = result['color']
            score = result['score']
            
            # Create tooltip with score
            html_parts.append(
                f'<span style="background-color: {color}20; border-left: 3px solid {color}; '
                f'padding: 2px 5px; margin: 2px 0; display: inline-block; border-radius: 3px;" '
                f'title="Relevance: {score:.2f}">{sentence}.</span> '
            )
        
        return ''.join(html_parts)
