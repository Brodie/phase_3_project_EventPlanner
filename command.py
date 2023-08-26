from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import User, Event, Invite
from simple_term_menu import TerminalMenu
from cli_color_py import red, yellow, cyan
import pyinputplus as pyinp
import time
from banner import Banner
import sys

engine = create_engine("sqlite:///EventPlanner.db")
Session = sessionmaker(bind=engine)
session = Session()


class CommandLine:
    def __init__(self):
        self.current_user = None

    def start(self):
        self.clear()
        Banner.welcome()
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
                session.add(user)
                session.commit()
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
        i = 1
        for eve in self.current_user.events:
            print(yellow(f"{i}: {eve.title},") + cyan(f"{eve.event_date}\n"))
            i = i + 1
        remove = input("Enter Number of Event to withdraw from: ")
        if int(remove) not in range(1, i):
            self.clear()
            print(red(f"Error. {remove} not accepted. Try Again\n"))
            self.withdraw()
        if not remove:
            print(red("Invalid Entry. Returning to main menu"))
            time.sleep(2)
            self.start()
        index = int(remove) - 1
        session.query(Event).filter(
            Event.id == self.current_user.events[index].id
        ).delete()
        session.commit()
        print(cyan("Withdrawn From Event\nReturning to menu"))
        time.sleep(2)
        self.start()

    def create_event(self):
        self.clear()
        check = (
            session.query(Event).filter(Event.owner_id == self.current_user.id).first()
        )
        if check:
            print(red("Cannot own multiple Events"))
            time.sleep(1.5)
            self.start()
        print(yellow("Creating Event...\n"))
        event_name = input("Please Enter Name of Event: ")
        print("\n\n")
        event_date = pyinp.inputRegex(
            r"^\d{4}-\d{2}-\d{2}$",
            prompt="Enter event date in following format: YYYY-MM-DD ",
        )

        eve = Event(
            title=event_name, owner_id=self.current_user.id, event_date=event_date
        )
        session.add(eve)
        session.commit()

        print(yellow("\nWould you like to Invite guests?"))
        menu = TerminalMenu(["Yes", "No"])
        answer = menu.show()
        if answer == 0:
            self.invite_guests()
        if answer == 1:
            print(cyan("Event created!\nReturning to Home"))
            time.sleep(2)
            self.start()

    def invite_guests(self):
        print(yellow("\n\n\nEnter nothing to exit\n"))
        name = input("Enter First and Last Name of guest to invite: ")
        if not name:
            self.start()
        query = session.query(User).filter(User.name.ilike(f"%{name}%")).first()

        if self == name:
            print(red("Cannot invite self"))
            self.invite_guests()
        if not query:
            print(red("User does not exist. Please try again\n\n\n"))
            self.invite_guests()

        message = f"You've been invited to {self.current_user.name}'s {self.current_user.owned_events[0].title} on {self.current_user.owned_events[0].event_date}!"
        invite = Invite(
            sender_id=self.current_user.id,
            invitee_id=query.id,
            invitation=message,
            event_id=self.current_user.owned_events[0].id,
        )
        session.add(invite)
        session.commit()
        print(
            cyan(
                f"\nInvite sent to {query.name} when they accept it\nthey will appear in your attendees\n\nWhat would you like to do?\n"
            )
        )
        menu = TerminalMenu(["Invite Another Guest", "Exit"])
        answer = menu.show()
        if answer == 0:
            self.clear()
            self.invite_guests()
        if answer == 1:
            self.start()

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
                if self.current_user.events:
                    for i in self.current_user.events:
                        print(
                            "Attending: "
                            + yellow(f"{i.title} ")
                            + "on "
                            + cyan(f"{i.event_date}\n\n")
                        )
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

                if not self.current_user.events:
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

        # is the owner of events
        if self.current_user.owned_events[0]:
            print(
                cyan("Owned Event:")
                + "\n"
                + f"{self.current_user.owned_events[0].title.upper()}, "
                + yellow(
                    f"Number of Attendees: {len(self.current_user.owned_events[0].attendees)} "
                )
                + cyan(
                    f"Event Date: {self.current_user.owned_events[0].event_date}\n\n"
                )
            )
            # owns events, has invites, and is attending events
            if self.current_user.invites and self.current_user.events:
                for i in self.current_user.events:
                    print(
                        "Attending: "
                        + yellow(f"{i.title} ")
                        + "on "
                        + cyan(f"{i.event_date}\n\n")
                    )
                print(yellow("You have invites!\n\n"))
                menu = TerminalMenu(
                    [
                        "Cancel Event",
                        "Invite/Remove Attendees",
                        "Withdraw from Event",
                        "Answer Invites",
                        "Go Back",
                    ]
                )
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
                        self.invite_guests()
                    if res == 1:
                        attendee = input("Enter First and Last of attendee to remove: ")
                        query = (
                            session.query(User)
                            .filter(User.name.ilike(f"%{attendee}%"))
                            .first()
                        )
                        self.current_user.owned_events[0].remove_attendee(query)
                        print(
                            red(
                                f"{query} Removed from Event\n Returning to Events Page"
                            )
                        )
                        time.sleep(3.5)
                        self.clear()
                        self.display_events()
                if answer == 2:
                    self.withdraw()
                if answer == 3:
                    self.answer_invites(self.current_user.invites)
                if answer == 4:
                    self.start()
            # owns event and has invites but not attending event
            if self.current_user.invites:
                print(yellow("You have invites!\n\n"))
                menu = TerminalMenu(
                    [
                        "Cancel Event",
                        "Invite/Remove Attendees",
                        "Answer Invites",
                        "Go Back",
                    ]
                )
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
                        self.invite_guests()
                    if res == 1:
                        attendee = input("Enter First and Last of attendee to remove: ")
                        query = (
                            session.query(User)
                            .filter(User.name.ilike(f"%{attendee}%"))
                            .first()
                        )
                        self.current_user.owned_events[0].remove_attendee(query)
                        print(
                            red(
                                f"{query} Removed from Event\n Returning to Events Page"
                            )
                        )
                        time.sleep(3.5)
                        self.clear()
                        self.display_events()
                if answer == 2:
                    self.answer_invites(self.current_user.invites)
                if answer == 3:
                    self.start()

            # owns events, is attending event, has no invites
            if self.current_user.events:
                for i in self.current_user.events:
                    print(
                        "Attending:"
                        + yellow(f"{i.title}")
                        + "on"
                        + cyan(f"{i.event_date}\n\n")
                    )
                menu = TerminalMenu(
                    [
                        "Cancel Event",
                        "Invite/Remove Attendees",
                        "Withdraw from Event",
                        "Go Back",
                    ]
                )
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
                        self.invite_guests()
                    if res == 1:
                        attendee = input("Enter First and Last of attendee to remove: ")
                        query = (
                            session.query(User)
                            .filter(User.name.ilike(f"%{attendee}%"))
                            .first()
                        )
                        self.current_user.owned_events[0].remove_attendee(query)
                        print(
                            red(
                                f"{query} Removed from Event\n Returning to Events Page"
                            )
                        )
                        time.sleep(3.5)
                        self.clear()
                        self.display_events()
                if answer == 2:
                    self.withdraw()
                if answer == 3:
                    self.start()
            # no invites, no attending events
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
                    self.invite_guests()
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

    def remove_event(self):
        session.query(Event).filter(Event.owner_id == self.current_user.id).delete()
        session.commit()
        print(red("Event Canceled"))
        time.sleep(2)
        self.start()

    def exit(self):
        print(red(f"Good Bye {self.current_user.name}!"))
        time.sleep(2)
        self.current_user = None
        self.start()

    def close_app(self):
        self.clear()
        Banner.goodbye()
        print(yellow("Thank you for using my Event Planner!"))
        time.sleep(2.5)
        self.clear()
        sys.exit()

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
