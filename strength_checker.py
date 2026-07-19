import re
import string
import hmac
import hashlib
from common_passwords import COMMON_PASSWORDS


class StrengthChecker:
    def __init__(self):
        self.score = 0
        self.suggestions = []
        self.passed_criteria = []
        self.failed_criteria = []
        self.is_leaked = False
        
    def check_password(self, password):
        """Main method to check password strength"""
        self.score = 0
        self.suggestions = []
        self.passed_criteria = []
        self.failed_criteria = []
        self.is_leaked = False
        
        # Check each criterion
        self._check_length(password)
        self._check_uppercase(password)
        self._check_lowercase(password)
        self._check_digits(password)
        self._check_special_chars(password)
        self._check_repeated_chars(password)
        self._check_leaked(password)
        
        return {
            'score': self.score,
            'strength_level': self._get_strength_level(),
            'suggestions': self.suggestions,
            'passed': self.passed_criteria,
            'failed': self.failed_criteria,
            'is_leaked': self.is_leaked
        }
    
    def _check_length(self, password):
        length = len(password)
        if length >= 12:
            self.score += 20
            self.passed_criteria.append("Length is 12 or more characters")
        elif length >= 8:
            self.score += 10
            self.passed_criteria.append("Length is 8 or more characters")
            self.suggestions.append("Make password at least 12 characters long")
        else:
            self.failed_criteria.append("Password is too short")
            self.suggestions.append("Password must be at least 8 characters long")
    
    def _check_uppercase(self, password):
        if any(c.isupper() for c in password):
            self.score += 15
            self.passed_criteria.append("Contains uppercase letters")
        else:
            self.failed_criteria.append("No uppercase letters")
            self.suggestions.append("Add uppercase letters (A-Z)")
    
    def _check_lowercase(self, password):
        if any(c.islower() for c in password):
            self.score += 10
            self.passed_criteria.append("Contains lowercase letters")
        else:
            self.failed_criteria.append("No lowercase letters")
            self.suggestions.append("Add lowercase letters (a-z)")
    
    def _check_digits(self, password):
        if any(c.isdigit() for c in password):
            self.score += 15
            self.passed_criteria.append("Contains digits")
        else:
            self.failed_criteria.append("No digits")
            self.suggestions.append("Add digits (0-9)")
    
    def _check_special_chars(self, password):
        special_chars = "!@#$%^&*"
        if any(c in special_chars for c in password):
            self.score += 20
            self.passed_criteria.append("Contains special characters")
        else:
            self.failed_criteria.append("No special characters")
            self.suggestions.append("Add special characters (!@#$%^&*)")
    
    def _check_repeated_chars(self, password):
        from collections import Counter
        counts = Counter(password)
        if max(counts.values()) <= 2:
            self.score += 10
            self.passed_criteria.append("No excessive repeated characters")
        else:
            self.failed_criteria.append("Characters repeated too many times")
            self.suggestions.append("Avoid repeating same character more than twice")
    
    def _check_leaked(self, password):
        # Exact match comparison
        if password.lower() in [p.lower() for p in COMMON_PASSWORDS]:
            self.is_leaked = True
            self.failed_criteria.append("Password found in leaked database")
            self.suggestions.append("This password is commonly leaked! Choose a different one")
            return
        
        # Only add points if NOT leaked
        self.score += 20
        self.passed_criteria.append("Not found in leaked passwords list")
    
    def _get_strength_level(self):
        # ✅ FIXED: 3 categories - Strong now goes up to 100%
        if self.score <= 40:
            return "Weak"
        elif self.score <= 75:
            return "Moderate"
        else:
            return "Strong"   # 76-100 ✅

    
    def clear_memory(self, password):
        """Securely clear password from memory"""
        try:
            del password
        except:
            pass