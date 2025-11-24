"""
AI Intro Evaluator - Streamlit Web Application
Modern and Advanced UI for evaluating student introductions
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.analyzers.content import ContentAnalyzer
from src.analyzers.grammar import GrammarAnalyzer
from src.analyzers.sentiment import SentimentAnalyzer
from src.analyzers.metrics import MetricsAnalyzer
from src.analyzers.semantic import SemanticAnalyzer
from src.utils.feedback_generator import (
    generate_comprehensive_feedback,
    generate_why_explanation
)
from src.utils.pdf_generator import generate_pdf_report
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Intro Evaluator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6C63FF;
        --secondary-color: #4CAF50;
        --accent-color: #FF6B6B;
        --bg-color: #F8F9FA;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin-top: 0.5rem;
        opacity: 0.95;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border-left: 4px solid var(--primary-color);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 1rem;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0,0,0,0.15);
    }
    
    .metric-title {
        font-size: 0.9rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1F2937;
    }
    
    /* Score badges */
    .score-excellent {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        font-size: 1.5rem;
    }
    
    .score-good {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        font-size: 1.5rem;
    }
    
    .score-average {
        background: linear-gradient(135deg, #FFA726 0%, #FB8C00 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        font-size: 1.5rem;
    }
    
    .score-poor {
        background: linear-gradient(135deg, #EF5350 0%, #E53935 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        display: inline-block;
        font-size: 1.5rem;
    }
    
    /* Section headers */
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.8rem;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #E5E7EB;
    }
    
    /* Info boxes */
    .info-box {
        background: #F3F4F6;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #1F2937;
    }
    
    .success-box {
        background: #ECFDF5;
        border-left: 4px solid #10B981;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #065F46;
    }
    
    .warning-box {
        background: #FFFBEB;
        border-left: 4px solid #F59E0B;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #92400E;
    }
    
    .error-box {
        background: #FEF2F2;
        border-left: 4px solid #EF4444;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: #991B1B;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 50px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    /* Text area styling */
    .stTextArea>div>div>textarea {
        border-radius: 10px;
        border: 2px solid #E5E7EB;
        font-size: 1rem;
        padding: 1rem;
    }
    
    .stTextArea>div>div>textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Keyword badge */
    .keyword-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    .found {
        background: #D1FAE5;
        color: #065F46;
        border: 1px solid #10B981;
    }
    
    .not-found {
        background: #FEE2E2;
        color: #991B1B;
        border: 1px solid #EF4444;
    }
</style>
""", unsafe_allow_html=True)

def get_score_badge(score, max_score):
    """Return HTML for score badge based on percentage"""
    percentage = (score / max_score) * 100
    
    if percentage >= 85:
        badge_class = "score-excellent"
        emoji = "🌟"
    elif percentage >= 70:
        badge_class = "score-good"
        emoji = "✅"
    elif percentage >= 50:
        badge_class = "score-average"
        emoji = "⚠️"
    else:
        badge_class = "score-poor"
        emoji = "❌"
    
    return f'<span class="{badge_class}">{emoji} {score}/{max_score}</span>'

def create_gauge_chart(score, max_score, title):
    """Create a modern gauge chart for scores"""
    percentage = (score / max_score) * 100
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20, 'color': '#1F2937'}},
        delta={'reference': max_score * 0.7},
        gauge={
            'axis': {'range': [None, max_score], 'tickwidth': 1, 'tickcolor': "#1F2937"},
            'bar': {'color': "#667eea"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "#E5E7EB",
            'steps': [
                {'range': [0, max_score * 0.5], 'color': '#FEE2E2'},
                {'range': [max_score * 0.5, max_score * 0.7], 'color': '#FEF3C7'},
                {'range': [max_score * 0.7, max_score * 0.85], 'color': '#D1FAE5'},
                {'range': [max_score * 0.85, max_score], 'color': '#DBEAFE'}
            ],
            'threshold': {
                'line': {'color': "#764ba2", 'width': 4},
                'thickness': 0.75,
                'value': max_score * 0.85
            }
        }
    ))
    
    fig.update_layout(
        height=300,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#1F2937", family="Arial")
    )
    
    return fig

