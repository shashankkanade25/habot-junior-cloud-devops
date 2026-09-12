"""
HabotConnect Hiring Project
Candidate: Shashank Kanade
Email: shashankkanade07@gmail.com
Phone: 7820963908

Task 3: Student onboarding data model.
"""

from django.db import models


class StudentOnboarding(models.Model):
    student_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    age = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=56)

    has_learning_difficulty = models.BooleanField()
    requires_learning_support = models.BooleanField()
    parental_consent = models.BooleanField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.student_name
