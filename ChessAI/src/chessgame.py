import const
import matrices as mat
import bitboards as bb
import bitops as bo
import aivalues as aiv
import copy

class ChessGame:
    def __init__(self):
        
        self.board = []
        
        self.figures = [ [0, 0] for x in const.FIGURE_NAME ]
        self.all_figures = [0, 0, 0]
        self.king_pos = [0, 0]
        self.playerTurn = const.WHITE
    
        self.note = [0, [[0,0], [0,0]], 0, 0 ]
        #            A        B         C  D
        #A: enpassant byte
        #B: castling rights
        #C: halfmoves for fifty-move-rule
        #D: halfmove count
        
        self.history = []
        #history pattern: (move, note)
    
        self.material_value = 0
        
        #evolved light-figures
        #self.light_fig_evolved = [ int("10011001",2) for p in (0, 1) ]
        
        
        self.setBoard(mat.STARTBOARD)
        
        
    def setBoard(self, board):
        self.board = copy.copy( board )
        
        self.figures = [ [0, 0] for x in const.FIGURE_NAME ]
        for sq in range(64):
            fig = abs(self.board[sq])
            color = const.WHITE if self.board[sq] > 0 else const.BLACK
            
            if( fig == 0):
                continue
            if(fig == const.KING ):
                self.king_pos[color] = sq
                
            self.figures[fig][color] |= bb.mask64[sq]
    
        self.refreshAllFigBitboard()
    
        self.material_value = 0
        for sq in range(64):
            self.material_value += aiv.MATERIAL_VALUE[abs(self.board[sq])]* (1 if self.board[sq] > 0 else -1)
    
    
    def refreshAllFigBitboard(self):
        for color in (const.WHITE, const.BLACK):
            self.all_figures[color] = 0
            for figure in self.figures:
                self.all_figures[color] |= figure[color]    #pervormance?
        
        self.all_figures[const.BOTH] = self.all_figures[const.WHITE] | self.all_figures[const.BLACK]
        
        
    def doMove(self, move):
        sq_start = bo.getBits(move, *const.MOVE_START)
        sq_dest = bo.getBits(move, *const.MOVE_DEST)
        
        fig_start = bo.getBits(move, *const.MOVE_FIG_START)
        fig_cap = bo.getBits(move, *const.MOVE_FIG_CAPTURE)
        
        fig_prom = bo.getBits(move, *const.MOVE_PROM) + 2
        
        move_type = bo.getBits(move, *const.MOVE_TYPE)
        color = bo.getBits(move, *const.MOVE_COLOR)
        
        #move on board
        self.board[sq_start] = 0
        self.board[sq_dest] = fig_start * (-1 if color else 1)
        
        #move source piece
        self.figures[fig_start][color] ^= bb.mask64[sq_start] 
        self.figures[fig_start][color] |= bb.mask64[sq_dest]
        
        #update king possition and castling rights
        if(fig_start == const.KING):
            self.king_pos[color] = sq_dest
        
        #remove captured piece
        if( fig_cap ):
            self.figures[fig_cap][not color] ^=  bb.mask64[sq_dest]
            self.material_value += aiv.MATERIAL_VALUE[fig_cap] * (-1 if color else 1)
        
        #special moves
        if(move_type == const.ENPASSANT_CAPTURE):
            self.board[sq_dest-8+16*color] = 0
            self.figures[const.PAWN][not color] ^= bb.pawn_singlestep[not color][sq_dest]
            self.material_value += aiv.MATERIAL_VALUE[const.PAWN] * (-1 if color else 1)
        if(move_type == const.PROMOTION):
            self.board[sq_dest] = fig_prom* (-1 if color else 1)
            self.figures[fig_prom][color] |= bb.mask64[sq_dest]
            self.figures[const.PAWN][color] ^= bb.mask64[sq_dest]
            self.material_value += (aiv.MATERIAL_VALUE[fig_prom] - aiv.MATERIAL_VALUE[const.PAWN]) * (-1 if color else 1)
        if(move_type == const.CASTLING):
            side = bb.line(sq_dest) == const.G
            self.board[bb.castling_rook_start_sq[color][side]] = 0
            self.board[bb.castling_rook_dest_sq[color][side]] = const.ROOK* (-1 if color else 1)
            self.figures[const.ROOK][color] ^= bb.mask64[bb.castling_rook_dest_sq[color][side]] | bb.mask64[bb.castling_rook_start_sq[color][side]]

        self.history.append( (move, copy.deepcopy(self.note)) )

        #update note
        self.note[0] = 0  #remove en-passant note
        if(move_type == const.DOUBLE_STEP):
            self.note[0] |= bb.mask8[bb.line(sq_start)]
            
        #castling rights
        if(fig_start == const.KING):
            self.note[1][color] = [1,1]
        if(fig_start == const.ROOK):
            for side in (const.CASTLING_LEFT, const.CASTLING_RIGHT):
                if(bb.castling_rook_start_sq[color][side] == sq_start):
                    self.note[1][color][side] = 1
        
        if(fig_start != const.PAWN and fig_cap == 0):
            self.note[2] += 1
        else:
            self.note[2] = 0
            
        #move counter
        self.note[3] += 1

        self.refreshAllFigBitboard()
        self.playerTurn = not color

        
    def undoMove(self):
        last_move = self.history.pop()
        
        sq_start = bo.getBits(last_move[0], *const.MOVE_START)
        sq_dest = bo.getBits(last_move[0], *const.MOVE_DEST)
        
        fig_start = bo.getBits(last_move[0], *const.MOVE_FIG_START)
        fig_capture = bo.getBits(last_move[0], *const.MOVE_FIG_CAPTURE)
        
        fig_prom = bo.getBits(last_move[0], *const.MOVE_PROM) + 2
        
        move_type = bo.getBits(last_move[0], *const.MOVE_TYPE)
        
        note = last_move[1]
        
        self.playerTurn = not self.playerTurn
        
        self.note = note
        
        self.board[sq_start] = fig_start * (-1 if self.playerTurn else 1)
        self.board[sq_dest] = fig_capture * (-1 if not self.playerTurn else 1)
        
        self.figures[fig_start][self.playerTurn] &= ~bb.mask64[sq_dest]
        self.figures[fig_start][self.playerTurn] |= bb.mask64[sq_start]
        
        if(fig_start == const.KING):
            self.king_pos[self.playerTurn] = sq_start
        
        if(fig_capture):
            self.figures[fig_capture][not self.playerTurn] |= bb.mask64[sq_dest]
            self.material_value -= aiv.MATERIAL_VALUE[fig_capture] * (-1 if self.playerTurn else 1)
            
        if(move_type == const.ENPASSANT_CAPTURE):
            self.board[sq_dest-8+16*self.playerTurn] = (1 if self.playerTurn else -1)
            self.figures[const.PAWN][not self.playerTurn] |= bb.pawn_singlestep[not self.playerTurn][sq_dest]
            self.material_value -= aiv.MATERIAL_VALUE[const.PAWN] * (-1 if self.playerTurn else 1)
            
        if(move_type == const.PROMOTION):
            self.figures[fig_prom][self.playerTurn] ^= bb.mask64[sq_dest]
            self.material_value -= (aiv.MATERIAL_VALUE[fig_prom] - aiv.MATERIAL_VALUE[const.PAWN]) * (-1 if self.playerTurn else 1)
            
        if(move_type == const.CASTLING):
            side = bb.line(sq_dest) == const.G
            self.board[bb.castling_rook_start_sq[self.playerTurn][side]] = const.ROOK* (-1 if self.playerTurn else 1)
            self.board[bb.castling_rook_dest_sq[self.playerTurn][side]] = 0
            self.figures[const.ROOK][self.playerTurn]  ^= bb.mask64[bb.castling_rook_dest_sq[self.playerTurn][side]] | bb.mask64[bb.castling_rook_start_sq[self.playerTurn][side]]
            
        self.refreshAllFigBitboard()
        
        
    def getPossibleMoves(self, color):
        pieces = self.all_figures[color]
        
        result = []
        
        sq = 0
        while(pieces and sq<64):
            if(pieces & bb.mask64[sq]):
                moves = 0
                fig = abs(self.board[sq])
                if(fig == const.PAWN ):
                    #single step
                    moves |= bb.pawn_singlestep[color][sq] & ~self.all_figures[const.BOTH]
                    #double step
                    if(moves):
                        moves |= bb.pawn_doublestep[color][sq] & ~self.all_figures[const.BOTH]
                    #capture
                    moves |= bb.pawn_attacks[color][sq] & self.all_figures[not color]
                    #en-passant capture
                    moves |= bb.pawn_attacks[color][sq] & ( self.note[0] << (40 if color==const.WHITE else 16))
        
                elif(fig == const.KING ):
                    moves |= bb.king_attacks[sq] & ~self.all_figures[const.BOTH]
                    moves |= (bb.king_attacks[sq] & ~self.all_figures[color] ) & self.all_figures[not color]
                    #castling
                    for side in (const.CASTLING_LEFT, const.CASTLING_RIGHT):
                        if(not self.note[1][color][side] and \
                           not (bb.castling_no_fig[color][side] & self.all_figures[const.BOTH]) and \
                           not self.isUnderAttack(bb.castling_no_attack_sq[color][side], color) and \
                           not self.isUnderAttack(bb.castling_king_start_sq[color], color)):
                            moves |= bb.castling_king_dest[color][side]
        
                else:
                    if(fig == const.KNIGHT):
                        moves |= bb.knight_attacks[sq]
                    else:
                        if(fig == const.BISHOP or fig == const.QUEEN):
                            moves |=   bb.diagonal_attacks_lr[sq][bb.getDiagonalByteLR(self.all_figures[const.BOTH], sq)] | \
                                                bb.diagonal_attacks_rl[sq][bb.getDiagonalByteRL(self.all_figures[const.BOTH], sq)] 
                        if(fig == const.ROOK or fig == const.QUEEN):
                            moves |=   bb.line_attacks[sq][bb.getLineByte(self.all_figures[const.BOTH], bb.line(sq))] | \
                                                bb.rank_attacks[sq][bb.getRankByte(self.all_figures[const.BOTH], bb.rank(sq))]
                        
                    moves &= ~self.all_figures[color]
                        
                dest = 0
                while(moves and dest<64):
                    if(moves & bb.mask64[dest]):
                        
                        move_type = const.NORMAL_MOVE
                        if(bb.mask64[dest] & self.all_figures[not color]):
                            move_type = const.CAPTURE
                        
                        if(fig == const.KING and abs(bb.line(dest)-bb.line(sq)) == 2):
                            move_type = const.CASTLING
                        elif(fig == const.PAWN):
                            if(abs(bb.rank(dest)-bb.rank(sq))==2):
                                move_type = const.DOUBLE_STEP
                            elif(bb.line(dest) != bb.line(sq) and self.board[dest] == 0):
                                move_type = const.ENPASSANT_CAPTURE
                            elif(bb.rank(dest) == 7-7*color):
                                move_type = const.PROMOTION
                        
                        move = move_type | (sq << const.MOVE_START[0]) | (dest << const.MOVE_DEST[0]) | (abs(self.board[sq]) << const.MOVE_FIG_START[0]) | (abs(self.board[dest]) << const.MOVE_FIG_CAPTURE[0]) | (color << const.MOVE_COLOR[0])
                        
                        if(move_type == const.PROMOTION):
                            for fig_prom in (const.PROM_KNIGHT, const.PROM_BISHOP, const.PROM_ROOK, const.PROM_QUEEN):
                                result.append( move | (fig_prom << const.MOVE_PROM[0]) )
                        else:
                            result.append(move)
                            
                        move ^= bb.mask64[dest]
                    dest +=1 
                pieces &= ~bb.mask64[sq]
            sq += 1
            
        return result
    
    
    def getValidMoves(self):
        valid_moves = []
        for move in self.getPossibleMoves(self.playerTurn):
            self.doMove(move)
            if(not self.isUnderAttack(self.king_pos[not self.playerTurn], not self.playerTurn)):
                valid_moves.append(move)
            self.undoMove()
        return valid_moves
    
    
    def isUnderAttack(self, sq, color):
        result = False
        
        attack_diag =   bb.diagonal_attacks_lr[sq][bb.getDiagonalByteLR(self.all_figures[const.BOTH], sq)] | \
                        bb.diagonal_attacks_rl[sq][bb.getDiagonalByteRL(self.all_figures[const.BOTH], sq)]
        
        attack_rank_line =  bb.line_attacks[sq][bb.getLineByte(self.all_figures[const.BOTH], bb.line(sq))] | \
                            bb.rank_attacks[sq][bb.getRankByte(self.all_figures[const.BOTH], bb.rank(sq))]
        
        #check for enemys
        if( bb.knight_attacks[sq] & self.figures[const.KNIGHT][not color] or \
            bb.pawn_attacks[color][sq] & self.figures[const.PAWN][not color] or \
            bb.king_attacks[sq] & self.figures[const.KING][not color] or \
            attack_diag & self.figures[const.BISHOP][not color] or \
            attack_diag & self.figures[const.QUEEN][not color] or \
            attack_rank_line & self.figures[const.ROOK][not color] or \
            attack_rank_line & self.figures[const.QUEEN][not color] ):
            
            result = True

        return result
    
    
    def getState(self):
        for color in (const.WHITE, const.BLACK):
            if(self.isUnderAttack(self.king_pos[color], color)):
                pass
            
    
    '''    
    def getPossibleMovesDiag(self, sq):
        return  bb.diagonal_attacks_lr[sq][bb.getDiagonalByteLR(self.all_figures[const.BOTH], sq)] | \
                bb.diagonal_attacks_rl[sq][bb.getDiagonalByteRL(self.all_figures[const.BOTH], sq)]
    
    
    def getPossibleMovesRankLine(self, sq):
        return  bb.line_attacks[sq][bb.getLineByte(self.all_figures[const.BOTH], bb.line(sq))] | \
                bb.rank_attacks[sq][bb.getRankByte(self.all_figures[const.BOTH], bb.rank(sq))]
    '''            
                
