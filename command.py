from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite


class CommandLine:
    def __init__(self):
        self.current_user = None

    def start(self):
        pass
