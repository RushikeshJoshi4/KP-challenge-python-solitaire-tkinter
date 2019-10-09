from tkinter import *
import datetime
import math
import enum
import numpy as np
import random
import time

np.random.seed(0)
random.seed(0)

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
        for i in range(self.total_no_of_full_sequences):
            for rank in range(1, no_of_ranks+1):
                for suit in [Suit.SPADES]:
                    self.all_cards.append(Card(rank, suit))

        #print(len(self.all_cards))
        # Initialize cards_used
        self.all_cards_random_perm = np.random.permutation(self.all_cards)
        self.index_into_all_cards_random_perm = no_of_initial_cards
        #print(no_of_initial_cards)
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

stacks = None

def my_find(canvas, obj_id):
    arr = canvas.find_all()
    x,y = canvas.coords(obj_id)
    min_dist = 1000000
    min_id = None
    #print('*')
    for arr_item in arr:
        #print(arr_item)
        if obj_id == arr_item: continue
        x0, y0, x1, y1 = canvas.bbox(arr_item)
        if(x0<x and x<x1 and y0<y and y<y1):
            #xm = (x0+x1)/2; ym = (y0+y1)/2
            dist = math.sqrt((x-x0)**2+(y-y0)**2)
            #print(dist)
            if min_dist > dist:
                min_dist = dist
                min_id = arr_item
    #print('&')
    #print("min_id: ", min_id)
    return min_id

def on_drop(event, obj_id, canvas):
    global droppable, d, stacks, d_obj_id_to_card
    #canvas = canvas
    x, y = canvas.coords(obj_id)
    droppable = False
    ovlp_id_valid = False
    try:
        ovlp_id = my_find(canvas, obj_id)
        print('ovlp_id', ovlp_id)
        if d_obj_id_to_card.get(ovlp_id, None)!=None:
            ovlp_id_valid = True
    except Exception as e:
        print('In Exception and marking droppable false')
        print(e)
        print('--------------------------------')
    
    if ovlp_id_valid:
        i1, j1 = d_obj_id_to_card[obj_id]
        card1 = stacks[i1].cards[j1]
        i, j = d_obj_id_to_card[ovlp_id]
        card = stacks[i].cards[j]
        print('card_rank: ', card.rank)
        print('card1_rank', card1.rank)
        print('ovlp_id', ovlp_id)
        if(card.rank == card1.rank+1): droppable = True
        else: droppable = False
        
    if droppable:
        i, j = d_obj_id_to_card[ovlp_id]
        print(stacks[i].cards[j].rank)
        print('canvas.coords: ', canvas.coords(stacks[i].cards[j].tag_id))
        x, y = canvas.coords(stacks[i].cards[j].tag_id) 
        canvas.coords(obj_id, x, y+20)
    
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

def almost_reached(a, b, c, d):
    return math.sqrt((a-c)**2+(b-d)**2)<2

def animate(obj_id, x1, y1, canvas):
    x0, y0 = canvas.coords(obj_id)
    
    if almost_reached(x0, y0, x1, y1):
        return
    canvas.tag_raise(obj_id)
    canvas.coords(obj_id, x0+(x1-x0)/10, y0+(y1-y0)/10)
    canvas.after(10, animate, obj_id, x1, y1, canvas)

dummy_arr_for_imgs = []
def on_click(event, stacks, canvas):
    #print('on_click')
    filename = "/home/rushikesh/Desktop/KP challenge pygame/Solitaire/playing_cards/king_diamonds.png"
    img = Image.open(filename)
    img = img.resize((width,height), Image.ANTIALIAS)
    image =  ImageTk.PhotoImage(img)
    dummy_arr_for_imgs.append(image)
    
    for i, stack in enumerate(stacks):
        #print(len(stack.cards))
        obj = canvas.create_image( (20,20), anchor=NW, image=image)
        #print(cur_label_stack[-1])
        tag_id = stack.cards[-1].tag_id
        #print('i: {} tag: {}'.format(i,tag_id))
        x, y = canvas.coords(tag_id)#canvas.coords(cur_label_stack[-1])
        y+=20
        #print('x, y: {}, {}'.format(x,y))
        animate(obj, x, y, canvas)
            
d_obj_id_to_card = None
def main():
    global width, height, padx, pady, shown_ht, canvas, stacks, d_obj_id_to_card
    root = Tk()
    root.geometry("800x600")

    canvas = Canvas(root, width=800, height=600)
    canvas.config(bg = "green")
    canvas.pack(fill="both", expand=True)

    #create frame2_arr
    frame2_arr = []
    for i in range(6):
        x1, y1 = x0+(i+2)*(width+padx), y0
        x2, y2 = x1+width, y1+height
        obj_id = canvas.create_rectangle(x1, y1, x2, y2, fill='pale green')
        frame2_arr.append(obj_id)

    stacks = []
    no_of_stacks = 10
    hidden, visible = 0, 0
    total_no_of_full_sequences = 6
    hidden_arr, visible_arr = [], []
    initial_no_cards = 0
    #print(no_of_stacks)
    for i in range(no_of_stacks):
        hidden = random.randrange(1,3)
        visible = random.randrange(1,3)
        initial_no_cards += (hidden+visible)
        hidden_arr.append(hidden); visible_arr.append(visible)

    #create frame3
    drawCardManager = DrawCardManager(total_no_of_full_sequences)
    initial_cards = drawCardManager.draw_initial_cards(initial_no_cards)
    initial_cards_i = 0
    for i in range(no_of_stacks):
        hidden = hidden_arr[i]; visible = visible_arr[i]
        cards = initial_cards[initial_cards_i:initial_cards_i+hidden+visible]
        initial_cards_i += (hidden + visible)
        stack = Stack(cards, hidden)
        stacks.append(stack)

    dummy_arr = []; dummy_img_arr = []
    d_obj_id_to_card = {}

    #print(len(stacks))
    for i, stack in enumerate(stacks):
        #print(i)
        for j, card in enumerate(stack.cards):
            #print(j)
            if j<stack.no_of_hidden_cards:
                image = get_preprocessed_image()
            else:
                image = get_preprocessed_image(card)
            x=i*80+20; y=160+j*20

            #print('creating obj with x,y: {}, {} for card: {}, {}'.format(x,y, card.rank, card.suit.name))
            #print(obj_id)
            obj_id = canvas.create_image( (x, y), anchor=NW, image=image)
            d_obj_id_to_card[obj_id] = (i, j)
            #time.sleep(0.5)
            make_draggable(obj_id, canvas)
            dummy_img_arr.append(image)
            #canvas.update()
            #canvas.tag_raise(obj_id)
            card.tag_id = obj_id
            card.canvas = canvas
            #print('created an obj with id: {}'.format(obj_id))

    #create frame1
    frame1_obj_id = canvas.create_rectangle(x0, y0, x0+width, y0+height, fill='pale green')
    canvas.tag_bind(frame1_obj_id, "<Button-1>", lambda event, canvas=canvas, stacks=stacks: on_click(event, stacks, canvas))
    
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