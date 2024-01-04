import json
from datetime import datetime

logs = False


# Logging
def log(message):
    """
    Log the given message with timestamp if logging is enabled.

    Args:
        message (str): The message to be logged.

    Returns:
        None
    """
    if logs:
        with open('logs', 'a') as f:
            f.write(f'{datetime.now().strftime("%d-%m-%Y, %H:%M")} : {message}  \n')


# Settings block
def get_settings():
    """
    Retrieve settings from 'settings.json' file or use default settings if the file is not found or invalid.

    Returns:
        dict: A dictionary containing the retrieved or default settings.
    """
    global logs
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except Exception as e:
        # No, or wrong settings file, use default
        settings = {'base': 'base.json', 'logs': True}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        log(e)
        log('Default settings saved to settings.json')
    logs = settings['logs']
    return settings


def save_settings(settings):
    """
    Save the provided settings to 'settings.json' file.

    Args:
        settings (dict): The settings to be saved.

    Returns:
        None
    """
    with open('settings.json', 'w') as f:
        json.dump(settings, f)
        log('Settings saved to settings.json')


class FileWork:
    def __init__(self, file_name):
        """
        Initialize a FileWork object with the specified file name.

        Args:
            file_name (str): The name of the file to work with.
        """
        self.file_name = file_name
        self.all_tasks = list()

    def get_all(self):
        """
        Retrieve all tasks from the specified file and mark overdue tasks as 'fail'.

        Returns:
            list: A list of dictionaries representing tasks.
        """
        try:
            with open(self.file_name, 'r+') as f:
                self.all_tasks = json.load(f)
        except Exception as e:
            log(e)
            self.all_tasks = list()
        for task in self.all_tasks:
            # Checking deadline status and mark outdated as 'fail'
            if task['deadline'] != 'No':
                date_obj = datetime.strptime(task['deadline'], "%d-%m-%Y")
                if date_obj < datetime.now() and task['done'] != 'yes':
                    task['done'] = 'fail'
        return self.all_tasks

    def save(self, task_list):
        """
        Save the provided list of tasks to the specified file.

        Args:
            task_list (list): A list of dictionaries representing tasks.

        Returns:
            None
        """
        with open(self.file_name, 'w') as f:
            json.dump(task_list, f)

    def clear_base(self):
        """
        Clear the contents of the specified file.

        Returns:
            None
        """
        with open(self.file_name, 'w'):
            log(f'{self.file_name} cleared!')
