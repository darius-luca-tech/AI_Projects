
#------ game constants -----#
#players
WHITE = 0
BLACK = 1
BOTH = 2

#color for onTurnLabel
PLAYER_COLOR = ["white", "black"]

#figures
PAWN = 1
KNIGHT = 2
BISHOP = 3
ROOK = 4
QUEEN = 5
KING = 6

FIGURE_NAME = [ "", "pawn", "knight", "bishop", "rook", "queen", "king" ]

#used in move 32bit for promotion figure prom_figure = figure-2
PROM_KNIGHT = 0
PROM_BISHOP = 1
PROM_ROOK = 2
PROM_QUEEN = 3

#all lines
A, B, C, D, E, F, G, H = range(8)

#all squares
A1, B1, C1, D1, E1, F1, G1, H1, \
A2, B2, C2, D2, E2, F2, G2, H2, \
A3, B3, C3, D3, E3, F3, G3, H3, \
A4, B4, C4, D4, E4, F4, G4, H4, \
A5, B5, C5, D5, E5, F5, G5, H5, \
A6, B6, C6, D6, E6, F6, G6, H6, \
A7, B7, C7, D7, E7, F7, G7, H7, \
A8, B8, C8, D8, E8, F8, G8, H8 = range(64)

#----- game display constants -----#
DEFAULTBORDERWIDTH = 20
DEFAULTTILEWIDTH = 45
DEFAULTFONTSIZE = (7, 15)
COLORS = {  "bg":"#EDC08C",
            "border":"#B55602",
            "tiles":("#FC9235", "#FFB87A") }

#----- move types -----#
NORMAL_MOVE, CAPTURE, PROMOTION, DOUBLE_STEP, ENPASSANT_CAPTURE, CASTLING, KING_CAPTURE = range(7)

#----- move 32bit reservation -----#
# a single move is stored in 32 bit as follows
# xxxxxxxx xx x xxx xxx xxxxxx xxxxxx xxx 
#           G F  E   D    C      B     A
#
# A: move type (0-6)
# B: start sq (0-63)
# C: destination sq (0-63)
# D: start figure (1-6)
# E: captured figure (1-6)
# F: color of moved piece (0-1)
# G: promotion figure  (0-3)

#NAME = (start_bit, lenght)
MOVE_TYPE = (0, 3)
MOVE_START = (3, 6)
MOVE_DEST = (9, 6)
MOVE_FIG_START = (15, 3)
MOVE_FIG_CAPTURE = (18, 3)
MOVE_COLOR = (21, 1)
MOVE_PROM = (22, 2)

#----- castling -----#
CASTLING_LEFT = 0
CASTLING_RIGHT = 1

#----- player status -----#
IDELING = 0
PICKING = 1


INF = 1000000


ASCII_FIG = [[],[]]
ASCII_FIG[WHITE] = [  'x', chr(9817), chr(9816), chr(9815), chr(9814), chr(9813), chr(9812)]
ASCII_FIG[BLACK] = [  'x', chr(9823), chr(9822), chr(9821), chr(9820), chr(9819), chr(9818)]


#AI constants
CASTLING_RIGHT_LOSS_PENALTY = -40
