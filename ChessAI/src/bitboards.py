import matrices as mat
import const

print("BITBOARDS INITIALIZING STARTING...")

def line(sq):
    #x%(2^y) = x&(2^y-1)    for x>0
    return sq&7     #sq%8

    
def rank(sq):
    #x/2^y = x>>y        for x>0 (and y>0)
    return sq>>3    #sq/8


def printBitboard(b):
    #convert bitboard into array 
    array_str = []  
    b = bin(b)[2::].zfill(64)   

    for i in range(8):
        l = []
        l += b[8*i : 8*(i+1)]
        array_str += [ l ]

    print("#-----------------#")
    for l in array_str:
        print( "| %i %i %i %i %i %i %i %i |" % (int(l[7]), int(l[6]), int(l[5]), int(l[4]), int(l[3]), int(l[2]), int(l[1]), int(l[0]) ))
    print("#-----------------#")
                

def getAllSq(b):
    result = []
    for sq in range(64):
        if( mask64[sq] & b ):
            result.append(sq)
            
    return result
                
def createMoveByteFromState( state, pos ):
    res = 0
        
    #to left
    tmp_pos = pos-1
    while( tmp_pos >= 0 ):
        res |= mask8[tmp_pos]
        if( not mask8[tmp_pos] & state ):
            tmp_pos -= 1
        else:
            break
    
    #to right
    tmp_pos = pos+1
    while( tmp_pos < 8 ):
        res |= mask8[tmp_pos]
        if( not mask8[tmp_pos] & state ):
            tmp_pos += 1
        else:
            break
            
    return res
    
    
def getRankByte(b, rank):
    #maybe use a rank mask
    return (b>>rank*8) & 255
    
    
def getLineByte(b, line):
    """get line of a bitmap and transform it into a byte"""
    return (mask8[0] if mask64[line] & b else 0) | \
        (mask8[1] if mask64[8 +line] & b else 0) | \
        (mask8[2] if mask64[16+line] & b else 0) | \
        (mask8[3] if mask64[24+line] & b else 0) | \
        (mask8[4] if mask64[32+line] & b else 0) | \
        (mask8[5] if mask64[40+line] & b else 0) | \
        (mask8[6] if mask64[48+line] & b else 0) | \
        (mask8[7] if mask64[56+line] & b else 0) 
        
        
def putByteInLine(line, b):
    """put byte in the line of a bitmap and return bitboard"""
    return (mask64[line] if b & mask8[0] else 0) | \
        (mask64[8 +line] if b & mask8[1] else 0) | \
        (mask64[16+line] if b & mask8[2] else 0) | \
        (mask64[24+line] if b & mask8[3] else 0) | \
        (mask64[32+line] if b & mask8[4] else 0) | \
        (mask64[40+line] if b & mask8[5] else 0) | \
        (mask64[48+line] if b & mask8[6] else 0) | \
        (mask64[56+line] if b & mask8[7] else 0) 
            
            
