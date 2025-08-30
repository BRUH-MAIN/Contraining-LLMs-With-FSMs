"""
Constraints and validators for FSM states.
"""
import re
import json
from typing import Any, Dict, List, Callable
import string


class TextConstraints:
    """Collection of text-based constraints for FSM states."""
    
    @staticmethod
    def max_length(max_len: int) -> Callable[[str], bool]:
        """Constraint for maximum text length."""
        def validator(text: str) -> bool:
            return len(text) <= max_len
        return validator
    
    @staticmethod
    def min_length(min_len: int) -> Callable[[str], bool]:
        """Constraint for minimum text length."""
        def validator(text: str) -> bool:
            return len(text) >= min_len
        return validator
    
    @staticmethod
    def contains_words(words: List[str]) -> Callable[[str], bool]:
        """Constraint to check if text contains specific words."""
        def validator(text: str) -> bool:
            return any(word.lower() in text.lower() for word in words)
        return validator
    
    @staticmethod
    def matches_pattern(pattern: str) -> Callable[[str], bool]:
        """Constraint for regex pattern matching."""
        def validator(text: str) -> bool:
            return bool(re.search(pattern, text))
        return validator
    
    @staticmethod
    def no_profanity(profanity_list: List[str] = None) -> Callable[[str], bool]:
        """Constraint to filter out profanity."""
        if profanity_list is None:
            profanity_list = ["badword1", "badword2"]  # Add actual profanity list
        
        def validator(text: str) -> bool:
            return not any(word.lower() in text.lower() for word in profanity_list)
        return validator
    
    @staticmethod
    def only_alphanumeric() -> Callable[[str], bool]:
        """Constraint for alphanumeric characters only."""
        def validator(text: str) -> bool:
            return text.replace(" ", "").isalnum()
        return validator
    
    @staticmethod
    def valid_json() -> Callable[[str], bool]:
        """Constraint for valid JSON format."""
        def validator(text: str) -> bool:
            try:
                json.loads(text)
                return True
            except (json.JSONDecodeError, ValueError):
                return False
        return validator
    
    @staticmethod
    def valid_email() -> Callable[[str], bool]:
        """Constraint for valid email format."""
        def validator(text: str) -> bool:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, text.strip()))
        return validator
    
    @staticmethod
    def valid_url() -> Callable[[str], bool]:
        """Constraint for valid URL format."""
        def validator(text: str) -> bool:
            pattern = r'^https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:#(?:\w*))?)?$'
            return bool(re.match(pattern, text.strip()))
        return validator
    
    @staticmethod
    def valid_phone() -> Callable[[str], bool]:
        """Constraint for valid phone number format."""
        def validator(text: str) -> bool:
            # Remove all non-digit characters
            digits = re.sub(r'\D', '', text)
            # Check if it's a valid length (10-15 digits)
            return 10 <= len(digits) <= 15
        return validator


class StructuralConstraints:
    """Collection of structural constraints for FSM states."""
    
    @staticmethod
    def starts_with(prefix: str) -> Callable[[str], bool]:
        """Constraint for text starting with specific prefix."""
        def validator(text: str) -> bool:
            return text.strip().startswith(prefix)
        return validator
    
    @staticmethod
    def ends_with(suffix: str) -> Callable[[str], bool]:
        """Constraint for text ending with specific suffix."""
        def validator(text: str) -> bool:
            return text.strip().endswith(suffix)
        return validator
    
    @staticmethod
    def has_balanced_brackets() -> Callable[[str], bool]:
        """Constraint for balanced brackets."""
        def validator(text: str) -> bool:
            stack = []
            pairs = {'(': ')', '[': ']', '{': '}'}
            
            for char in text:
                if char in pairs:
                    stack.append(char)
                elif char in pairs.values():
                    if not stack:
                        return False
                    if pairs[stack.pop()] != char:
                        return False
            
            return len(stack) == 0
        return validator
    
    @staticmethod
    def sentence_count(min_sentences: int, max_sentences: int = None) -> Callable[[str], bool]:
        """Constraint for number of sentences."""
        def validator(text: str) -> bool:
            sentences = re.split(r'[.!?]+', text.strip())
            sentences = [s for s in sentences if s.strip()]
            count = len(sentences)
            
            if max_sentences is None:
                return count >= min_sentences
            return min_sentences <= count <= max_sentences
        return validator
    
    @staticmethod
    def word_count(min_words: int, max_words: int = None) -> Callable[[str], bool]:
        """Constraint for number of words."""
        def validator(text: str) -> bool:
            words = text.split()
            count = len(words)
            
            if max_words is None:
                return count >= min_words
            return min_words <= count <= max_words
        return validator
    
    @staticmethod
    def paragraph_count(min_paragraphs: int, max_paragraphs: int = None) -> Callable[[str], bool]:
        """Constraint for number of paragraphs."""
        def validator(text: str) -> bool:
            paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
            count = len(paragraphs)
            
            if max_paragraphs is None:
                return count >= min_paragraphs
            return min_paragraphs <= count <= max_paragraphs
        return validator


