import const
import bitops as bo
import bitboards as bb
import matrices as mat
import aivalues as aiv
import promotiondialog as prom_dialog
from random import randint
import time
import copy

class Player:
    def __init__(self, manager, color):
        self.color = color
        self.manager = manager
        self.status = const.IDELING
        self.game = None
        self.result = None
        
    def processInput(self, game, sq):
        pass
    
    def doMove(self, game):
        pass
    
class Human(Player):
    def processInput(self, game, sq= -1):
        self.game = game
        
        if(sq == -1):
            return
        
        if(self.status == const.IDELING):
            if(self.game.board[sq] == 0 or (const.WHITE if self.game.board[sq] > 0 else const.BLACK) != self.color ):
                return
            
            #get possible moves and test them if valid
            self.possible_moves = []     
            for move in self.game.getValidMoves():
                if(bo.getBits(move, *const.MOVE_START) == sq):
                    self.possible_moves.append(move)
                    
            #highlight possible moves
            self.manager.gui.gameDisplay.removeHighlight()
            for move in self.possible_moves:
                move_type = bo.getBits(move, *const.MOVE_TYPE)
                color_highlight = 0
                if(move_type in (const.NORMAL_MOVE, const.DOUBLE_STEP) ):
                    color_highlight = 0
                elif(move_type in (const.CAPTURE, const.ENPASSANT_CAPTURE) ):
                    color_highlight = 1
                elif(move_type == const.CASTLING ):
                    color_highlight = 2
                else:
                    color_highlight = 3
                
                self.manager.gui.gameDisplay.highlightTile(bo.getBits(move, *const.MOVE_DEST), color_highlight)
            
            if(self.possible_moves != [] ):
                self.status = const.PICKING
            
        elif(self.status == const.PICKING):
            selected_move = -1
                
            #find corresponding move
            for move in self.possible_moves:
                if(bo.getBits(move, *const.MOVE_DEST) == sq):
                    selected_move = move
                    break
                    
            if(selected_move != -1):
                if(bo.getBits(selected_move, *const.MOVE_TYPE) == const.PROMOTION):
                    dialog = prom_dialog.PromotionDialog()
                    selected_move |= dialog.result << const.MOVE_PROM[0]
                
                self.result = selected_move
                
                self.manager.master.event_generate("<<turn_complete>>")
                
            self.manager.gui.gameDisplay.removeHighlight()
            self.status = const.IDELING
    
    
