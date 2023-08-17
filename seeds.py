#!/usr/bin/env python3

from models import User, Event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker

fake = Faker()

engine = create_engine("sqlite:///EventPlanner.db")

Session = sessionmaker(bind=engine)
session = Session()

for i in range(5):
    user = User(name=fake.unique.name())
    session.add(user)
    session.commit()
