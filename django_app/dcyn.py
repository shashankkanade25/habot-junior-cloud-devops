"""
HabotConnect Hiring Project
Candidate: Shashank Kanade
Email: shashankkanade07@gmail.com
Phone: 7820963908

Task 3: Deterministic Yes/No (DCYN) decision library.
"""

DCYN_RULES = {
    "DCYN-01": {
        "field": "has_learning_difficulty",
        "yes_when": True,
        "no_when": False,
    },
    "DCYN-02": {
        "field": "requires_learning_support",
        "yes_when": True,
        "no_when": False,
    },
    "DCYN-03": {
        "field": "parental_consent",
        "yes_when": True,
        "no_when": False,
    },
}


def evaluate_dcyn(data):
    """Evaluate onboarding data using deterministic Yes/No rules."""
    decisions = {}

    for rule_id, rule in DCYN_RULES.items():
        value = data[rule["field"]]

        if value is rule["yes_when"]:
            decisions[rule_id] = "YES"
        else:
            decisions[rule_id] = "NO"

    return decisions
