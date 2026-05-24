from sqlalchemy import Column, String, DateTime
from datetime import datetime
from api.core.database import Base

class ProcessedEvent(Base):
    __tablename__ = 'processed_events'

    event_id = Column(String, primary_key=True, index=True)
    processed_at = Column(DateTime, default=datetime.utcnow)
    