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
        options = ["Login", "Sign-Up"]
        menu = TerminalMenu(options)
        entry_index = menu.show()
        print(cyan(f"selected {options[entry_index]}"))

    def clear(self):
        print("\n" * 50)
