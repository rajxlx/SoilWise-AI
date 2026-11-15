from app.services.diagnostics import diagnose_soil, build_recommendations, crop_suggestions

def test_low_nutrient_is_flagged():
    result = diagnose_soil(100, 10, 50, 6.5, 1.2, 30)
    assert result["score"] < 100
    assert "low_nitrogen" in {x["code"] for x in result["issues"]}
    assert build_recommendations(result, 6.5)

def test_healthy_screening_has_no_alerts():
    result = diagnose_soil(350, 30, 180, 6.8, 1.5, 35)
    assert result["score"] == 100
    assert result["issues"] == []

def test_extreme_ph_is_flagged():
    acidic = diagnose_soil(350, 30, 180, 4.8, 1.5, 35)
    alkaline = diagnose_soil(350, 30, 180, 8.5, 1.5, 35)
    assert "acidic" in {x["code"] for x in acidic["issues"]}
    assert "alkaline" in {x["code"] for x in alkaline["issues"]}
    assert crop_suggestions(8.5)


def test_trend_requires_three_observations_and_detects_direction():
    from datetime import datetime, timezone, timedelta
    from types import SimpleNamespace
    from app.services.trends import summarize_trend

    now = datetime.now(timezone.utc)
    two = [SimpleNamespace(created_at=now + timedelta(days=i), health_score=70 + i) for i in range(2)]
    assert summarize_trend(two)["trend_available"] is False
    three = [SimpleNamespace(created_at=now + timedelta(days=i), health_score=70 + i * 5) for i in range(3)]
    result = summarize_trend(three)
    assert result["trend_available"] is True
    assert result["direction"] == "improving"
