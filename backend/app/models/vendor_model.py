from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base

class Vendor(Base):
    __tablename__ = "tb_inai_mas_vendor"
    __table_args__ = {"schema": "invoai"}

    vendor_id = Column(Integer, primary_key=True, index=True)
    vendor_name = Column(String(100), nullable=False, unique=True)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=False))
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP(timezone=False))
    is_deleted = Column(Integer, default=0)
