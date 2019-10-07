#py7 backed up

from tkinter import *
import datetime
import math

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
        x, y = widget._pos_before_drag
        widget.place(x=x, y=y)    

def on_drag_start(event):
    widget = event.widget
    widget._drag_start_x = event.x
    widget._drag_start_y = event.y
    widget._pos_before_drag = widget.winfo_x(), widget.winfo_y()


def on_drag_motion(event):
    t = datetime.datetime.now()
    #print('on_drag_motion {} {}'.format(t.minute, t.second))
    widget = event.widget
    x = widget.winfo_x() - widget._drag_start_x + event.x
    y = widget.winfo_y() - widget._drag_start_y + event.y
    widget.place(x=x, y=y)
    #global main
    #main.update()

root = Tk()
root.geometry("800x600")

main = Canvas(root, width=200, height=200)
main.pack(fill="both", expand=True)

#main = Tk()


filename = "/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/king_diamonds.png"
image = PhotoImage(file=filename)

frame1 = Label(main, text="hello", bg="blue")
frame1.place(x=20, y=20, height=95, width=75)

def almost_reached(a, b, c, d):
    return math.sqrt((a-c)**2+(b-d)**2)<2

def animate(obj_id, x1, y1, frame3_arr_of_arrs):
    canvas = main
    #canvas.move(obj_id, 1, 50)
    #x1, y1 = 96, 160 

    x0, y0 = canvas.coords(obj_id)
    canvas.update()
    for cur_label_stack in frame3_arr_of_arrs:
        print('len of cur label stack: {}'.format(len(cur_label_stack)))
    
    canvas.tag_raise(obj_id)
        #for i in range(len(cur_label_stack)-1):
        #    cur_label.lower(cur_label_stack[i+1])
        #cur_label_stack[-1].lower(canvas)
    #canvas.lift()
    if almost_reached(x0, y0, x1, y1):
        print('returning')
        return
    canvas.coords(obj_id, x0+(x1-x0)/10, y0+(y1-y0)/10)
    #if y0 > canvas.winfo_height():
    #    canvas.coords(obj_id, 50,-50, 100, 0)
    canvas.after(100, animate, obj_id, x1, y1, frame3_arr_of_arrs)

def on_click(event, frame3_arr_of_arrs):
    for cur_label_stack in frame3_arr_of_arrs:
        obj = main.create_image( (20,20), anchor=NW, image=image)
        x, y = cur_label_stack[-1].winfo_x(), cur_label_stack[-1].winfo_y()+30
        animate(obj, x, y, frame3_arr_of_arrs)
    print('foo')

frame2_arr = []
for i in range(6):
    cur_label = Label(main, text="hello2", bg="green")
    cur_label.place(x=i*76+120, y=20, height=95, width=75)
    frame2_arr.append(cur_label)

frame3_arr_of_arrs = []
for i in range(10):
    cur_label_stack = []
    for j in range(2):
        cur_label = Label(main, image=image, borderwidth=2)
        cur_label.place(x=i*76+20, y=160+j*30, height=95, width=75)
        make_draggable(cur_label)
        cur_label_stack.append(cur_label)
    frame3_arr_of_arrs.append(cur_label_stack)

frame1.bind("<Button-1>", lambda event, frame_arr_of_arrs = frame3_arr_of_arrs: on_click(event, frame3_arr_of_arrs))
root.mainloop()

'''
20 160
96 160
'''