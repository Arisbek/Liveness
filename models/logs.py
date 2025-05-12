from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from dependencies.db import Base


class Logs(Base):
    __tablename__ = "logs"
    time_created = Column(TIMESTAMP, nullable=True, default=func.now())
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    method = Column(String, nullable=False)
    url = Column(Text, nullable=False)
    ip_address = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("services.id"), index=True, nullable=True)
    request = Column(String)
    response = Column(String)

    # Relationship
    service = relationship("Services", back_populates="logs")
