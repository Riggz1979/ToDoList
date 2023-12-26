import json


class Tasks:
    def __init__(self, task_id: int, name='',deadline = 0):
        self.all_tasks = dict()
        self.task_id = str(task_id)
        self.name = name
        self.deadline = deadline

    def get_all(file_name):
        try:
            with open(file_name, 'r+') as f:
                all_tasks = json.load(f)
        except Exception:
            all_tasks = dict()
        return all_tasks
    def get_last_ind(self):
        all_tasks = self.get_all()
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

    def add(self):
        task_to_add = {self.task_id: {'name': self.name, 'deadline': self}}
        all_tasks = self.get_all()
        all_tasks.update(task_to_add)
        print(all_tasks)

