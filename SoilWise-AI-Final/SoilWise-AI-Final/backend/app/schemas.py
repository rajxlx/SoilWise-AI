from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Any

class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=120)
    preferred_language: Literal["en", "hi", "kn"] = "en"

class UserOut(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    preferred_language: str
    model_config = {"from_attributes": True}

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class AnalysisOut(BaseModel):
    id: str
    field_name: str
    nitrogen: float
    phosphorus: float
    potassium: float
    ph: float
    organic_matter: float
    moisture: float
    health_score: int
    diagnosis: dict[str, Any]
    recommendations: list[dict[str, Any]]
    created_at: Any
    model_config = {"from_attributes": True}
