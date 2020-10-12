CallMemory = []

root = [['_','b','_','_','_'],
        ['_','_','b','_','_'],
        ['_','_','_','_','_'],
        ['_','_','_','_','_'],
        ['_','w','_','_','_']]

# Display( Board )
def Display(Board):
    print ('  _  _  _  _  _')
    for i in Board:
        for j in i:
            print('| ', j, sep='',end='')
        print('|')
    print ()

# Copy( Board )
def Copy(Board):
    copy2 = []
    for i in Board:
        copy2.append(i.copy())
    return copy2

# Moves( Player, Board )
def Moves(Player, Board):
    moveList = []
    if Player == 'Black':
        piece = 'b'
        piece2 = 'w'
    else:
        piece = 'w'
        piece2 = 'b'
    for i in range(len(Board)):
        for j in range(len(Board[i])):
            if Board[i][j] == piece:
                if i+1<len(Board) and j+1<len(Board[i]):
                    if Board[i+1][j+1] == '_':
                        moveList.append(Copy(Board))
                        moveList[-1][i][j]='_'
                        moveList[-1][i+1][j+1]=piece
                    elif Board[i+1][j+1] == piece2:
                        if i+2<len(Board) and j+2<len(Board[i]):
                            moveList.append(Copy(Board))
                            moveList[-1][i][j]='_'
                            moveList[-1][i+1][j+1]='_'
                            moveList[-1][i+2][j+2]=piece
                            
                if i-1>0 and j+1<len(Board[i]):
                    if Board[i-1][j+1] == '_':
                        moveList.append(Copy(Board))
                        moveList[-1][i][j]='_'
                        moveList[-1][i-1][j+1]=piece
                    elif Board[i-1][j+1] == piece2:
                        if i-2>0 and j+2<len(Board[i]):
                            moveList.append(Copy(Board))
                            moveList[-1][i][j]='_'
                            moveList[-1][i-1][j+1]='_'
                            moveList[-1][i-2][j+2]=piece
                            
                if i+1<len(Board) and j-1<len(Board[i]):
                    if Board[i+1][j-1] == '_':
                        moveList.append(Copy(Board))
                        moveList[-1][i][j]='_'
                        moveList[-1][i+1][j-1]=piece
                    elif Board[i+1][j-1] == piece2:
                        if i+2<len(Board) and j-2>0:
                            moveList.append(Copy(Board))
                            moveList[-1][i][j]='_'
                            moveList[-1][i+1][j-1]='_'
                            moveList[-1][i+2][j-2]=piece
                            
                if i-1>0 and j-1>0:
                    if Board[i-1][j-1] == '_':
                        moveList.append(Copy(Board))
                        moveList[-1][i][j]='_'
                        moveList[-1][i-1][j-1]=piece
                    elif Board[i-1][j-1] == piece2:
                        if i-2>0 and j-2>0:
                            moveList.append(Copy(Board))
                            moveList[-1][i][j]='_'
                            moveList[-1][i-1][j-1]='_'
                            moveList[-1][i-2][j-2]=piece
    numlist=[]
    blist=[]
    for i in moveList:
        no = StateNumber(i)
        if no not in numlist:
            numlist.append(no)
            blist.append(i)
    return blist
                    
# StateNumber( Board )
def StateNumber(Board):
    d=0
    s=1
    for i in range(len(Board)):
        for j in range(len(Board[i])):
            if (i+j)%2==1:
                if Board[i][j]=='w':
                    d=d+1*s
                elif Board[i][j]=='b':
                    d=d+2*s
                s=s*3
    return d

def SolveGame(Board):
    global CallMemory
    CallMemory = [Board]
    for i in range(1000):
        Outcome = WhoWins('White', 0, i)
        if Outcome != 'Not Sure':
            print('Game Solved! Winner is', Outcome)
            return 'exit'
        else:
            print('Current depth', i)

def WhoWins(Player, MemId, MaxDepth, Hierarchy=None):
    global CallMemory
    if Player == 'White':
        Player2 = 'Black'
    else:
        Player2 = 'White'
    if MaxDepth == 0:
        ChildNodes = Moves(Player, CallMemory[MemId])
        if Hierarchy == None:
            Hierarchy = []
        UpdatedHierarchy = Hierarchy.copy()
        UpdatedHierarchy.append(StateNumber(CallMemory[MemId]))
        if len(ChildNodes) == 0:
            return Player2
        ChildMem = []
        CallMemory[MemId] = [ChildMem, 0, UpdatedHierarchy]
        for i in ChildNodes:
            SNo = StateNumber(i)
            if SNo not in Hierarchy[::-2]:
                ChildId = len(CallMemory)
                ChildMem.append(ChildId)
                CallMemory.append(i)
        if len(ChildMem) == 0:
            return 'Invalid ' + Player2
        return 'Not Sure'
    else:
        ChildNodes = CallMemory[MemId][0]
        LoseCount = CallMemory[MemId][1]
        Hierarchy = CallMemory[MemId][2]
        iMax = len(ChildNodes)
        i = 0
        while i < iMax:
            Outcome = WhoWins(Player2, ChildNodes[i], MaxDepth-1, Hierarchy)
            if Outcome == Player:
                return Player
            elif Outcome == 'Invalid ' + Player:
                ChildNodes.pop(i)
                iMax = iMax - 1
                i = i - 1
            elif Outcome == Player2:
                LoseCount = LoseCount + 1
                ChildNodes.pop(i)
                iMax = iMax - 1
                i = i - 1
            i = i + 1
        CallMemory[MemId][1] = LoseCount
        if iMax == 0:
            return Player2
        else:
            return 'Not Sure'

Display(root)
for i in Moves('White', root):
    Display(i)
    
print(SolveGame(root))
            
