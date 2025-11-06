from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ReturnJson(Base):
    __tablename__ = "tb_inai_return_json"

    return_id = Column(Integer, primary_key=True, index=True)
    invoice_number = Column(String(30))
    extracted_json = Column(JSON)
    vendor_id = Column(Integer, ForeignKey("tb_inai_mas_vendor.vendor_id"))
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=False))
    is_deleted = Column(Integer, default=0)

    vendor = relationship("Vendor", backref="extracted_invoices")
