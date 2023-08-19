from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite


class CommandLine:
    def __init__(self):
        self.current_user = None

    def start(self):
        self.new_screen()
        print("Hello!")

    def new_screen(self):
        print("\n" * 50)
