from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), unique=True, index=True)
    region = Column(String(100))
    segment = Column(String(50))  # SMB, Mid-Market, Enterprise
    contract_value = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_churned = Column(Boolean, default=False)

    orders = relationship("Order", back_populates="customer")
    interactions = relationship("Interaction", back_populates="customer")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    product = Column(String(200))
    amount = Column(Float)
    region = Column(String(100))
    status = Column(String(50))  # completed, refunded, pending
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="orders")


class Interaction(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    channel = Column(String(50))   # email, call, chat
    sentiment = Column(Float)       # -1.0 to 1.0
    resolved = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    customer = relationship("Customer", back_populates="interactions")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String(100), unique=True, index=True)
    user_id = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

    messages = relationship("ChatMessage", back_populates="session")


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("chat_sessions.id"))
    role = Column(String(20))   # user | assistant
    content = Column(Text)
    tool_calls = Column(Text, nullable=True)  # JSON serialized
    created_at = Column(DateTime, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")
