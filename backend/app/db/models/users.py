from app.db.database import Base

from sqlalchemy import Column, Boolean, Integer, Text, DateTime, String
from sqlalchemy.dialects.postgresql import UUID, CITEXT
from sqlalchemy.sql import func
from sqlalchemy import text

class User(Base):
    __tablename__ = "users"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()")
    )

    username = Column(CITEXT, unique=True, nullable=False)
    email = Column(CITEXT, unique=True, nullable=False)

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50))

    password = Column(Text, nullable=False)

    role = Column(Text, nullable=False, server_default="user")
    is_active = Column(Boolean, nullable=False, server_default=text("true"))
    is_verified = Column(Boolean, nullable=False, server_default=text("false"))
    failed_login_attempts = Column(Integer, nullable=False, server_default=text("0"))
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    locked_until = Column(DateTime(timezone=True), nullable=True)
    
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
