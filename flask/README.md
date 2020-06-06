If you haven't already created a virtual environment for the project, do so.

If you have created a virtual environment for the project, activate it.

Once it is activated, run the following command to install the prerequisites.

    pip install -r requirements.txt


Then, run the following command to launch the app:
    
    python run.py

To launch the app in debug mode, prepend `FLASK_DEBUG=1` to the above command.
That is, do:

    FLASK_DEBUG=1 python run.py
