import random
# import numpy as np Did not worked for bitwise

class SameGame:

    def __init__(self):
        self.w = 20
        self.h = 10
        w = self.w
        h = self.h  # 2D array python 3 ve 2 de farklı
        self.score = 0
        self.gameArray = [random.randint(1, 4) for _ in range(w * h)] #Array Kullandım uzunlugu oyunun boyu ve eninin çarpımı



    def select(self, index):
        userSelects = self.gameArray[index]
        selected =  set ()  #list()
        if userSelects == 0: # için boş bir location girerse
           return selected
        selected.add(index) #append(idx)
        groups = self.groupFinder(selected, userSelects)
        while groups:
            selected = selected | groups #Çalışmadı, list yerine set denedim np.bitwise_or(selected,neighbors)
            groups = self.groupFinder(selected, userSelects)
        if len(selected) == 1:
            return set()
        else:
            return selected


    def groupFinder(self, selected, userSelects):
        groups = set() #list() to set NumPy also does not do bitwise comparison between Lists !
        for i in range(len(self.gameArray)): #
            if self.gameArray[i] != userSelects or i in selected:
                continue
            for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                selectedIndex = i + x * self.w + y
                if selectedIndex < 0 or selectedIndex >= self.w * self.h:
                    continue
                if self.gameArray[selectedIndex] == userSelects and selectedIndex in selected:
                    groups.add(i) #append(i)
        return groups



    def pick(self, index,isHintUsed):
        selected = self.select(index)
        if selected:
            for indexes in selected:
                self.gameArray[indexes] = 0 # gruupları sakladık sonra tek tek valuelarını 0 yapalım
            for i in reversed(range(len(self.gameArray))): # reversed sondan başlamasına yarıyor.
                if self.gameArray[i] == 0 and (i - self.w) >= 0: # selectionda yaptığımız 0 ları tek tek aşağı düşürme
                    self.drop(i)
            for i in range(self.w):
                if self.gameArray[(self.h - 1) * self.w + i] == 0:# bütün sütun 0sa  sütunu slide
                    self.slide(i)
            self.score = self.score + (len(selected) - 2)*(len(selected) - 2)

    def drop(self, index):
        i = index - self.w # bir üst hücre indexi
        while i >= 0 and self.gameArray[i] == 0:
            i -= self.w
        if i >= 0:
            self.gameArray[index] = self.gameArray[i] # üstündekini aşağı düşürme
            self.gameArray[i] = 0

    def slide(self, column):
        i = column
        while i < self.w:# Bütün sütunuu kontrol et ' ' boş ? 1:0
            if self.gameArray[(self.h - 1) * self.w + i] != 0:
                break
            i += 1
        if i != self.w: #Break condition occurs
            for j in range(self.h):
                self.gameArray[j * self.w + column] = self.gameArray[j * self.w + i]
                self.gameArray[j * self.w + i] = 0

    def countItem(self, item):
        return self.gameArray.count(item)

Items = [
        ' ', #0 ///This is for printing empty cell that 'd be deleted
        'A', #1
        'B', #2
        'C', #3
        'D', #4

    ]

def printGame(samegame):
    n = 0
    for i, row in enumerate(samegame.gameArray):
        if i % samegame.w == 0:
            print(n, end=' ')
            n += 1
        print(
            Items[samegame.gameArray[i]],
            end=' \n' if i % samegame.w == (samegame.w - 1) else '   '
        )
    print('  ', end='')
    for i in range(samegame.w):
        if i >=10:
            print('{}  '.format(i),end='')
        elif i<=9:
            print('{}   '.format(i), end='')

    print('\n score:{}'.format(samegame.score))
    if(samegame.gameArray[181]== Items[0]):
        samegame.score=samegame.score*5
        return -1 # Meaning for left bottom corner is empty so game ends

def getHint(samegame):
    #Lets check by using brude force with traveling all array.
    max=0
    indexHint=0
    for a in samegame.gameArray:
        lenghtSelect=len(samegame.select(a))
        if max<lenghtSelect:
            indexHint=a
            max=len(samegame.select(a))
    print("Hint indexes are : with Max Select #",max," and Its index is ",indexHint)
    print("Height is ",int(indexHint/samegame.h))
    print("Width is ", (indexHint%samegame.w))
    samegame.score = samegame.score/2


def userInput(samegame):
    while True:
        print("Enter -1 to quit: ")
        print("Enter -2 to get Hint:")
        s = eval(input('Enter the position for Horizantal [0-width]:'))
        d = eval(input('Enter the position for Vertical [0-height]:'))
        if d==-1 or s==-1: # Checks any of input is -1
            return -1   # Then return -1 (This just an identifier)
        if s>samegame.h and s<0 or d>samegame.w and d<0:
          print("You have entered wrong inputs ! ")
          continue
        if s ==-2 or d==-2:
            getHint(samegame)
            continue
        print('\n')
        break
    return s + d * samegame.w


def testMethod(samegame):
    while samegame.w * samegame.h != samegame.countItem(0): # Boşluk sayısı oyun arayinin uzunluguna eşitse !
        if printGame(samegame)==-1:
            print("Congrulagations , You Win !")
            return
        isHintUsed = False
        index = userInput(samegame)
        if index == -1:
            return
        samegame.pick(index,isHintUsed)


if __name__ == "__main__":
    samegame = SameGame()
    testMethod(samegame)
