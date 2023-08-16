from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, Integer, String, Table, ForeignKey, MetaData

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
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    events = relationship("Event", secondary=user_event, back_populates="event")

    def __repr__(self):
        return f"<User: {self.name}>"


class Event(Base):
    __tablename__ = "event"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner = Column(Integer, ForeignKey("user.id"))

    attendees = relationship("User", secondary=user_event, back_populates="user")

    def __repr__(self):
        return f"<Event: {self.name}>"
