from tkinter import *
#from tkinter.ttk import *
import datetime

def make_draggable(widget):
    widget.bind("<Button-1>", on_drag_start)
    widget.bind("<B1-Motion>", on_drag_motion)
    widget.bind("<ButtonRelease-1>", on_drop)

droppable = FALSE

def on_drop(event):
    global droppable
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    if droppable:
        pass
    else:
        widget.place(x=widget._drag_start_x, y=widget._drag_start_y)    

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y

def on_drag_motion(event):
    t = datetime.datetime.now()
    #print('on_drag_motion {} {}'.format(t.minute, t.second))
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)

main = Tk()
main.geometry("800x600")

filename = "/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/king_diamonds.png"
image = PhotoImage(file=filename)

frame1 = Label(main, bg="blue", text="hello")

frame2_arr = []
for i in range(6):
    cur_frame = Label(main, bg="blue")
    cur_frame.pack()
    cur_label = Label(main)
    #make_draggable(cur_label)
    cur_label.place(in_=cur_frame)
    frame2_arr.append(cur_label)

frame3_arr = []
for i in range(10):
    cur_frame = Label(main, bg="green")
    cur_frame.pack()
    cur_label = Label(main, image=image)
    #make_draggable(cur_label)
    cur_label.place(in_=cur_frame)
    frame3_arr.append(cur_label)

main.mainloop()