import tkinter as tk
from tkinter import ttk, filedialog, simpledialog, messagebox
from filework import FileWork, get_settings, save_settings
from datetime import datetime, timedelta
import platform

settings = get_settings()

tasks_work = FileWork(settings['base'])
tasks_list = tasks_work.get_all()

# Cross-platform compatibility
platform = platform.system()
if platform == 'Darwin':
    RMB = '<Button-2>'
else:
    RMB = '<Button-3>'


def get_index():
    if todo_list.selection():
        selected_item = todo_list.selection()
        return todo_list.index(selected_item)
    return None


# Add button
def add_task():
    """
        Add a new task to the To-Do List.

        The function retrieves the task name and deadline from the input widgets.
        If a numerical value is provided for the deadline, it calculates the deadline date based on the current date.
        The task is then inserted into the To-Do List display using 'todo_list.insert'.
        A new task dictionary is created and appended to the 'tasks_list' data structure.
        The input widgets are cleared after adding the task.
        The changes are saved using the 'tasks_work.save' method (assuming 'tasks_work' is an object
        with a 'save' method to persist the changes).

        :return: None
        """
    task_name = input_box.get()
    task_deadline = input_box_dl.get()
    if task_deadline.isdigit():
        dead_date = datetime.now() + timedelta(days=int(task_deadline))
        str_date = dead_date.strftime('%d-%m-%Y')
    else:
        str_date = 'No'
    if task_name:
        todo_list.insert('', tk.END, values=(task_name, str_date))
        new_task = {'name': task_name, 'deadline': str_date, 'done': 'no', 'subtasks': []}
        tasks_list.append(new_task)
        input_box.delete(0, tk.END)
        input_box_dl.delete(0, tk.END)
        tasks_work.save(tasks_list)


def add_subtask():
    """
        Add a new subtask to the selected task in the To-Do List.

        The function checks if a task is selected and if the selected item is a parent (not a subtask).
        If these conditions are met, the function prompts the user to enter the name of the new subtask.
        If the user provides a subtask name, it is inserted into the To-Do List display using 'todo_list.insert'.
        A new subtask dictionary is created and appended to the 'subtasks' list of the selected task in 'tasks_list'.
        The changes are then saved using the 'tasks_work.save' method (assuming 'tasks_work' is an object
        with a 'save' method to persist the changes).

        :return: None
        """
    selected_item = todo_list.selection()
    ind = get_index()
    if selected_item and todo_list.parent(selected_item) == '':
        subtask = simpledialog.askstring('', '')
        if subtask:
            todo_list.insert(selected_item, tk.END, values=subtask)
            subtask_to_add = {'name': subtask, 'done': 'no'}
            tasks_list[ind]['subtasks'].append(subtask_to_add)
            tasks_work.save(tasks_list)


# Remove button
def remove_task():
    """
    Remove the selected task or subtask from the To-Do List.

    The function checks if a task is selected and if the selected item is a parent (not a subtask).
    If these conditions are met, the selected task is removed from 'tasks_list' and the changes are saved.
    The selected task is also deleted from the To-Do List display using 'todo_list.delete'.
    If a subtask is selected, it is removed from the list of subtasks of the parent task in 'tasks_list'.
    The changes are then saved, and the To-Do List display is refreshed using 'fill_todo'.

    :return: None
    """
    selected_item = todo_list.selection()

    if selected_item and todo_list.parent(selected_item) == '':
        # Removing the selected task from 'tasks_list'
        ind_to_del = get_index()
        tasks_list.pop(ind_to_del)

        # Saving the changes
        tasks_work.save(tasks_list)

        # Deleting the selected task from the To-Do List display
        todo_list.delete(selected_item)

    elif selected_item and todo_list.parent(selected_item) != '':
        # Removing the selected subtask from the list of subtasks of the parent task
        selected_item = todo_list.selection()
        ind = todo_list.index(todo_list.parent(selected_item))
        selected_sub_name = todo_list.item(selected_item)['values'][0]

        i = 0
        for subtask in tasks_list[ind]['subtasks']:
            if subtask['name'] == selected_sub_name:
                tasks_list[ind]['subtasks'].pop(i)
                break
            i += 1

        # Saving the changes and refreshing the To-Do List display
        tasks_work.save(tasks_list)
        fill_todo()


