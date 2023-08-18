#!/usr/bin/env python3

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite

if __name__ == "__main__":
    engine = create_engine("sqlite:///EventPlanner.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    import ipdb

    ipdb.set_trace()
