import tkinter as tk
import players
import const

class NewGameDialog:
    def __init__(self):
        self.master = tk.Toplevel()
        self.master.title("Promotion")
        self.master.resizable(False, False)
        
        #self.manager = manager
        
        self.result = [ players.Human, players.Human]
        
        self.label_head_white = tk.Label(self.master, text="White")
        self.label_head_white.grid(row= 0, column= 0)
        self.label_head_black = tk.Label(self.master, text="Black")
        self.label_head_black.grid(row= 0, column= 1)
        
        self.class_options = ["Human", "Com"]
        
        self.white_class = tk.StringVar(self.master)
        self.white_class.set(self.class_options[0])
        self.black_class = tk.StringVar(self.master)
        self.black_class.set(self.class_options[0])
        
        self.optionmenu_class_white = tk.OptionMenu(self.master, self.white_class, *self.class_options)
        self.optionmenu_class_white.grid(row=1, column=0)
        self.optionmenu_class_black = tk.OptionMenu(self.master, self.black_class, *self.class_options)
        self.optionmenu_class_black.grid(row=1, column=1)
        
        self.but_finish = tk.Button(self.master, text="Create", command= self.callback)
        self.but_finish.grid( row= 2, columnspan=2, sticky=tk.W+tk.E )
        
        self.master.grab_set()
        self.master.focus()
        self.master.wait_window(self.master)
        
    def callback(self):
        if(self.white_class.get() == "Human"):
            self.result[const.WHITE]= players.Human
        elif(self.white_class.get() == "Com"):
            self.result[const.WHITE]= players.AI
            
        if(self.black_class.get() == "Human"):
            self.result[const.BLACK]= players.Human
        elif(self.black_class.get() == "Com"):
            self.result[const.BLACK]= players.AI
        
        
        self.master.destroy()