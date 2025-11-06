from app.core.response_handler import success_response, error_response
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/vendor/{vendor_id}")
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    vendor = db.query(Vendor).filter(Vendor.vendor_id == vendor_id).first()
    if not vendor:
        return error_response("Vendor not found", 404)
    return success_response(vendor, "Vendor retrieved successfully")
