from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    ForeignKey,
    MetaData,
    create_engine,
)

engine = create_engine("sqlite:///EventPlanner.db")
Session = sessionmaker(bind=engine)
session = Session()

# foreign keys naming convention, so that all tables are standardized
con = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=con)

Base = declarative_base(metadata=metadata)

user_event = Table(
    "user_event",
    Base.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("event_id", ForeignKey("event.id"), primary_key=True),
    extend_existing=True,
)


class User(Base):
    # table setup / relations
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    owned_events = relationship("Event", back_populates="owner")
    events = relationship("Event", secondary=user_event, back_populates="attendees")
    invites = relationship("Invite", back_populates="user")

    # instance methods
    def __repr__(self):
        return f"<User: {self.name}>"

    def __init__(self, name):
        self.name = name
        self.invites = []
        self.invited_events = []

    def create_event(self, event):
        eve = Event(title=event)
        session.add(eve)
        session.commit()

    # need to fix these methods:

    # def invite_user(self, user):
    #     invite = f"You've been invited to {self.name}'s {self.owned_events}!"
    #     user.invites.append(invite)
    #     user.invited_events.append(self.owned_events)

    # def answer_invite(self, input):
    #     if not input:
    #         self.invites.pop[0]
    #         self.invited_events.pop[0]
    #         return "Declined Invite"
    #     self.invited_events[0].attendees.append(self)
    #     self.invites.pop[0]
    #     self.invited_events.pop[0]
    #     return "Successfully added to Event! Invitation deleted"

    @classmethod
    def get_all(cls):
        all = session.query(cls)
        for user in all:
            print(user)


class Event(Base):
    # table setup / relations
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"), unique=True)

    owner = relationship("User", back_populates="owned_events", foreign_keys=[owner_id])
    attendees = relationship("User", secondary=user_event, back_populates="events")
    invites = relationship("Invite", back_populates="event")

    # instance methods
    def __repr__(self):
        return f"<Event: {self.title}>"

    def check_attendees(self):
        for i in self.attendees:
            print(i.name)

    @classmethod
    def get_all(cls):
        all = session.query(cls)
        for event in all:
            print(event)


class Invite(Base):
    __tablename__ = "invite"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    invitation = Column(String)
    event_id = Column(Integer, ForeignKey("event.id"))
    user = relationship("User", back_populates="invites")
    event = relationship("Event", back_populates="invites")
