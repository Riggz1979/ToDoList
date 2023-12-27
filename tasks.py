import json
from datetime import datetime, timedelta


class Tasks:
    def __init__(self, file_name):
        self.file_name = file_name

    def get_all(self):
        try:
            with open(self.file_name, 'r+') as f:
                self.all_tasks = json.load(f)

        except Exception:
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