def create_radar_chart(categories, scores, max_scores):
    """Create a radar chart for category breakdown"""
    percentages = [(s / m * 100) for s, m in zip(scores, max_scores)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=percentages,
        theta=categories,
        fill='toself',
        fillcolor='rgba(102, 126, 234, 0.3)',
        line=dict(color='#667eea', width=3),
        name='Your Score'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=[100] * len(categories),
        theta=categories,
        fill='toself',
        fillcolor='rgba(118, 75, 162, 0.1)',
        line=dict(color='#764ba2', width=2, dash='dash'),
        name='Maximum'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                ticksuffix='%',
                gridcolor='#E5E7EB'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=True,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#1F2937", family="Arial", size=12)
    )
    
    return fig

def create_bar_chart(categories, scores, max_scores):
    """Create a horizontal bar chart for scores"""
    percentages = [(s / m * 100) for s, m in zip(scores, max_scores)]
    
    # Create color scale based on percentage
    colors = ['#EF4444' if p < 50 else '#F59E0B' if p < 70 else '#10B981' if p < 85 else '#667eea' 
              for p in percentages]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=categories,
        x=scores,
        orientation='h',
        marker=dict(
            color=colors,
            line=dict(color='white', width=2)
        ),
        text=[f'{s}/{m}' for s, m in zip(scores, max_scores)],
        textposition='auto',
        textfont=dict(color='white', size=14, family='Arial Black'),
        hovertemplate='<b>%{y}</b><br>Score: %{x}<br>Percentage: %{customdata:.1f}%<extra></extra>',
        customdata=percentages
    ))
    
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#1F2937", family="Arial"),
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E7EB',
            title=dict(text='Score', font=dict(size=14, color='#6B7280'))
        ),
        yaxis=dict(
            showgrid=False,
            title=dict(text='', font=dict(size=14, color='#6B7280'))
        ),
        hoverlabel=dict(
            bgcolor="white",
            font=dict(size=12, family="Arial")
        )
    )
    
    return fig

def evaluate_text(text, audio_duration=None):
    """Evaluate the input text and return results
    
    Args:
        text (str): The text to evaluate
        audio_duration (float, optional): Duration of audio in minutes for accurate WPM calculation
    """
    # Content Analysis
    content_analyzer = ContentAnalyzer(text)
    keywords_result = content_analyzer.check_keywords()
    flow_result = content_analyzer.check_flow()
    salutation_result = content_analyzer.check_salutation()
    
    # Grammar Analysis
    grammar_analyzer = GrammarAnalyzer(text)
    grammar_result = grammar_analyzer.count_grammar_errors()
    filler_result = grammar_analyzer.count_filler_words()
    
    # Sentiment Analysis
    sentiment_analyzer = SentimentAnalyzer(text)
    sentiment_result = sentiment_analyzer.analyze_sentiment()
    
    # Metrics Analysis
    metrics_analyzer = MetricsAnalyzer(text)
    # Use actual audio duration if available, otherwise default to 1 minute
    speech_rate_result = metrics_analyzer.calculate_speech_rate(
        duration_minutes=audio_duration if audio_duration else 1.0
    )
    vocab_result = metrics_analyzer.calculate_vocabulary_richness()
    
    return {
        'keywords': keywords_result,
        'flow': flow_result,
        'salutation': salutation_result,
        'grammar': grammar_result,
        'filler': filler_result,
        'sentiment': sentiment_result,
        'speech_rate': speech_rate_result,
        'vocabulary': vocab_result
    }

