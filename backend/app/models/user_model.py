from sqlalchemy import Column, Integer, String, TIMESTAMP
from app.core.database import Base

class User(Base):
    __tablename__ = "tb_inai_mas_user"

    user_id = Column(Integer, primary_key=True, index=True)
    bio_id = Column(Integer)
    user_name = Column(String(25), nullable=False)
    password_hash = Column(String(250), nullable=False)
    created_by = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=False))
    updated_by = Column(Integer)
    updated_at = Column(TIMESTAMP(timezone=False))
    is_deleted = Column(Integer, default=0)
