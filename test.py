import tkinter as tk
root = tk.Tk()
button = tk.Button(root, text="Red Button",bg="green", fg="green",command=lambda: root.destroy())
button.pack()
root.mainloop()