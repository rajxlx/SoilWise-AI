from datetime import datetime
from typing import Iterable


def summarize_trend(records: Iterable) -> dict:
    """Summarize observed health-score history; this is not a future-risk ML model."""
    rows = sorted(records, key=lambda item: item.created_at)
    points = [
        {"date": item.created_at.isoformat() if isinstance(item.created_at, datetime) else str(item.created_at),
         "health_score": int(item.health_score)}
        for item in rows
    ]
    if len(points) < 3:
        return {"observations": points, "trend_available": False, "direction": "insufficient_history",
                "message": "At least three dated assessments are required to summarize a trend."}
    values = [point["health_score"] for point in points]
    x_mean = (len(values) - 1) / 2
    y_mean = sum(values) / len(values)
    denominator = sum((index - x_mean) ** 2 for index in range(len(values)))
    slope = sum((index - x_mean) * (value - y_mean) for index, value in enumerate(values)) / denominator
    direction = "improving" if slope > 1 else "declining" if slope < -1 else "stable"
    return {"observations": points, "trend_available": True, "direction": direction,
            "average_score_change_per_assessment": round(slope, 2),
            "message": "Observed historical direction only; no future degradation prediction is made."}
