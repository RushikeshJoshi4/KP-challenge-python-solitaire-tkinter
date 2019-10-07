from tkinter import *
import datetime
import math
import enum
import numpy as np
import random
import time

from PIL import Image
from PIL import ImageTk

droppable = FALSE

class Suit(enum.Enum):
    SPADES = 1
    HEARTS = 2
    CLUBS = 3
    DIAMONDS = 4

no_of_ranks = 13

class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def set_canvas(self, canvas):
        self.canvas = canvas

    def set_tag_id(self, tag_id):
        self.tag_id = tag_id

class Stack:
    def __init__(self, cards, no_of_hidden_cards):
        self.cards = cards
        self.no_of_hidden_cards = no_of_hidden_cards

class DrawCardManager:
    def __init__(self, total_no_of_full_sequences):
        self.total_no_of_full_sequences = total_no_of_full_sequences
        self.all_cards = []
        self.cards_used = []
        self.all_cards_random_perm = []
        self.index_into_all_cards_random_perm = 0
        self.no_of_full_sequences_completed_by_user = 0
        #draw_initial_cards(no_of_initial_cards)

    def draw_initial_cards(self, no_of_initial_cards):
        # Initialize all cards
        global no_of_ranks
        for rank in range(1, no_of_ranks+1):
            for suit in Suit:
                self.all_cards.append(Card(rank, suit))

        # Initialize cards_used
        self.all_cards_random_perm = np.random.permutation(self.all_cards)
        self.index_into_all_cards_random_perm = no_of_initial_cards
        return self.all_cards_random_perm[:no_of_initial_cards]


    def getNextRandomCards(self, no_of_cards):
        ret = []
        ret = self.all_cards_random_perm[self.index_into_all_cards_random_perm:self.index_into_all_cards_random_perm+no_of_cards]
        self.index_into_all_cards_random_perm += no_of_cards
        return ret        

all_cards_file_path = '/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/'
hidden_card_file_name = 'card_back.jpg'

correction = {
    1:'ace',
    11:'jack',
    12:'queen',
    13:'king'
}

def on_drop(event, obj_id, canvas):
    global droppable, d
    #canvas = canvas
    x, y = canvas.coords(obj_id)
    if droppable:
        pass
    else:
        x, y = d[obj_id]
        canvas.coords(obj_id, x, y)

d = {}
def on_drag_start(event, obj_id, canvas):
    global d
    #canvas = canvas
    x,y = canvas.coords(obj_id)
    d[obj_id] = (x, y)
    

def on_drag_motion(event, obj_id, canvas):
    global d
    canvas = canvas
    x,y = canvas.coords(obj_id)
    x2, y2 = event.x, event.y
    canvas.coords(obj_id, x2, y2)
    canvas.tag_raise(obj_id)
    

def get_card_file_name(card):
    global all_cards_file_path
    #print('Called get_card_file_name for card: {}, {}'.format(card.rank, card.suit.name))
    rank, suit = card.rank, card.suit
    if(rank==1 or rank>10): rank = correction[rank]
    rank = str(rank)
    suit_string = suit.name.lower()
    ret = all_cards_file_path+rank+'_'+suit_string+'.png'
    #print('returning : {}'.format(ret))
    return ret

def make_draggable(obj_id, canvas):
    canvas.tag_bind(obj_id, "<Button-1>", lambda event: on_drag_start(event, obj_id, canvas))
    canvas.tag_bind(obj_id, "<B1-Motion>", lambda event: on_drag_motion(event, obj_id, canvas))
    canvas.tag_bind(obj_id, "<ButtonRelease-1>", lambda event: on_drop(event, obj_id, canvas))



width, height = 75, 95
def get_preprocessed_image(card=None):
    global all_cards_file_path, hidden_card_file_name, width, height
    if card==None:
        filename = all_cards_file_path+hidden_card_file_name
    else:
        filename = get_card_file_name(card)
    img = Image.open(filename)
    img = img.resize((width,height), Image.ANTIALIAS)
    image =  ImageTk.PhotoImage(img)
    return image
    
padx, pady = 5, 10
x0 = 20; y0 = 20
shown_ht = 20

#def create_canvas_objs_for_stack(stack, i, canvas):
    
