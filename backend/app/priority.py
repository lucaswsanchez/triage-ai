"""Priority = impact × urgency, using the helpdesk-kb priority matrix.

The model estimates impact and urgency (judgement calls); the priority itself is computed
deterministically here so it always follows the documented matrix.
"""

from app.schemas import Level3, Priority

MATRIX: dict[tuple[str, str], Priority] = {
    ("High", "High"): "P1",
    ("High", "Medium"): "P2",
    ("High", "Low"): "P3",
    ("Medium", "High"): "P2",
    ("Medium", "Medium"): "P3",
    ("Medium", "Low"): "P4",
    ("Low", "High"): "P3",
    ("Low", "Medium"): "P4",
    ("Low", "Low"): "P4",
}


def effective_impact(impact: Level3, category: str) -> Level3:
    """Security events affecting one user are treated as Medium impact (matrix examples)."""
    if category == "Security" and impact == "Low":
        return "Medium"
    return impact


def compute_priority(impact: Level3, urgency: Level3, category: str = "") -> Priority:
    return MATRIX[(effective_impact(impact, category), urgency)]
