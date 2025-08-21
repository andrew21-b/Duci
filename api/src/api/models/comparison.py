from datetime import datetime
from sqlalchemy import Float, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column
from src.api.models.base import Base

    
class Comparison(Base):
    __tablename__ = "comparisons"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    before_image : Mapped[str] = mapped_column(String, unique=True)
    after_image : Mapped[str] = mapped_column(String, unique=True)
    diff_image : Mapped[str] = mapped_column(String, unique=True)
    pixel_difference: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
