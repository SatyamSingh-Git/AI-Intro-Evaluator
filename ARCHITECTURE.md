# Architecture & Design Decisions

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE LAYER                     │
│                     (Streamlit Frontend)                     │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐ │
│  │Text Input   │  │ Audio Upload │  │  File Upload      │ │
│  │Widget       │  │ + Recording  │  │  (.txt)           │ │
│  └──────┬──────┘  └──────┬───────┘  └─────────┬─────────┘ │
│         │                 │                     │            │
│         └─────────────────┴─────────────────────┘            │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  PREPROCESSING LAYER                         │
│  ┌──────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ Speech-to-   │  │Text Cleaning│  │  Tokenization    │  │
│  │ Text (Whisper│  │& Normalize  │  │  (NLTK)          │  │
│  └──────────────┘  └─────────────┘  └──────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    ANALYSIS ENGINE LAYER                     │
│                                                              │
│  ┌───────────────────┐  ┌────────────────────────────────┐ │
│  │ Content Analyzer  │  │  Metrics Analyzer              │ │
│  │ - Keywords        │  │  - Word Count                  │ │
│  │ - Flow            │  │  - Speech Rate                 │ │
│  │ - Salutation      │  │  - Vocabulary Richness (TTR)   │ │
│  └───────────────────┘  └────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────┐  ┌────────────────────────────────┐ │
│  │ Grammar Analyzer  │  │  Sentiment Analyzer            │ │
│  │ - LanguageTool    │  │  - VADER Sentiment             │ │
│  │ - Error Detection │  │  - Positivity Score            │ │
│  │ - G-Index Calc    │  │  - Compound Score              │ │
│  └───────────────────┘  └────────────────────────────────┘ │
│                                                              │
│  ┌───────────────────┐  ┌────────────────────────────────┐ │
│  │ Semantic Analyzer │  │  Acoustic Analyzer             │ │
│  │ - Sentence-       │  │  - WPM from Audio              │ │
│  │   Transformers    │  │  - Pause Detection             │ │
│  │ - Relevance Score │  │  - Filler Word Detection       │ │
│  └───────────────────┘  └────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    RUBRIC EVALUATION LAYER                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Scoring Algorithm                        │  │
│  │  - Apply rubric criteria to analysis results         │  │
│  │  - Calculate category scores                         │  │
│  │  - Generate overall score (0-100)                    │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  FEEDBACK GENERATION LAYER                   │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Actionable Feedback Generator                 │  │
│  │  - Identify weaknesses                                │  │
│  │  - Generate specific suggestions                      │  │
│  │  - Prioritize by severity                             │  │
│  │  - Create "Why" explanations                          │  │
│  └──────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT LAYER                              │
│                                                              │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ Interactive │  │ Visualizations│  │  PDF Report      │  │
│  │ Dashboard   │  │ (Plotly)      │  │  (ReportLab)     │  │
│  │ (Streamlit) │  │ - Gauge       │  │  - Downloadable  │  │
│  │             │  │ - Radar       │  │  - Professional  │  │
│  │             │  │ - Bar Chart   │  │                  │  │
│  └─────────────┘  └──────────────┘  └──────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow Diagram

```
Input Text/Audio
      │
      ▼
┌──────────────┐
│ Text Input   │
│ OR           │──────┐
│ Audio Upload │      │
└──────────────┘      │
                      │
                ┌─────▼──────┐
                │  Whisper   │
                │ (if audio) │
                └─────┬──────┘
                      │
                ┌─────▼───────┐
                │   Cleaned   │
                │     Text    │
                └─────┬───────┘
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
┌──────────┐    ┌─────────┐    ┌──────────┐
│ Content  │    │Grammar  │    │Sentiment │
│ Analysis │    │Analysis │    │ Analysis │
└────┬─────┘    └────┬────┘    └────┬─────┘
     │               │              │
     └───────┬───────┴──────┬───────┘
             │              │
             ▼              ▼
        ┌────────┐    ┌──────────┐
        │ Rubric │    │ Feedback │
        │ Scoring│    │Generator │
        └───┬────┘    └────┬─────┘
            │              │
            └──────┬───────┘
                   │
                   ▼
           ┌───────────────┐
           │ Results +     │
           │ Feedback +    │
           │ Visualizations│
           │ + PDF         │
           └───────────────┘
```

## Technology Stack

### Frontend
- **Streamlit 1.51.0**
  - Rapid prototyping
  - Built-in widgets and components
  - Real-time updates
  - Mobile-responsive

### NLP & Analysis
- **VADER Sentiment** - Rule-based sentiment analysis
- **LanguageTool** - Grammar and style checking
- **NLTK** - Tokenization and text processing
- **sentence-transformers** - Semantic similarity
- **TextStat** - Readability and text statistics

### Audio Processing
- **OpenAI Whisper** - Speech-to-text transcription
- **pydub** - Audio file manipulation
- **SpeechRecognition** - Live audio capture

### Visualization
- **Plotly** - Interactive charts (gauge, radar, bar)
- **Custom CSS** - Modern, gradient-based UI

### Reporting
- **ReportLab** - PDF generation
- **Downloadable reports** - Professional formatting

## Key Design Decisions & Trade-offs

### 1. **Streamlit vs Flask/FastAPI**

**Decision:** Streamlit

**Why:**
- ✅ **Rapid Development:** Build UI in pure Python, no HTML/CSS/JS needed
- ✅ **Built-in Widgets:** File upload, charts, buttons out-of-the-box
- ✅ **Hot Reload:** Instant feedback during development
- ✅ **Educational Context:** Perfect for demo tools and PoCs

**Trade-offs:**
- ❌ **Limited Customization:** Less control over frontend than React/Vue
- ❌ **Session State:** Requires careful management of state
- ❌ **Scalability:** Not ideal for thousands of concurrent users

**Verdict:** For an educational evaluation tool with moderate traffic, Streamlit's productivity wins outweigh scalability concerns.

---

### 2. **VADER Sentiment vs Transformer Models (BERT, RoBERTa)**

**Decision:** VADER Sentiment

**Why:**
- ✅ **Speed:** Instant results, no GPU required
- ✅ **Interpretability:** Rule-based, easy to debug
- ✅ **Lightweight:** Minimal dependencies
- ✅ **Good for Social Text:** Designed for informal language

**Trade-offs:**
- ❌ **Accuracy:** Less accurate than deep learning models
- ❌ **Context Limitation:** Doesn't understand complex semantics
- ❌ **Domain Specific:** Trained on social media, not formal writing

**Verdict:** For student introductions (informal, short text), VADER's speed and simplicity are ideal. If we need higher accuracy for formal essays, we'd switch to `transformers` with DistilBERT.

---

### 3. **LanguageTool vs Grammarly API / GPT-based Correction**

**Decision:** LanguageTool (Open-source)

**Why:**
- ✅ **Free & Open-source:** No API costs
- ✅ **Privacy:** Runs locally, no data sent to third parties
- ✅ **Customizable:** Can add custom rules
- ✅ **Offline Capable:** Works without internet

**Trade-offs:**
- ❌ **Accuracy:** Lower than Grammarly or GPT-4
- ❌ **Speed:** Can be slow for very long texts
- ❌ **Limited Context:** Doesn't understand document-level coherence

**Verdict:** For educational use (privacy-sensitive), open-source wins. For production at scale, we'd use GPT-4 API with caching.

---

### 4. **Sentence-Transformers vs spaCy for Semantic Similarity**

**Decision:** Sentence-Transformers

**Why:**
- ✅ **Purpose-Built:** Designed specifically for semantic similarity
- ✅ **Pre-trained Models:** `all-MiniLM-L6-v2` balances speed & accuracy
- ✅ **Cosine Similarity:** Simple, effective metric
- ✅ **Multi-lingual Support:** Easy to extend to other languages

**Trade-offs:**
- ❌ **Model Size:** ~80MB for MiniLM model
- ❌ **CPU Load:** Slower than keyword-based approaches
- ❌ **Cache Requirement:** Needs caching for performance

**Verdict:** Semantic understanding adds significant value over keyword matching. The model size is acceptable, and we use `@st.cache_resource` to mitigate speed issues.

---

### 5. **Whisper (Local) vs Google Speech-to-Text API**

**Decision:** OpenAI Whisper (Local)

**Why:**
- ✅ **Accuracy:** State-of-the-art transcription
- ✅ **Privacy:** Audio stays local
- ✅ **Free:** No API costs
- ✅ **Multilingual:** Supports 99 languages

**Trade-offs:**
- ❌ **Speed:** Slower than cloud APIs (especially on CPU)
- ❌ **Resource Intensive:** Requires good hardware
- ❌ **Model Download:** ~150MB for base model

**Verdict:** For student privacy and zero cost, Whisper is ideal. For production with high volume, we'd use Google/Azure Speech APIs.

---

### 6. **ReportLab vs WeasyPrint for PDF Generation**

**Decision:** ReportLab

**Why:**
- ✅ **Low-level Control:** Precise layout control
- ✅ **Mature Library:** Well-documented, stable
- ✅ **Customizable:** Can create complex, branded PDFs
- ✅ **Pure Python:** No external dependencies

**Trade-offs:**
- ❌ **Verbose Code:** Requires more code than HTML-to-PDF
- ❌ **Learning Curve:** Steeper than markdown-to-PDF tools

**Verdict:** Professional reports require precise control. ReportLab's verbosity is worth it for quality output.

---

## Performance Optimizations

### 1. **Model Caching**
```python
@st.cache_resource
def load_sentence_model():
    return SentenceTransformer('all-MiniLM-L6-v2')
```
- Prevents reloading models on every run
- Reduces memory usage

### 2. **Lazy Loading**
- Only import heavy libraries when needed
- Example: Whisper only imported when audio is uploaded

### 3. **Result Memoization**
```python
@st.cache_data
def evaluate_text(text):
    # Expensive computation
    return results
```
- Caches results for identical inputs
- Improves user experience

### 4. **Async Processing** (Future)
- For batch processing, use `asyncio` or `concurrent.futures`
- Process multiple introductions in parallel

## Security Considerations

### 1. **Input Validation**
- Limit file size (max 10MB for audio)
- Validate file types (only .txt, .wav, .mp3)
- Sanitize user inputs to prevent injection

### 2. **Data Privacy**
- No data is stored permanently
- Audio/text processed in-memory only
- Optional: Add GDPR-compliant consent

### 3. **Rate Limiting** (Future)
- Prevent abuse by limiting requests per IP
- Use `streamlit-authenticator` for user management

## Scalability Path

### Current: Single-user Desktop App
- Streamlit on localhost
- Local processing

### Phase 1: Multi-user Cloud Deployment
- Deploy on Streamlit Cloud / Heroku
- Add Redis for session management
- Use CDN for static assets

### Phase 2: API-First Architecture
- FastAPI backend for evaluation logic
- Streamlit as frontend only
- Horizontal scaling with load balancer

### Phase 3: Enterprise SaaS
- Multi-tenancy support
- PostgreSQL for user data & history
- Background job queue (Celery)
- Auto-scaling on AWS/GCP

## Testing Strategy

### Unit Tests
- Test each analyzer independently
- Mock external APIs (Whisper, LanguageTool)
- Validate scoring logic

### Integration Tests
- Test full evaluation pipeline
- Verify PDF generation
- Check audio-to-text flow

### UI Tests
- Streamlit interactions
- Button clicks, file uploads
- Visual regression testing

## Future Architectural Improvements

1. **Microservices:** Separate audio processing, NLP, and reporting into independent services
2. **Message Queue:** Use RabbitMQ/Kafka for async processing
3. **GraphQL API:** More flexible than REST for complex queries
4. **Real-time Collaboration:** WebSockets for live feedback during recording
5. **ML Pipeline:** MLflow for model versioning and A/B testing


