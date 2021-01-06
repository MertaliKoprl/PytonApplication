import random
import itertools

class Node:
    def __init__(self, val):
        self.l_child = None
        self.r_child = None
        self.data = val

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):

        # No child.
        if self.r_child is None and self.l_child is None:
            line = '%s' % self.data
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.r_child is None:
            lines, n, p, x = self.l_child._display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.l_child is None:
            lines, n, p, x = self.r_child._display_aux()
            s = '%s' % self.data
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.l_child._display_aux()
        right, m, q, y = self.r_child._display_aux()
        s = '%s' % self.data
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

    def hasLeftChild(self):
        return self.l_child is not None

    def hasRightChild(self):
        return self.r_child is not None

def treeBranchGenerator(root, node,director):
    if root is None:
        root = node
        return root
    else:
        if director == 'N':
            if root.l_child is None:
                root.l_child = node
                return root.l_child
            else:
                return root.l_child
        else:
            if root.r_child is None:
                root.r_child = node
                return root.r_child
            else:
                return root.r_child


def in_order_print(root):
    if not root:
        return
    in_order_print(root.l_child)
    print(root.data)
    in_order_print(root.r_child)


def branchMaker(root,path,result):  # TREE GENERATED
    nextNode= root
    r1=root
    for i in range(0,len(path)): #  'N','N','N' lenght=3  loop to 0 1 2
        if(i == len(path)-1):
            edgeNode = Node(result)
            nextNode =treeBranchGenerator(nextNode,edgeNode,path[i])

        else:
            zeroNode=Node(0)
            nextNode = treeBranchGenerator(nextNode, zeroNode, path[i])


gameArea = []
class Game():

    def __init__(self, N):
        self.N = N
        self.Tree = Node(0)
        self.treePlayer1=self.Tree
        self.treePlayer2=self.Tree
        self.pawnIndex=[self.N-1,0] # x,y
        self.selectionTree = self.treePlayer1
        self.isfinished = False

    def generateGameTree(self):
        for path in combList:
            result = traverseResult(path)
            branchMaker(self.Tree,path,result)
       #print("I AM INITIAL TREE")
        #self.Tree.display()

    def minimaxGameTreeMaker(self,root,maximizing): # depth removed !
        if root.r_child is None and root.l_child is None: ## If there is no left or right depth ==0 return data But IT CAN BE UNBALANCED TREE SOME OF THE ITEMS COULD BE WITH LESS DEPTH !!!
            return root.data
        if maximizing:    ## BECAUSE OF UNBALANCED TREE I HAVE DECIDED TO BASICALLY CHECK IF THERE ARE ANY CHILDREN OR NOT
            if(root.l_child is None):
                root.data = self.minimaxGameTreeMaker(root.r_child, False) # IF WE DONT HAVE ANY RIGHT SO ONLY SELECTION COMES FROM LEFT !!!
            elif(root.r_child is None):
                root.data = self.minimaxGameTreeMaker(root.l_child, False)
            elif root.r_child is not None and root.l_child is not None:
                root.data = max(self.minimaxGameTreeMaker(root.l_child,False),self.minimaxGameTreeMaker(root.r_child,False)) # UPDATING DATA IN NODES
        else:
            if (root.l_child is None):
                root.data = self.minimaxGameTreeMaker(root.r_child, True)
            elif (root.r_child is None):
                root.data = self.minimaxGameTreeMaker(root.l_child, True)
            elif root.r_child is not None and root.l_child is not None:
                root.data=min(self.minimaxGameTreeMaker(root.l_child,True),self.minimaxGameTreeMaker(root.r_child,True))
        return root.data

    def minimaxTreeGenerator(self):
        self.treePlayer1 = self.Tree # This one starts with MAX If Player Pass' its turn go to treePlayer2 find state and make decision!
        self.treePlayer2 = self.Tree # This one starts with MİN
        self.minimaxGameTreeMaker(self.treePlayer1,True) # treePlayer1 Updated Against Player's movement
        self.minimaxGameTreeMaker(self.treePlayer2,False) # treePlayer2 Updated
        # On decision it will be swap when user Pass' its turn so Computer will decide for its benefit.
        # On selection Max user Passes its turn so we can use this term to min selection !!!
        node =self.treePlayer1
        print("-----------------------------------")
        #print("I AM MINIMAX-MAX TREE")
        #node.display()
        print("-----------------------------------")

    def playerDecision(self):
         # select min child on current state !
        kStroked=False
        gameArea[self.pawnIndex[0]][self.pawnIndex[1]]=0 ## MAKE PAWN 0
        pawnX=self.pawnIndex[0]
        pawnY=self.pawnIndex[1]
        currentNode = Node(0)
        for moveindex in range(0,len(playerMovements)):
            if playerMovements[-1] == 'P':## It means Pass
                kStroked= not kStroked
                if kStroked:
                    self.selectionTree = self.treePlayer2
                else:
                    self.selectionTree=self.treePlayer1
            if move == 'N':
                currentNode= self.selectionTree.l_child
                if moveindex==len(playerMovements)-1:
                    pawnX=pawnX-1
            elif move =='E':
                currentNode = self.selectionTree.r_child
                if moveindex==len(playerMovements)-1:
                    pawnY=pawnY+1

        self.pawnIndex[0]=pawnX
        self.pawnIndex[1]=pawnY
        if(self.pawnIndex[0]==0 or self.pawnIndex[1]==self.N-1):
            point = gameArea[self.pawnIndex[0]][self.pawnIndex[1]]
            gameArea[self.pawnIndex[0]][self.pawnIndex[1]] = 'P'
            print("GAME FINISHED ",point," Earned")
            self.printGameArea()
            self.isfinished = True
            return
        else:
            if (currentNode.hasLeftChild() and currentNode.hasRightChild()):
                left = currentNode.l_child
                right = currentNode.r_child
                if left.data >right.data:
                    playerMovements.append('E')
                    print("Computer played E")
                    pawnY = pawnY + 1
                else:
                    playerMovements.append('N')
                    print("Computer played N")
                    pawnX = pawnX -1
            else:
                if currentNode.hasLeftChild():
                    playerMovements.append('N')
                    print("Computer played N")
                    pawnX = pawnX -1
                elif currentNode.hasRightChild():
                    playerMovements.append('E')
                    print("Computer played E")
                    pawnY = pawnY + 1


            self.pawnIndex[0] = pawnX
            self.pawnIndex[1] = pawnY
            if (self.pawnIndex[0] == 0 or self.pawnIndex[1] == self.N - 1):
                point = gameArea[self.pawnIndex[0]][self.pawnIndex[1]]
                gameArea[self.pawnIndex[0]][self.pawnIndex[1]]='P'
                print("GAME FINISHED ",point," EARNED")
                self.printGameArea()
                self.isfinished=True
                return
            else:
                gameArea[self.pawnIndex[0]][self.pawnIndex[1]] = 'P'





    def initializeGame(self):
        for i in range(0, self.N):
            row = []
            for j in range(0, self.N):
                if (i == self.pawnIndex[0] and j == self.pawnIndex[1]):
                    row.append('P')
                elif (i == 0 and j != self.N - 1):
                    row.append(random.randint(-2, 2))
                elif (i == 0 and j == self.N - 1):
                    row.append(0)
                elif (j == self.N - 1):
                    row.append(random.randint(-2, 2))
                else:
                    row.append(0)
            gameArea.append(row)
        solutionSet()
        self.generateGameTree()
        self.minimaxTreeGenerator()



    def printGameArea(self):
        for row in gameArea:
            print(row)