def getDiagonalByteLR(b, sq):
    return (mask8[0] if mat.diagonal_lr_lenght[sq] > 0 and b & mask64[mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[1] if mat.diagonal_lr_lenght[sq] > 1 and b & mask64[7 +mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[2] if mat.diagonal_lr_lenght[sq] > 2 and b & mask64[14+mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[3] if mat.diagonal_lr_lenght[sq] > 3 and b & mask64[21+mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[4] if mat.diagonal_lr_lenght[sq] > 4 and b & mask64[28+mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[5] if mat.diagonal_lr_lenght[sq] > 5 and b & mask64[35+mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[6] if mat.diagonal_lr_lenght[sq] > 6 and b & mask64[42+mat.diagonal_lr_start[sq]] else 0 ) | \
        (mask8[7] if mat.diagonal_lr_lenght[sq] > 7 and b & mask64[49+mat.diagonal_lr_start[sq]] else 0 )
        
        
def putByteInDiagonalLR(sq, b):
    return (mask64[mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 0 and b & mask8[0] else 0) | \
        (mask64[7 +mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 1 and b & mask8[1] else 0) | \
        (mask64[14+mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 2 and b & mask8[2] else 0) | \
        (mask64[21+mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 3 and b & mask8[3] else 0) | \
        (mask64[28+mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 4 and b & mask8[4] else 0) | \
        (mask64[35+mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 5 and b & mask8[5] else 0) | \
        (mask64[42+mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 6 and b & mask8[6] else 0) | \
        (mask64[49+mat.diagonal_lr_start[sq]] if mat.diagonal_lr_lenght[sq] > 7 and b & mask8[7] else 0)
        
        
def getDiagonalByteRL(b, sq):
    return (mask8[0] if mat.diagonal_rl_lenght[sq] > 0 and b & mask64[mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[1] if mat.diagonal_rl_lenght[sq] > 1 and b & mask64[9 +mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[2] if mat.diagonal_rl_lenght[sq] > 2 and b & mask64[18+mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[3] if mat.diagonal_rl_lenght[sq] > 3 and b & mask64[27+mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[4] if mat.diagonal_rl_lenght[sq] > 4 and b & mask64[36+mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[5] if mat.diagonal_rl_lenght[sq] > 5 and b & mask64[45+mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[6] if mat.diagonal_rl_lenght[sq] > 6 and b & mask64[54+mat.diagonal_rl_start[sq]] else 0 ) | \
        (mask8[7] if mat.diagonal_rl_lenght[sq] > 7 and b & mask64[63+mat.diagonal_rl_start[sq]] else 0 )
    
    
def putByteInDiagonalRL(sq, b):
    return (mask64[mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 0 and b & mask8[0] else 0) | \
        (mask64[9 +mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 1 and b & mask8[1] else 0) | \
        (mask64[18+mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 2 and b & mask8[2] else 0) | \
        (mask64[27+mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 3 and b & mask8[3] else 0) | \
        (mask64[36+mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 4 and b & mask8[4] else 0) | \
        (mask64[45+mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 5 and b & mask8[5] else 0) | \
        (mask64[54+mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 6 and b & mask8[6] else 0) | \
        (mask64[63+mat.diagonal_rl_start[sq]] if mat.diagonal_rl_lenght[sq] > 7 and b & mask8[7] else 0)



#----- init masks -----#
mask64 = []
for x in range(64):
    mask64.append(1<<x) 
            
mask8 = []
for x in range(8):
    mask8.append(1<<x) 
    
ranks = []
for x in range(8):
    ranks.append(255<<8*x)
    
lines = []
for x in range(8):
    lines.append( putByteInLine(x, 255) )
    
    
#----- king attacks -----#
king_attacks = [0 for x in range(64)]
for i in range(64):
    for j in range(64):
        if( abs(line(j)-line(i)) <= 1 and abs(rank(j)-rank(i)) <= 1 and i!=j ):
            king_attacks[i] |= mask64[j]
        
#----- knight attacks -----#
knight_attacks = [0 for x in range(64)]
for i in range(64):
    for j in range(64):
        if( abs(line(j)-line(i)) == 2 and abs(rank(j)-rank(i)) == 1 or
            abs(line(j)-line(i)) == 1 and abs(rank(j)-rank(i)) == 2 ):
            knight_attacks[i] |= mask64[j]
        
#----- pawn moves/attacks -----#            
pawn_singlestep = [[ 0 for x in range(64) ] for x in range(2)]
pawn_attacks = [[ 0 for x in range(64) ] for x in range(2)]
        
for p in (const.WHITE, const.BLACK):
    for i in range(64):
        if( (p==const.WHITE and i>0 and i<56) or (p==const.BLACK and i>7 and i<64) ):
            pawn_singlestep[p][i] =  mask64[i+8-p*16]
            if(line(i) != 0): 
                pawn_attacks[p][i] |= mask64[i+7-p*16]  
            if(line(i) != 7):
                pawn_attacks[p][i] |= mask64[i+9-p*16]  
            
#----- relativ attack lines -----#
rank_attacks = [[ 0 for x in range(256) ] for x in range(64)]
line_attacks = [[ 0 for x in range(256) ] for x in range(64)]
diagonal_attacks_lr = [[ 0 for x in range(256) ] for x in range(64)]
diagonal_attacks_rl = [[ 0 for x in range(256) ] for x in range(64)]


for sq in range(64):
    for state in range(256):
        #get postion in byte
        pos_rank = line(sq)
        pos_line = rank(sq)
        pos_dia_lr = line(mat.diagonal_lr_start[sq]) - line(sq)
        pos_dia_rl = line(sq) - line(mat.diagonal_rl_start[sq])
        
        #get pos move byte        
        byte_rank = createMoveByteFromState(state, pos_rank)
        byte_line = createMoveByteFromState(state, pos_line)
        byte_dia_lr = createMoveByteFromState(state, pos_dia_lr)
        byte_dia_rl = createMoveByteFromState(state, pos_dia_rl)
        
        #set byte in bitboards and save them        
        rank_attacks[sq][state] = byte_rank << (8*rank(sq))
        line_attacks[sq][state] = putByteInLine(line(sq), byte_line)
        diagonal_attacks_lr[sq][state] = putByteInDiagonalLR(sq, byte_dia_lr)
        diagonal_attacks_rl[sq][state] = putByteInDiagonalRL(sq, byte_dia_rl)

pawn_doublestep = [[0 for x in range(64)] for x in range(2)]
for sq in range(8, 15+1):
    pawn_doublestep[const.WHITE][sq] = mask64[sq+16]    

for sq in range(48, 55+1):
    pawn_doublestep[const.BLACK][sq] = mask64[sq-16]
    
castling_no_fig = [[0, 0] for x in range(2)]
castling_no_attack_sq = [[0, 0] for x in range(2)]
castling_king_dest = [[0, 0] for x in range(2)]
castling_rook_dest_sq = [[0, 0] for x in range(2)]
castling_rook_start_sq = [[0, 0] for x in range(2)]
castling_king_start_sq = [0, 0]

castling_no_fig[const.WHITE][const.CASTLING_LEFT] = mask64[const.B1] | mask64[const.C1] | mask64[const.D1]
castling_no_fig[const.WHITE][const.CASTLING_RIGHT] = mask64[const.F1] | mask64[const.G1]
castling_no_fig[const.BLACK][const.CASTLING_LEFT] = mask64[const.B8] | mask64[const.C8] | mask64[const.D8]
castling_no_fig[const.BLACK][const.CASTLING_RIGHT] = mask64[const.F8] | mask64[const.G8]

castling_no_attack_sq[const.WHITE][const.CASTLING_LEFT] = const.D1
castling_no_attack_sq[const.WHITE][const.CASTLING_RIGHT] = const.F1
castling_no_attack_sq[const.BLACK][const.CASTLING_LEFT] = const.D8
castling_no_attack_sq[const.BLACK][const.CASTLING_RIGHT] = const.F8

castling_king_start_sq[const.WHITE] = const.E1
castling_king_start_sq[const.BLACK] = const.E8

castling_king_dest[const.WHITE][const.CASTLING_LEFT] = mask64[const.C1]
castling_king_dest[const.WHITE][const.CASTLING_RIGHT] = mask64[const.G1]
castling_king_dest[const.BLACK][const.CASTLING_LEFT] = mask64[const.C8]
castling_king_dest[const.BLACK][const.CASTLING_RIGHT] = mask64[const.G8]

castling_rook_dest_sq[const.WHITE][const.CASTLING_LEFT] = const.D1
castling_rook_dest_sq[const.WHITE][const.CASTLING_RIGHT] = const.F1
castling_rook_dest_sq[const.BLACK][const.CASTLING_LEFT] = const.D8
castling_rook_dest_sq[const.BLACK][const.CASTLING_RIGHT] = const.F8

castling_rook_start_sq[const.WHITE][const.CASTLING_LEFT] = const.A1
castling_rook_start_sq[const.WHITE][const.CASTLING_RIGHT] = const.H1
castling_rook_start_sq[const.BLACK][const.CASTLING_LEFT] = const.A8
castling_rook_start_sq[const.BLACK][const.CASTLING_RIGHT] = const.H8

print("BITBOARDS INITIALIZING FINISHED")