def main():
    # Header
    st.markdown("""
        <div class="main-header">
            <h1>🎓 AI Intro Evaluator</h1>
            <p>Advanced evaluation system for student introductions using AI-powered analysis</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 📊 Evaluation Criteria")
        st.markdown("""
        - **Content & Structure** (30 pts)
        - **Speech Rate** (10 pts)
        - **Language & Grammar** (20 pts)
        - **Clarity** (15 pts)
        - **Engagement** (15 pts)
        """)
        
        st.markdown("---")
        st.markdown("### 📝 Instructions")
        st.markdown("""
        1. Upload a text file or paste your introduction
        2. Click 'Evaluate' to analyze
        3. Review your detailed scores
        4. Download the report
        """)
        
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This tool uses advanced NLP techniques including:
        - VADER Sentiment Analysis
        - LanguageTool Grammar Checking
        - Vocabulary Richness Analysis
        - Content Structure Evaluation
        """)
    
    # Main content
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<p class="section-header">📄 Input Your Introduction</p>', unsafe_allow_html=True)
        
        # Student name input
        student_name = st.text_input(
            "👤 Student Name (Optional)",
            placeholder="Enter your name...",
            help="Your name will appear on the PDF report"
        )
        
        # Store in session state for PDF generation
        if student_name:
            st.session_state['student_name'] = student_name
        
        # Input method selection
        input_method = st.radio("Choose input method:", ["✍️ Type/Paste Text", "📁 Upload File", "🎤 Upload Audio"], horizontal=True)
        
        text_input = ""
        audio_duration = None
        
        if input_method == "✍️ Type/Paste Text":
            text_input = st.text_area(
                "Enter your introduction here:",
                height=300,
                placeholder="Hello everyone, my name is...",
                help="Type or paste your introduction speech here"
            )
        elif input_method == "📁 Upload File":
            uploaded_file = st.file_uploader(
                "Upload a text file (.txt)",
                type=['txt'],
                help="Upload a .txt file containing your introduction"
            )
            
            if uploaded_file is not None:
                text_input = uploaded_file.read().decode('utf-8')
                st.text_area("Preview:", text_input, height=200, disabled=True)
        else:  # Audio upload
            st.markdown("**Upload an audio recording of your introduction**")
            audio_file = st.file_uploader(
                "Choose an audio file",
                type=['mp3', 'wav', 'm4a', 'ogg'],
                help="Upload audio in MP3, WAV, M4A, or OGG format"
            )
            
            if audio_file is not None:
                # Display audio player
                st.audio(audio_file, format=f'audio/{audio_file.type.split("/")[1]}')
                
                # Transcribe with Whisper
                with st.spinner("🎧 Transcribing audio with Whisper AI..."):
                    try:
                        import whisper
                        import tempfile
                        import os
                        from pydub import AudioSegment
                        
                        # Save uploaded file temporarily
                        with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{audio_file.name.split(".")[-1]}') as tmp_file:
                            tmp_file.write(audio_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        try:
                            # Get audio duration
                            audio = AudioSegment.from_file(tmp_path)
                            audio_duration = len(audio) / 1000.0 / 60.0  # Convert to minutes
                            
                            # Load Whisper model (base model for speed)
                            model = whisper.load_model("base")
                            
                            # Transcribe
                            result = whisper.transcribe(model, tmp_path, language="en")
                            text_input = result["text"]
                            
                            # Perform acoustic analysis
                            from src.analyzers.acoustic import AcousticAnalyzer
                            acoustic_analyzer = AcousticAnalyzer(tmp_path)
                            acoustic_results = acoustic_analyzer.get_comprehensive_analysis(text_input)
                            
                            st.success(f"✅ Transcription complete! Duration: {audio_duration:.2f} minutes")
                            st.text_area("📝 Transcribed Text:", text_input, height=200)
                            
                            # Display acoustic analysis
                            with st.expander("🎵 Acoustic Analysis Details"):
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Pause Count", acoustic_results['pauses']['pause_count'])
                                    st.metric("Pause Time", f"{acoustic_results['pauses']['total_pause_duration']:.1f}s")
                                with col2:
                                    st.metric("Speaking Time", f"{acoustic_results['speaking_segments']['total_speaking_time']:.1f}s")
                                    st.metric("Speaking %", f"{acoustic_results['speaking_segments']['speaking_percentage']:.1f}%")
                                with col3:
                                    st.metric("Actual WPM", f"{acoustic_results['wpm_analysis']['wpm']:.0f}")
                                    st.metric("Filler Words", acoustic_results['filler_analysis']['filler_count'])
                            
                        finally:
                            # Clean up temp file
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
                    
                    except ImportError as e:
                        st.error("📦 Audio transcription requires `openai-whisper` and `pydub`. Please install them.")
                        st.code("pip install openai-whisper pydub", language="bash")
                    except Exception as e:
                        st.error(f"❌ Transcription failed: {str(e)}")
    
    with col2:
        st.markdown('<p class="section-header">⚡ Quick Stats</p>', unsafe_allow_html=True)
        
        if text_input:
            word_count = len(text_input.split())
            char_count = len(text_input)
            sentence_count = text_input.count('.') + text_input.count('!') + text_input.count('?')
            
            st.metric("Words", word_count, help="Total word count")
            st.metric("Characters", char_count, help="Total character count")
            st.metric("Sentences", sentence_count, help="Approximate sentence count")
            
            # Show audio duration if available
            if audio_duration:
                st.metric("Audio Duration", f"{audio_duration:.2f} min", help="Recorded audio length")
        else:
            st.info("📝 Enter text to see statistics")
    
    # Evaluate button
    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("🚀 Evaluate Introduction", width="stretch"):
        if not text_input or len(text_input.strip()) < 10:
            st.error("⚠️ Please provide a valid introduction text (at least 10 characters)")
        else:
            with st.spinner("🔍 Analyzing your introduction..."):
                # Pass audio duration if available for accurate WPM calculation
                results = evaluate_text(text_input, audio_duration=audio_duration)
                
                # Calculate total score
                total_score = (
                    results['salutation']['score'] +
                    results['keywords']['score'] +
                    results['flow']['score'] +
                    results['speech_rate']['score'] +
                    results['grammar']['score'] +
                    results['vocabulary']['score'] +
                    results['filler']['score'] +
                    results['sentiment']['score']
                )
                
                max_total = 100
                
                # Display total score
                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<p class="section-header">🏆 Overall Score</p>', unsafe_allow_html=True)
                
                score_col1, score_col2, score_col3 = st.columns([1, 2, 1])
                
                with score_col2:
                    st.markdown(f"""
                        <div style='text-align: center; padding: 2rem; background: white; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);'>
                            {get_score_badge(total_score, max_total)}
                            <p style='margin-top: 1rem; color: #6B7280; font-size: 1.1rem;'>
                                {'🌟 Excellent!' if total_score >= 85 else '✅ Good Job!' if total_score >= 70 else '⚠️ Room for Improvement' if total_score >= 50 else '❌ Needs Work'}
                            </p>
                        </div>
                    """, unsafe_allow_html=True)
                
                # Gauge chart
                st.plotly_chart(create_gauge_chart(total_score, max_total, "Overall Performance"), width="stretch")
                
                # Category breakdown
                st.markdown('<p class="section-header">📊 Category Breakdown</p>', unsafe_allow_html=True)
                
                tab1, tab2, tab3 = st.tabs(["📈 Bar Chart", "🎯 Radar Chart", "📋 Detailed Scores"])
                
                categories = ["Salutation", "Keywords", "Flow", "Speech Rate", "Grammar", "Vocabulary", "Clarity", "Engagement"]
                scores = [
                    results['salutation']['score'],
                    results['keywords']['score'],
                    results['flow']['score'],
                    results['speech_rate']['score'],
                    results['grammar']['score'],
                    results['vocabulary']['score'],
                    results['filler']['score'],
                    results['sentiment']['score']
                ]
                max_scores = [5, 30, 5, 10, 10, 10, 15, 15]
                
                with tab1:
                    st.plotly_chart(create_bar_chart(categories, scores, max_scores), width="stretch")
                
                with tab2:
                    st.plotly_chart(create_radar_chart(categories, scores, max_scores), width="stretch")
                
                with tab3:
                    # Detailed breakdown
                    st.markdown("#### 1. Content & Structure (30 points)")
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Salutation</div>
                                <div class='metric-value'>{results['salutation']['score']}/5</div>
                                <small>{results['salutation']['type'] if results['salutation']['present'] else 'None'}</small>
                            </div>
                        """, unsafe_allow_html=True)
                        # Why tooltip
                        with st.expander("ℹ️ Why this score?"):
                            why_text = generate_why_explanation('salutation', results['salutation']['score'], 5, results['salutation'])
                            st.markdown(why_text)
                    
                    with col2:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Keywords</div>
                                <div class='metric-value'>{results['keywords']['score']}/30</div>
                            </div>
                        """, unsafe_allow_html=True)
                        # Why tooltip
                        with st.expander("ℹ️ Why this score?"):
                            why_text = generate_why_explanation('keywords', results['keywords']['score'], 30, results['keywords'])
                            st.markdown(why_text)
                    
                    with col3:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Flow</div>
                                <div class='metric-value'>{results['flow']['score']}/5</div>
                                <small>{'✓ Proper order' if results['flow']['valid_order'] else '✗ Needs improvement'}</small>
                            </div>
                        """, unsafe_allow_html=True)
                        # Why tooltip
                        with st.expander("ℹ️ Why this score?"):
                            why_text = generate_why_explanation('flow', results['flow']['score'], 5, results['flow'])
                            st.markdown(why_text)
                    
                    # Keywords detail
                    with st.expander("🔍 View Keyword Details"):
                        st.markdown("**Must Have Topics:**")
                        keyword_html = ""
                        for topic, found in results['keywords']['topics'].items():
                            if topic in ['Name', 'Age', 'Class_School', 'Family', 'Hobbies']:
                                badge_class = "found" if found else "not-found"
                                status = "✓" if found else "✗"
                                keyword_html += f'<span class="keyword-badge {badge_class}">{status} {topic}</span> '
                        st.markdown(keyword_html, unsafe_allow_html=True)
                        
                        st.markdown("<br>**Good to Have Topics:**", unsafe_allow_html=True)
                        keyword_html2 = ""
                        for topic, found in results['keywords']['topics'].items():
                            if topic not in ['Name', 'Age', 'Class_School', 'Family', 'Hobbies']:
                                badge_class = "found" if found else "not-found"
                                status = "✓" if found else "✗"
                                keyword_html2 += f'<span class="keyword-badge {badge_class}">{status} {topic.replace("_", " ")}</span> '
                        st.markdown(keyword_html2, unsafe_allow_html=True)
                    
                    st.markdown("#### 2. Speech Rate (10 points)")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Words Per Minute</div>
                                <div class='metric-value'>{results['speech_rate']['wpm']:.0f}</div>
                                <small>Ideal: 111-140 WPM</small>
                            </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Score</div>
                                <div class='metric-value'>{results['speech_rate']['score']}/10</div>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Why tooltip for speech rate
                    with st.expander("ℹ️ Why this score?"):
                        why_text = generate_why_explanation('speech_rate', results['speech_rate']['score'], 10, results['speech_rate'])
                        st.markdown(why_text)
                    
                    st.markdown("#### 3. Language & Grammar (20 points)")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Grammar</div>
                                <div class='metric-value'>{results['grammar']['score']}/10</div>
                                <small>{results['grammar']['count']} errors found</small>
                            </div>
                        """, unsafe_allow_html=True)
                        # Why tooltip
                        with st.expander("ℹ️ Why this score?"):
                            why_text = generate_why_explanation('grammar', results['grammar']['score'], 10, results['grammar'])
                            st.markdown(why_text)
                    
                    with col2:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Vocabulary</div>
                                <div class='metric-value'>{results['vocabulary']['score']}/10</div>
                                <small>TTR: {results['vocabulary']['ttr']:.2f}</small>
                            </div>
                        """, unsafe_allow_html=True)
                        # Why tooltip
                        with st.expander("ℹ️ Why this score?"):
                            why_text = generate_why_explanation('vocabulary', results['vocabulary']['score'], 10, results['vocabulary'])
                            st.markdown(why_text)
                    
                    # Grammar errors detail with inline highlighting
                    if results['grammar']['count'] > 0:
                        st.markdown("##### 📝 Grammar Issues Found")
                        
                        # Create highlighted text with errors
                        highlighted_text = text_input
                        matches = results['grammar']['matches'][:10]  # Limit to 10 errors
                        
                        # Sort matches by position (descending) to avoid offset issues
                        sorted_matches = sorted(matches, key=lambda x: x.offset, reverse=True)
                        
                        for match in sorted_matches:
                            start = match.offset
                            end = match.offset + match.error_length
                            error_text = highlighted_text[start:end]
                            
                            # Replace with highlighted version - red text on light red background
                            replacement = f'<span style="background-color: #FEE2E2; color: #DC2626; border-bottom: 2px solid #EF4444; padding: 2px 4px; border-radius: 3px; font-weight: 500;" title="{match.message}">{error_text}</span>'
                            highlighted_text = highlighted_text[:start] + replacement + highlighted_text[end:]
                        
                        # Display highlighted text with dark text on light background
                        st.markdown(
                            f'<div style="background: #F9FAFB; color: #1F2937; padding: 1rem; border-radius: 8px; border-left: 4px solid #EF4444; line-height: 1.8; font-size: 0.95rem;">{highlighted_text.replace(chr(10), "<br>")}</div>',
                            unsafe_allow_html=True
                        )
                        
                        # Show error list
                        with st.expander(f"⚠️ View {results['grammar']['count']} Grammar Error Details"):
                            for i, match in enumerate(matches, 1):
                                st.markdown(f"""
                                    <div class='warning-box'>
                                        <strong>Error {i}:</strong> {match.message}<br>
                                        <small><em>Type: {match.rule_id}</em></small>
                                    </div>
                                """, unsafe_allow_html=True)
                    else:
                        st.success("✅ No grammar errors detected!")
                    
                    st.markdown("#### 4. Clarity (15 points)")
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-title'>Filler Words</div>
                            <div class='metric-value'>{results['filler']['score']}/15</div>
                            <small>{results['filler']['count']} fillers ({results['filler']['rate']:.2f}%)</small>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Why tooltip for clarity
                    with st.expander("ℹ️ Why this score?"):
                        why_text = generate_why_explanation('clarity', results['filler']['score'], 15, results['filler'])
                        st.markdown(why_text)
                    
                    st.markdown("#### 5. Engagement (15 points)")
                    st.markdown(f"""
                        <div class='metric-card'>
                            <div class='metric-title'>Sentiment/Positivity</div>
                            <div class='metric-value'>{results['sentiment']['score']}/15</div>
                            <small>Positivity: {results['sentiment']['positivity_score']:.2f}</small>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Why tooltip for engagement
                    with st.expander("ℹ️ Why this score?"):
                        why_text = generate_why_explanation('sentiment', results['sentiment']['score'], 15, results['sentiment'])
                        st.markdown(why_text)
                
                # Semantic Similarity Analysis
                st.markdown('<p class="section-header">🎯 Semantic Relevance Analysis</p>', unsafe_allow_html=True)
                
                try:
                    from src.analyzers.semantic import SemanticAnalyzer
                    
                    with st.spinner("Analyzing semantic relevance..."):
                        semantic_analyzer = SemanticAnalyzer(text_input)
                        semantic_results = semantic_analyzer.analyze_relevance()
                        overall_semantic_score = semantic_analyzer.get_overall_score()
                    
                    # Display overall semantic coherence
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Semantic Coherence</div>
                                <div class='metric-value'>{overall_semantic_score:.2f}</div>
                                <small>How relevant sentences are to introduction topics</small>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        # Count relevance levels
                        high_count = sum(1 for r in semantic_results if r['relevance'] == 'high')
                        medium_count = sum(1 for r in semantic_results if r['relevance'] == 'medium')
                        low_count = sum(1 for r in semantic_results if r['relevance'] == 'low')
                        
                        st.markdown(f"""
                            <div class='metric-card'>
                                <div class='metric-title'>Sentence Breakdown</div>
                                <div class='metric-value'>
                                    <span style='color: #10B981;'>●</span> {high_count} 
                                    <span style='color: #F59E0B;'>●</span> {medium_count} 
                                    <span style='color: #EF4444;'>●</span> {low_count}
                                </div>
                                <small>High / Medium / Low relevance</small>
                            </div>
                        """, unsafe_allow_html=True)
                    
                    # Display highlighted text
                    with st.expander("📝 View Sentence-by-Sentence Analysis", expanded=True):
                        st.markdown("**Color Legend:** <span style='color: #10B981;'>● High relevance</span> | <span style='color: #F59E0B;'>● Medium relevance</span> | <span style='color: #EF4444;'>● Low relevance</span>", unsafe_allow_html=True)
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        highlighted_html = semantic_analyzer.get_highlighted_text()
                        st.markdown(highlighted_html, unsafe_allow_html=True)
                        
                        st.markdown("<br><small><i>💡 Hover over sentences to see exact relevance scores</i></small>", unsafe_allow_html=True)
                    
                    # Detailed sentence scores
                    with st.expander("📊 Detailed Sentence Scores"):
                        for i, result in enumerate(semantic_results, 1):
                            relevance_emoji = {'high': '✅', 'medium': '⚠️', 'low': '❌'}[result['relevance']]
                            st.markdown(f"""
                                <div style='padding: 8px; margin: 4px 0; background: {result['color']}20; border-left: 3px solid {result['color']}; border-radius: 4px;'>
                                    {relevance_emoji} <b>Sentence {i}:</b> "{result['sentence']}"<br>
                                    <small>Relevance Score: {result['score']:.3f} ({result['relevance'].upper()})</small>
                                </div>
                            """, unsafe_allow_html=True)
                
                except ImportError:
                    st.info("📦 Semantic analysis requires `sentence-transformers`. Install it to enable this feature.")
                except Exception as e:
                    st.warning(f"⚠️ Could not perform semantic analysis: {str(e)}")
                
                # Comprehensive Feedback with AI-powered suggestions
                st.markdown('<p class="section-header">💡 Actionable Feedback & Recommendations</p>', unsafe_allow_html=True)
                
                # Generate comprehensive feedback
                all_feedback = generate_comprehensive_feedback(results)
                
                # Organize feedback by severity
                feedback_data = {
                    'high_priority': [f for f in all_feedback if f['severity'] == 'high'],
                    'medium_priority': [f for f in all_feedback if f['severity'] == 'medium'],
                    'low_priority': [f for f in all_feedback if f['severity'] == 'low']
                }
                
                # High priority feedback
                if feedback_data['high_priority']:
                    st.markdown("**🔴 High Priority Issues:**")
                    for item in feedback_data['high_priority']:
                        st.markdown(f"""
                            <div class='error-box'>
                                <strong>{item['category']}:</strong> {item['issue']}<br>
                                <small>💡 <em>{item['suggestion']}</em></small>
                            </div>
                        """, unsafe_allow_html=True)
                
                # Medium priority feedback
                if feedback_data['medium_priority']:
                    st.markdown("**🟡 Medium Priority Improvements:**")
                    for item in feedback_data['medium_priority']:
                        st.markdown(f"""
                            <div class='warning-box'>
                                <strong>{item['category']}:</strong> {item['issue']}<br>
                                <small>💡 <em>{item['suggestion']}</em></small>
                            </div>
                        """, unsafe_allow_html=True)
                
                # Low priority feedback
                if feedback_data['low_priority']:
                    with st.expander("🟢 Low Priority Suggestions"):
                        for item in feedback_data['low_priority']:
                            st.markdown(f"""
                                <div class='info-box'>
                                    <strong>{item['category']}:</strong> {item['issue']}<br>
                                    <small>💡 <em>{item['suggestion']}</em></small>
                                </div>
                            """, unsafe_allow_html=True)
                
                # Success message if all good
                if not feedback_data['high_priority'] and not feedback_data['medium_priority']:
                    st.markdown("""
                        <div class='success-box'>
                            ✨ Excellent work! Your introduction is well-structured and engaging.
                        </div>
                    """, unsafe_allow_html=True)
                
                # Download report
                st.markdown('<p class="section-header">📥 Download Report</p>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Text report
                    report_text = f"""AI Intro Evaluator Report
{'='*50}

OVERALL SCORE: {total_score}/100

Category Breakdown:
- Salutation: {results['salutation']['score']}/5
- Keywords: {results['keywords']['score']}/30
- Flow: {results['flow']['score']}/5
- Speech Rate: {results['speech_rate']['score']}/10
- Grammar: {results['grammar']['score']}/10
- Vocabulary: {results['vocabulary']['score']}/10
- Clarity: {results['filler']['score']}/15
- Engagement: {results['sentiment']['score']}/15

Detailed Analysis:
{'-'*50}
Grammar Errors: {results['grammar']['count']}
G-Index: {results['grammar'].get('g_index', 0):.2f}
Filler Words: {results['filler']['count']} ({results['filler']['rate']:.2f}%)
Vocabulary Richness (TTR): {results['vocabulary']['ttr']:.2f}
Sentiment Score: {results['sentiment']['positivity_score']:.2f}
Speech Rate: {results['speech_rate']['wpm']:.0f} WPM

Actionable Feedback:
{'-'*50}
"""
                    for category in ['high_priority', 'medium_priority', 'low_priority']:
                        if feedback_data[category]:
                            priority_label = category.replace('_', ' ').title()
                            report_text += f"\n{priority_label}:\n"
                            for item in feedback_data[category]:
                                report_text += f"- {item['category']}: {item['issue']}\n  → {item['suggestion']}\n"
                    
                    st.download_button(
                        label="📄 Download Text Report",
                        data=report_text,
                        file_name=f"ai_intro_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                        use_container_width=True
                    )
                
                with col2:
                    # PDF report
                    try:
                        pdf_bytes = generate_pdf_report(
                            student_name=st.session_state.get('student_name', 'Student'),
                            text_input=text_input,
                            results=results,
                            total_score=total_score
                        )
                        
                        st.download_button(
                            label="📕 Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"ai_intro_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                    except ImportError:
                        st.info("PDF generation requires `reportlab`. Install it to enable PDF downloads.")
                    except Exception as e:
                        st.error(f"PDF generation error: {str(e)}")

if __name__ == "__main__":
    main()
