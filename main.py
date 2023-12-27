import tkinter as tk
from tkinter import ttk
from tasks import Tasks
from datetime import datetime, timedelta

tasks_work = Tasks('base.json')
tasks_list = tasks_work.get_all()



# Add button
def add_task():
    task_name = input_box.get()
    task_deadline = input_box_dl.get()
    if task_deadline.isdigit():
        dead_date = datetime.now() + timedelta(days=int(task_deadline))
        str_date = dead_date.strftime('%d-%m-%Y')
    else:
        str_date = 'No'
    if task_name:
        todo_list.insert('', tk.END, values=(task_name, str_date))
        new_task = {'name': task_name, 'deadline': str_date, 'done': 'no'}
        tasks_list.append(new_task)
        input_box.delete(0, tk.END)
        input_box_dl.delete(0, tk.END)
        tasks_work.save(tasks_list)


# Remove button
def remove_task():
    if todo_list.selection():
        selected_item = todo_list.selection()
        ind_to_del = int(todo_list.index(selected_item))
        tasks_list.pop(ind_to_del)
        tasks_work.save(tasks_list)
        todo_list.delete(selected_item)


def mark_unmark():
    selected_item = todo_list.selection()
    if selected_item:
        ind = (todo_list.index(selected_item))
        if tasks_list[ind]['done'] == 'yes':
            todo_list.item(selected_item, tags=('',))
            tasks_list[ind]['done'] = 'no'
        else:
            todo_list.item(selected_item, tags=('green',))
            tasks_list[ind]['done'] = 'yes'
        tasks_work.save(tasks_list)


def show_context_menu(event):
    item = todo_list.identify_row(event.y)
    print(item)
    if item:
        todo_list.selection_set(item)
        context_menu.post(event.x_root+30, event.y_root)

# Main window
main_app = tk.Tk()
main_app.title('ToDo List')
# List window
todo_list = ttk.Treeview(main_app, columns=('Task', 'Deadline'), show='headings')
todo_list.heading('Task', text='Task')
todo_list.heading('Deadline', text='Deadline')
todo_list.column("#0", width=0, stretch=tk.NO)
todo_list.column("#2", width=100, stretch=tk.NO)
todo_list.grid(row=0, column=0, sticky='nsew', columnspan=3)
todo_list.tag_configure('green', foreground='lightgreen')
todo_list.tag_configure('red', foreground='red')

# Input labels
input_label = ttk.Label(main_app, text='Enter task/subtask name:')
input_label.grid(row=1, column=0, sticky='nsew', columnspan=2, padx=5, pady=5)
input_label_dl = ttk.Label(main_app, text='Deadline: ')
input_label_dl.grid(row=1, column=2, sticky='w', padx=5, pady=5)
# Input boxs
input_box = ttk.Entry(main_app)
input_box.grid(row=2, column=0, sticky='nsew', columnspan=2, padx=5, pady=5)
input_box_dl = ttk.Entry(main_app, width=7)
input_box_dl.grid(row=2, column=2, sticky='w', padx=5, pady=5)
# Buttons
add_button = ttk.Button(main_app, text='Add', command=add_task)
add_button.grid(row=3, column=0, sticky='w', padx=5, pady=5)
remove_button = ttk.Button(main_app, text='Remove', command=remove_task)
remove_button.grid(row=3, column=2, sticky='e', padx=5, pady=5)
mark_button = ttk.Button(main_app, text='Mark', command=mark_unmark)
mark_button.grid(row=3, column=1, sticky='', padx=5, pady=5)
# Right-click menu
context_menu = tk.Menu(main_app, tearoff=0)
context_menu.add_command(label='Edit', command=mark_unmark)
context_menu.add_command(label='Remove', command=remove_task)

main_app.columnconfigure(0, weight=1)
main_app.rowconfigure(0, weight=1)
# Events
todo_list.bind("<Button-2>", show_context_menu)

for task in tasks_list:
    print(task['done'])
    if task['done'] == 'yes':
        todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='green')
    elif task['done'] == 'fail':
        todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='red')
    else:
        todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='')
main_app.mainloop()
