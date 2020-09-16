Install the app by running the following command (this assumes you have Python
3.6 or higher installed already):

    ./tools/install

Run the webapp in debug mode by running the following command:
   
    ./tools/run_webapp_debug

Then open http://127.0.0.1:5000/ in your web browser to go to the webapp.


This flask-aided python program reads in data from static/scivocab/sv_bv1_input and images from static/scivocab/sv_bv1. The following packages are required- Pandas, 
Flask, Itertools and Random.

This program expects there to be only four images per target.

It contains five flask render templates, which represent different browser pages.

To launch this program, run the command run.py in the flask folder.
