import tkinter as tk
import display
import const

class Gui(tk.Frame):
    def __init__(self, manager):
        tk.Frame.__init__(self)
        self.pack( side= tk.LEFT, fill= tk.BOTH, expand= True)
        
        self.manager = manager
        
        self.menubar = tk.Menu(self)
        
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label= "Open", command= self.manager.event_menu_file_open)
        self.filemenu.add_command(label= "Save", command= self.manager.event_menu_file_save)
        self.filemenu.add_separator()
        self.filemenu.add_command(label= "Exit", command= self.manager.event_menu_file_exit)
        self.menubar.add_cascade(label= "File", menu= self.filemenu)
        
        self.gamemenu = tk.Menu(self.menubar, tearoff=0)
        self.gamemenu.add_command(label= "New", command= self.manager.event_menu_game_new)
        self.gamemenu.add_command(label= "Reset", command= self.manager.event_menu_game_reset)
        self.menubar.add_cascade(label= "Game", menu= self.gamemenu)
        
        self.master.config(menu= self.menubar)
        
        self.gameDisplay = display.GameDisplay(self, self.manager)
        self.gameDisplay.pack( side= tk.LEFT, fill=tk.BOTH, expand= True )
        
        optionFrame = tk.Frame( self )
        optionFrame.pack( side= tk.RIGHT, fill=tk.Y )
        
        self.stringvar_turn = tk.StringVar()
        self.stringvar_turn.set("WHITE")
        
        self.label_turn = tk.Label( optionFrame, textvariable=self.stringvar_turn, bg= "white" )
        self.label_turn.pack(fill=tk.X)
        
        self.history_frame = tk.Frame( optionFrame, bd= 2, relief=tk.SUNKEN )
        self.history_frame.pack()
        
        self.history_sb = tk.Scrollbar( self.history_frame )
        self.history_sb.pack( side= tk.RIGHT, fill= tk.Y)
        
        self.history_lb = tk.Listbox( self.history_frame, bd= 0, yscrollcommand= self.history_sb.set )
        self.history_lb.pack()
        
        self.history_lb.bind('<<ListboxSelect>>', self.onselect)
        self.history_lb.bind("<ButtonRelease-1>", self.fixHistoryActiveItem)
        self.history_sb.config( command= self.history_lb.yview )
        
        self.but_undo = tk.Button( optionFrame, text= "Undo", command= self.manager.event_but_undo )
        self.but_undo.pack(fill= tk.X)
        
        self.but_claimdraw = tk.Button( optionFrame, text= "Claim Draw", state= tk.DISABLED, command= self.manager.event_but_claimdraw )
        self.but_claimdraw.pack(fill= tk.X)
        
    def fixHistoryActiveItem(self, event):
        self.history_lb.activate( self.history_lb.curselection()[0] )
        print( "foo")
        print(self.history_lb.curselection()[0])
        
    def updateLabelTurn(self, player):
        self.stringvar_turn.set(const.PLAYER_COLOR[player].upper())
        self.label_turn.config(bg=const.PLAYER_COLOR[player],fg=const.PLAYER_COLOR[not player])

    def onselect(self, var):
        self.manager.event_history_onselect( self.history_lb.curselection()[0] )
        
    def setHistoryFocus(self, i=tk.END):
        self.history_lb.select_set(i, i)
        self.history_lb.activate(i)
        self.history_lb.yview(i )
        
    def disableButClaimDraw(self):
        self.but_claimdraw.config(state= tk.DISABLED)

    def enableButClaimDraw(self):
        self.but_claimdraw.config(state= tk.NORMAL)
    
    def addToHistory(self, line):
        self.history_lb.insert(tk.END, line)
    
    def removeFromHistory(self, i= tk.END):
        self.history_lb.delete(i)