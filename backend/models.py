from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    username = Column(String(20), unique=True, nullable=False)
    password_hash = Column(String(128), nullable=False)  # Hash qilingan password
    
    def __repr__(self):
        return f"<User(username={self.username}, fullname={self.fullname})>"
