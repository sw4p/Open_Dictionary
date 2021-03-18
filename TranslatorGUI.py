import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2

class Translator_GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("Translator")
        self.window.rowconfigure([0, 1], weight=1, minsize=50)
        self.window.columnconfigure(0, weight=1, minsize=50)

        # The frame where the detected word will be displayed
        self.frm_word = tk.Frame(master=self.window, borderwidth=1)
        self.frm_word.grid(row=0, column=0, padx=5, pady=5)

        lbl_fixedWord = tk.Label(master=self.frm_word, text="Word = ")
        lbl_fixedWord.grid(row=0, column=0, sticky='w')

        self.lbl_word = tk.Label(master=self.frm_word, text="Getting Started now")
        self.lbl_word.grid(row=0, column=1, sticky='w')

        # The frame where meaning of the word will be displayed
        self.frm_meaning = tk.Frame(master=self.window, borderwidth=1)
        self.frm_meaning.grid(row=1, column=0, padx=5, pady=5)

        lbl_fixedMeaning = tk.Label(master=self.frm_meaning, text="Meaning = ")
        lbl_fixedMeaning.grid(row=0, column=0, sticky='w')

        self.lbl_meaning = tk.Label(master=self.frm_meaning, text="Getting Started now")
        self.lbl_meaning.grid(row=0, column=1, sticky='w')
        
        self.window.update()

    def update(self, word, noun, verb, adjective):
        self.lbl_word["text"] = word
        self.lbl_meaning["text"] = noun
        self.window.update()

