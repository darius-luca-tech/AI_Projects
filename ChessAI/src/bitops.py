import bitboards as bb

#----- byte operations -----#
def LSB( b ):
    i = 0
    while(i< 64 and not (b & bb.mask64[i]) ):
        i += 1
    return i
    
def MSB( b ):
    # propaply use 
    # b.bit_length()
    i = 63
    while(i >= 0 and not (b & bb.mask64[i]) ):
        i -= 1
    return i
    
def CntBits( b ):
    cnt= 0
    while(b):   #solange b>0
        if(b&1):
            cnt += 1
        b >>= 1
    return cnt

def getBits( b, start, lenght):
    return (b>>start) & ((1<<lenght) -1)

def setBits( data, start ):
    return data << start
