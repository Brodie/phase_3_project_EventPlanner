import myfiglet


class Banner:
    def welcome():
        myfiglet.display("Event Planner", rainbow=True, pattern="name")

    def goodbye():
        myfiglet.display("Goodbye!", colour="red", pattern="name")
