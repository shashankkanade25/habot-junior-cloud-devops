"""
HabotConnect Hiring Project
Candidate: Shashank Kanade
Email: shashankkanade07@gmail.com
Phone: 7820963908

Task 3: Deterministic Django REST Framework validation.
"""

from rest_framework import serializers

from .models import StudentOnboarding


class StudentOnboardingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentOnboarding
        fields = [
            "student_name",
            "email",
            "age",
            "country",
            "has_learning_difficulty",
            "requires_learning_support",
            "parental_consent",
        ]

    def validate_student_name(self, value):
        value = value.strip()

        if not 2 <= len(value) <= 100:
            raise serializers.ValidationError(
                "Student name must contain between 2 and 100 characters."
            )

        if not all(character.isalpha() or character in " -'" for character in value):
            raise serializers.ValidationError(
                "Student name may contain only letters, spaces, hyphens and apostrophes."
            )

        return value

    def validate_age(self, value):
        if not 3 <= value <= 18:
            raise serializers.ValidationError(
                "Student age must be between 3 and 18 years."
            )

        return value

    def validate_country(self, value):
        value = value.strip()

        if not 2 <= len(value) <= 56:
            raise serializers.ValidationError(
                "Country must contain between 2 and 56 characters."
            )

        if not all(character.isalpha() or character in " -'" for character in value):
            raise serializers.ValidationError(
                "Country may contain only letters, spaces, hyphens and apostrophes."
            )

        return value

    def validate(self, attrs):
        if not attrs["parental_consent"]:
            raise serializers.ValidationError(
                {
                    "parental_consent": (
                        "Parental consent is mandatory for student onboarding."
                    )
                }
            )

        if (
            attrs["requires_learning_support"]
            and not attrs["has_learning_difficulty"]
        ):
            raise serializers.ValidationError(
                {
                    "requires_learning_support": (
                        "Learning support cannot be requested when "
                        "no learning difficulty is declared."
                    )
                }
            )

        return attrs
