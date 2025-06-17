import tkinter as tk
import random
import pygame
import threading

# Initialize audio
pygame.mixer.init()
MOVE_S = pygame.mixer.Sound("mouse_move.wav")
WIN_S = pygame.mixer.Sound("win_cheese.wav")
LOSE_S = pygame.mixer.Sound("game_over_cat.wav")

ROWS, COLS = 6, 8
CELL = 60
W, H = COLS * CELL, ROWS * CELL

root = tk.Tk()
root.title("Mouse Escape!")  # ✅ Set window title
root.attributes("-topmost", True)
root.geometry(f"{W}x{H}+1200+80")
root.resizable(True, True )  # ✅ Make window non-resizable

c = tk.Canvas(root, width=W, height=H, highlightthickness=0)
c.pack()

CUTE_FONT = ("Comic Sans MS", 16, "bold")
mouse = [0, 0]
cheese = [0, 0]
cats = []
blink = True
game = False
mouse_item = bow = None
message_text = None
start_button = None

def play(sound):
    threading.Thread(target=lambda: sound.play()).start()

def reset():
    global mouse, cheese, cats, message_text, start_button
    if message_text:
        c.delete(message_text)
    if start_button:
        start_button.destroy()
    mouse = [0, 0]
    cheese = [random.randrange(ROWS), random.randrange(COLS)]
    cats = []
    for _ in range(3):
        pos = cheese
        while pos == cheese or pos == mouse or pos in cats:
            pos = [random.randrange(ROWS), random.randrange(COLS)]
        cats.append(pos)
    draw()

def draw():
    c.delete("all")
    for r in range(ROWS):
        for col in range(COLS):
            c.create_rectangle(col*CELL, r*CELL,
                               (col+1)*CELL, (r+1)*CELL,
                               fill="#fce4ec", outline="white")
    c.create_text(cheese[1]*CELL + CELL//2,
                  cheese[0]*CELL + CELL//2,
                  text="🧀", font=("Arial", 24))
    for cat in cats:
        c.create_text(cat[1]*CELL + CELL//2,
                      cat[0]*CELL + CELL//2,
                      text="🐱", font=("Arial", 24))
    draw_mouse()

def draw_mouse():
    global mouse_item, bow
    if mouse_item:
        c.delete(mouse_item)
    if bow:
        c.delete(bow)
    x = mouse[1]*CELL + CELL//2
    y = mouse[0]*CELL + CELL//2
    mouse_item = c.create_text(x, y, text="🐭", font=("Arial", 28))
    bow = c.create_text(x, y-20, text="🎀", font=("Arial", 16))

def blink_anim():
    global blink
    if not game: return
    blink = not blink
    c.itemconfigure(mouse_item, text="🐭" if blink else "")
    c.itemconfigure(bow, text="🎀" if blink else "")
    root.after(500, blink_anim)

def move_cats():
    if not game: return
    for idx, pos in enumerate(cats):
        for _ in range(4):
            dr, dc = random.choice([(0,1),(0,-1),(1,0),(-1,0)])
            nr, nc = pos[0]+dr, pos[1]+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and [nr,nc] not in cats \
               and [nr,nc] != mouse and [nr,nc] != cheese:
                cats[idx] = [nr, nc]
                break
    draw()
    root.after(1000, move_cats)

def keypress(e):
    global game
    if not game: return
    d = {"Up":(-1,0),"Down":(1,0),"Left":(0,-1),"Right":(0,1)}
    if e.keysym in d:
        play(MOVE_S)
        mouse[0] += d[e.keysym][0]
        mouse[1] += d[e.keysym][1]
        mouse[0] = max(0, min(ROWS-1, mouse[0]))
        mouse[1] = max(0, min(COLS-1, mouse[1]))
        draw()
        check()

def check():
    global game, message_text, start_button
    if mouse == cheese:
        game = False
        play(WIN_S)
        message_text = c.create_text(W//2, H//2-30, text="🎉 You Win!", font=CUTE_FONT, fill="deeppink")
        start_button = tk.Button(root, text="Play Again", font=CUTE_FONT, command=start)
        start_button.place(x=W//2-60, y=H//2+10)
    elif mouse in cats:
        game = False
        play(LOSE_S)
        message_text = c.create_text(W//2, H//2-30, text="💥 Caught by 🐱", font=CUTE_FONT, fill="red")
        start_button = tk.Button(root, text="Play Again", font=CUTE_FONT, command=start)
        start_button.place(x=W//2-60, y=H//2+10)

def start():
    global game
    game = True
    reset()
    blink_anim()
    move_cats()
    root.focus_force()

def welcome():
    global start_button
    c.delete("all")
    c.create_rectangle(0,0,W,H, fill="#ffe6f0")
    c.create_text(W//2, H//3, text="🐭🎀 Welcome!", font=CUTE_FONT)
    start_button = tk.Button(root, text="Start", font=CUTE_FONT, command=start)
    start_button.place(x=W//2-40, y=H//2)

root.bind("<Key>", keypress)
welcome()
root.mainloop()
