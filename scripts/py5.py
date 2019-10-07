from tkinter import *

class DragManager():
    def add_dragable(self, widget):
        widget.bind("<ButtonPress-1>", self.on_start)
        widget.bind("<B1-Motion>", self.on_drag)
        widget.bind("<ButtonRelease-1>", self.on_drop)
        widget.configure(cursor="hand1")

    def on_start(self, event):
        # you could use this method to create a floating window
        # that represents what is being dragged.
        #x=
        #event.widget.place(x=, y=, in_=root)
        pass

    def on_drag(self, event):
        # you could use this method to move a floating window that
        # represents what you're dragging
        x, y = event.x_root, event.y_root
        #event.widget.place(x=x, y=y, in_=root)
        #pass

    def on_drop(self, event):
        # find the widget under the cursor
        x,y = event.widget.winfo_pointerxy()
        target = event.widget.winfo_containing(x,y)
        try:
            target.configure(image=event.widget.cget("image"))
        except:
            pass

root = Tk()
root.geometry("640x480")

canvas = Canvas(root, height=480, width=640, bg="white")

frame = Frame(root, height=480, width=640, bg="white")
frame.propagate(0)

image = PhotoImage(file="/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/king_diamonds.png")

label = Label(canvas, image=image)
label.pack()

label_2 = Label(frame, text="Drop Here !")
label_2.pack()
label_2.place(x=200, y=225, anchor=CENTER)

canvas.pack(side=LEFT)
frame.pack()

dnd = DragManager()
dnd.add_dragable(label)

root.mainloop()

'''
root = Tk()
root.geometry("800x100")
label = Label(root, text="hello", height=500, width=50, bg='white')
label.pack(side=LEFT)

dnd = DragManager()
dnd.add_dragable(label)

root.mainloop()
'''