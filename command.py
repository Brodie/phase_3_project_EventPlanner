from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite
from simple_term_menu import TerminalMenu
from cli_color_py import red, green, yellow, cyan
import pyinputplus as pimp

engine = create_engine("sqlite:///EventPlanner.db")
Session = sessionmaker(bind=engine)
session = Session()


class CommandLine:
    def __init__(self):
        self.current_user = None

    def start(self):
        self.clear()
        if not self.current_user:
            select = ["Login", "Sign-Up"]
        if self.current_user:
            select = [
                "Manage My Events",
                "Create New Event",
                "Events to Attend",
                "Sign Out and Exit",
            ]
        menu = TerminalMenu(select)
        entry_index = menu.show()
        self.handle_select(select[entry_index])

    def clear(self):
        print("\n" * 50)

    def handle_login(self, selection):
        pass

    def create_user(self):
        username = pimp.inputRegex(
            r"^[a-zA-Z]+ [a-zA-Z]+$",
            prompt="Please enter First and Last name with one space and no symbols please :) ",
        )
        print(f"You Entered: {username} \n Is this Correct?")
        menu = TerminalMenu(["Yes", "No"])
        answer = menu.show()
        if answer == 1:
            self.clear()
            self.create_user()
        user = User(name=f"{username}")
        session.add(user)
        session.commit()
        self.current_user = user
        self.start()

    def handle_select(self, selection):
        switch_dict = {"Sign-Up": self.create_user, "Login": self.handle_login}
        switch_dict[selection]()
