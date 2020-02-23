import random
import os
from time import sleep
from copy import deepcopy
from tensorflow.keras.utils import Progbar
class GameBoard:
	def __init__(self, n):
		self.gameBoard = [[0 for i in range(n)] for j in range(n)]
		self.visited = [[False for i in range(n)] for j in range(n)]
		self.size = n
		self.location = [0,0]
		self.visited[0][0]=True
		self.printLocation = False
		return
	def __repr__(self):
		string = ""
		for rowLoc in range(self.size):
			string += ("|")
			for colLoc in range(self.size):
				if self.printLocation and [rowLoc,colLoc] == self.location:
					string += ("XX ")
				elif self.gameBoard[rowLoc][colLoc] > 9:
					string += (str(self.gameBoard[rowLoc][colLoc]) + " ")
				else:
					string += (" " + str(self.gameBoard[rowLoc][colLoc]) + " ")
			string += ("|\n")
		return string
	def setTile(self,row,col,value):
		if not self.__sizeCheck(row,col,value): raise
		self.gameBoard[row][col] = value
		return
	def randomInit(self):
		for rowLoc in range(self.size):
			for colLoc in range(self.size):
				self.gameBoard[rowLoc][colLoc] = random.randint(1,max(self.size-rowLoc-1,self.size-colLoc-1,colLoc-1,rowLoc-1))
		self.gameBoard[self.size-1][self.size-1] = 0
		return
	def setTileRandomly(self,row,col):
		self.setTile(row,col,random.randint(1,max(self.size-row-1,self.size-col-1,col-1,row-1)))
		return
	def getTile(self,row,col):
		if not self.__sizeCheck(row,col): raise
		return self.gameBoard[row][col]
	def __sizeCheck(self, row, col, val = None):
		if row >= self.size or col >= self.size:
			return False
		if val != None and val >= self.size:
			return False
		if row < 0 or col < 0:
			return False
		if val != None and val < 0:
			return False
		return True
	def move(self, direction):
		amount = self.gameBoard[self.location[0]][self.location[1]]
		if direction == "up":
			if not self.__sizeCheck(self.location[0]-amount,self.location[1]): raise
			self.location[0] -= amount
			return self.location
		if direction == "down":
			if not self.__sizeCheck(self.location[0]+amount,self.location[1]): raise
			self.location[0] += amount
			return self.location
		if direction == "left":
			if not self.__sizeCheck(self.location[0],self.location[1]-amount): raise
			self.location[1] -= amount
			return self.location
		if direction == "right":
			if not self.__sizeCheck(self.location[0],self.location[1]+amount): raise
			self.location[1] += amount
			return self.location
		raise
	def legalMoves(self, row, col):
		moves = []
		amount = self.gameBoard[row][col]
		if self.__sizeCheck(row-amount,col):
			moves.append("up")
		if self.__sizeCheck(row+amount,col):
			moves.append("down")
		if self.__sizeCheck(row,col-amount):
			moves.append("left")
		if self.__sizeCheck(row,col+amount):
			moves.append("right")
		return moves
	def getLocation(self):
		return self.location		
	def availableTiles(self,row,col):
		moves = self.legalMoves(row,col)
		amount = self.gameBoard[row][col]
		tiles = []
		if "up" in moves:
			tiles.append((row-amount,col))
		if "down" in moves:
			tiles.append((row+amount,col))
		if "left" in moves:
			tiles.append((row,col-amount))
		if "right" in moves:
			tiles.append((row,col+amount))
		return tiles
	def getTargetTile(self):
		return (self.size-1,self.size-1)
	def setLocation(self, row,col):
		if not self.__sizeCheck(row,col): raise
		self.location = [row,col]
	def setVisited(self, row, col):
		if not self.__sizeCheck(row,col): raise
		self.visited[row][col] = True
		return
	def printVisited(self):
		string = ""
		for rowLoc in range(self.size):
			string += ("|")
			for colLoc in range(self.size):
				if self.visited[rowLoc][colLoc]:
					string += ("VV ")
				elif self.gameBoard[rowLoc][colLoc] > 9:
					string += (str(self.gameBoard[rowLoc][colLoc]) + " ")
				else:
					string += (" " + str(self.gameBoard[rowLoc][colLoc]) + " ")
			string += ("|\n")
		print(string)
	def getSize(self):
		return self.size
	def manhattanDistance(self, row, col):
		if not self.__sizeCheck(row,col): raise
		return self.size - row + self.size - col
	def reset(self):
		self.location = [0,0]
		self.visited = [[False for i in range(self.size)] for j in range(self.size)]
		self.visited[0][0]=True
	def getBoard(self):
		return self.gameBoard
	def makeFromCopy(self, board):

		self.gameBoard = deepcopy(board.getBoard())
	def setPrintLocation(self,setState):
		self.printLocation = setState

