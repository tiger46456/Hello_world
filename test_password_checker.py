import unittest
from utils import (
    check_length,
    check_character_variety,
    check_common_patterns,
    calculate_strength_score,
    provide_feedback
)

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
        self.assertIn("Add uppercase letters", feedback[1])
        self.assertIn("Add numbers", feedback[1])
        self.assertIn("Add special characters", feedback[1])

if __name__ == '__main__':
    unittest.main()
