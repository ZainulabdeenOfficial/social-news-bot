from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    link = Column(String, unique=True, nullable=False)
    description = Column(Text)
    pub_date = Column(DateTime)
    source = Column(String)
    image_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    generated_content = relationship("GeneratedContent", back_populates="article")

class GeneratedContent(Base):
    __tablename__ = 'generated_content'
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey('articles.id'))
    platform = Column(String, nullable=False)
    post_text = Column(Text, nullable=False)
    hashtags = Column(String)
    image_prompt = Column(String)
    image_path = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    article = relationship("Article", back_populates="generated_content")
    posted_content = relationship("PostedContent", back_populates="generated_content")

class PostedContent(Base):
    __tablename__ = 'posted_content'
    id = Column(Integer, primary_key=True)
    generated_content_id = Column(Integer, ForeignKey('generated_content.id'))
    platform = Column(String, nullable=False)
    post_url = Column(String)
    posted_at = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default='success')
    error_message = Column(Text)
    generated_content = relationship("GeneratedContent", back_populates="posted_content")
