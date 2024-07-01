#!/usr/bin/python3
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database connection
PASSWORD = os.environ.get('password')
DATABASE_URL = "postgresql+psycopg2://eyen:PASSWORD@localhost:5432/mydb"
engine = create_engine(DATABASE_URL)

# Define the base
Base = declarative_base()

# Define the model
class User(Base):
    __tablename__ = 'campaign'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    contribution_id = Column(Integer())
    email = Column(String(100))
#    campaign = Column(String(255))

# Create tables
#Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Add a new user
#new_user = User(contribution_id=101, email='john.doe@example.com')
#session.add(new_user)
#session.commit()
