Scivocab
========

This repo contains the code for the Scientific Vocabulary study webapp.

Installation
------------

Install the app by running the following command (this assumes you have Python
3.6 or higher installed already):

    ./tools/install

Creating the database
---------------------

To create the database or overwrite the existing database, run the following
(while in the virtual environment):

    ./tools/create_db

Running the app
---------------

### Development mode

Run the webapp in debug mode by running the following command:

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

Contents
--------

- `README.md`: This README.
- `requirements.txt`: The Python packages that the app depends upon.
- `Dockerfile`: The recipe for building the Docker container for deploying this
  app on a server.
- `docker-compose.yml`: A Docker Compose configuration file to help deploy the
  app on a server.
- `app`: The code for the app, along with the static content and templates.
  `app/static` contains the images and the spreadsheets with the words and
  foils.
- `tools`: Scripts to help automate installing and launching the app.
