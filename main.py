from tkinter import *
import datetime
import math
import enum
import numpy as np
import random
import time
import tkinter.messagebox

np.random.seed(0)
random.seed(0)

from PIL import Image
from PIL import ImageTk

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
        self.tag_id = None
        self.canvas = None

    def set_canvas(self, canvas):
        self.canvas = canvas

    def set_tag_id(self, tag_id):
        self.tag_id = tag_id


dummy_arr_for_imgs = []
stacks_ = None
class Stack:
    def __init__(self, cards, no_of_hidden_cards):
        self.cards = cards
        self.no_of_hidden_cards = no_of_hidden_cards
        self.no_of_draggable_cards = 0
        self.init_no_of_draggable_cards() 

    def init_no_of_draggable_cards(self):
        global stacks_
        n = len(self.cards)
        if n==0: 
            self.no_of_draggable_cards = 0
            return
        flag = False
        for i in reversed(range(  n-1  )):
            print('ranks: {} {}'.format(self.cards[i].rank, self.cards[i+1].rank))
            if self.cards[i].rank != self.cards[i+1].rank+1:
                flag = True
                print('marking no_of_draggable_cards: ', n-(i+1))
                self.no_of_draggable_cards = n - (i+1)
                break
        if not flag: self.no_of_draggable_cards = n
        
        try:
            print('iterating from 0 to {} and setting them non-draggable'.format(n-self.no_of_draggable_cards))
            for i in range(n-self.no_of_draggable_cards):
                make_non_draggable(self.cards[i].tag_id)

            print('iterating from {} to {} and setting draggable'.format(n-self.no_of_draggable_cards, n))
            for i in range(n-self.no_of_draggable_cards, n):
                print('*')
                print('{}, {}'.format(self.cards[i].tag_id, self.cards[i].canvas))
                print('&')
                make_draggable(self.cards[i].tag_id, self.cards[i].canvas, stacks_)
        except Exception as e:
            print(e)
            pass

    def remove_cards_from_stack_from_index(self, j):
        #j is the no_of_cards_to_be_removed
        ret = self.cards[-j:]
        for i in range(j): self.cards.pop()
        n = len(self.cards)
        global dummy_arr_for_imgs
        if n!=0 and n == self.no_of_hidden_cards:
            #print(n)
            card = self.cards[n-1]
            obj_id = card.tag_id
            image = get_preprocessed_image(card)
            dummy_arr_for_imgs.append(image)
            #print(image)
            canvas.itemconfig(obj_id, image = image)
            canvas.tag_raise(obj_id)
            #time.sleep(2)
            self.no_of_hidden_cards -= 1
            make_draggable(obj_id, canvas, stacks)
        self.init_no_of_draggable_cards()
        return ret

    def add_cards_to_stack(self, new_cards, i):
        n = len(self.cards)
        for idx, new_card in enumerate(new_cards):
            obj_id = new_card.tag_id
            j = n+idx
            print('updating for: rank: {} from {}, {} to {}, {}'.format(new_card.rank, d_obj_id_to_card[obj_id][0], d_obj_id_to_card[obj_id][1], i, j))
            d_obj_id_to_card[obj_id] = (i, j)
        
        self.cards.extend(new_cards)
        self.init_no_of_draggable_cards()

        

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
        self.all_cards_random_perm = list(np.random.permutation(self.all_cards))
        self.index_into_all_cards_random_perm = no_of_initial_cards
        #print(no_of_initial_cards)
        return self.all_cards_random_perm[:no_of_initial_cards]


    def getNextRandomCards(self, no_of_cards):
        if self.index_into_all_cards_random_perm+no_of_cards > self.total_no_of_full_sequences*13:
            tkinter.messagebox.showerror("Error", "No more cards!")
            return None
        ret = []
        ret = self.all_cards_random_perm[self.index_into_all_cards_random_perm:self.index_into_all_cards_random_perm+no_of_cards]
        self.index_into_all_cards_random_perm += no_of_cards
        return ret        

all_cards_file_path = 'images/'
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
    for arr_item in arr:
        
        #if arr_item in d_obj_id_to_card:
        #    if d_obj_id_to_card[arr_item][1] == -1: continue
        
        if obj_id == arr_item: continue
        
        x0, y0, x1, y1 = canvas.bbox(arr_item)
        if(x0<x and x<x1 and y0<y and y<y1):
            dist = math.sqrt((x-x0)**2+(y-y0)**2)
            if min_dist > dist:
                min_dist = dist
                min_id = arr_item
        
    return min_id

def get_obj_ids_of_all_subsequent_elements(obj_id ,stacks):
    i, j = d_obj_id_to_card[obj_id]
    n = len(stacks[i].cards)
    arr = []
    for j2 in range(j, n): arr.append(stacks[i].cards[j2].tag_id)
    return arr

frame2_arr, no_of_frame2_arr_items_done = None, None

