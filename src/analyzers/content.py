from src.config import KEYWORDS, SALUTATIONS, CLOSINGS
from src.utils.text_utils import clean_text

class ContentAnalyzer:
    def __init__(self, text):
        self.text = clean_text(text).lower()

    def check_keywords(self):
        """
        Checks for the presence of mandatory keywords/topics.
        Returns a dictionary with found topics and a score.
        """
        found_topics = {}
        score = 0
        
        # Check Must Have (Max 20, 4 each)
        for topic, phrases in KEYWORDS["Must Have"].items():
            found = False
            for phrase in phrases:
                if phrase in self.text:
                    found = True
                    break
            found_topics[topic] = found
            if found:
                score += 4
        
        # Check Good to Have (Max 10, 2 each)
        for topic, phrases in KEYWORDS["Good to Have"].items():
            found = False
            for phrase in phrases:
                if phrase in self.text:
                    found = True
                    break
            found_topics[topic] = found
            if found:
                score += 2
            
        return {"topics": found_topics, "score": score}

    def check_flow(self):
        """
        Checks if the introduction follows the order:
        Salutation --> Name --> Mandatory details --> Optional Details --> Closing
        """
        # Find indices of first occurrence of each section
        indices = {
            "Salutation": -1,
            "Name": -1,
            "Details": -1,
            "Closing": -1
        }

        # Salutation
        for level, phrases in SALUTATIONS.items():
            for phrase in phrases:
                idx = self.text.find(phrase)
                if idx != -1:
                    if indices["Salutation"] == -1 or idx < indices["Salutation"]:
                        indices["Salutation"] = idx

        # Name
        for phrase in KEYWORDS["Must Have"]["Name"]:
            idx = self.text.find(phrase)
            if idx != -1:
                if indices["Name"] == -1 or idx < indices["Name"]:
                    indices["Name"] = idx

        # Details (Group Age, Class_School, Family as Mandatory)
        mandatory_phrases = []
        for topic in ["Age", "Class_School", "Family"]:
            mandatory_phrases.extend(KEYWORDS["Must Have"][topic])
        
        for phrase in mandatory_phrases:
            idx = self.text.find(phrase)
            if idx != -1:
                if indices["Details"] == -1 or idx < indices["Details"]:
                    indices["Details"] = idx

        # Closing
        for closing in CLOSINGS:
            idx = self.text.find(closing)
            if idx != -1:
                if indices["Closing"] == -1 or idx > indices["Closing"]:
                    indices["Closing"] = idx

        # Check order
        flow_score = 0
        feedback = []
        
        valid_order = True
        last_idx = -1
        
        order_check = ["Salutation", "Name", "Details", "Closing"]
        
        for section in order_check:
            current_idx = indices[section]
            if current_idx != -1:
                if last_idx != -1 and current_idx < last_idx:
                    valid_order = False
                    feedback.append(f"{section} appears before previous section.")
                last_idx = current_idx
            else:
                feedback.append(f"{section} not found.")

        if valid_order and all(indices[s] != -1 for s in order_check):
            flow_score = 5 # Full score if perfect
        else:
            flow_score = 0

        return {"valid_order": valid_order, "indices": indices, "score": flow_score, "feedback": feedback}

    def check_salutation(self):
        """
        Scores the salutation based on its presence and type.
        """
        # Check Excellent
        for phrase in SALUTATIONS["Excellent"]:
            if phrase in self.text:
                return {"present": True, "score": 5, "type": "Excellent", "phrase": phrase}
        
        # Check Good
        for phrase in SALUTATIONS["Good"]:
            if phrase in self.text:
                return {"present": True, "score": 4, "type": "Good", "phrase": phrase}
                
        # Check Normal
        for phrase in SALUTATIONS["Normal"]:
            if phrase in self.text:
                return {"present": True, "score": 2, "type": "Normal", "phrase": phrase}
        
        return {"present": False, "score": 0, "type": "None", "phrase": None}


