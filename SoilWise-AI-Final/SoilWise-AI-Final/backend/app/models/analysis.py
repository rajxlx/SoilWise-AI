import uuid
from sqlalchemy import String, Float, Integer, DateTime, ForeignKey, JSON, func, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class Analysis(Base):
    __tablename__ = "analyses"
    __table_args__ = (Index("ix_analyses_user_created", "user_id", "created_at"),)
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id", ondelete="CASCADE"), index=True)
    field_name: Mapped[str] = mapped_column(String(120), default="My field")
    image_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    nitrogen: Mapped[float] = mapped_column(Float)
    phosphorus: Mapped[float] = mapped_column(Float)
    potassium: Mapped[float] = mapped_column(Float)
    ph: Mapped[float] = mapped_column(Float)
    organic_matter: Mapped[float] = mapped_column(Float)
    moisture: Mapped[float] = mapped_column(Float)
    health_score: Mapped[int] = mapped_column(Integer)
    diagnosis: Mapped[dict] = mapped_column(JSON)
    recommendations: Mapped[list] = mapped_column(JSON)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="analyses")