def handle_stack_done(stack, canvas):
    global frame2_arr, no_of_frame2_arr_items_done
    
    try: x1, y1 = canvas.coords(frame2_arr[no_of_frame2_arr_items_done])
    except: x1, y1, _, _ = canvas.coords(frame2_arr[no_of_frame2_arr_items_done])

    for card in stack.cards:
        obj_id = card.tag_id
        animate(obj_id, x1, y1, canvas)
        canvas.tag_raise(obj_id)
    
    time.sleep(0.1)
    for card in stack.cards:
        obj_id = card.tag_id
        if card.rank==1: 
            make_non_draggable(obj_id)
            continue
        canvas.delete(obj_id)
    
    no_of_frame2_arr_items_done += 1
    if no_of_frame2_arr_items_done == 6:
        messagebox.showinfo("Congratulations","----You won!----")

def on_drop(event, obj_id, canvas, stacks):
    global d, d_obj_id_to_card
    obj_ids = get_obj_ids_of_all_subsequent_elements(obj_id, stacks)
    
    x, y = canvas.coords(obj_id)
    droppable = False
    ovlp_id_valid = False
    #decide whether overlap id is a valid id!
    #try:
    ovlp_id = my_find(canvas, obj_id)
    print('ovlp_id', ovlp_id)
    if d_obj_id_to_card.get(ovlp_id, None)!=None:
        ovlp_id_valid = True
    #except Exception as e:
    #    print(e)
    
    empty = False
    #Decide whether droppable
    if ovlp_id_valid:
        i, j = d_obj_id_to_card[ovlp_id]
        # Note: if stack is empty, then it is droppable:
        if j==-1: 
            droppable = True
            empty = True
        else:
            i1, j1 = d_obj_id_to_card[obj_id]
            card1 = stacks[i1].cards[j1]
            i, j = d_obj_id_to_card[ovlp_id]
            print('i, j: {}, {}'.format(i,j))
            card = stacks[i].cards[j]
            print('card_rank: ', card.rank)
            print('card1_rank', card1.rank)
            print('ovlp_id', ovlp_id)
            if i!=i1 or i1 == len(stacks[i1].cards)-1:
                if card.rank == card1.rank+1:
                    droppable = True
            else: droppable = False    
    
    if droppable:
        #start the dropping process
        #i, j = d_obj_id_to_card[ovlp_id]
        print(canvas.coords(ovlp_id))
        try: x, y = canvas.coords(ovlp_id)
        except: x, y, _, _ = canvas.coords(ovlp_id) 

        obj_id = None
        y_offset = None
        for idx, obj_id in enumerate(obj_ids):
            i_, j_ = d_obj_id_to_card[obj_id]
            y_offset = idx+1
            if empty: y_offset = idx
            canvas.coords(obj_id, x, y+y_offset*20)
        #i1, j1 = d_obj_id_to_card[obj_id]
        #print(stacks[i].cards[j].rank)
        no_of_cards_to_remove = len(obj_ids)
        i1, j1 = d_obj_id_to_card[obj_id]
        cards = stacks[i1].remove_cards_from_stack_from_index(no_of_cards_to_remove)
        stacks[i].add_cards_to_stack(cards, i)

        #Now if stack is done, full!, we will animate it to the next frame2 item and empty it
        if stacks[i].no_of_draggable_cards==13:
            handle_stack_done(stacks[i], canvas)
            stacks[i].remove_cards_from_stack_from_index(13)    
    else:
        #xy_arr = d[obj_id]
        for idx, obj_id in enumerate(obj_ids):
            x, y = d[obj_id]
            canvas.coords(obj_id, x, y)

d = {}
def on_drag_start(event, obj_id, canvas, stacks):
    global d
    obj_ids = get_obj_ids_of_all_subsequent_elements(obj_id, stacks)
    for obj_id in obj_ids:
        x, y = canvas.coords(obj_id)
        d[obj_id] = (x,y)
        #if obj_id not in d: d[obj_id] = []
        #d[obj_id].append((x, y))
    

def on_drag_motion(event, obj_id, canvas, stacks):
    global d
    obj_ids = get_obj_ids_of_all_subsequent_elements(obj_id, stacks)
    #print(len(obj_ids))
    for i, obj_id in enumerate(obj_ids):
        x,y = canvas.coords(obj_id)
        x2, y2 = event.x, event.y
        canvas.coords(obj_id, x2, y2+20*i)
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

def do_nothing(event):
    pass

def make_non_draggable(obj_id):
    canvas.tag_bind(obj_id, "<Button-1>", do_nothing)
    canvas.tag_bind(obj_id, "<B1-Motion>", do_nothing)
    canvas.tag_bind(obj_id, "<ButtonRelease-1>", do_nothing)

