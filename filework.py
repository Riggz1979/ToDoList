import json
from datetime import datetime

logs = False


# Logging
def log(message):
    if logs:
        with open('logs', 'a') as f:
            f.write(f'{datetime.now().strftime('%d-%m-%Y, %H:%M')} : {message}  \n')


# Settings block
def get_settings():
    global logs
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except Exception as e:
        # No, or wrong settings file, go default

        settings = {'base': 'base.json', 'logs': True}
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
        log(e)
        log('Default settings saved to settings.json')
    logs = settings['logs']
    return settings


def save_settings(settings):
    with open('settings.json', 'w') as f:
        json.dump(settings, f)
        log('Settings saved to settings.json')


class FileWork:
    def __init__(self, file_name):
        self.file_name = file_name
        self.all_tasks = list()

    def get_all(self):
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
        with open(self.file_name, 'w') as f:
            json.dump(task_list, f)

    def clear_base(self):
        with open(self.file_name, 'w'):
            log(f'{self.file_name} cleared!')
