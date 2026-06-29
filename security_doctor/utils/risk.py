from dataclasses import dataclass, field
from typing import Any


@dataclass
class CheckResult:
    name: str
    status: str
    message: str
    details: str
    risk_points: int
    explanation: str = ""
    recommendation: str = ""
    learn_more_url: str = ""
    display_data: dict[str, Any] = field(default_factory=dict)


def calculate_general_risk(results: list[CheckResult]) -> str:
    """
    Calculates the general risk level based on accumulated risk points.

    Suggested scale:
    0-2   Low
    3-6   Medium
    7+    High
    """
    total_points = sum(result.risk_points for result in results)

    if total_points >= 7:
        return "Alto"

    if total_points >= 3:
        return "Medio"

    return "Bajo"


def status_icon(status: str) -> str:
    icons = {
        "ok": "✔",
        "warning": "⚠",
        "critical": "❌",
        "info": "ℹ",
        "unknown": "?",
    }

    return icons.get(status, "?")