class OrderedCue:
	def __init__(self):
	 self.cue = []
	 return

	def __repr__(self):
	 return str(self.cue)
	
	def add(self,item,value):
		position = 0
		while position < len(self.cue) and self.cue[position][1] < value:
			position+=1
		self.cue.insert(position,(item,value))
		return

	def pop(self):
		if len(self.cue) == 0:
			return None
		value = self.cue[0][0]
		del(self.cue[0])
		return value
	
	def length(self):
		return len(self.cue)

def AnimateSolution(board,path):
	for item in path:
		board.setLocation(item[0],item[1])
		board.setVisited(item[0],item[1])
		os.system('cls' if os.name == 'nt' else 'clear')
		print(board)
		sleep(1)
	os.system('cls' if os.name == 'nt' else 'clear')
	board.printVisited()
	print("Path:", path)
	board.reset()
	return

def getPath(board, prevTile, animate = False):
	target = board.getTargetTile()
	path = [board.getTargetTile()]
	while target != (0,0):
		path.append(prevTile[target])
		target = prevTile[target]
	if animate:
		path.reverse()
		AnimateSolution(board,path)
	return path

def BFS(board, animate = False):
	cue = []
	visited = []
	prevTile = {}
	target = board.getTargetTile()
	cue.append((0,0))
	solved = False
	while len(cue) > 0:
		currTile = cue[0]
		del(cue[0])
		visited.append(currTile)
		moves = board.availableTiles(currTile[0], currTile[1])
		for tile in moves:
			if tile in visited:
				continue
			cue.append(tile)
			prevTile[tile] = currTile
			if tile == target:
				solved = True
				break
		if solved: break
	if solved:
		path = getPath(board,prevTile,animate)
		return len(path)
	else:
		return -1*board.getSize()*board.getSize() - len(prevTile)
	return

def AStar(board, animate = False):
	cue = OrderedCue()
	visited = []
	prevTile = {}
	cue.add((0,0),board.manhattanDistance(0,0))
	solved = False
	while(cue.length()>0):
		currTile = cue.pop()
		visited.append(currTile)
		tiles = board.availableTiles(currTile[0],currTile[1])
		for tile in tiles:
			if tile in visited:
				continue
			cue.add(tile,board.manhattanDistance(tile[0],tile[1]))
			prevTile[tile] = currTile
			if tile == board.getTargetTile():
				solved = True
				break
		if solved == True:
			break
	if solved == True:
		path = getPath(board,prevTile,animate)
		return len(path)
	return -1*board.getSize()*board.getSize() - len(prevTile)

def getHuristics(board, row, coloumn):
    return board.getTile(row, coloumn) + myGame.manhattanDistance(row, coloumn) - 2

def hillClimbing(oldBoard, evalMethod, iterations = 10000, changesPerIteration = 1):
	size = oldBoard.getSize()
	oldScore = BFS(oldBoard) if evalMethod == "BFS" else AStar(oldBoard)
	currIteration = 0
	loadingBar = Progbar(target = iterations)
	while currIteration < iterations:
		newBoard = GameBoard(size)
		newBoard.makeFromCopy(oldBoard)
		for i in range(changesPerIteration):
			randRow = random.randint(1,size-1)
			randCol = random.randint(1,size-1)
			newBoard.setTileRandomly(randRow,randCol)
		newScore = BFS(newBoard) if evalMethod == "BFS" else AStar(newBoard)
		if newScore > oldScore:
			oldBoard = newBoard
			oldScore = newScore
		loadingBar.add(1)
		currIteration +=1
	return oldBoard, oldScore

