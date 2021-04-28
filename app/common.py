from flask import jsonify

def check_managers_dict(global_manager_dict, current_user_id, task_manager_class):
    # If there isn't a BreadthTaskManager for the current user yet, create one
    # and add it to the MANAGERS dictionary.
    if global_manager_dict.get(current_user_id) is None:
        global_manager_dict[current_user_id] = task_manager_class()
