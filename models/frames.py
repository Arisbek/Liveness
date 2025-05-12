from sqlalchemy import Column, Integer, String, Text, ForeignKey, TIMESTAMP,JSON
from sqlalchemy.orm import relationship
from dependencies.db import Base

class Frames(Base):
    __tablename__ = "frames"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey('services.id'), index=True, nullable=False)
    frame = Column(String, nullable=False)
    time_created = Column(TIMESTAMP, nullable=False)
    predictions = Column(JSON,nullable=True) 
    # Relationship
    service = relationship("Services", back_populates="frames")