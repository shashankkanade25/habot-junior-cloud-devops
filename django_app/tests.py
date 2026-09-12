"""
HabotConnect Hiring Project
Candidate: Shashank Kanade
Email: shashankkanade07@gmail.com
Phone: 7820963908

Task 3: Automated validation tests.
"""

from django.test import TestCase

from .dcyn import evaluate_dcyn
from .serializers import StudentOnboardingSerializer


class DCYNLibraryTests(TestCase):
    def test_yes_no_decisions(self):
        data = {
            "has_learning_difficulty": True,
            "requires_learning_support": True,
            "parental_consent": True,
        }

        result = evaluate_dcyn(data)

        self.assertEqual(result["DCYN-01"], "YES")
        self.assertEqual(result["DCYN-02"], "YES")
        self.assertEqual(result["DCYN-03"], "YES")

    def test_no_decisions(self):
        data = {
            "has_learning_difficulty": False,
            "requires_learning_support": False,
            "parental_consent": False,
        }

        result = evaluate_dcyn(data)

        self.assertEqual(result["DCYN-01"], "NO")
        self.assertEqual(result["DCYN-02"], "NO")
        self.assertEqual(result["DCYN-03"], "NO")


class StudentOnboardingSerializerTests(TestCase):
    def valid_payload(self):
        return {
            "student_name": "Aarav Sharma",
            "email": "aarav.sharma@example.com",
            "age": 12,
            "country": "India",
            "has_learning_difficulty": True,
            "requires_learning_support": True,
            "parental_consent": True,
        }

    def test_valid_payload_is_accepted(self):
        serializer = StudentOnboardingSerializer(data=self.valid_payload())

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_age_below_minimum_is_rejected(self):
        data = self.valid_payload()
        data["age"] = 2

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("age", serializer.errors)

    def test_age_above_maximum_is_rejected(self):
        data = self.valid_payload()
        data["age"] = 19

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("age", serializer.errors)

    def test_invalid_email_is_rejected(self):
        data = self.valid_payload()
        data["email"] = "invalid-email"

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("email", serializer.errors)

    def test_missing_parental_consent_is_rejected(self):
        data = self.valid_payload()
        data["parental_consent"] = False

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("parental_consent", serializer.errors)

    def test_inconsistent_support_request_is_rejected(self):
        data = self.valid_payload()
        data["has_learning_difficulty"] = False
        data["requires_learning_support"] = True

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("requires_learning_support", serializer.errors)

    def test_invalid_student_name_is_rejected(self):
        data = self.valid_payload()
        data["student_name"] = "Aarav123"

        serializer = StudentOnboardingSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn("student_name", serializer.errors)
