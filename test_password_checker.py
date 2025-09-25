import unittest
import hashlib
from unittest.mock import patch, MagicMock
from utils import (
    check_length,
    check_character_variety,
    check_common_patterns,
    calculate_strength_score,
    provide_feedback,
    check_pwned_password
)
import requests

class TestPasswordChecker(unittest.TestCase):

    def test_check_length(self):
        self.assertIn("too short", check_length("short"))
        self.assertIn("adequate", check_length("longenough"))
        self.assertIn("very long", check_length("thisisareallylongpassword"))

    def test_check_character_variety(self):
        self.assertIn("uppercase", check_character_variety("nouppercase1!"))
        self.assertIn("lowercase", check_character_variety("NOLOWERCASE1!"))
        self.assertIn("numbers", check_character_variety("NoDigits!"))
        self.assertIn("special characters", check_character_variety("NoSpecialChars1"))
        self.assertIn("good mix", check_character_variety("GoodMix1!"))

    def test_check_common_patterns(self):
        self.assertIsNotNone(check_common_patterns("password"))
        self.assertIsNotNone(check_common_patterns("123456"))
        self.assertIsNone(check_common_patterns("notacommonpassword"))

    def test_calculate_strength_score(self):
        # Weak passwords
        self.assertEqual(calculate_strength_score("123456"), 1)
        self.assertEqual(calculate_strength_score("password"), 1)

        # Medium passwords
        self.assertGreater(calculate_strength_score("GoodEnough"), 4)
        self.assertLessEqual(calculate_strength_score("GoodEnough"), 7)

        # Strong passwords
        self.assertGreater(calculate_strength_score("VeryStrongP@ssw0rd!"), 7)
        self.assertEqual(calculate_strength_score("ThisIsAVeryLongAndSecureP@ssw0rd123"), 10)

    def test_provide_feedback(self):
        feedback = provide_feedback("weak")
        self.assertIn("Password is too short", feedback[0])
        combined_feedback = " ".join(feedback[1:])
        self.assertIn("Add uppercase letters", combined_feedback)
        self.assertIn("Add numbers", combined_feedback)
        self.assertIn("Add special characters", combined_feedback)

    @patch('utils.requests.get')
    def test_check_pwned_password(self, mock_get):
        # Test a pwned password
        pwned_password = "password"
        sha1_pwned = hashlib.sha1(pwned_password.encode('utf-8')).hexdigest().upper()
        prefix, suffix = sha1_pwned[:5], sha1_pwned[5:]

        mock_response_pwned = MagicMock()
        mock_response_pwned.status_code = 200
        mock_response_pwned.text = f"{suffix}:12345"
        mock_get.return_value = mock_response_pwned

        result = check_pwned_password(pwned_password)
        self.assertIn("found 12345 times", result)
        mock_get.assert_called_with(f"https://api.pwnedpasswords.com/range/{prefix}")

        # Test a safe password
        safe_password = "a_very_safe_password_that_is_not_pwned_123!@#"
        sha1_safe = hashlib.sha1(safe_password.encode('utf-8')).hexdigest().upper()
        prefix_safe = sha1_safe[:5]

        mock_response_safe = MagicMock()
        mock_response_safe.status_code = 200
        mock_response_safe.text = "SOMEOTHERHASH:10"
        mock_get.return_value = mock_response_safe

        result = check_pwned_password(safe_password)
        self.assertIn("not found", result)
        mock_get.assert_called_with(f"https://api.pwnedpasswords.com/range/{prefix_safe}")

        # Test a network error
        mock_get.side_effect = requests.RequestException
        result = check_pwned_password("any_password")
        self.assertIn("Could not check", result)

if __name__ == '__main__':
    unittest.main()
