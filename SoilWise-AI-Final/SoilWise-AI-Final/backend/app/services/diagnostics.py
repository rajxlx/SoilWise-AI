from typing import Any

# MVP screening thresholds only. Current assumed units: N/P/K mg/kg, organic matter %, moisture %.
# Validate extraction method, crop, soil type and regional lab reference ranges before agronomic use.

def diagnose_soil(n: float, p: float, k: float, ph: float, organic_matter: float, moisture: float) -> dict[str, Any]:
    issues = []
    if n < 280: issues.append({"code": "low_nitrogen", "nutrient": "Nitrogen", "level": "low", "message": "Nitrogen is below the illustrative MVP screening threshold."})
    if p < 22: issues.append({"code": "low_phosphorus", "nutrient": "Phosphorus", "level": "low", "message": "Phosphorus is below the illustrative MVP screening threshold."})
    if k < 140: issues.append({"code": "low_potassium", "nutrient": "Potassium", "level": "low", "message": "Potassium is below the illustrative MVP screening threshold."})
    if ph < 5.5: issues.append({"code": "acidic", "nutrient": "pH", "level": "attention", "message": "Soil is strongly acidic; confirm with a laboratory test."})
    elif ph > 7.8: issues.append({"code": "alkaline", "nutrient": "pH", "level": "attention", "message": "Soil is alkaline; confirm with a laboratory test."})
    if organic_matter < 0.5: issues.append({"code": "low_organic_matter", "nutrient": "Organic matter", "level": "low", "message": "Organic matter is below the illustrative MVP screening threshold."})
    if moisture < 10: issues.append({"code": "low_moisture", "nutrient": "Moisture", "level": "attention", "message": "Moisture is low at the time of measurement."})
    score = max(20, min(100, 100 - len(issues) * 12))
    return {"score": score, "status": "Good" if score >= 80 else "Needs attention" if score >= 55 else "Critical review",
            "issues": issues, "method": "Illustrative rule-based MVP screening; not a laboratory diagnosis or trained ML prediction."}

def build_recommendations(diagnosis: dict, ph: float) -> list[dict]:
    recs = []
    codes = {x["code"] for x in diagnosis["issues"]}
    if "low_nitrogen" in codes: recs.append({"title": "Review nitrogen management", "detail": "Ask a local agronomist to calculate nitrogen application from your laboratory report; split application only where locally recommended."})
    if "low_phosphorus" in codes: recs.append({"title": "Review phosphorus availability", "detail": "Confirm available phosphorus with a soil test before selecting a phosphorus fertilizer."})
    if "low_potassium" in codes: recs.append({"title": "Review potassium management", "detail": "Confirm exchangeable potassium and local crop requirement before applying potash."})
    if ph < 5.5: recs.append({"title": "Check soil acidity", "detail": "Request a lime requirement test; do not estimate lime dosage from pH alone."})
    elif ph > 7.8: recs.append({"title": "Check alkaline soil constraints", "detail": "Test salinity and micronutrient availability; seek local extension advice."})
    if "low_organic_matter" in codes: recs.append({"title": "Build soil organic matter", "detail": "Consider well-decomposed compost, residue retention and suitable cover crops."})
    if "low_moisture" in codes: recs.append({"title": "Conserve soil moisture", "detail": "Consider mulching, irrigation scheduling and field-specific water conservation."})
    recs.append({"title": "Crop suitability", "detail": "Check season, rainfall, irrigation, soil texture, variety and local market conditions before crop selection."})
    return recs

def crop_suggestions(ph: float) -> list[dict]:
    if ph < 5.5:
        return [{"name": "Millets", "reason": "Some varieties tolerate a range of soil conditions; confirm local suitability."}, {"name": "Pulses", "reason": "Select locally adapted varieties after checking acidity and nutrient status."}]
    if ph > 7.8:
        return [{"name": "Barley", "reason": "Some varieties tolerate mildly alkaline conditions; verify salinity and local recommendations."}, {"name": "Cotton", "reason": "Suitability depends on drainage, salinity, rainfall and region."}]
    return [{"name": "Maize", "reason": "Potential option where season, water and nutrient needs are met."}, {"name": "Soybean", "reason": "Potential option where climate, drainage and local variety recommendations fit."}, {"name": "Wheat", "reason": "Potential option in a suitable season with adequate irrigation."}]
