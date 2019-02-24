
from z3 import *

"""
15 tiles
9 colors
    yellow       0
    light orange 1
    dark orange  2

    light green  3
    green        4
    dark green   5

    light pink   6
    dark pink    7
    purple       8
3 kinds of tiles (does not matter)
different number of semicircles in connections (does not matter)

assumed solution
    3x5 board
    colors match
"""

# colors of connections, order is top, right, down, left
# follows figure 1 in order
#  0  1  2  3  4
#  5  6  7  8  9
# 10 11 12 13 14
tiles = [
    [8,0,0,8],
    [7,1,0,1],
    [7,6,3,6],
    [8,5,4,8],
    [6,7,8,6],

    [6,5,0,5],
    [2,1,5,4],
    [0,2,0,0],
    [4,3,4,0],
    [8,5,0,3],

    [6,7,5,4],
    [7,8,6,8],
    [0,8,0,6],
    [4,1,5,8],
    [0,2,1,1],
]

# rotates a list to the right
def rotate(l, n):
    return l[-n:] + l[:-n]

# returns rotations of a tile
def rotations(tile):
    return [rotate(tile, i) for i in range(4)]

# converts integer code to color name
def ccode2cname(n):
    t = ["yellow","light orange","dark orange",
    "light green","green","dark green",
    "light pink","dark pink","purple"]
    return t[n]

def solve():
    # variable for each position
    X = [[Int("x_%s_%s" % (i, j)) for j in range(5) ] for i in range(3)]
    # variable for each color connection
    # A are the left, right sides
    # B are the top, down sides
    A = [[Int("a_%s_%s" % (i, j)) for j in range(8) ] for i in range(3)]
    B = [[Int("b_%s_%s" % (i, j)) for j in range(10) ] for i in range(2)]

    # each position has a tile from 0 to 14
    restriction_tile  = [ And(0 <= X[i][j], X[i][j] <= 14) for i in range(3) for j in range(5) ]
    # each position holds distinct tile
    restriction_distinct = Distinct([X[i][j] for i in range(3) for j in range(5)])
    # colors in connections must match
    restriction_color = [A[i][j] == A[i][j+1] for i in range(3) for j in [0,2,4,6]]
    restriction_color += [B[i][j] == B[i][j+1] for i in range(2) for j in [0,2,4,6,8]]
    # tiles placed restrict colors in each position and connection
    def colors_at_intersections(i,j,T):
        """
        if i == 0 and j == 0:
            r = Or([And(A[0][0]==t[1],B[0][0]==t[2]) for t in rotations(T)])
        elif i == 0 and j == 4:
            r = Or([And(A[0][7]==t[2],B[0][8]==t[3]) for t in rotations(T)])
        elif i == 0:
            r = Or([And(A[i][j+1]==t[3],A[i][j+2]==t[3],B[i][0]==t[1]) for t in rotations(T)])
        elif i == 1 and j == 0:
            r = Or(True,True)
        elif i == 1 and j == 4:
            r = Or(True,True)
        elif i == 1:
            r = Or(True,True)
        elif i == 2 and j == 0:
            r = Or(True,True)
        elif i == 2 and j == 4:
            r = Or(True,True)
        elif i == 2:
            r = Or(True,True)
        """
        r = []
        for t in rotations(T):
            r0 = []
            if i!=0:
                r0.append( B[i-1][j*2+1]==t[0] )
            if i!=2:
                r0.append( B[i][j*2]==t[2] )
            if j!=0:
                r0.append( A[i][(j-1)*2+1]==t[3] )
            if j!=4:
                r0.append( A[i][j*2]==t[1] )
            r.append( And(r0) )
        r = Or(r)
        return r
    restriction_tiles_inserted = [
        Implies(X[i][j] == t, colors_at_intersections(i,j,tiles[t]))
            for i in range(3)
            for j in range(5)
            for t in range(15)
    ]
    
    s = Solver()
    s.add(restriction_tile)
    s.add(restriction_distinct)
    s.add(restriction_color)
    s.add(restriction_tiles_inserted)
    # want another solution
    #s.add(X[0][0]!=5)
    print("start")
    check = s.check()
    print(check)
    if check == sat:
        model = s.model()
        print(model)
        print([[model.evaluate(X[i][j]) for j in range(5)] for i in range(3)])
        print([[ccode2cname(model[A[i][j*2]].as_long()) for j in range(4)] for i in range(3)])
        print([[ccode2cname(model[B[i][j*2]].as_long()) for j in range(5)] for i in range(2)])
    print("end")

def main():
    solve()

if __name__ == '__main__':
    main()
