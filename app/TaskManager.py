import itertools
from random import shuffle
from app.models import (
    Word,
    Strand,
)
from flask import jsonify, request, url_for


class TaskManager(object):
    def __init__(self, task: str):
        """The code in this method would normally be in the class's __init__
        method. However, we put the logic in this function instead because we
        need a top-level instance of this class to persist across requests in
        order to keep track of which item (word) a user has reached in the
        task, in order to prevent page refreshes/logouts from resetting
        progress.

        The normal method of persisting data across requests with Flask is to
        use Flask's 'session' object. However, this persistence is implemented
        by storing data on the user's computer as a cookie, which means that
        any data that is put into the Flask 'session' object must be
        JSON-serializable. Unfortunately, SQLAlchemy classes are not trivially
        serializable. In principle, we could implement custom serialization and
        deserialization logic, but for expediency's sake, we opt instead to
        keep the instance of the manager in memory rather than reconstructing
        it for every request."""

        self.task = task
        self.task_completed=False
        # Create an empty list to hold Word objects
        randomized_word_list: list[Word] = []

        if self.task == "breadth":
            training_items = (
                Word.query.filter(Word.breadth_id.startswith("bt"))
                .order_by(Word.breadth_id)
                .all()
            )
        else:
            training_items = (
                Word.query.filter(Word.depth_id.startswith("dt"))
                .order_by(Word.depth_id)
                .all()
            )

        # training items
        randomized_word_list.extend(training_items)

        # Get the strands from the database

        # Excluding training items because they have already been added to the list; see above
        strands = [
            strand for strand in Strand.query.all() if strand.id != "training"
        ]

        # Currently, we randomize the order of the strands.
        shuffle(strands)
        strand_word_counts: list = []

        # For each strand, we shuffle the words in the strand, and add those
        # words to randomized_word_list.
        for strand in strands:
            strand.words = strand.words[0:1]
            strand_word_counts.append(len(strand.words))
            shuffle(strand.words)
            randomized_word_list.extend(strand.words)

        # create the accumulative count variable
        self.cumulative_word_counts = list(
            itertools.accumulate(strand_word_counts)
        )

        print("strand word counts", strand_word_counts)
        print("cumulative word counts", self.cumulative_word_counts)
        self.current_word_index = 0

        # Which phase are we in - training counts as a phase, as does each
        # strand.
        self.current_phase_index = 0

        # We create an iterator out of the list in order to have the Python
        # runtime keep track of our iteration and as an additional safeguard to
        # prevent going backwards in the sequence.
        # (https://docs.python.org/3/glossary.html#term-iterator)
        self.randomized_word_iterator = iter(randomized_word_list)
        self.current_word = next(self.randomized_word_iterator)

    def go_to_next_word(self):
        # Shuffle the image_types list.
        shuffle(self.image_types)

        # Set the current_word attribute of the class instance to the next Word
        # in the iterator.
        self.current_word = next(self.randomized_word_iterator)
        self.current_word_index += 1

    # We attempt to go to the next word. If a StopIteration exception is
    # raised, that means we are at the end of the list, and so we redirect the
    # user to the post-task page.
    def check_redirect(self):
        try:
            self.go_to_next_word()
            print("current word index", self.current_word_index)
            # If the current_word_index is in cumulative_word_counts then we redirect
            if self.current_word_index-2 in self.cumulative_word_counts:
                self.current_phase_index += 1

                # Since we use Ajax and jQuery, we cannot use the usual Flask redirect
                # function here. This is our workaround.
                return jsonify(
                    {"redirect": "fun_fact/" + str(self.current_phase_index)}
                )


        except StopIteration:
            self.task_completed=True
            self.current_phase_index = 4
            return self.redirect_to_end()

    def redirect_to_end(self):
        return jsonify(
            {"redirect": "fun_fact/" + str(self.current_phase_index)}
        )

    def make_response(self, image_class):
        # We gather the filenames for the browser.
        filename_dict = {
            img.image_type.id: request.script_root
            + f"/static/scivocab/images/{self.task}/"
            + img.filename
            for img in image_class.query.filter_by(
                word_id=self.current_word.id
            ).all()
        }

        filenames = [
            filename_dict[image_type] for image_type in self.image_types
        ]

        # We construct a JSON-serializable dictionary with the filenames and the
        # target word.
        if self.current_word.audio_file is None:
            audio_file = ""
        else:
            audio_file = self.current_word.audio_file

        response = {
            "filenames": filenames,
            "current_target_word": self.current_word.target,
            "audio_file": url_for(
                "static", filename="scivocab/audio/" + audio_file
            ),
        }

        # We convert the dictionary into a JSON message using Flask's 'jsonify'
        # function and return that as a response, which will trigger the webpage to
        # change the images displayed with new ones based on this message.
        return jsonify(response)
