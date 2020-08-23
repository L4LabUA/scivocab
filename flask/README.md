Install the app by running the following command (this assumes you have Python
3.6 or higher installed already):

    ./tools/install

Run the webapp in debug mode by running the following command:
   
    ./tools/run_webapp_debug

Then open http://127.0.0.1:5000/ in your web browser to go to the webapp.

Programs:

run.py- 
	Running run.py will launch the local flask server. It will run until manually shut down (or it crashes).
	While it is running, you can access the website at http://127.0.0.1:5000/(page), where page is the website page you want to go to, i.e. http://127.0.0.1:5000/breadth.


translate.py- 
	construct_word_dict takes in a filename for an excel sheet that is a list of words for input (see excel file flask/status/scivocab/sv_bv1_input for the format.)
	For each seperate name in target, it creates a word datatype (see below). Finally, it returns a dictionary of all created word datatypes.

	get_filename takes a word and id to translate into the format in which the images are saved- see the file sv_bv1.


word.py- A class that stores all the information needed to make one set of images associated with a target. The variable breakdown goes as such-
	strand = the strand number (identifies which science category it belongs to)
	target = the name of the word (target)
	tw, fp, fx, fs = the position each of these identifications is stored in- images are labelled 1 to 4, but one set may have tw in position 3 and fp in position 1, while another
		may have fp in 3 and tw in 1.
	id = linked to what test this word is attached to. (Breadth or Depth- specifically bv1 and dv1)

	identify.py- calling word.identify(num) will return the identification of any numbered image- word.identify(3) will return the value of the image in position 3.


breadth.py- The workhorse of the breadth app.
	Outside of method lines- Sets up what's needed at the beginning of the program. Specifically, it imports the required materials, loads the blueprint for the breadth webapp,
		imports all words from the given filename and stores them in a dictionary WORDS. Splits the words in WORDS into four strands in STRANDS, where each strand correlates
		to the strand types. It shuffles the words in each strand, and concatenates each strand in a list RANDOMIZED_LIST. Then it creates a list where we store the
		user inputs (which starts as an empty list, ANSWERS) and WORD_TYPE_LIST, which we will use later.

	main() starts the webapp up, and leads to a loop of selectImage().
	
	selectImage()- each call of selectImage loads a new word, waits for the user to select an image, and adds the selected word to ANSWERS in a data format known as answer. 
		In doing so, it slowly iterates through the list RANDOMIZED_LIST, and moves on to a new page when we reach the last word. In the process of ending, it should call
		postprocessing(ANSWERS).

answer.py- A class that stores all the information needed by the researcher after the program is done. This is three things.
	word = the name of the word (target)
	answer = tw, fp, fx, or fs, whichever the user selected.
	strand = which strand the word belonged to.

postprocessing.py- This method turns a list of answers into an excel file.
	This creates an empty 2D array with three columns, word, answer, and strand (see a pattern?). Then for each answer in answerArray, add those three things in the next row.
	This then gets translated into a dataframe, which is processed into an excelsheet using the to_excel method, at the file position static/scivocab/answers.xlsx. This will
	overwrite old files with that name without asking, fair warning.
	
	