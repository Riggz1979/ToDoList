import json
class Tasks:
    def __init__(self,file_name):
        self.file_name = file_name


    def get_all(self):
        try:
            with open(self.file_name, 'r+') as f:
                self.all_tasks = json.load(f)
        except Exception:
            self.all_tasks = list()
        return self.all_tasks

    def save(self, task_list):
        with open(self.file_name, 'w') as f:
            json.dump(task_list, f)

    def remove(self, task_num):
        self.all_tasks = self.get_all()
        del self.all_tasks[task_num]
        with open(self.file_name, 'w') as f:
            json.dump(self.all_tasks, f)