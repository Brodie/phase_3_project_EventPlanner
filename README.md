# Event Planner

Phase 3 CLI project

## Description

CLI Application that uses Python, SQLAlchemy, and Alembic to create Users and Events, and manage the relationship between them. Users can create events, invite other users to events, and modify the list of event attendees. Repo has a built in seeding file to pre-seed the database with test data to test out the application's features

## Installation

After Forking, and copying the SSH, navigate to the folder you wish to clone the repo into and run:

```bash
git clone SSH_File
```

Pasting the copied URL in place of SSH_File

## Usage

After cloning, run the following command to install the relavant dependancies to make the application function

```bash
pipenv install && pipenv shell
```

pipenv shell will navigate us into the virtual environment where the application will run.

To seed the database with some fake data to test out the features of the app run the following (optional) command:

```bash
python seeds.py
```

Then to start the app run the following command:

```bash
python run.py
```

Have Fun!

## Information

This application while functional, does not include many aspects one might expect an Event planner to have. This project was built with the goal of displaying the ability to create python classes and successfully map them to a database using SQLAlchemy. Then manage proper database migrations using Alembic when creating the relationships between said classes.

## Improvements / Roadmap

- Add method to edit owned event name.
- Add method to edit username
- Add more attributes to the Event Class so that it feels more like a real event (due to time constraints, left some of these out in favor of building out the CLI application)
- Add more secure login with User Password. Would probably only add this to 1, show that i'm capable and 2, if I was going to expand this into a fully fledged application

## Resources

- https://pypi.org/ -- Used this site to find the CLI text color changer, as well as a package to create the banner message
    - Check pipfile for full list of packages used

<br>

- https://docs.sqlalchemy.org/en/14/index.html -- Constantly had to check and recheck the SQLAlchemy docs while building out my classes and ensuring the relationships were working as intended

- Huge thanks to the Flatiron instructors. Everything that went into creating this project felt extremely overwhelming trying to learn at once. Thru watching and rewatching some of the demonstrations and lectures, I was able to work my way through this project and create a proper CLI application!!! Thank you! 