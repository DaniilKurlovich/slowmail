import datetime

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime

from .session import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    location = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class ComingMessages(Base):
    __tablename__ = 'coming_message'

    id = Column(Integer, primary_key=True)
    from_addr = Column(Integer, ForeignKey("user.id"), nullable=False)
    to_addr = Column(Integer, ForeignKey("user.id"), nullable=False)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String(500), nullable=False)
    delay = Column(Integer, nullable=False)


class MailBox(Base):
    __tablename__ = 'mailbox'

    id = Column(Integer, primary_key=True, index=True)
    to_addr = Column(Integer, ForeignKey("user.id"), nullable=False)
    from_addr = Column(Integer, ForeignKey("user.id"), nullable=False)
    received = Column(DateTime, default=datetime.datetime.utcnow)
    message = Column(String(500), nullable=False)
    as_read = Column(Boolean, default=0)


class ConversationDialog(Base):
    __tablename__ = 'conversation_ids'

    chat_id = Column(Integer, primary_key=True, index=True)
    from_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    to_id = Column(Integer, ForeignKey('user.id'), nullable=False)
