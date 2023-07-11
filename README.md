# Booking System for Cinema Customers - Ryan Morgan

This implentation is a containerised Django website which allows customers to book tickets for cinema showings.

Make sure project is opened as directory (in terminal/IDE).
If a venv is needed, then one can be created (python3 -m venv .venv). Though running the project in a container doesn't need a venv, dependencies can be installed from the requirements.txt (this is what the docker script uses).

## How to Run

When testing the django project; the create, read, update and delete (all CRUD) operations were fully working when containerised.

Run this line in the terminal to build image based from the Dockerfile.
**'docker build -t desdcustomerslim:1.0 .'**

Run this line to start/run the container on port 8000
**'docker run -p 8000:8000 desdcustomerslim:1.0'**

Once running, the django project can be accessed from '127.0.0.1:8000' in the web browser. It may say in the terminal that it's open in '0.0.0.0:8000', but that may not work. Open on '127.0.0.1:8000' instead.

Run this line in the terminal to build image based from the Dockerfile.\
**'docker build -t desdcustomerslim:1.0 .'**

Run this line to start/run the container on port 8000.\
**'docker run -p 8000:8000 desdcustomerslim:1.0'**

Once running, the django project can be accessed from '127.0.0.1:8000' in the web browser. It may say in the terminal that it's open in '0.0.0.0:8000', but that may not work. Open on '127.0.0.1:8000' instead.