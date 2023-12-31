#!/usr/bin/env python3

from models import User, Event, Invite, user_event
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from faker import Faker
import random

fake = Faker()

engine = create_engine("sqlite:///EventPlanner.db")

Session = sessionmaker(bind=engine)
session = Session()

EVENTS = ["wedding", "birthday", "expo", "concert", "corporate", "house-warming"]


# creating methods to seed db
def delete_entries():
    session.query(User).delete()
    session.query(Event).delete()
    session.query(Invite).delete()
    session.query(user_event).delete()


def seed_db():
    delete_entries()
    for i in range(5):
        user = User(name=fake.unique.name())
        session.add(user)
        session.commit()

        event = Event(
            title=random.choice(EVENTS), owner_id=user.id, event_date=fake.date()
        )
        for i in range(3):
            event.attendees.append(User(name=fake.unique.name()))
        session.add(event)
        session.commit()
        invitee = User(name=fake.unique.name())
        session.add(invitee)
        session.commit()

        inv = Invite(
            sender_id=user.id,
            invitee_id=invitee.id,
            invitation=f"You've been invited to {user.name}'s {user.owned_events[0].title}!",
            event_id=user.owned_events[0].id,
        )
        session.add(inv)
        session.commit()


# running methods to seed db
seed_db()
