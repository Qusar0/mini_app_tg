from datetime import  datetime, time, date
from sqlalchemy import Integer, ForeignKey, text, Text, DateTime
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import List, Optional
from app.dao.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True)
    username: Mapped[Optional[str]]
    first_name: Mapped[str]
    last_name: Mapped[Optional[str]]

    # Relationships
    bookings: Mapped[List["Booking"]] = relationship(back_populates="user")


class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    patronymic: Mapped[Optional[str]]
    special: Mapped[str]
    specialization_id: Mapped[int] = mapped_column(ForeignKey('specializations.id'), server_default=text("1"))
    work_experience: Mapped[int] = mapped_column(Integer, nullable=False)
    experience: Mapped[int]
    description: Mapped[str] = mapped_column(Text)
    photo: Mapped[str]

    # Relationships
    bookings: Mapped[List["Booking"]] = relationship(back_populates="doctor")
    specialization: Mapped["Specialization"] = relationship("Specialization", back_populates="doctors",
                                                            lazy="joined")


class Specialization(Base):
    __tablename__ = "specializations"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str]
    label: Mapped[str]
    specialization: Mapped[str]

    # Relationships
    doctors: Mapped[List["Doctor"]] = relationship(back_populates="specialization")


class Booking(Base):
    __tablename__ = "booking"

    id: Mapped[int] = mapped_column(primary_key=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    day_booking: Mapped[date] = mapped_column(nullable=False)
    time_booking: Mapped[time] = mapped_column(nullable=False)
    booking_status: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships
    doctor: Mapped["Doctor"] = relationship(back_populates="bookings")
    user: Mapped["User"] = relationship(back_populates="bookings")