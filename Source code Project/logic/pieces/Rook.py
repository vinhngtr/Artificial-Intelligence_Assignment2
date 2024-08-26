import pygame
from typing import Tuple, List
from logic.attributes import Piece, GameState, Move, Action


class Rook(Piece):
  NOTATION = 'R'
  # VALUE = 500
  VALUE = 50
  def __init__(self, pos, color, board):
    super().__init__(pos, color, board)

    img_path = 'data/imgs/' + color[0] + '_rook.png'
    self.img = pygame.image.load(img_path)
    self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))
    self.notation = 'R'


  def getValidMoves(gc, gs: GameState, pos:Tuple[int], notCheckEndanger: bool = False) -> List[Action]:
    row, col = pos
    player_color = "w" if gs.turn.value == 0 else "b"
    # Check if the piece is valid
    if gs.board[row][col][0] != player_color or  gs.board[row][col][1] != Rook.NOTATION:
      return []

    # Upper move checking
    for uI in range(row+1,8):
      target_square = gs.board[uI][col]
      action = Move((row,col), (uI,col))
      if target_square != '':
        if target_square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action
    
    # Lower move checking
    for lI in list(reversed(range(0, row))):
      target_square = gs.board[lI][col]
      action = Move((row,col),(lI,col))
      if target_square != '':
        if target_square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action
      
    # Right move checking
    for rI in range(col+1, 8):
      target_square = gs.board[row][rI]
      action = Move((row,col),(row,rI))
      if target_square != '':
        if target_square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action
    
    # Left move checking
    for lI in list(reversed(range(0,col))):
      target_square = gs.board[row][lI]
      action = Move((row,col),(row,lI))
      if target_square != '':
        if target_square[0] != player_color and (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
          yield action
        break
      if (notCheckEndanger or not gc._isKingInEndanger(gs, action)):
        yield action