import tkinter as tk
from tkinter import ttk
from tasks2 import Tasks
from datetime import datetime, timedelta

tasks_work = Tasks('base.json')
tasks_list = tasks_work.get_all()
print(tasks_list)


# Add button
def add_task():
    task_name = input_box.get()
    task_deadline = input_box_dl.get()
    if task_deadline.isdigit():
        dead_date = datetime.now() + timedelta(days=int(task_deadline))
        dead_date.strptime()
    if task_name:
        print(tk.END)

        todo_list.insert('', tk.END, values=(task_name, dead_date))
        new_task = {'name': task_name, 'deadline': dead_date}
        tasks_list.append(new_task)
        input_box.delete(0, tk.END)
        tasks_work.save(tasks_list)


# Remove button
def remove_task():
    if todo_list.selection():
        selected_item = todo_list.selection()
        ind_to_del = int(todo_list.index(selected_item))
        tasks_list.pop(ind_to_del)
        tasks_work.save(tasks_list)
        todo_list.delete(selected_item)


# Main window
main_app = tk.Tk()
main_app.title('ToDo List')

todo_list = ttk.Treeview(main_app, columns=('Task', 'Deadline'), show='headings')

todo_list.heading('Task', text='Task')
todo_list.heading('Deadline', text='Deadline')
todo_list.column("#0", width=0, stretch=tk.NO)
todo_list.column("#2", width=100, stretch=tk.NO)

todo_list.grid(row=0, column=0, sticky='nsew')

input_label = ttk.Label(main_app, text='Enter task/subtask name:')
input_label.grid(row=1, column=0, sticky='nsew')

input_label_dl = ttk.Label(main_app, text='Deadline: ')
input_label_dl.grid(row=1, column=0, sticky='nse')

input_box = ttk.Entry(main_app)
input_box.grid(row=2, column=0, sticky='nsew')

input_box_dl = ttk.Entry(main_app, width=7)
input_box_dl.grid(row=2, column=0, sticky='nse')

add_button = ttk.Button(main_app, text='Add', command=add_task)
add_button.grid(row=3, column=0, sticky='w', padx=5, pady=5)

remove_button = ttk.Button(main_app, text='Remove', command=remove_task)
remove_button.grid(row=3, column=0, sticky='e', padx=5, pady=5)

main_app.columnconfigure(0, weight=1)
main_app.rowconfigure(0, weight=1)
for task in tasks_list:
    print(task)
    todo_list.insert('', tk.END, values=(task['name'], task['deadline']))
main_app.mainloop()
