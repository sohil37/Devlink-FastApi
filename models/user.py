from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, TIMESTAMP, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from db.base import Base
from enums.user import GenderEnum

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
    line_1 = Column(String(100), nullable=False)
    line_2 = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    postal_code = Column(String(15), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="addresses")
    profiles = relationship("UserProfile", back_populates="address", cascade="all, delete-orphan")


# User Profiles Table
class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    gender = Column(Enum(GenderEnum), default=None)
    phone_no = Column(String(15))
    dob = Column(Date)
    address_id = Column(Integer, ForeignKey("user_addresses.id", ondelete="CASCADE"))
    profile_picture_url = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    # Relationships
    user = relationship("User", back_populates="profile")
    address = relationship("UserAddress", back_populates="profiles")
