"""
Feedback Generator Module
Generates actionable, specific feedback based on evaluation results
"""

def generate_keyword_feedback(keywords_result):
    """Generate specific feedback for missing keywords"""
    feedback = []
    topics = keywords_result['topics']
    
    # Must Have topics
    must_have_missing = [topic for topic in ['Name', 'Age', 'Class_School', 'Family', 'Hobbies'] 
                         if not topics.get(topic, False)]
    
    if must_have_missing:
        feedback.append({
            'category': 'Content',
            'severity': 'high',
            'issue': f"Missing essential topics: {', '.join(must_have_missing)}",
            'suggestion': f"Add clear statements about your {', '.join([t.lower().replace('_', '/') for t in must_have_missing])}. For example: 'My name is...', 'I am X years old', 'I study at...'"
        })
    
    # Good to Have topics
    good_to_have_missing = [topic for topic in ['About Family', 'Origin', 'Goals', 'Unique', 'Strengths'] 
                           if not topics.get(topic.replace(' ', '_'), False) and not topics.get(topic, False)]
    
    if good_to_have_missing:
        feedback.append({
            'category': 'Content Enhancement',
            'severity': 'medium',
            'issue': f"Could include: {', '.join(good_to_have_missing)}",
            'suggestion': f"Consider adding 1-2 sentences about {good_to_have_missing[0].lower()}. This adds personality and helps you stand out."
        })
    
    return feedback

def generate_grammar_feedback(grammar_result):
    """Generate specific feedback for grammar issues"""
    feedback = []
    
    if grammar_result['count'] > 0:
        error_count = grammar_result['count']
        
        if error_count >= 5:
            severity = 'high'
            suggestion = "Review your text carefully. Consider using a grammar checker or asking someone to proofread before finalizing."
        elif error_count >= 3:
            severity = 'medium'
            suggestion = "Fix the highlighted grammar errors. Pay attention to punctuation, subject-verb agreement, and spelling."
        else:
            severity = 'low'
            suggestion = "Just a few minor fixes needed. Review the specific errors highlighted below."
        
        feedback.append({
            'category': 'Grammar',
            'severity': severity,
            'issue': f"{error_count} grammar error{'s' if error_count > 1 else ''} detected",
            'suggestion': suggestion
        })
    
    return feedback

def generate_sentiment_feedback(sentiment_result):
    """Generate feedback for sentiment and positivity"""
    feedback = []
    score = sentiment_result['positivity_score']
    
    if score < 0.5:
        feedback.append({
            'category': 'Tone & Engagement',
            'severity': 'medium',
            'issue': 'Your introduction sounds neutral or negative',
            'suggestion': "Use more positive and enthusiastic language. Words like 'enjoy', 'love', 'excited', 'passionate' help create engagement. Example: Instead of 'I do sports', try 'I really enjoy playing sports!'"
        })
    elif score < 0.7:
        feedback.append({
            'category': 'Tone & Engagement',
            'severity': 'low',
            'issue': 'Good tone, but could be more enthusiastic',
            'suggestion': "Add a bit more energy! Show your personality and what makes you unique."
        })
    
    return feedback

def generate_flow_feedback(flow_result):
    """Generate feedback for structure and flow"""
    feedback = []
    
    if not flow_result['valid_order']:
        feedback.append({
            'category': 'Structure',
            'severity': 'high',
            'issue': 'Your introduction doesn\'t follow the ideal structure',
            'suggestion': "Reorganize to follow this order: 1) Greeting, 2) Name, 3) Basic details (age, school), 4) Family/hobbies, 5) Closing. This creates a natural flow that's easy to follow."
        })
    
    return feedback

def generate_speech_rate_feedback(speech_rate_result):
    """Generate feedback for speech pacing"""
    feedback = []
    wpm = speech_rate_result['wpm']
    
    if wpm < 100:
        feedback.append({
            'category': 'Delivery',
            'severity': 'medium',
            'issue': f'Speaking too slowly ({wpm:.0f} WPM)',
            'suggestion': "Your pace is quite slow. Practice speaking a bit faster to maintain audience engagement. Aim for 111-140 words per minute."
        })
    elif wpm > 160:
        feedback.append({
            'category': 'Delivery',
            'severity': 'medium',
            'issue': f'Speaking too fast ({wpm:.0f} WPM)',
            'suggestion': "You're speaking very quickly. Slow down to ensure clarity. Take breaths between sentences. Aim for 111-140 words per minute."
        })
    elif wpm > 140:
        feedback.append({
            'category': 'Delivery',
            'severity': 'low',
            'issue': f'Slightly fast pace ({wpm:.0f} WPM)',
            'suggestion': "Good pace, but slightly fast. Slowing down just a bit will improve clarity."
        })
    
    return feedback

def generate_filler_feedback(filler_result):
    """Generate feedback for filler words"""
    feedback = []
    
    if filler_result['count'] > 5:
        feedback.append({
            'category': 'Clarity',
            'severity': 'high',
            'issue': f"{filler_result['count']} filler words detected ({filler_result['rate']:.1f}%)",
            'suggestion': f"You're using too many filler words: {', '.join(filler_result['fillers'][:5])}. Practice pausing instead of saying 'um' or 'like'. Record yourself and listen back to identify patterns."
        })
    elif filler_result['count'] > 2:
        feedback.append({
            'category': 'Clarity',
            'severity': 'medium',
            'issue': f"{filler_result['count']} filler words found",
            'suggestion': "Try to eliminate filler words by practicing your introduction. Pause briefly instead of saying 'um' or 'like'."
        })
    
    return feedback

