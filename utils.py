import re
import requests
import hashlib

def check_length(password):
    length = len(password)
    if length < 8:
        return "Password is too short. It should be at least 8 characters long."
    elif length > 16:
        return "Password is very long, which is good for security."
    return "Password length is adequate."

def check_character_variety(password):
    variety = {
        "uppercase": bool(re.search(r'[A-Z]', password)),
        "lowercase": bool(re.search(r'[a-z]', password)),
        "digits": bool(re.search(r'\d', password)),
        "special_chars": bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
    }
    feedback = []
    if not variety["uppercase"]:
        feedback.append("Add uppercase letters to improve strength.")
    if not variety["lowercase"]:
        feedback.append("Add lowercase letters to improve strength.")
    if not variety["digits"]:
        feedback.append("Add numbers to improve strength.")
    if not variety["special_chars"]:
        feedback.append("Add special characters (e.g., !@#$%) to improve strength.")

    if len(feedback) == 0:
        return "Password has a good mix of character types."
    return " ".join(feedback)

def check_common_patterns(password):
    common_patterns = [
        "123456", "password", "12345678", "qwerty", "12345", "123456789", "123", "abcdef"
    ]
    if password.lower() in common_patterns:
        return "Password is a very common and weak password. Please choose a different one."
    return None

def calculate_strength_score(password, pwned_info=None):
    score = 0

    # Length score
    if len(password) >= 8:
        score += 2
    if len(password) >= 12:
        score += 2
    if len(password) > 16:
        score += 1

    # Variety score
    if re.search(r'[A-Z]', password):
        score += 2
    if re.search(r'[a-z]', password):
        score += 1
    if re.search(r'\d', password):
        score += 1
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1

    # Penalty for common patterns
    if check_common_patterns(password):
        score = 1

    # Penalty for being pwned
    if pwned_info and "found" in pwned_info:
        score = max(1, score - 4)

    return min(10, score)

def check_pwned_password(password):
    """Checks if a password has been pwned using the Have I Been Pwned API."""
    try:
        sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_password[:5], sha1_password[5:]

        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}")
        response.raise_for_status()

        hashes = (line.split(':') for line in response.text.splitlines())
        for h, count in hashes:
            if h == suffix:
                return f"This password has been found {count} times in data breaches. It is compromised and should not be used."

        return "This password was not found in any known data breaches. Good job!"

    except requests.RequestException:
        return "Could not check for breaches due to a network error."

def provide_feedback(password):
    length_feedback = check_length(password)
    variety_feedback = check_character_variety(password)
    common_pattern_feedback = check_common_patterns(password)

    feedback = [length_feedback, variety_feedback]
    if common_pattern_feedback:
        feedback.append(common_pattern_feedback)

    return feedback