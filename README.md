Scivocab
========

This repo contains the code for the Scientific Vocabulary study webapp.

Installation
------------

Install the requirements by running the following command (this assumes you
have Python 3.6 or higher installed already):

    ./tools/install

This command also creates a Python virtual environment called `scivocab_venv``

Creating the database
---------------------

To create the database or overwrite the existing database, run the following
(while in the virtual environment):

    ./tools/create_db

Running the app
---------------

### Development mode

Activate the `scivocab_venv` virtual environment:

    . scivocab_venv/bin/activate
    
After you activate the virtual environment, run the webapp in debug mode by
running the following command:

    ./tools/run_webapp_debug

Then open http://127.0.0.1:5000/ in your web browser to go to the webapp.

### Production mode

The following assumes you have [Docker Compose
installed](https://docs.docker.com/compose/install/).

To run the app in production mode (e.g. when deploying it to a server), run

    docker-compose up --build -d

You can then view the webpage at http://127.0.0.1:5001 (if you are running it on your
local computer). If you want to run the app in the foreground rather than as a
background process (e.g. for development purposes), omit the `-d` flag (`-d`
stands for 'detached').

To bring down the webapp safely, run

    docker-compose down

Exporting the data
------------------

Run this script to export the data

    ./tools/create_task_response_csvs

This script will create three CSV files, corresponding to the responses for the
breadth, depth, and definition task responses.

Contents
--------

- `README.md`: This README.
- `docker-requirements.txt`: The Python packages that the app depends upon to
  run using Docker.
- `Dockerfile`: The recipe for building the Docker container for deploying this
  app on a server.
- `docker-compose.yml`: A Docker Compose configuration file to help deploy the
  app on a server.
- `app`: The code for the app, along with the static content and templates.
  `app/static` contains the images, audio, and Javascript files.
- `tools`: Scripts to help automate installing and launching the app, creating
  the database, and exporting data from the database.
- `input_tables`: This contains raw data for creating `app/app.db`.
