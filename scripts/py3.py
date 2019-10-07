import tkinter as tk
#from tkinter import dnd

root = tk.Tk()
root.title('Hey')
root.resizable(False, False)

a = tk.dnd(root, text='Hello')
b = tk.Button(root, text='Hello button')

tk.Label(root, text='label!').pack()
root.mainloop()