# Mark button
def mark_unmark():
    selected_item = todo_list.selection()
    if selected_item:
        # Task or subtask?
        if todo_list.parent(selected_item) == '':
            ind = (todo_list.index(selected_item))
            if tasks_list[ind]['done'] == 'yes':
                todo_list.item(selected_item, tags=('',))
                tasks_list[ind]['done'] = 'no'
            else:
                todo_list.item(selected_item, tags=('good',))
                tasks_list[ind]['done'] = 'yes'
        else:
            ind = (todo_list.index(todo_list.parent(selected_item)))
            selected_sub_name = str((todo_list.item(selected_item)['values'][0]))
            for subtask in tasks_list[ind]['subtasks']:
                if subtask['name'] == selected_sub_name:
                    if subtask['done'] == 'no':
                        subtask['done'] = 'yes'
                        todo_list.item(selected_item, tags=('good',))
                    else:
                        subtask['done'] = 'no'
                        todo_list.item(selected_item, tags=('',))
        fill_todo()
        tasks_work.save(tasks_list)


# New base creation func
def new_base():
    global tasks_list, tasks_work
    new_base_dialog = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("JSON", "*.json")])
    settings['base'] = new_base_dialog
    save_settings(settings)
    tasks_work = FileWork(settings['base'])
    tasks_work.clear_base()
    tasks_list = tasks_work.get_all()
    fill_todo()


# Open base menu func
def open_base():
    global tasks_list, tasks_work
    open_base_dialog = (tk.filedialog.askopenfilename
                        (parent=main_app, title='Open base:', filetypes=[('json', '*.json')]))
    if 'settings.json' in open_base_dialog:
        tk.messagebox.showerror('Alert!', 'settings.json is not a base!')
    else:
        settings['base'] = open_base_dialog
        save_settings(settings)
        tasks_work = FileWork(settings['base'])
        tasks_list = tasks_work.get_all()
        fill_todo()


def show_context_menu(event):
    item = todo_list.identify_row(event.y)
    if item:
        todo_list.selection_set(item)
        if todo_list.parent(todo_list.selection()) != '':
            context_menu.entryconfig('Add subtask', state='disabled')
            context_menu.entryconfig('Edit deadline', state='disabled')
        else:
            context_menu.entryconfig('Add subtask', state='normal')
            context_menu.entryconfig('Edit deadline', state='normal')
        context_menu.post(event.x_root + 30, event.y_root)


# Edit task name
def edit_name():
    """
    Edit the name of task or subtask
    Name
    :return:
    """
    index = get_index()
    new_name = tk.simpledialog.askstring(title='', prompt='Enter new name:')
    if new_name:
        if todo_list.parent(todo_list.selection()) == '':
            tasks_list[index]['name'] = new_name
        else:
            ind = (todo_list.index(todo_list.parent(todo_list.selection())))
            name_to_edit = todo_list.item(todo_list.selection())['values'][0]
            for subtask in tasks_list[ind]['subtasks']:
                if str(subtask['name']) == str(name_to_edit):
                    subtask['name'] = new_name
        tasks_work.save(tasks_list)
        fill_todo()


# Edit deadline
def edit_deadline():
    """
    Edit the deadline of the selected task in the To-Do List.

    The function prompts the user to enter the number of days to the new deadline using 'tk.simpledialog.askstring'.
    If a valid numerical value is provided, the function calculates the new deadline date based on the current date.
    The new deadline is then saved in 'tasks_list', and the changes are persisted using 'tasks_work.save'.
    If the task was marked as failed ('done' is 'fail'), it is marked as not done ('no').
    The To-Do List display is refreshed using 'fill_todo'.

    :return: None
    """
    index = get_index()
    new_deadline = tk.simpledialog.askstring(title='', prompt='Enter days to deadline:')

    # Checking if the provided deadline is a number
    if new_deadline.isdigit():
        dead_date = datetime.now() + timedelta(days=int(new_deadline))
        str_date = dead_date.strftime('%d-%m-%Y')
    else:
        str_date = 'No'

    # Updating the deadline in 'tasks_list'
    tasks_list[index]['deadline'] = str_date

    # If the task was marked as failed, mark it as not done
    if tasks_list[index]['done'] == 'fail':
        tasks_list[index]['done'] = 'no'

    # Saving the changes
    tasks_work.save(tasks_list)

    # Refreshing the To-Do List display
    fill_todo()


