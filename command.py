from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite
from simple_term_menu import TerminalMenu
from cli_color_py import red, green, yellow, cyan
import pyinputplus as pyinp
import time

engine = create_engine("sqlite:///EventPlanner.db")
Session = sessionmaker(bind=engine)
session = Session()


class CommandLine:
    def __init__(self):
        self.current_user = None

    def start(self):
        self.clear()
        if not self.current_user:
            select = ["Login", "Sign-Up", "Close Application"]
        if self.current_user:
            print(f"Logged in as: {self.current_user.name} \n\n")
            select = [
                "Manage My Events",
                "Create New Event",
                "Sign Out and Exit",
            ]
        menu = TerminalMenu(select)
        entry_index = menu.show()
        self.handle_select(select[entry_index])

    def clear(self):
        print("\n" * 50)

    def create_user(self):
        username = pyinp.inputRegex(
            r"^[a-zA-Z]+ [a-zA-Z]+$",
            prompt=red(
                "Please enter First and Last name with one space and no symbols please :) "
            ),
        )
        print(cyan(f"You Entered: {username} \n Is this Correct?"))
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

    def handle_login(self):
        name = pyinp.inputRegex(
            r"^[a-zA-Z]+ [a-zA-Z]+$",
            prompt=red("Please enter First and Last name to Login: "),
        )
        search = session.query(User).filter(User.name.ilike(f"%{name}%")).first()
        if not search:
            print(
                red(
                    f"User {name} not found, would you like to create a new User with this name?"
                )
            )
            menu = TerminalMenu(["Yes", "Retry", "Exit"])
            answer = menu.show()
            if answer == 0:
                user = User(name=name)
                self.current_user = user
                self.start()
            if answer == 1:
                self.clear()
                self.handle_login()
            if answer == 2:
                self.start()

        self.current_user = search
        self.start()

    def withdraw(self):
        self.display_events()
        pass

    def create_event(self):
        self.display_events()
        pass

    def display_events(self):
        # no owned events
        if not self.current_user.owned_events:
            print(red("You do not own any Events\n"))

            # no attending events and no invites
            if not self.current_user.events and not self.current_user.invites:
                print(
                    red(
                        "You are currently not attending any events.\nNo event Invites :("
                    )
                    + yellow("\nReturning to Login Menu")
                )
                time.sleep(5)
                self.start()
            # either attending events or has invites
            if self.current_user.events or self.current_user.invites:
                events = [event.title for event in self.current_user.events]
                if events:
                    for i in events:
                        print("Attending: " + cyan(i) + "\n")
                    if not self.current_user.invites:
                        print(red("No Invites"))
                        menu = TerminalMenu(
                            ["Create Event", "Withdraw from Event", "Go Back"]
                        )
                        answer = menu.show()
                        if answer == 0:
                            self.create_event()
                        if answer == 1:
                            self.withdraw()
                        if answer == 2:
                            self.start()
                    print(yellow(f"You have invites!\n"))
                    menu = TerminalMenu(
                        [
                            "Create Event",
                            "Withdraw from Event",
                            "Answer Invites",
                            "Go Back",
                        ]
                    )
                    answer = menu.show()
                    if answer == 0:
                        self.create_event()
                    if answer == 1:
                        self.withdraw()
                    if answer == 2:
                        self.answer_invites(self.current_user.invites)
                    if answer == 3:
                        self.start

                if not events:
                    print(red("No Events to Attend \n"))
                    print(yellow(f"You have invites!\n"))
                    menu = TerminalMenu(["Create Event", "Answer Invites", "Go Back"])
                    answer = menu.show()
                    if answer == 0:
                        self.create_event()
                    if answer == 1:
                        self.answer_invites(self.current_user.invites)
                    if answer == 2:
                        self.start()
        if self.current_user.owned_events[0]:
            print(
                cyan("Owned Event:")
                + "\n"
                + f"{self.current_user.owned_events[0].title.upper()}, "
                + yellow(
                    f"Number of Attendees: {len(self.current_user.owned_events[0].attendees)} \n"
                )
            )
            menu = TerminalMenu(["Cancel Event", "Invite/Remove Attendees", "Go Back"])
            answer = menu.show()
            if answer == 0:
                print(red("Are you sure? This cannot be undone\n"))
                confirm = TerminalMenu(["Yes", "No"])
                response = confirm.show()
                if response == 0:
                    self.remove_event()
                if response == 1:
                    self.display_events()
            if answer == 1:
                print(cyan("Current Attendees:\n"))
                for a in self.current_user.owned_events[0].attendees:
                    print(yellow(a.name + "\n"))
                edit = TerminalMenu(["Invite Attendees", "Remove Attendee"])
                res = edit.show()
                if res == 0:
                    attendee = input("Enter First and Last of Attendee to Invite: ")
                    self.current_user.invite_user(attendee)
                    print(
                        cyan(
                            "User Invited! When they accept they will be added!\nReturning to Events Page"
                        )
                    )
                    time.sleep(3.5)
                    self.clear()
                    self.display_events()
                if res == 1:
                    attendee = input("Enter First and Last of attendee to remove: ")
                    query = (
                        session.query(User)
                        .filter(User.name.ilike(f"%{attendee}%"))
                        .first()
                    )
                    self.current_user.owned_events[0].remove_attendee(query)
                    print(red(f"{query} Removed from Event\n Returning to Events Page"))
                    time.sleep(3.5)
                    self.clear()
                    self.display_events()
            if answer == 2:
                self.start()

    def answer_invites(self, invites):
        for inv in invites:
            print(cyan(f"{inv.invitation}\n"))

            menu = TerminalMenu(["Accept", "Decline"])
            answer = menu.show()
            if answer == 0:
                query = (
                    session.query(Event).filter(Event.owner_id == inv.sender_id).first()
                )
                query.attendees.append(self.current_user)
                self.current_user.invites.remove(inv)
                print(cyan("Accepted Invite!"))
            if answer == 1:
                self.current_user.invites.remove(inv)
                print(red("Declined Invite"))
        session.commit()
        time.sleep(2)
        self.clear()
        self.display_events()

    def exit(self):
        print(red(f"Good Bye {self.current_user.name}!"))
        time.sleep(2)
        self.current_user = None
        self.start()

    def close_app(self):
        print(red("Thank you for using my Event Planner!"))
        time.sleep(1.5)
        self.clear()
        return "exit"

    def handle_select(self, selection):
        dictionary = {
            "Sign-Up": self.create_user,
            "Login": self.handle_login,
            "Close Application": self.close_app,
            "Manage My Events": self.display_events,
            "Create New Event": self.create_event,
            "Sign Out and Exit": self.exit,
        }
        dictionary[selection]()
