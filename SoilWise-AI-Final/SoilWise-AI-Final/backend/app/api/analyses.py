from fastapi import APIRouter, Depends, File, Form, UploadFile, HTTPException, Query
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.core.database import get_db
from app.dependencies import current_user
from app.models.analysis import Analysis
from app.models.user import User
from app.schemas import AnalysisOut
from app.services.diagnostics import diagnose_soil, build_recommendations, crop_suggestions
from app.services.storage import save_image
from app.services.reports import make_report
from app.services.trends import summarize_trend

router = APIRouter()

def validate_values(n: float, p: float, k: float, ph: float, organic_matter: float, moisture: float):
    if not all(map(lambda x: x == x and abs(x) != float("inf"), [n, p, k, ph, organic_matter, moisture])):
        raise HTTPException(422, "All measurements must be finite numbers.")
    if not (0 <= n <= 10000 and 0 <= p <= 10000 and 0 <= k <= 10000):
        raise HTTPException(422, "NPK values must be between 0 and 10000 mg/kg.")
    if not (0 <= ph <= 14 and 0 <= organic_matter <= 100 and 0 <= moisture <= 100):
        raise HTTPException(422, "pH must be 0–14; organic matter and moisture must be 0–100.")

@router.post("", response_model=AnalysisOut, status_code=201)
async def create_analysis(
    nitrogen: float = Form(...), phosphorus: float = Form(...), potassium: float = Form(...),
    ph: float = Form(...), organic_matter: float = Form(...), moisture: float = Form(...),
    field_name: str = Form("My field", max_length=120), image: UploadFile | None = File(None),
    db: Session = Depends(get_db), user: User = Depends(current_user)
):
    validate_values(nitrogen, phosphorus, potassium, ph, organic_matter, moisture)
    diagnosis = diagnose_soil(nitrogen, phosphorus, potassium, ph, organic_matter, moisture)
    recommendations = build_recommendations(diagnosis, ph)
    recommendations.append({"title": "Possible crops to investigate", "detail": ", ".join(x["name"] for x in crop_suggestions(ph))})
    image_path = await save_image(image)
    row = Analysis(user_id=user.id, field_name=field_name.strip()[:120] or "My field", image_path=image_path,
                   nitrogen=nitrogen, phosphorus=phosphorus, potassium=potassium, ph=ph,
                   organic_matter=organic_matter, moisture=moisture,
                   health_score=diagnosis["score"], diagnosis=diagnosis, recommendations=recommendations)
    try:
        db.add(row)
        db.commit()
        db.refresh(row)
    except Exception:
        db.rollback()
        if image_path:
            from pathlib import Path
            Path(image_path).unlink(missing_ok=True)
        raise
    return row

@router.get("", response_model=list[AnalysisOut])
def list_analyses(
    limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0),
    db: Session = Depends(get_db), user: User = Depends(current_user)
):
    statement = select(Analysis).where(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()).offset(offset).limit(limit)
    return db.scalars(statement).all()


@router.get("/trends/summary")
def trend_summary(
    field_name: str = Query(..., min_length=1, max_length=120),
    db: Session = Depends(get_db), user: User = Depends(current_user),
):
    """Return observed score history for one field; does not extrapolate future risk."""
    rows = db.scalars(
        select(Analysis).where(Analysis.user_id == user.id, Analysis.field_name == field_name.strip())
        .order_by(Analysis.created_at.asc()).limit(100)
    ).all()
    return {"field_name": field_name.strip(), **summarize_trend(rows)}

@router.get("/{analysis_id}", response_model=AnalysisOut)
def get_analysis(analysis_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    row = db.scalar(select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id))
    if not row: raise HTTPException(404, "Analysis not found")
    return row

@router.get("/{analysis_id}/report")
def report(analysis_id: str, db: Session = Depends(get_db), user: User = Depends(current_user)):
    row = db.scalar(select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id))
    if not row: raise HTTPException(404, "Analysis not found")
    return Response(make_report(row), media_type="application/pdf",
                    headers={"Content-Disposition": f'attachment; filename="soil-report-{row.id[:8]}.pdf"', "Cache-Control": "private, no-store"})
