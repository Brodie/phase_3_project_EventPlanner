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

    # instance methods
    def __repr__(self):
        return f"<User: {self.name}>"

    def __init__(self, name):
        self.name = name
        self.invites = []

    def create_event(self, event):
        eve = Event(title=event)
        session.add(eve)
        session.commit()

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
