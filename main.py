import tkinter as tk
from tkinter import ttk, filedialog  # , simpledialog
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


# Mark button
def mark_unmark():
    selected_item = todo_list.selection()
    if selected_item:
        ind = (todo_list.index(selected_item))
        if tasks_list[ind]['done'] == 'yes':
            todo_list.item(selected_item, tags=('',))
            tasks_list[ind]['done'] = 'no'
        else:
            todo_list.item(selected_item, tags=('good',))
            tasks_list[ind]['done'] = 'yes'
        tasks_work.save(tasks_list)


def new_base():
    global tasks_list, tasks_work
    new_base_dialog = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("JSON", "*.json")])
    settings['base'] = new_base_dialog
    save_settings(settings)
    tasks_work = FileWork(settings['base'])
    tasks_work.clear_base()
    tasks_list = tasks_work.get_all()
    fill_todo()


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
        context_menu.post(event.x_root + 30, event.y_root)


def fill_todo():
    todo_list.delete(*todo_list.get_children())
    for task in tasks_list:
        if task['done'] == 'yes':
            todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='good')
        elif task['done'] == 'fail':
            todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='bad')
        else:
            todo_list.insert('', tk.END, values=(task['name'], task['deadline']), tags='')


# Main window
main_app = tk.Tk()
main_app.title('ToDo List')
# Menu
main_app_menu = tk.Menu(main_app)
# File
file_menu = tk.Menu(main_app_menu, tearoff=0)
file_menu.add_command(label='New Base', command=new_base)
file_menu.add_command(label="Open base", command=open_base)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=main_app.destroy)
main_app_menu.add_cascade(label='File', menu=file_menu)

# List window
todo_list = ttk.Treeview(main_app, columns=('Task', 'Deadline'), show='headings')
todo_list.heading('Task', text='Task')
todo_list.heading('Deadline', text='Deadline')
todo_list.column("#0", width=0, stretch=tk.NO)
todo_list.column("#2", width=100, stretch=tk.NO)
todo_list.grid(row=0, column=0, sticky='nsew', columnspan=3)
todo_list.tag_configure('good', background='lightgreen', foreground='blue')
todo_list.tag_configure('bad', background='pink', foreground='red')

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
context_menu.add_command(label='Edit name', command=mark_unmark)
context_menu.add_command(label='Edit deadline', command=mark_unmark)

context_menu.add_command(label='Remove', command=remove_task)

main_app.columnconfigure(0, weight=1)
main_app.rowconfigure(0, weight=1)

# Events
todo_list.bind(RMB, show_context_menu)
# Set items color
fill_todo()
main_app.config(menu=main_app_menu)
main_app.mainloop()
