import tkinter as tk
# try code palang po from the link galing ang code 

running = False 
hours, minutes, seconds = 0, 0, 0

def start():
    global running
    if not running:
        # update() - not defined so hashtag muna  
        running = True