class ContentConstraints:
    """Collection of content-based constraints for FSM states."""
    
    @staticmethod
    def requires_keywords(keywords: List[str], min_count: int = 1) -> Callable[[str], bool]:
        """Constraint requiring specific keywords."""
        def validator(text: str) -> bool:
            text_lower = text.lower()
            found_count = sum(1 for keyword in keywords if keyword.lower() in text_lower)
            return found_count >= min_count
        return validator
    
    @staticmethod
    def forbids_keywords(keywords: List[str]) -> Callable[[str], bool]:
        """Constraint forbidding specific keywords."""
        def validator(text: str) -> bool:
            text_lower = text.lower()
            return not any(keyword.lower() in text_lower for keyword in keywords)
        return validator
    
    @staticmethod
    def sentiment_positive() -> Callable[[str], bool]:
        """Constraint for positive sentiment (basic implementation)."""
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "fantastic", "love", "like", "happy", "joy"]
        negative_words = ["bad", "terrible", "awful", "hate", "dislike", "sad", "angry", "horrible", "worst"]
        
        def validator(text: str) -> bool:
            text_lower = text.lower()
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            return positive_count > negative_count
        return validator
    
    @staticmethod
    def requires_numbers() -> Callable[[str], bool]:
        """Constraint requiring numeric content."""
        def validator(text: str) -> bool:
            return bool(re.search(r'\d', text))
        return validator
    
    @staticmethod
    def requires_uppercase() -> Callable[[str], bool]:
        """Constraint requiring uppercase letters."""
        def validator(text: str) -> bool:
            return any(c.isupper() for c in text)
        return validator
    
    @staticmethod
    def requires_lowercase() -> Callable[[str], bool]:
        """Constraint requiring lowercase letters."""
        def validator(text: str) -> bool:
            return any(c.islower() for c in text)
        return validator
    
    @staticmethod
    def requires_punctuation() -> Callable[[str], bool]:
        """Constraint requiring punctuation."""
        def validator(text: str) -> bool:
            return any(c in string.punctuation for c in text)
        return validator


class CompositeConstraints:
    """Collection of composite constraints combining multiple validators."""
    
    @staticmethod
    def all_of(*validators: Callable[[str], bool]) -> Callable[[str], bool]:
        """Constraint requiring all validators to pass."""
        def validator(text: str) -> bool:
            return all(v(text) for v in validators)
        return validator
    
    @staticmethod
    def any_of(*validators: Callable[[str], bool]) -> Callable[[str], bool]:
        """Constraint requiring at least one validator to pass."""
        def validator(text: str) -> bool:
            return any(v(text) for v in validators)
        return validator
    
    @staticmethod
    def none_of(*validators: Callable[[str], bool]) -> Callable[[str], bool]:
        """Constraint requiring no validators to pass."""
        def validator(text: str) -> bool:
            return not any(v(text) for v in validators)
        return validator
    
    @staticmethod
    def not_constraint(validator: Callable[[str], bool]) -> Callable[[str], bool]:
        """Negation of a constraint."""
        def negated_validator(text: str) -> bool:
            return not validator(text)
        return negated_validator