class AI(Player):
    def doMove(self, game):
        self.game = game
        
        self.searched_nots = 0
        self.evaluated_pos = 0 
        
        self.move_best = 0
        
        t1 = time.perf_counter()
        
        #self.explore(self.max_depth, -const.INF, const.INF)
        self.iterate(4)
        #self.exploreRoot(4)
            
        t2 = time.perf_counter()
        
        print("########################################")
        print("KNOTS SEARCHED:\t\t", self.searched_nots)
        print("EVALUATED POSSITIONS:\t", self.evaluated_pos)
        print("TIME NEEDED:\t\t", t2-t1)
        print("BEST MOVE:\t\t", self.move_best)
        print("########################################")
        
        #rnd = randint(0, len(self.move_best))
        
        self.result= self.move_best
        
        self.manager.master.event_generate("<<turn_complete>>")
    
    
    def iterate(self, depth):
        for d in range(1, depth+1):
            self.exploreRoot(d)#(d, -const.INF, const.INF)
    
    def explore(self, depth, alpha, beta):
        self.searched_nots += 1
        
        if(depth <= 0):
            return self.evaluate()
        
        for move in self.sort( self.game.getPossibleMoves(self.game.playerTurn) ):
            if(move&7 == const.CASTLING):
                self.castling_move_done[self.game.playerTurn] = True
            
            self.game.doMove(move)
            val = -self.explore(depth-1, -beta, -alpha);    
            self.game.undoMove()

            if(move&7 == const.CASTLING):
                self.castling_move_done[self.game.playerTurn] = False

            if(val >= beta):
                return beta
                    
            if(val > alpha):
                alpha = val;
                    
        return alpha;
    
    
    def exploreRoot(self, depth):
        self.castling_root = [  self.game.note[1][0] == [0, 0], 
                                self.game.note[1][1] == [0, 0] ] 
        self.castling_move_done = [ False, False ]
        
        moves = self.sort( self.game.getValidMoves() )
        if(depth > 1):
            moves.remove(self.move_best)
            moves.insert(0, self.move_best)
        
        alpha = -const.INF
        
        for move in moves:
            if(move&7 == const.CASTLING):
                self.castling_move_done[self.game.playerTurn] = True
            
            self.game.doMove(move)
            val = -self.explore(depth-1, -const.INF, -alpha);    
            self.game.undoMove()
            
            if(move&7 == const.CASTLING):
                self.castling_move_done[self.game.playerTurn] = False
            
            if(val > alpha):
                alpha = val;
                self.move_best = move
                
    
    def quiesce(self, alpha, beta):
        val = self.evaluate()
        
        if(val>=beta):
            return beta
        if(val > alpha):
            alpha = val
            
        for move in self.sort( self.game.getPossibleMoves(self.game.playerTurn) ):
            if(move&7 != const.CAPTURE):
                break
            self.game.doMove(move)
            val = -self.quiesce(-beta, -alpha)
            self.game.undoMove()
            
            if(val>=beta):
                return beta
            if(val > alpha):
                alpha = val
                
        return alpha
    
    
    def sort(self, moves):
        high = []
        low = []
        for move in moves:
            if(move&7 == const.CAPTURE):
                high.append(move)
            else:
                low.append(move)
                
        return high+low
        
        
    def evaluate(self):
        self.evaluated_pos += 1
        
        value = self.game.material_value

        for sq in range(64):
            if( self.game.board[sq] != 0 ):
                fig = abs(self.game.board[sq])
                color = const.WHITE if self.game.board[sq] > 0 else const.BLACK
                value_piece = 0
                
                value_piece += aiv.POSSITION_VALUE[color][fig][sq]
                
                if( fig == const.PAWN ):
                    #---pawn structure---
                    #pawn chain
                    if( self.game.figures[const.PAWN][color] & bb.pawn_attacks[not color][sq] ):
                        value_piece += aiv.PAWN_IS_IN_CHAIN[color][bb.rank(sq)]
                    #free pawn
                    if( not self.game.figures[const.PAWN][not color] & bb.lines[bb.line(sq)] ):
                        value_piece += aiv.PAWN_FREE[color][bb.rank(sq)]
                
                value += value_piece * (-1 if color else 1)
        
        for color in (0, 1):
            if( self.castling_root[color] and self.game.note[1][color] != [0, 0] and not self.castling_move_done ):
                value += const.CASTLING_RIGHT_LOSS_PENALTY * (-1 if color else 1)
        
        return value* (-1 if self.game.playerTurn==const.BLACK else 1)
    
    
    
    '''
    def doMoveNegamax(self, game):
        if(self.status != 0):
            print("THEADING ERROR")
        
        self.status = 10
        self.game = game
        
        self.searched_nots = 0
        self.evaluated_pos = 0 
        
        score_best = -const.INF
        self.move_best = []
        
        t1 = time.clock()
            
        for move in self.game.getPossibleMoves(self.color):
            #x= self.game.all_figures[self.color]
            self.game.doMove(move)
            score = -self.exploreNegamax(2)
            self.game.undoMove()
            
            #if(self.game.all_figures[self.color] != x):
            #    print("ERROR ROOT")
            if(score == score_best):
                self.move_best.append(move)
                #print("BEST SCORE ROOT:",score)
            elif(score > score_best):
                self.move_best = [move]
                score_best = score
                #print("BEST SCORE ROOT:",score)
           
        t2 = time.clock() 
        print("TIME NEEDED:", t2-t1)
        
        print("BEST MOVES:", self.move_best)
        i = randint(0, len(self.move_best)-1 )
        
        self.result= self.move_best[i]
        self.status = 0
        
        print("KNOTS SEARCHED:", self.searched_nots)
        print("EVALUATED POSSITIONS", self.evaluated_pos)
        
        self.manager.master.event_generate("<<turn_complete>>")
        
        
    def doMoveAlphaBeta(self, game):
        if(self.status != 0):
            print("THEADING ERROR")
        
        self.status = 10
        self.game = game
        
        self.searched_nots = 0
        self.evaluated_pos = 0 
        
        alpha = -const.INF
        #beta = 10000000
        
        self.move_best = []
        
        t1 = time.clock()
            
        for move in self.game.getPossibleMoves(self.color):

            self.game.doMove(move)
            val = -self.exploreAB(2, -const.INF, -alpha )
            self.game.undoMove()

            if(val > alpha):
                self.move_best = [move]
                alpha = val
                print("BEST SCORE ROOT:", alpha)
           
           
        t2 = time.clock() 
        print("TIME NEEDED:", t2-t1)
        
        
        print("BEST MOVES:", self.move_best)
        i = randint(0, len(self.move_best)-1 )
        
        self.result= self.move_best[i]
        self.status = 0
        
        print("KNOTS SEARCHED:", self.searched_nots)
        print("EVALUATED POSSITIONS", self.evaluated_pos)
        
        self.manager.master.event_generate("<<turn_complete>>")
    
    
    def exploreAll(self, depth):
        alpha = -const.INF
        self.searched_nots += 1
        if(depth <= 0):
            return self.evaluate()
        
        for move in self.game.getPossibleMoves(self.game.playerTurn):
            self.game.doMove(move)
            val = -self.exploreAll(depth - 1);
            self.game.undoMove()

            if(depth == self.max_depth):
                if(alpha == val):
                    self.move_best.append(move)
                elif(val > alpha):
                    self.move_best = [move]
                    
            if(val > alpha):
                alpha = val;
                    
        return alpha;
    
    
    def exploreAB(self, depth, alpha, beta):
        
        self.searched_nots += 1
        if(depth <= 0):
            return self.evaluate()
        
        for move in self.game.getPossibleMoves(self.game.playerTurn):

            self.game.doMove(move)
            val = -self.exploreAB(depth-1, -beta, -alpha);    
            self.game.undoMove()
            #if( val >= beta):
            #    return beta
            if(val >= beta):
                return beta
            
            if(val > alpha):
                alpha = val;
                
        return alpha;
    
    
    def exploreNegamax(self, depth):
        alpha = -const.INF
        self.searched_nots += 1
        if(depth <= 0):
            return self.evaluate()
        
        for move in self.game.getPossibleMoves(self.game.playerTurn):
            x= self.game.all_figures[self.game.playerTurn]
            p= self.game.playerTurn
            self.game.doMove(move)
            val = -self.exploreNegamax(depth - 1);    
            self.game.undoMove()
            if(self.game.all_figures[self.game.playerTurn] != x):
                print("ERROR")
                print("MOVE_TYPE", bo.getBits(move, *const.MOVE_TYPE))
                print("PLAYER:", p, self.game.playerTurn)

            if(val > alpha):
                alpha = val;
        return alpha;
        
        
    '''
    
        
    
