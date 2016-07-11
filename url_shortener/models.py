from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
import config

Base = declarative_base()

class ShortUrl(Base):
    __tablename__  = 'short_urls'
    id             = Column(Integer, primary_key=True)
    created_at     = Column(DateTime, default=datetime.utcnow)
    key            = Column(String(10), nullable=False, index=True)
    target_url     = Column(String(1024), index=True)
    criteria       = Column(String(255))
    __table_args__ = (
                      UniqueConstraint('key', 'target_url', 'criteria', name='uq_1'),
                     )

class Click(Base):
    __tablename__  = 'clicks'
    id             = Column(Integer, primary_key=True)
    created_at     = Column(DateTime, default=datetime.utcnow)
    short_url_id   = Column(Integer, ForeignKey('short_urls.id'))
    referrer_url   = Column(String(1024))

engine = create_engine(config.DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
