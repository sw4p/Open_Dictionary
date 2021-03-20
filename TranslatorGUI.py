import tkinter as tk
from PIL import Image
from PIL import ImageTk
import cv2

class Translator_GUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_title("Translator")
        self.window.rowconfigure([0, 1, 2, 3], weight=1, minsize=50)
        self.window.columnconfigure(0, weight=1, minsize=50)

        # The frame where the detected word will be displayed
        self.frm_word = tk.Frame(master=self.window, borderwidth=1)
        self.frm_word.grid(row=0, column=0, padx=5, pady=5)

        lbl_fixedWord = tk.Label(master=self.frm_word, text="Word: ")
        lbl_fixedWord.grid(row=0, column=0, sticky='W')

        self.lbl_word = tk.Label(master=self.frm_word, text="Getting Started now")
        self.lbl_word.grid(row=0, column=1, sticky='W')

        # The frame where meaning(noun) of the word will be displayed
        self.frm_noun = tk.Frame(master=self.window, borderwidth=1)
        self.frm_noun.grid(row=1, column=0, padx=5, pady=5)

        lbl_fixedNoun = tk.Label(master=self.frm_noun, text="Noun: ")
        lbl_fixedNoun.grid(row=0, column=0, sticky='W')

        self.lbl_noun = tk.Label(master=self.frm_noun, text="Getting Started now")
        self.lbl_noun.grid(row=0, column=1, sticky='W')

        # The frame where meaning(verb) of the word will be displayed
        self.frm_verb = tk.Frame(master=self.window, borderwidth=1)
        self.frm_verb.grid(row=2, column=0, padx=5, pady=5)

        lbl_fixedVerb = tk.Label(master=self.frm_verb, text="Verb: ")
        lbl_fixedVerb.grid(row=0, column=0, sticky='W')

        self.lbl_verb = tk.Label(master=self.frm_verb, text="Getting Started now")
        self.lbl_verb.grid(row=0, column=1, sticky='W')

        # The frame where meaning(adjective) of the word will be displayed
        self.frm_adj = tk.Frame(master=self.window, borderwidth=1)
        self.frm_adj.grid(row=3, column=0, padx=5, pady=5)

        lbl_fixedAdj = tk.Label(master=self.frm_adj, text="Adjective: ")
        lbl_fixedAdj.grid(row=0, column=0, sticky='W')

        self.lbl_adj = tk.Label(master=self.frm_adj, text="Getting Started now")
        self.lbl_adj.grid(row=0, column=1, sticky='W')
        
        self.window.update()

    def update(self, word, noun, verb, adjective):
        self.lbl_word["text"] = word
        self.lbl_noun["text"] = noun
        self.lbl_verb["text"] = verb
        self.lbl_adj["text"] = adjective
        self.window.update()

