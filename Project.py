import random
import os
from time import sleep
class GameBoard:
	def __init__(self, n):
		self.gameBoard = [[0 for i in range(n)] for j in range(n)]
		self.visited = [[False for i in range(n)] for j in range(n)]
		self.size = n
		self.location = [0,0]
		self.visited[0][0]=True
		return
	def __repr__(self):
		string = ""
		for rowLoc in range(self.size):
			string += ("|")
			for colLoc in range(self.size):
				if [rowLoc,colLoc] == self.location:
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
		self.setTile(row,col,random.randint(1,self.size-1))
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
		# print(moves)
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
					string += ("XX ")
				elif self.gameBoard[rowLoc][colLoc] > 9:
					string += (str(self.gameBoard[rowLoc][colLoc]) + " ")
				else:
					string += (" " + str(self.gameBoard[rowLoc][colLoc]) + " ")
			string += ("|\n")
		print(string)
	def getSize(self):
		return self.size*self.size
	def manhattanDistance(self, row, col):
		if not self.__sizeCheck(row,col): raise
		return self.size - row + self.size - col

def AnimateSolution(board,path):
	for item in path:
		board.setLocation(item[0],item[1])
		board.setVisited(item[0],item[1])
		os.system('cls' if os.name == 'nt' else 'clear')
		print(board)
		sleep(1)
	os.system('cls' if os.name == 'nt' else 'clear')
	board.printVisited()
	print(path)
	return

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
		target = board.getTargetTile()
		path = [board.getTargetTile()]
		while target != (0,0):
			path.append(prevTile[target])
			target = prevTile[target]
		if animate:
			path.reverse()
			AnimateSolution(board,path)
		return len(path)
	else:
		print("Cannot be solved")
		return -1*board.getSize() - len(prevTile)
	return
myGame = GameBoard(int(input("Enter map size: ")))
myGame.randomInit()
print(BFS(myGame, animate=True))