def generate_vocabulary_feedback(vocab_result):
    """Generate feedback for vocabulary richness"""
    feedback = []
    ttr = vocab_result['ttr']
    
    if ttr < 0.4:
        feedback.append({
            'category': 'Vocabulary',
            'severity': 'medium',
            'issue': f'Limited vocabulary variety (TTR: {ttr:.2f})',
            'suggestion': "You're repeating words too often. Try using synonyms and more varied vocabulary. Example: Instead of repeating 'like', use 'enjoy', 'love', 'prefer', 'appreciate'."
        })
    elif ttr < 0.5:
        feedback.append({
            'category': 'Vocabulary',
            'severity': 'low',
            'issue': f'Vocabulary could be more diverse (TTR: {ttr:.2f})',
            'suggestion': "Good variety, but you can improve. Use a thesaurus to find more expressive alternatives for common words."
        })
    
    return feedback

def generate_comprehensive_feedback(results):
    """Generate comprehensive feedback from all evaluation results"""
    all_feedback = []
    
    # Collect feedback from all categories
    all_feedback.extend(generate_keyword_feedback(results['keywords']))
    all_feedback.extend(generate_grammar_feedback(results['grammar']))
    all_feedback.extend(generate_sentiment_feedback(results['sentiment']))
    all_feedback.extend(generate_flow_feedback(results['flow']))
    all_feedback.extend(generate_speech_rate_feedback(results['speech_rate']))
    all_feedback.extend(generate_filler_feedback(results['filler']))
    all_feedback.extend(generate_vocabulary_feedback(results['vocabulary']))
    
    # Sort by severity
    severity_order = {'high': 0, 'medium': 1, 'low': 2}
    all_feedback.sort(key=lambda x: severity_order.get(x['severity'], 3))
    
    return all_feedback

def generate_why_explanation(category, score, max_score, details):
    """Generate 'why' explanation for each score"""
    percentage = (score / max_score) * 100 if max_score > 0 else 0
    
    explanations = {
        'salutation': {
            'high': f"You included a {details.get('type', 'proper')} greeting which shows professionalism and friendliness.",
            'medium': f"You have a basic greeting, but it could be more enthusiastic or formal depending on context.",
            'low': "Your introduction lacks a clear greeting. Start with 'Hello', 'Good morning', or 'Hi everyone' to engage your audience.",
            'none': "No greeting detected. Always start your introduction with a salutation to create a welcoming tone."
        },
        'keywords': {
            'high': "You covered all essential topics! Your introduction is comprehensive and informative.",
            'medium': f"You mentioned most key topics, but you're missing: {', '.join([k for k, v in details.get('topics', {}).items() if not v][:3])}.",
            'low': f"Several important topics are missing: {', '.join([k for k, v in details.get('topics', {}).items() if not v][:5])}. Make sure to cover the basics."
        },
        'flow': {
            'good': "Your introduction follows a logical structure: greeting → name → details → closing. Well organized!",
            'poor': "Your introduction jumps around. Try this order: greeting → name → age/school → family/hobbies → unique facts → closing."
        },
        'speech_rate': {
            'high': f"Your speech rate of {details.get('wpm', 0):.0f} WPM is excellent - within the ideal 111-140 range. Perfect pacing!",
            'medium': f"Your speech rate is {details.get('wpm', 0):.0f} WPM. Try to aim for 111-140 WPM for better clarity and engagement.",
            'low': f"Your speech rate is {details.get('wpm', 0):.0f} WPM, which is outside the ideal range. Adjust your pacing for better comprehension."
        },
        'grammar': {
            'high': "Excellent grammar! Your writing is clean and professional.",
            'medium': f"{details.get('count', 0)} grammar errors found. These are minor issues that can be easily fixed.",
            'low': f"{details.get('count', 0)} grammar errors detected. Review spelling, punctuation, and sentence structure."
        },
        'vocabulary': {
            'high': f"Excellent vocabulary richness (TTR: {details.get('ttr', 0):.2f})! You use varied and diverse words.",
            'medium': f"Your vocabulary is decent (TTR: {details.get('ttr', 0):.2f}), but try using more varied words to avoid repetition.",
            'low': f"Limited vocabulary diversity (TTR: {details.get('ttr', 0):.2f}). Use synonyms and more descriptive words to enrich your introduction."
        },
        'clarity': {
            'high': f"Excellent clarity! Only {details.get('count', 0)} filler words detected ({details.get('rate', 0):.1f}%). Your speech is confident and clear.",
            'medium': f"You used {details.get('count', 0)} filler words ({details.get('rate', 0):.1f}%). Reduce words like 'um', 'like', 'you know' for better clarity.",
            'low': f"Too many filler words: {details.get('count', 0)} ({details.get('rate', 0):.1f}%). Practice speaking more confidently without fillers."
        },
        'sentiment': {
            'high': f"Your positivity score is {details.get('positivity_score', 0):.2f}! You sound enthusiastic and engaged.",
            'medium': "Your tone is somewhat positive, but adding more enthusiastic language would increase engagement.",
            'low': "Your introduction sounds neutral or negative. Use words like 'enjoy', 'excited', 'passionate' to sound more positive."
        }
    }
    
    # Determine the level
    if percentage >= 80:
        level = 'high'
    elif percentage >= 50:
        level = 'medium'
    elif percentage > 0:
        level = 'low'
    else:
        level = 'none'
    
    return explanations.get(category, {}).get(level, "Score calculated based on rubric criteria.")
