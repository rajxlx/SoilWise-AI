import uuid
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(120), default="")
    preferred_language: Mapped[str] = mapped_column(String(5), default="en")
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    analyses = relationship("Analysis", back_populates="user", cascade="all, delete-orphan")
