# Phase 3 Project: MMA Database & CLI Interface

This project consists of a CLI interface which interacts with a relational database consisting of 3 tables. 

# Installation

Clone this repository and save it to your local environment. While in the project-phase-3 directory run "pipenv install" to install the dependencies for the project, then run "pipenv shell" to enter the virtual environment. If permissions are needed, navigate to the "lib" directory and run "chmod +x seed.py cli.py".

# Running the Program

## Database

This program works with an empty database, and will create tables on startup if there aren't any present. If you would like to start with a set of data to play around with, navigate to the lib directory and run "./seed.py" to seed the database.

## CLI

Navigate to the lib directory and run "./cli.py" to execute the command line interface. 

# Usage

Using the series of prompts in the terminal, you may interact witht the database in multiple ways. Viewing, searching for, adding, updating, and deleting from all three tables is possible. Additionally, you may view related information such as a fighter's opponents and fights, as well as which fighters are in a weight class. 

# Acknowledgments

* Justin Rodriguez for support, guidance, and encouragement. 