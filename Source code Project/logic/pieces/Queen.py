import pygame
from logic.attributes import Piece, GameState, Move, Action
from typing import Tuple, List

class Queen(Piece):
  NOTATION = 'Q'
  # VALUE = 900
  VALUE = 90
  def __init__(self, pos, color, board):
    super().__init__(pos, color, board)

    img_path = 'data/imgs/' + color[0] + '_queen.png'
    self.img = pygame.image.load(img_path)
    self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))
    self.notation = 'Q'

  def getValidMoves(gc, gs: GameState, pos: Tuple[int], notCheckEndanger: bool = False) -> List[Action]:
    row, col = pos
    player_color = "w" if gs.turn.value == 0 else "b"
    # Check if the piece is valid
    if gs.board[row][col][0] != player_color or  gs.board[row][col][1] != Queen.NOTATION:
      return []


    # Move North
    for x in range(row)[::-1]:
      square = gs.board[x][col]
      action = Move((row,col),(x,col))
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if notCheckEndanger or not gc._isKingInEndanger(gs, action):
        yield action

    # Move SouthEast
    for i in range(1, 8):
      tar_row, tar_col = (row+i, col+i)
      if tar_row > 7 or tar_col > 7:
        break
      action = Move((row,col),(tar_row, tar_col))
      square = gs.board[tar_row][tar_col]
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if notCheckEndanger or not gc._isKingInEndanger(gs, action):
        yield action

    # Move East
    for x in range(col + 1, 8):
      square = gs.board[row][x]
      action = Move((row,col),(row,x))
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if notCheckEndanger or not gc._isKingInEndanger(gs, action):
        yield action

    # Move NorthEast
    for i in range(1, 8):
      tar_row, tar_col = (row-i, col+i)
      if tar_row < 0 or tar_col > 7:
        break
      square = gs.board[tar_row][tar_col]
      action = Move((row,col),(tar_row, tar_col))
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if notCheckEndanger or not gc._isKingInEndanger(gs, action):
        yield action

    # Move South
    for x in range(row + 1, 8):
      square = gs.board[x][col]
      action = Move((row,col),(x,col))
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action

    # Move NorthWest
    for i in range(1, 8):
      tar_row, tar_col = (row-i, col-i)
      if tar_row < 0 or tar_col < 0:
        break
      square = gs.board[tar_row][tar_col]
      action = Move((row,col),(tar_row, tar_col)) 
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action

    # Move West
    for y in range(col)[::-1]:
      square = gs.board[row][y]
      action = Move((row,col),(row,y))
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action

    # Move SouthWest
    for i in range(1, 8):
      tar_row, tar_col = (row+i, col-i)
      if tar_row > 7 or tar_col < 0:
        break
      square = gs.board[tar_row][tar_col]
      action = Move((row,col),(tar_row, tar_col))
      if square != "":
        if square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action