import const


def invertMat(data):
    result = []
    for row in range(7,-1,-1):
        result += data[row*8:row*8+8]
    return result


#----- material value ----#
MATERIAL_VALUE = [0, 100, 300, 300, 500, 900, 10000]


POSSITION_VALUE = [[ [] for x in const.FIGURE_NAME ] for x in (const.WHITE, const.BLACK)]

POSSITION_VALUE[const.WHITE][const.PAWN] = [     0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  5,  2,  2,  5,  0,  0,
                                                -3, -3,  3,  3,  3,  3, -3, -3,
                                                -5, -5, -2, 10, 10, -2, -5, -5,
                                                -6, -6,  5, 16, 16,  5, -6, -6,
                                                -6, -6, 18, 25, 25, 18, -6, -6,
                                                30, 30, 35, 45, 45, 35, 30, 30,
                                                 0,  0,  0,  0,  0,  0,  0,  0 ]


POSSITION_VALUE[const.WHITE][const.ROOK] = [    -3, 0, 5, 6, 6, 5, 0,-3,
                                                 0, 0, 5, 6, 6, 5, 0, 0,
                                                 0, 0, 5, 6, 6, 5, 0, 0,
                                                 0, 0, 5, 6, 6, 5, 0, 0,
                                                 0, 0, 5, 6, 6, 5, 0, 0,
                                                 0, 0, 5, 6, 6, 5, 0, 0,
                                                 0, 0, 5, 6 ,6, 5, 0, 0,
                                                 7, 8, 8, 8 ,8 ,8, 8, 7 ]


POSSITION_VALUE[const.WHITE][const.BISHOP] = [   0, 0,-3, 0, 0,-3, 0, 0,
                                                 0, 0, 0, 0, 0, 0, 0, 0,
                                                 0, 5, 6, 6, 6, 6, 5, 0,
                                                 0, 5, 7, 8, 8, 7, 5, 0,
                                                 0, 5, 7, 8, 8, 7, 5, 0,
                                                 0, 5, 7, 7, 7, 7, 5, 0,
                                                 0, 4, 4, 4, 4, 4, 4, 0,
                                                 0, 0, 0, 0, 0, 0, 0, 0 ]


POSSITION_VALUE[const.WHITE][const.KNIGHT] = [   0,-1, 0, 0, 0, 0,-1, 0,
                                                 0, 1, 1, 1, 1, 1, 1, 0,
                                                 0, 2, 4, 5, 5, 4, 2, 0,
                                                 0, 2, 5, 5, 5, 5, 2, 0,
                                                 0, 2, 5, 6, 6, 5, 2, 0,
                                                 0, 2, 5, 5, 5, 5, 2, 0,
                                                 0, 3, 3, 3, 3, 3, 3, 0,
                                                 0, 0, 0, 0, 0, 0, 0, 0 ]


POSSITION_VALUE[const.WHITE][const.KING] = [    14, 19, 18, -5, -1, -5, 21, 15,
                                                -5, -4, -6, -8, -9, -8, -3, -5,
                                                 0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0 ]


POSSITION_VALUE[const.WHITE][const.QUEEN] = [    -5, 0,  0,  0,  0,  0,  0, -5,
                                                 -2, 0,  0,  0,  0,  0,  0, -2,
                                                 0,  2,  3,  3,  3,  3,  2,  0,
                                                 0,  2,  5,  4,  4,  5,  2,  0,
                                                 0,  2,  5,  6,  6,  5,  2,  0,
                                                 0,  2,  5,  5,  5,  5,  2,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0,
                                                 0,  0,  0,  0,  0,  0,  0,  0 ]

PAWN_IS_IN_CHAIN = [ [], [] ]
PAWN_IS_IN_CHAIN[const.WHITE] = [ 0, 0, 5, 10, 15, 20, 25, 0 ]
PAWN_IS_IN_CHAIN[const.BLACK] = PAWN_IS_IN_CHAIN[const.WHITE][::-1]

PAWN_FREE = [ [], [] ]
PAWN_FREE[const.WHITE] = [ 0, 0, 10, 20, 35, 50, 70, 0]
PAWN_FREE[const.BLACK] = PAWN_FREE[const.WHITE][::-1]


for piece in range(1,7):
    POSSITION_VALUE[const.BLACK][piece] = invertMat( POSSITION_VALUE[const.WHITE][piece]) 
    
    
    
    