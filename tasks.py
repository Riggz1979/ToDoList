import json


class Tasks:
    def __init__(self, task_id: int):
        self.all_tasks = dict()
        self.task_id = str(task_id)
        self.name = ''
        self.deadline = 0

    def get_all(self, base):
        try:
            with open(base, 'r+') as f:
                self.all_tasks = json.load(f)
        except Exception:
            self.all_tasks = dict()
        return self.all_tasks

    def rename(self, new_name):
        self.name = new_name

    def new_deadline(self, new_deadline):
        self.deadline = new_deadline

    def base_save(self, base):
        self.get_all(base)
        self.all_tasks[self.task_id] = {'name': self.name, 'deadline': self.deadline}
        with open(base, 'w') as f:
            json.dump(self.all_tasks, f)

    def get(self, base):
        self.get_all(base)
        return self.all_tasks[self.task_id]

    def remove(self, base):
        self.get_all(base)
        del self.all_tasks[self.task_id]
        with open(base, 'w') as f:
            json.dump(self.all_tasks, f)
        del self
