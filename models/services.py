from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from dependencies.db import Base

class Services(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationships
    frames = relationship("Frames", back_populates="service")
    logs = relationship("Logs", back_populates="service")