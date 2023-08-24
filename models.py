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


class Invite(Base):
    __tablename__ = "invite"

    id = Column(Integer, primary_key=True)
    sender_id = Column(Integer, ForeignKey("user.id"))
    invitee_id = Column(Integer, ForeignKey("user.id"))
    invitation = Column(String)
    event_id = Column(Integer, ForeignKey("event.id"))

    sender = relationship("User", back_populates="invites", foreign_keys=[sender_id])
    invitee = relationship("User", foreign_keys=[invitee_id])
    event = relationship("Event", back_populates="invites")

    def __repr__(self):
        return f"<Invite from: {self.sender.name}"


class User(Base):
    # table setup / relations
    # ------------------------------------------------------------------------------
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    owned_events = relationship("Event", back_populates="owner")
    events = relationship("Event", secondary=user_event, back_populates="attendees")
    invites = relationship(
        "Invite", back_populates="invitee", foreign_keys=[Invite.invitee_id]
    )

    # instance methods
    # ------------------------------------------------------------------------------
    def __repr__(self):
        return f"<User: {self.name}>"

    def create_event(self, event):
        if self.owned_events[0]:
            return "User cannot own multiple events."
        eve = Event(title=event, owner_id=self.id)
        session.add(eve)
        session.commit()

    def invite_user(self, user):
        query = session.query(User).filter(User.name.ilike(f"%{user}%")).first()

        if self == user:
            return "Cannot invite self"
        message = f"You've been invited to {self.name}'s {self.owned_events[0].title}!"
        invite = Invite(
            sender_id=self.id,
            invitee_id=query.id,
            invitation=message,
            event_id=self.owned_events[0].id,
        )
        session.add(invite)
        session.commit()

    def answer_invite(self, input):
        pass

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
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="owned_events", foreign_keys=[owner_id])
    attendees = relationship("User", secondary=user_event, back_populates="events")
    invites = relationship("Invite", back_populates="event")

    # instance methods
    def __repr__(self):
        return f"<Event: {self.title}>"

    def check_attendees(self):
        for i in self.attendees:
            print(i.name)

    def remove_attendee(self, user):
        for i in self.attendees:
            if i.name == user.name:
                self.attendees.remove(i)
        session.commit()

    @classmethod
    def get_all(cls):
        all = session.query(cls)
        for event in all:
            print(event)
