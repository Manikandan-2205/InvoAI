from sqlalchemy import Column, Integer, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Log(Base):
    __tablename__ = "tb_inai_log"
    __table_args__ = {"schema": "invoai"}

    log_id = Column(Integer, primary_key=True, index=True)
    login_time = Column(TIMESTAMP(timezone=False))
    logout_time = Column(TIMESTAMP(timezone=False))
    user_id = Column(Integer, ForeignKey("invoai.tb_inai_mas_user.user_id"))

    user = relationship("User", backref="logs")
