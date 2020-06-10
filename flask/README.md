If you haven't already created a virtual environment for the project, do so by
running the following command:

    ./tools/create_venv

If you have created a virtual environment for the project, activate it by doing

    . scivocab_venv/bin/activate

Once it is activated, run the following command to install the prerequisites.

    pip install -r requirements.txt


The creation of the virtual environment and the installation of the prerequisites only need to be done once, but the activation of the virtual environment needs to be done in every new terminal session where you are trying to run the app.

Once the virtual environment is activated (you'll see `(scivocab_venv)` at the
command prompt), run the following command to launch the app:
    
    python run.py

To launch the app in debug mode, prepend `FLASK_DEBUG=1` to the above command.
That is, do:

    FLASK_DEBUG=1 python run.py