def make_draggable(obj_id, canvas, stacks):
    canvas.tag_bind(obj_id, "<Button-1>", lambda event: on_drag_start(event, obj_id, canvas, stacks))
    canvas.tag_bind(obj_id, "<B1-Motion>", lambda event: on_drag_motion(event, obj_id, canvas, stacks))
    canvas.tag_bind(obj_id, "<ButtonRelease-1>", lambda event: on_drop(event, obj_id, canvas, stacks))
  


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
    return math.sqrt((a-c)**2+(b-d)**2)<0.01

def animate(obj_id, x1, y1, canvas):
    try:
        x0, y0 = canvas.coords(obj_id)
    except: 
        return
    if almost_reached(x0, y0, x1, y1):
        return
    canvas.tag_raise(obj_id)
    canvas.coords(obj_id, x0+(x1-x0)/10, y0+(y1-y0)/10)
    canvas.after(10, animate, obj_id, x1, y1, canvas)

dummy_arr_for_imgs = []
def on_click(event, stacks, canvas, drawCardManager):
    
    for stack in stacks:
        if len(stack.cards) == 0:
            tkinter.messagebox.showerror("Error", "There can't be any empty stacks!")
            return

    cards = drawCardManager.getNextRandomCards(10)
    if cards is None: return
    
    images = []
    for card in cards:
        image = get_preprocessed_image(card)
        dummy_arr_for_imgs.append(image)
        images.append(image)
    
    for i, stack in enumerate(stacks):
        obj = canvas.create_image( (20,20), anchor=NW, image=images[i])
        n = len(stack.cards)
        d_obj_id_to_card[obj] = (i, n-1)
        cards[i].tag_id = obj
        cards[i].canvas = canvas
        tag_id = stack.cards[n-1].tag_id
        x, y = canvas.coords(tag_id)
        y+=20
        animate(obj, x, y, canvas)
        stack.add_cards_to_stack([cards[i]], i)
            
d_obj_id_to_card = None
def main():
    global width, height, padx, pady, shown_ht, canvas, stacks, d_obj_id_to_card, stacks_, frame2_arr, no_of_frame2_arr_items_done
    root = Tk()
    root.geometry("800x600")

    canvas = Canvas(root, width=800, height=600)
    canvas.config(bg = "green")
    canvas.pack(fill="both", expand=True)

    #create frame2_arr
    frame2_arr = []
    no_of_frame2_arr_items_done = 0
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
    for i in range(no_of_stacks):
        hidden = random.randrange(1,3)
        visible = random.randrange(1,3)
        initial_no_cards += (hidden+visible)
        hidden_arr.append(hidden); visible_arr.append(visible)
    stacks_ = stacks

    #create frame3
    drawCardManager = DrawCardManager(total_no_of_full_sequences)
    initial_cards = drawCardManager.draw_initial_cards(initial_no_cards)
    initial_cards_i = 0

    #remove this after testing
    hidden_arr[0] = 0; visible_arr[0] = 12
    cards = []
    for i in range(12):
        cards.append(Card(13-i, Suit.SPADES))
    stacks.append(Stack(cards, 0))

    for i in range(1, no_of_stacks):
        hidden = hidden_arr[i]; visible = visible_arr[i]
        cards = initial_cards[initial_cards_i:initial_cards_i+hidden+visible]
        initial_cards_i += (hidden + visible)
        stack = Stack(cards, hidden)
        stacks.append(stack)

    
    '''
    for i in range(no_of_stacks):
        hidden = hidden_arr[i]; visible = visible_arr[i]
        cards = initial_cards[initial_cards_i:initial_cards_i+hidden+visible]
        initial_cards_i += (hidden + visible)
        stack = Stack(cards, hidden)
        stacks.append(stack)
    '''
    dummy_arr = []; dummy_img_arr = []
    d_obj_id_to_card = {}

    for i, stack in enumerate(stacks):
        x=i*80+20; y=160
        empty_card_obj_id = canvas.create_rectangle(x, y, x+width, y+height, fill='pale green')
        d_obj_id_to_card[empty_card_obj_id] = (i, -1)
        for j, card in enumerate(stack.cards):
            if j<stack.no_of_hidden_cards:
                image = get_preprocessed_image()
            else:
                image = get_preprocessed_image(card)
            x=i*80+20; y=160+j*20

            obj_id = canvas.create_image( (x, y), anchor=NW, image=image)
            d_obj_id_to_card[obj_id] = (i, j)
            n = len(stack.cards)
            if j>=n-stack.no_of_draggable_cards: make_draggable(obj_id, canvas, stacks)
            dummy_img_arr.append(image)
            card.tag_id = obj_id
            card.canvas = canvas
            
    frame1_obj_id = canvas.create_rectangle(x0, y0, x0+width, y0+height, fill='pale green')
    canvas.tag_bind(frame1_obj_id, "<Button-1>", lambda event, canvas=canvas, stacks=stacks: on_click(event, stacks, canvas, drawCardManager))
    
    root.mainloop()

main()
