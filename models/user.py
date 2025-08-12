from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, TIMESTAMP, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base import Base
import enum

# Enum for gender
class GenderEnum(enum.Enum):
    male = "male"
    female = "female"
    other = "other"

# Users Table
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(500))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(
        TIMESTAMP, 
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )

    # Relationships
    addresses = relationship("UserAddress", back_populates="user", cascade="all, delete-orphan")
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


# User Addresses Table
class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    line_1 = Column(String(100))
    line_2 = Column(String(100))
    city = Column(String(100))
    postal_code = Column(String(15))
    state = Column(String(100))
    country = Column(String(100))
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="addresses")
    profiles = relationship("UserProfile", back_populates="address", cascade="all, delete-orphan")


# User Profiles Table
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    gender = Column(Enum(GenderEnum), default=None)
    phone_no = Column(String(15), nullable=False)
    dob = Column(Date, nullable=False)
    address_id = Column(Integer, ForeignKey("user_addresses.id", ondelete="CASCADE"))
    profile_picture_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="profile")
    address = relationship("UserAddress", back_populates="profiles")
