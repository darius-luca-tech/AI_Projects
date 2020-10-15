from tkinter import filedialog
from threading import Thread, active_count
import tkinter as tk
import pickle
import const
import gui
import chessgame
import newgamedialog
import players
import matrices as mat
import bitboards as bb
import bitops as bo
import copy

class Manager:
    def __init__(self, master):
        self.master = master
        self.game = chessgame.ChessGame()
        self.history = []   #the history which is shown in the listbox
        
        self.gui = gui.Gui(self)
        self.gui.gameDisplay.game = self.game
        
        self.players = [None, None]
        self.players[const.WHITE] = players.Human(self, const.WHITE)
        self.players[const.BLACK] = players.AI(self, const.BLACK)

        self.game.setBoard(mat.TESTBOARD)

        self.master.bind("<<turn_complete>>", self.turnComplete)

        
    def turnComplete(self, event):
        print("NOTE:", self.game.note)
        move = self.players[self.game.playerTurn].result
        if(move != None):
            self.players[self.game.playerTurn].result = None
            self.game.doMove(move)
            self.history = copy.deepcopy(self.game.history)
            self.update()
            self.gui.setHistoryFocus()
            print("MOVE DONE:", move)
        
        if(not type(self.players[self.game.playerTurn]) is players.Human):
            Thread(target= self.players[self.game.playerTurn].doMove, args= (copy.deepcopy(self.game),)).start()
            
            
    def event_chessboardClick(self, sq):
        print("ANZ THREADS", active_count())
        if(type(self.players[self.game.playerTurn]) is players.Human):
            self.players[self.game.playerTurn].processInput(self.game, sq)
        else:
            if(active_count() == 1):
                Thread(target= self.players[self.game.playerTurn].doMove, args= (copy.deepcopy(self.game),)).start()
        
        
    def update(self):
        self.gui.gameDisplay.update()
        self.gui.updateLabelTurn(self.game.playerTurn)
            
        self.updateHistoryList()
            
        if(self.game.note[2] >= 100):
            self.gui.enableButClaimDraw()
        else:
            self.gui.disableButClaimDraw()
            
        print("50-move:", self.game.note[2])
    
    def updateHistoryList(self):
        self.gui.history_lb.delete(0, tk.END)
        
        
        #move = self.game.history[-1][0]
        
        for history_note in self.history:
            move = history_note[0]
        
            sq_start = bo.getBits(move, *const.MOVE_START)
            sq_dest = bo.getBits(move, *const.MOVE_DEST)
            fig_start = bo.getBits(move, *const.MOVE_FIG_START)
            fig_cap = bo.getBits(move, *const.MOVE_FIG_CAPTURE)
            fig_prom = bo.getBits(move, *const.MOVE_PROM) + 2
            move_type = bo.getBits(move, *const.MOVE_TYPE)
            color = bo.getBits(move, *const.MOVE_COLOR)
            
            
            rank_start = bb.rank(sq_start)
            rank_dest = bb.rank(sq_dest)
            
            line_start = bb.line(sq_start)
            line_dest = bb.line(sq_dest)
            
            comb_chr = '-'
            if(fig_cap!=0):
                comb_chr = 'x'
            
            suffix = ''
            if(move_type == const.PROMOTION):
                suffix = " =" + const.ASCII_FIG[color][fig_prom]
            history_entry = "%c%c%i%c%c%i%s" % (const.ASCII_FIG[color][fig_start],chr(97+line_start), rank_start+1, comb_chr, chr(97+line_dest), rank_dest+1, suffix)
            
            self.gui.addToHistory(history_entry)
    
    
    def event_history_onselect(self, index):
        print("select")
        if(len(self.game.history) < index+1):       #move of the future selected
            i= len(self.game.history)
            while(len(self.game.history) < index+1):
                self.game.doMove(self.history[i][0])
                i += 1
                
        elif(len(self.game.history)-1 > index):     #move of the past selected
            while(len(self.game.history) > index+1):
                self.game.undoMove()   
        
        self.update()
        
        self.gui.setHistoryFocus(index)
        
    def event_but_undo(self):
        if(self.game.history == []):
            return
        self.game.undoMove()
        self.update()
    
    
    def event_but_claimdraw(self):
        pass
    
    
    def event_menu_file_save(self):
        filename = filedialog.asksaveasfilename(initialfile='save', defaultextension='.mcc', filetypes=[('My Chess Computer', '.mcc')] )
        #data = [self.game.board, self.game.note, self.game.history]
        data = self.game
        with open(filename, "wb") as file:
            pickle.dump(data, file)
            print(self.game.figures[const.PAWN])
    
    
    def event_menu_file_open(self):
        filename = filedialog.askopenfilename(initialfile='save', defaultextension='.mcc', filetypes=[('My Chess Computer', '.mcc')] )
        with open(filename, "rb") as file:
            data = pickle.load(file)
            #self.game.figures , self.game.board  = data
            self.game = data
            self.gui.gameDisplay.game = self.game
            self.update()
    
    
    def event_menu_file_exit(self):
        self.master.quit()
    
    
    def event_menu_game_new(self):
        dialog = newgamedialog.NewGameDialog()
        Player = dialog.result
        self.players[const.WHITE] = Player[const.WHITE](self, const.WHITE)
        self.players[const.BLACK] = Player[const.BLACK](self, const.BLACK)
        
        self.game= chessgame.ChessGame()
        self.gui.gameDisplay.game = self.game
        
        self.update()
    
    
    def event_menu_game_reset(self):
        self.game.setBoard(mat.STARTBOARD)
        self.gui.gameDisplay.game = self.game
        self.update()
        
        