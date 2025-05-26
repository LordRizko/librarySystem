from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    full_name = Column(String(100), nullable=False)
    address = Column(String(200))
    phone = Column(String(20))
    is_admin = Column(Boolean, default=False)
    registration_date = Column(DateTime, default=datetime.now)
    
    # Relationships
    borrows = relationship("Borrow", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")
    
    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

class Book(Base):
    __tablename__ = 'books'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True)
    publication_year = Column(Integer)
    publisher = Column(String(100))
    genre = Column(String(50))
    description = Column(Text)
    available_copies = Column(Integer, default=1)
    total_copies = Column(Integer, default=1)
    
    # Relationships
    borrows = relationship("Borrow", back_populates="book")
    reservations = relationship("Reservation", back_populates="book")
    
    def __repr__(self):
        return f"<Book(id={self.id}, title='{self.title}', author='{self.author}')>"

class Borrow(Base):
    __tablename__ = 'borrows'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    borrow_date = Column(DateTime, default=datetime.now)
    due_date = Column(DateTime, default=lambda: datetime.now() + timedelta(days=14))
    return_date = Column(DateTime, nullable=True)
    is_returned = Column(Boolean, default=False)
    extended_times = Column(Integer, default=0)
    
    # Relationships
    user = relationship("User", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")
    
    def __repr__(self):
        return f"<Borrow(id={self.id}, user_id={self.user_id}, book_id={self.book_id})>"

class Reservation(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    book_id = Column(Integer, ForeignKey('books.id'), nullable=False)
    reservation_date = Column(DateTime, default=datetime.now)
    expiry_date = Column(DateTime, default=lambda: datetime.now() + timedelta(days=3))
    fulfilled = Column(Boolean, default=False)
    cancelled = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="reservations")
    book = relationship("Book", back_populates="reservations")
    
    def __repr__(self):
        return f"<Reservation(id={self.id}, user_id={self.user_id}, book_id={self.book_id})>"

