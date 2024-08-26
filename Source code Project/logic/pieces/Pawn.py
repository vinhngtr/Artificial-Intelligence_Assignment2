import pygame
from typing import Tuple, List
from logic.attributes import Piece, GameState, QueenPromote, Move, Action

class Pawn(Piece):
  NOTATION = 'P'
#   VALUE = 100
  VALUE = 10
  def __init__(self, pos, color, board):
    super().__init__(pos, color, board)

    img_path = 'data/imgs/' + color[0] + '_pawn.png'
    self.img = pygame.image.load(img_path)
    self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))
    self.notation = 'P'


  def getValidMoves(gc, gs: GameState, pos:Tuple[int], notCheckEndanger: bool = False) -> List[Action]:
    row, col = pos
    player_color = "w" if gs.turn.value == 0 else "b"

    # Check if the piece is valid
    if gs.board[row][col][0] != player_color or  gs.board[row][col][1] != Pawn.NOTATION:
      return []

    valid_moves = []
    # Checking move forward
    diff = 1 if player_color == "b" else -1
    range = 1
    if (row == 1 and player_color == "b") or (row == 6 and player_color == "w"):
      range = 2
    while abs(diff) <= range and not notCheckEndanger: #TO FIX: Fix added capture move to separate
      tar_row = row + diff
      tar_square = gs.board[tar_row][col]
      if tar_square != '':
        break
      if tar_row == 0 or tar_row == 7: #Queen Promotion here
        action = QueenPromote((row,col),(tar_row, col))
      else:
        action = Move((row,col),(tar_row, col))
      if not gc._isKingInEndanger(gs, action):
        yield action
      diff += diff 
    
    # Checking capture diagonally
    vector_dict = {
      "w": [(-1,1), (-1,-1)],
      "b": [(1,+1), (1,-1)]
    }
    diagonal_vectors = vector_dict[player_color]
    possible_moves = ((row+diagonal_vectors[0][0], col+diagonal_vectors[0][1]), (row+diagonal_vectors[1][0], col+diagonal_vectors[1][1]))
    for tar_row, tar_col in possible_moves:
      if tar_row > 7 or tar_row < 0 or tar_col > 7 or tar_col < 0:
        continue
      tar_square = gs.board[tar_row][tar_col]
      if tar_row == 0 or tar_row == 7:
        action = QueenPromote((row,col),(tar_row, tar_col))
      else: 
        action = Move((row,col),(tar_row, tar_col))
      if tar_square != '' and tar_square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield  action

	# def get_possible_moves(self, board):
	# 	output = []
	# 	moves = []

	# 	# move forward
	# 	if self.color == 'white':
	# 		moves.append((0, -1))
	# 		if not self.has_moved:
	# 			moves.append((0, -2))

	# 	elif self.color == 'black':
	# 		moves.append((0, 1))
	# 		if not self.has_moved:
	# 			moves.append((0, 2))

	# 	for move in moves:
	# 		new_pos = (self.x, self.y + move[1])
	# 		if new_pos[1] < 8 and new_pos[1] >= 0:
	# 			output.append(
	# 				board.get_square_from_pos(new_pos)
	# 			)

	# 	return output


	# def get_moves(self, board):
	# 	output = []
	# 	for square in self.get_possible_moves(board):
	# 		if square.occupying_piece != None:
	# 			break
	# 		else:
	# 			output.append(square)

	# 	if self.color == 'white':
	# 		if self.x + 1 < 8 and self.y - 1 >= 0:
	# 			square = board.get_square_from_pos(
	# 				(self.x + 1, self.y - 1)
	# 			)
	# 			if square.occupying_piece != None:
	# 				if square.occupying_piece.color != self.color:
	# 					output.append(square)
	# 		if self.x - 1 >= 0 and self.y - 1 >= 0:
	# 			square = board.get_square_from_pos(
	# 				(self.x - 1, self.y - 1)
	# 			)
	# 			if square.occupying_piece != None:
	# 				if square.occupying_piece.color != self.color:
	# 					output.append(square)

	# 	elif self.color == 'black':
	# 		if self.x + 1 < 8 and self.y + 1 < 8:
	# 			square = board.get_square_from_pos(
	# 				(self.x + 1, self.y + 1)
	# 			)
	# 			if square.occupying_piece != None:
	# 				if square.occupying_piece.color != self.color:
	# 					output.append(square)
	# 		if self.x - 1 >= 0 and self.y + 1 < 8:
	# 			square = board.get_square_from_pos(
	# 				(self.x - 1, self.y + 1)
	# 			)
	# 			if square.occupying_piece != None:
	# 				if square.occupying_piece.color != self.color:
	# 					output.append(square)

	# 	return output

	# def attacking_squares(self, board):
	# 	moves = self.get_moves(board)
	# 	# return the diagonal moves 
	# 	return [i for i in moves if i.x != self.x]