def main():
    global width, height, padx, pady, shown_ht, canvas
    root = Tk()
    root.geometry("800x600")

    canvas = Canvas(root, width=800, height=600)
    canvas.pack(fill="both", expand=True)
    
    stacks = []
    no_of_stacks = 10
    hidden, visible = 0, 0
    total_no_of_full_sequences = 6
    hidden_arr, visible_arr = [], []
    initial_no_cards = 0
    for i in range(no_of_stacks):
        hidden = random.randrange(1,3)
        visible = random.randrange(1,3)
        initial_no_cards += (hidden+visible)
        hidden_arr.append(hidden); visible_arr.append(visible)

    drawCardManager = DrawCardManager(total_no_of_full_sequences)
    initial_cards = drawCardManager.draw_initial_cards(initial_no_cards)
    initial_cards_i = 0
    for i in range(no_of_stacks):
        hidden = hidden_arr[i]; visible = visible_arr[i]
        cards = initial_cards[initial_cards_i:initial_cards_i+hidden+visible]
        stack = Stack(cards, hidden)
        stacks.append(stack)

    dummy_arr = []; dummy_img_arr = []

    for i, stack in enumerate(stacks):
        for j, card in enumerate(stack.cards):
            
            filename = "/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/king_diamonds.png"
            img = Image.open(filename)
            img = img.resize((width,height), Image.ANTIALIAS)
            image =  ImageTk.PhotoImage(img)

            #if j<stack.no_of_hidden_cards:
            #    image = get_preprocessed_image()
            #else:
            #    image = get_preprocessed_image(card)
            #print('got an image: {}'.format(image==None))
            #x=i*(width+padx)+x0; y=y0+j*shown_ht+height+2*pady
            x=i*80+20; y=160+j*20

            #print('creating obj with x,y: {}, {} for card: {}, {}'.format(x,y, card.rank, card.suit.name))
            obj_id = canvas.create_image( (x, y), anchor=NW, image=image)
            #time.sleep(0.5)
            make_draggable(obj_id, canvas)
            dummy_img_arr.append(image)
            #canvas.update()
            dummy_arr.append(obj_id)
            #canvas.tag_raise(obj_id)
            card.tag_id = obj_id
            card.canvas = canvas
            #print('created an obj with id: {}'.format(obj_id))

    z= dummy_arr
    for zz in z:
        x, y = canvas.coords(zz)
        print('obj_id: {}, coords: {}, {}'.format(zz, x, y))

    root.mainloop()

main()


'''
filename = "/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/king_diamonds.png"
img = Image.open(filename)
img = img.resize((width,height), Image.ANTIALIAS)
image =  ImageTk.PhotoImage(img)

frame1 = Label(canvas, text="hello", bg="blue")
frame1.place(x=20, y=20, height=95, width=75)

def almost_reached(a, b, c, d):
    return math.sqrt((a-c)**2+(b-d)**2)<2

def animate(obj_id, x1, y1, frame3_arr_of_arrs):
    canvas = canvas
    x0, y0 = canvas.coords(obj_id)
    
    if almost_reached(x0, y0, x1, y1):
        return
    canvas.tag_raise(obj_id)
    canvas.coords(obj_id, x0+(x1-x0)/10, y0+(y1-y0)/10)
    canvas.after(10, animate, obj_id, x1, y1, frame3_arr_of_arrs)

def on_click(event, frame3_arr_of_arrs):
    for cur_label_stack in frame3_arr_of_arrs:
        obj = canvas.create_image( (20,20), anchor=NW, image=image)
        #print(cur_label_stack[-1])
        x, y = canvas.coords(cur_label_stack[-1])
        y+=20
        animate(obj, x, y, frame3_arr_of_arrs)

frame2_arr = []
for i in range(6):
    cur_label = Label(canvas, text="hello2", bg="green")
    cur_label.place(x=i*76+120, y=20, height=95, width=75)
    frame2_arr.append(cur_label)

frame3_arr_of_arrs = []
for i in range(10):
    cur_label_stack = []
    for j in range(2):
        x=i*80+20; y=160+j*20
        obj = canvas.create_image( (x, y), anchor=NW, image=image)
        make_draggable(obj)
        cur_label_stack.append(obj)
    frame3_arr_of_arrs.append(cur_label_stack)

#frame1.bind("<Button-1>", lambda event, frame_arr_of_arrs = frame3_arr_of_arrs: on_click(event, frame3_arr_of_arrs))
#root.mainloop()
'''