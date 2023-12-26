import tkinter as tk
from tkinter import ttk


# Add button
def add_task():
    if input_box:
        task_name = input_box.get()
        todo_list.insert('', tk.END, values=task_name)
        input_box.delete(0, tk.END)


def remove_task():
    selected_item = todo_list.selection()
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

input_box_dl = ttk.Entry(main_app,width=7)
input_box_dl.grid(row=2, column=0, sticky='nse')


add_button = ttk.Button(main_app, text='Add', command=add_task)
add_button.grid(row=3, column=0, sticky='w', padx=5, pady=5)

remove_button = ttk.Button(main_app, text='Remove',command=remove_task)
remove_button.grid(row=3, column=0, sticky='e', padx=5, pady=5)

main_app.columnconfigure(0, weight=1)
main_app.rowconfigure(0, weight=1)

main_app.mainloop()
