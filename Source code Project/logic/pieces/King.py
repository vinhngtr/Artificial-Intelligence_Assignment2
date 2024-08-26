import pygame
from typing import Tuple, List
from logic.attributes import Piece, GameState, Turn, Action, Move, EnterTower
import copy 
class King(Piece):
	NOTATION = 'K'
	# VALUE = 20000
	VALUE = 900
	def __init__(self, pos, color, board):
		super().__init__(pos, color, board)

		img_path = 'data/imgs/' + color[0] + '_king.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))


	def enterTower(isRight, gs: GameState, pos: Tuple[int]):
		row, col = pos
		if isRight:
			gs.board[row][6], gs.board[row][col] =  gs.board[row][col], gs.board[row][6]
			gs.board[row][5], gs.board[row][7] =  gs.board[row][7], gs.board[row][5]  
		else:
			gs.board[row][2], gs.board[row][col] =  gs.board[row][col], gs.board[row][2]
			gs.board[row][0], gs.board[row][3] =  gs.board[row][3], gs.board[row][0] 


	def getValidMoves(gc, gs: GameState, pos:Tuple[int]) -> List[Action]:
		actions = []
		for action in King.getNormalMoves(gc, gs, pos):
			actions.append(action)
		return actions + King.getEnterTowerMoves(gc, gs, pos)


	def getNormalMoves(gc, gs: GameState, pos:Tuple[int], notCheckEndanger: bool = False) -> List[Tuple[int]]:
		"""
		gc: is GameController specifically called to check if the King can enter tower
		"""
		row, col = pos
		player_color = "w" if gs.turn.value == 0 else "b"
		# Check if the piece is valid
		if gs.board[row][col][0] != player_color or  gs.board[row][col][1] != King.NOTATION:
			return []

		# Get possible moves without legitimate
		for i in range(-1,2):
			for j in range(-1,2):
				if i == 0 and j == 0:
					continue
				tarRow, tarCol = row+i, col+j
				if tarRow > 7 or tarRow < 0 or tarCol > 7 or tarCol <0:
					continue
				square = gs.board[tarRow][tarCol]
				if square != "" and square[0] == player_color:
					continue
				action = Move((row,col),(tarRow, tarCol))
				if not notCheckEndanger and gc._isKingInEndanger(gs, action):
					continue
				yield action


	def getEnterTowerMoves(gc, gs: GameState, pos:Tuple[int]) -> List[Tuple[int]]:
		# Check enter tower conditions
		row, col = pos
		sideValue = gs.turn.value
		opponentTurn = Turn.WHITE if sideValue == 1 else Turn.BLACK
		isEnterMoveImpossible = gs.isEnterTower[sideValue] or gs.isKingMove[sideValue]
		if isEnterMoveImpossible:
			return []

		# Check if the King is in endanger
		enterTowerMoves = []
		if gc._isEndangered(gs, pos, opponentTurn):
			return []

		# For the right enter tower
		# Check if is the squares on the way to rook placed by any pieces or in endanger
		isRightEnterMoveImpossible = False
		for i in range(col+1,7):
			if gs.board[row][i] != "" or gc._isEndangered(gs, (row,i), opponentTurn):
				isRightEnterMoveImpossible = isRightEnterMoveImpossible or True

		# Check if the King is in endangered if entering tower
		King.enterTower(True, gs, pos)
		if gc._isEndangered(gs, (row,6), opponentTurn):
			isRightEnterMoveImpossible = isRightEnterMoveImpossible or True
		King.enterTower(True, gs, pos)

		if not isRightEnterMoveImpossible:
			enterTowerMoves.append(EnterTower((row,col), (row, 6), (row, 7), (row, 5)))

		# For the left enter tower
		# Check if is the squares on the way to rook placed by any pieces or in endanger
		isLeftEnterMoveImpossible = False
		for i in range(1,col):
			if gs.board[row][i] != "":
				isLeftEnterMoveImpossible = isLeftEnterMoveImpossible or True
			if gc._isEndangered(gs, (row,i), opponentTurn):
				isLeftEnterMoveImpossible = isLeftEnterMoveImpossible or True

		# Check if the King is endangered if entering tower
		King.enterTower(False, gs, pos)
		if gc._isEndangered(gs, (row,2), opponentTurn):
			isLeftEnterMoveImpossible = isLeftEnterMoveImpossible or True
		King.enterTower(False, gs, pos)

		if not isLeftEnterMoveImpossible:
			enterTowerMoves.append(EnterTower((row,col), (row, 2), (row, 0), (row, 3)))
		return enterTowerMoves

