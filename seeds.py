from models import User, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///EventPlanner.db")

Session = sessionmaker(bind=engine)
session = Session()
