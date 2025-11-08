from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Extraction(Base):
    __tablename__ = "tb_inai_extraction_details"
    __table_args__ = {"schema": "invoai"}

    extraction_id = Column(Integer, primary_key=True, index=True)
    extraction_name = Column(String(50), nullable=False)
    x_min = Column(Integer)
    x_max = Column(Integer)
    y_min = Column(Integer)
    y_max = Column(Integer)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=False))
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP(timezone=False))
    is_deleted = Column(Integer, default=0)
    vendor_id = Column(Integer, ForeignKey("invoai.tb_inai_mas_vendor.vendor_id"))

    vendor = relationship("Vendor", backref="extraction_details")
