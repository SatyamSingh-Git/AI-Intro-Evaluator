"""
Acoustic Analysis Module
Analyzes audio characteristics like pauses, pace, and speech patterns
"""

from pydub import AudioSegment
from pydub.silence import detect_silence, detect_nonsilent
import re

class AcousticAnalyzer:
    """Analyze acoustic properties of audio recordings"""
    
    def __init__(self, audio_path=None):
        """
        Initialize acoustic analyzer
        
        Args:
            audio_path: Path to the audio file (optional)
        """
        self.audio_path = audio_path
        self.audio = None
        if audio_path:
            self.audio = AudioSegment.from_file(audio_path)
    
    def detect_pauses(self, min_silence_len=500, silence_thresh=-40):
        """
        Detect pauses/silence in the audio
        
        Args:
            min_silence_len: Minimum length of silence in milliseconds (default 500ms)
            silence_thresh: Silence threshold in dBFS (default -40)
            
        Returns:
            Dictionary with pause analysis
        """
        if not self.audio:
            return {
                'pause_count': 0,
                'total_pause_duration': 0,
                'average_pause_duration': 0,
                'pause_percentage': 0,
                'pauses': []
            }
        
        # Detect silent segments
        silent_ranges = detect_silence(
            self.audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        
        total_duration = len(self.audio)
        total_pause_duration = sum(end - start for start, end in silent_ranges)
        pause_count = len(silent_ranges)
        
        return {
            'pause_count': pause_count,
            'total_pause_duration': total_pause_duration / 1000.0,  # Convert to seconds
            'average_pause_duration': (total_pause_duration / pause_count / 1000.0) if pause_count > 0 else 0,
            'pause_percentage': (total_pause_duration / total_duration * 100) if total_duration > 0 else 0,
            'pauses': [{'start': s/1000.0, 'end': e/1000.0, 'duration': (e-s)/1000.0} for s, e in silent_ranges]
        }
    
    def analyze_speaking_segments(self, min_silence_len=500, silence_thresh=-40):
        """
        Analyze actual speaking (non-silent) segments
        
        Args:
            min_silence_len: Minimum silence length to separate segments
            silence_thresh: Silence threshold in dBFS
            
        Returns:
            Dictionary with speaking segment analysis
        """
        if not self.audio:
            return {
                'speaking_segment_count': 0,
                'total_speaking_time': 0,
                'average_segment_duration': 0,
                'speaking_percentage': 0
            }
        
        # Detect non-silent segments
        speaking_ranges = detect_nonsilent(
            self.audio,
            min_silence_len=min_silence_len,
            silence_thresh=silence_thresh
        )
        
        total_duration = len(self.audio)
        total_speaking_time = sum(end - start for start, end in speaking_ranges)
        segment_count = len(speaking_ranges)
        
        return {
            'speaking_segment_count': segment_count,
            'total_speaking_time': total_speaking_time / 1000.0,  # Seconds
            'average_segment_duration': (total_speaking_time / segment_count / 1000.0) if segment_count > 0 else 0,
            'speaking_percentage': (total_speaking_time / total_duration * 100) if total_duration > 0 else 0
        }
    
    def calculate_actual_wpm(self, text, exclude_pauses=True):
        """
        Calculate words per minute based on actual speaking time
        
        Args:
            text: Transcribed text
            exclude_pauses: If True, use only speaking time for WPM calculation
            
        Returns:
            Dictionary with WPM metrics
        """
        if not self.audio or not text:
            return {
                'wpm': 0,
                'total_words': 0,
                'calculation_method': 'text_only'
            }
        
        word_count = len(text.split())
        total_duration_minutes = len(self.audio) / 1000.0 / 60.0
        
        if exclude_pauses:
            speaking_data = self.analyze_speaking_segments()
            speaking_time_minutes = speaking_data['total_speaking_time'] / 60.0
            wpm = word_count / speaking_time_minutes if speaking_time_minutes > 0 else 0
            method = 'speaking_time_only'
        else:
            wpm = word_count / total_duration_minutes if total_duration_minutes > 0 else 0
            method = 'total_duration'
        
        return {
            'wpm': wpm,
            'total_words': word_count,
            'total_duration_minutes': total_duration_minutes,
            'calculation_method': method
        }
    
    def analyze_filler_words_from_text(self, text):
        """
        Analyze filler words from transcribed text
        
        Args:
            text: Transcribed text
            
        Returns:
            Dictionary with filler word analysis
        """
        filler_patterns = [
            r'\buh+\b', r'\bum+\b', r'\blike\b', r'\byou know\b',
            r'\bso+\b', r'\bactually\b', r'\bbasically\b', r'\bliterally\b',
            r'\bkinda\b', r'\bsorta\b', r'\bI mean\b', r'\bright\b'
        ]
        
        text_lower = text.lower()
        filler_words = []
        filler_count = 0
        
        for pattern in filler_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                filler_words.append(match.group())
                filler_count += 1
        
        word_count = len(text.split())
        filler_rate = (filler_count / word_count * 100) if word_count > 0 else 0
        
        return {
            'filler_count': filler_count,
            'filler_words': filler_words,
            'filler_rate': filler_rate,
            'unique_fillers': list(set(filler_words))
        }
    
    def get_comprehensive_analysis(self, text=None):
        """
        Get comprehensive acoustic analysis
        
        Args:
            text: Transcribed text (optional)
            
        Returns:
            Dictionary with complete acoustic analysis
        """
        analysis = {
            'audio_available': self.audio is not None
        }
        
        if self.audio:
            pause_analysis = self.detect_pauses()
            speaking_analysis = self.analyze_speaking_segments()
            
            analysis.update({
                'duration_seconds': len(self.audio) / 1000.0,
                'duration_minutes': len(self.audio) / 1000.0 / 60.0,
                'pauses': pause_analysis,
                'speaking_segments': speaking_analysis
            })
            
            if text:
                wpm_analysis = self.calculate_actual_wpm(text)
                filler_analysis = self.analyze_filler_words_from_text(text)
                analysis.update({
                    'wpm_analysis': wpm_analysis,
                    'filler_analysis': filler_analysis
                })
        
        return analysis