def fill_todo():
    """
    Fill and display the To-Do List with tasks and subtasks from the 'tasks_list'.

    The function clears the current content of the To-Do List display using 'todo_list.delete'.
    Then, it iterates through each task in 'tasks_list' and inserts it into the To-Do List display.
    If a task is completed ('done' is 'yes' or 'fail'), it is tagged as 'good' or 'bad' accordingly.
    If a task has subtasks, it iterates through them and inserts them as child items.
    The main task is marked as completed if all subtasks are completed, and vice versa.
    The changes are applied recursively, and the To-Do List display is updated accordingly.

    :return: None
    """
    subs_completed = True

    # Clearing the current content of the To-Do List
    todo_list.delete(*todo_list.get_children())

    for task in tasks_list:
        if task['done'] == 'yes':
            added_task = todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='good')
        elif task['done'] == 'fail':
            added_task = todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='bad')
        else:
            added_task = todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='')

        # Checking if the task has subtasks
        if task['subtasks']:
            for subtask in task['subtasks']:
                if subtask['done'] == 'yes':
                    todo_list.insert(added_task, tk.END, values=(subtask['name']), tags='good')
                else:
                    todo_list.insert(added_task, tk.END, values=(subtask['name']), tags='')
                    subs_completed = False

            # Marking the main task as completed or uncompleted according to subtasks
            if subs_completed and task['done'] == 'no':
                task['done'] = 'yes'
                fill_todo()
            if not subs_completed and task['done'] == 'yes':
                task['done'] = 'no'
                fill_todo()


def logs_switch():
    """
    Switch logs on/off
    Get var from settings menu
    """
    settings['logs'] = log_var.get()
    save_settings(settings)


def get_help():
    help_text = ("Enter task name and deadline and press \"Add\" to add a new task.\n\n"
                 "Deadline should be in days.\n"
                 "Task can be entered without deadline.\n"
                 "Deadline can be adjusted later.\n"
                 "Right click on added task to open menu.\n"
                 "You can use \"Mark\" button or command to mark task as completed or uncompleted.\n")
    messagebox.showinfo("Help", help_text, icon=None)


# Main window
main_app = tk.Tk()
main_app.title('ToDo List')
main_app.minsize(width=400, height=400)
log_var = tk.BooleanVar()
log_var.set(settings['logs'])
# Menu
main_app_menu = tk.Menu(main_app)
# File
file_menu = tk.Menu(main_app_menu, tearoff=0)
file_menu.add_command(label='New base', command=new_base)
file_menu.add_command(label="Open base", command=open_base)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=main_app.destroy)
main_app_menu.add_cascade(label='File', menu=file_menu)
# Settings
set_menu = tk.Menu(main_app_menu, tearoff=0)
set_menu.add_checkbutton(label='Logging', variable=log_var, command=logs_switch)
main_app_menu.add_cascade(label='Settings', menu=set_menu)
# Help
help_menu = tk.Menu(main_app_menu, tearoff=0)
help_menu.add_command(label='Help', command=get_help)
main_app_menu.add_cascade(label='Help', menu=help_menu)
# List window
todo_list = ttk.Treeview(main_app, columns=('Task', 'Deadline'))
todo_list.heading('Task', text='Task')
todo_list.heading('Deadline', text='Deadline')
todo_list.column("#0", width=30, stretch=tk.NO)
todo_list.column("#2", width=100, stretch=tk.NO)
todo_list.grid(row=0, column=0, sticky='nsew', columnspan=3)
todo_list.tag_configure('good', background='lightgreen', foreground='blue')
todo_list.tag_configure('bad', background='pink', foreground='red')

# Input labels
input_label = ttk.Label(main_app, text='Enter task name:')
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
context_menu.add_command(label='Mark', command=mark_unmark)
context_menu.add_command(label='Edit name', command=edit_name)
context_menu.add_command(label='Edit deadline', command=edit_deadline)
context_menu.add_command(label='Add subtask', command=add_subtask)
context_menu.add_command(label='Remove', command=remove_task)

main_app.columnconfigure(0, weight=1)
main_app.rowconfigure(0, weight=1)

# Events
todo_list.bind(RMB, show_context_menu)
# Set items color
fill_todo()
main_app.config(menu=main_app_menu)
main_app.mainloop()
