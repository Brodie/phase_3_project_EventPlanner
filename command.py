from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite
from simple_term_menu import TerminalMenu
from cli_color_py import red, green, yellow, cyan


class CommandLine:
    def __init__(self):
        self.current_user = None

    def start(self):
        self.clear()
        if not self.current_user:
            options = ["Login", "Sign-Up"]
        if self.current_user:
            options = [
                "Manage My Events",
                "Create New Event",
                "Events to Attend",
                "Sign Out and Exit",
            ]
        menu = TerminalMenu(options)
        entry_index = menu.show()
        self.handle_login(entry_index)

    def clear(self):
        print("\n" * 50)

    def handle_login(self, selection):
        if selection == 1:
            self.create_user()

    def create_user(self):
        username = input("Please enter First and Last name: ")
        print(username)