def randomGen(oldBoard, evalMethod, iterations = 10000):
	size = oldBoard.getSize()
	oldScore = BFS(oldBoard) if evalMethod == "BFS" else AStar(oldBoard)
	currIteration = 0
	loadingBar = Progbar(target = iterations)
	while currIteration < iterations:
		newBoard = GameBoard(size)
		newBoard.randomInit()
		newScore = BFS(newBoard) if evalMethod == "BFS" else AStar(newBoard)
		if newScore > oldScore:
			oldBoard = newBoard
			oldScore = newScore
		loadingBar.add(1)
		currIteration +=1
	return oldBoard, oldScore

def crossBoards(board1,board2,amount = 10, mutationChance = 10):
	size = board1.getSize()
	boardList = [GameBoard(size) for i in range(size)]
	for row in range(size):
		for col in range(size):
			b1Cell = board1.getTile(row,col)
			b2Cell = board2.getTile(row,col)
			for board in boardList:
				if random.randint(1,mutationChance) == 0:
					board.setTileRandomly(row,col)
				elif random.randint(0,1) == 0:
					board.setTile(row,col,b1Cell)
				else:
					board.setTile(row,col,b2Cell)
	return boardList

def geneticAlgorithm(board1, evalMethod, iterations = 10000, mutationRate = 10):
	size = board1.getSize()
	board2 = GameBoard(size)
	board2.randomInit()
	currIteration = 0
	loadingBar = Progbar(target = iterations)
	while currIteration < iterations:
		candidates = crossBoards(board1,board2, mutationChance = mutationRate)
		board1 = candidates[0]
		board2 = candidates[1]
		score1 = BFS(board1) if evalMethod == "BFS" else AStar(board1)
		score2 = BFS(board2) if evalMethod == "BFS" else AStar(board2)
		for board in candidates[2:]:
			bScore = BFS(board) if evalMethod == "BFS" else AStar(board)
			if bScore > score1:
				score2 = score1
				score1 = bScore
				board2 = board1
				board1 = board
			elif bScore > score2:
				board2 = board
				score2 = bScore
		loadingBar.add(1)
		currIteration+=1
	if score1>score2:
		return board1, score1
	return board2, score2

myGame = GameBoard(int(input("Enter map size: ")))
evalMethod = input("Enter BFS or A*: ")
iterations = int(input("Number of puzzle creation iterations to perform: "))
mutationRate = int(input("1 our of x chance of genetic mutation: "))
changesPerIteration = int(input("Number of changes to make to board every iteration during hill climbing: "))
myGame.randomInit()
print("Initial Maze:")
IM = myGame
IMScore = BFS(myGame) if evalMethod == "BFS" else AStar(myGame)
print("Best path:", IMScore)
print("Hill Climbing:")
HC = hillClimbing(myGame, evalMethod, iterations = iterations, changesPerIteration = changesPerIteration)
HCScore = HC[1]
HC = HC[0]
print("Best path:", HCScore)
print("Genetic Algorithm:")
GA = geneticAlgorithm(myGame, evalMethod, iterations = iterations, mutationRate = mutationRate)
GAScore = GA[1]
GA = GA[0]
print("Best path:", GAScore)
print("Random Generation:")
RG = randomGen(myGame, evalMethod, iterations = iterations)
RGScore = RG[1]
RG = RG[0]
print("Best path:", RGScore)

if input("Print Initial Maze (Y/N): ") == "Y":
	print(IM)
if input("Print Hill Climbing Maze (Y/N): ") == "Y":
	print(HC)
if input("Print Genetic Algorithm Maze (Y/N): ") == "Y":
	print(GA)
if input("Print Random Generation Maze (Y/N): ") == "Y":
	print(RG)

if input("Print solution to Initial Maze (Y/N): ") == "Y":
	IM.setPrintLocation(True)
	BFS(IM, animate = True) if evalMethod == "BFS" else AStar(IM, animate = True)
if input("Print solution to Hill Climbing Maze (Y/N): ") == "Y":
	HC.setPrintLocation(True)
	BFS(HC, animate = True) if evalMethod == "BFS" else AStar(HC, animate = True)
if input("Print solution to Genetic Algorithm Maze (Y/N): ") == "Y":
	GA.setPrintLocation(True)
	BFS(GA, animate = True) if evalMethod == "BFS" else AStar(GA, animate = True)
if input("Print solution to Random Generation Maze (Y/N): ") == "Y":
	RG.setPrintLocation(True)
	BFS(RG, animate = True) if evalMethod == "BFS" else AStar(RG, animate = True)