combList = []
stuff = ['N', 'E']
def solutionSet():
    for solutionSet in range(g1.N-1, g1.N+(g1.N-2)): ## N =4 ise min set 3 'den başlar ve max set N+(N-3)' kadar olur.
        for combo in itertools.product(stuff, repeat=solutionSet):
            countN = 0
            countE = 0
            indexGoalN = 0
            indexGoalE = 0
            for iterator in range(0,len(combo)):
                if combo[iterator] == 'N' :
                    countN=countN+1
                    indexGoalN=iterator
                else :
                    countE = countE+1
                    indexGoalE=iterator
                if countN == g1.N-1 and indexGoalN == iterator and indexGoalN==len(combo)-1:
                    combList.append(combo)
                elif countE == g1.N-1 and indexGoalE == iterator and indexGoalE==len(combo)-1:
                    combList.append(combo)
    #print("Possible Solution Space :",combList)

def traverseResult(path):
    x=g1.N-1
    y=0
    gamePoint = 0
    for i in range(0,len(path)):
        if path[i] == 'N':
            x=x-1
        else:
            y=y+1
    return gameArea[x][y]




print("Game ~ AI by Mertali")
N = int(input("Enter the size of Game ?"))
playerMovements=[]
while N <4:
    N = int(input("More then 4 Please , Enter the size of Game ?"))
g1= Game(N)# Input is N
g1.initializeGame()

counter=1
while not g1.isfinished:
    print(counter," gen , Board")
    g1.printGameArea()
    move = input("Make your Move ['N','E','P']. ( N -> North , E -> East , P -> Pass H-> Hint Decision Tree , T -> Game Tree , S -> Possible Solution Paths ) ")
    print(move)
    if move =='H':
        print("------DECISION TREE------")
        g1.selectionTree.display()
        print("-------------------------")
        continue
    elif move =='T':
        print("------GAME TREE------")
        g1.Tree.display()
        print("---------------------")
        continue
    elif move =='S':
        print("------GAME TREE------")
        print(combList)
        print("---------------------")
        continue
    playerMovements.append(move)
    g1.playerDecision()# AI MAKES MOVEMENT ! PRINT STATEMENT !
    counter=counter+1


    ##print(combList) ## MAKE TREE FROM COMB LIST !!!!
print("Bye Bye... ")





