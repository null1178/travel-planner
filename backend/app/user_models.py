from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    plans = relationship("SavedPlan", back_populates="user", cascade="all, delete-orphan")


class SavedPlan(Base):
    __tablename__ = "saved_plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    destination = Column(String(100), nullable=False)
    total_days = Column(Integer, nullable=False)
    budget_level = Column(String(20), nullable=False)
    plan_data = Column(JSON, nullable=False)  # full TripPlan as JSON
    request_data = Column(JSON, nullable=True)  # original PlanRequest
    rating = Column(Integer, nullable=True)
    comment = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="plans")
