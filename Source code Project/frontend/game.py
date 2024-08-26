import pygame
import sys
import random
import time
from .pieces import Rook, Queen, Pawn, Knight, King, Bishop
from typing import Optional
from logic.game import GameState, chessLogic, Action
from enum import Enum
from frontend import settings
from logic.attributes import Action, Move, QueenPromote, EnterTower
from algorithms.searchAlgo import MinMaxAlgo, SearchAlgo, AlphaBetaAlgo
from algorithms.heuristic import Heuristic, MovingMatrixAndMaterialHeuristic

class Square:
	def __init__(self, x, y, width, height):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

		self.abs_x = y * width
		self.abs_y = x * height
		self.abs_pos = (self.abs_x, self.abs_y)
		self.pos = (x, y)
		self.color = 'light' if (x + y) % 2 == 0 else 'dark'
		self.draw_color = (220, 189, 194) if self.color == 'light' else (53, 53, 53)
		self.highlight_color = (100, 249, 83) if self.color == 'light' else (0, 228, 10)
		self.occupying_piece = None
		self.coord = self.get_coord()
		self.highlight = False

		self.rect = pygame.Rect(
			self.abs_x,
			self.abs_y,
			self.width,
			self.height
		)


	def get_coord(self):
		columns = 'abcdefgh'
		return columns[self.x] + str(self.y + 1)


	def draw(self, display):
		if self.highlight:
			pygame.draw.rect(display, self.highlight_color, self.rect)
		else:
			pygame.draw.rect(display, self.draw_color, self.rect)

		if self.occupying_piece != None:
			centering_rect = self.occupying_piece.img.get_rect()
			centering_rect.center = self.rect.center
			display.blit(self.occupying_piece.img, centering_rect.topleft)
		


class Turn(Enum):
   WHITE = 0
   BLACK = 1


class Player():
  pass


class Agent(Player):
  def __init__(self):
    pass


class RandomAgent(Agent):
  def __init__(self):
    pass

  def getMove(self, gs: GameState):
    actions = []
    for action in chessLogic.actions(gs):
       actions.append(action)
    return random.choice(actions)
  

class AlgoAgent(Agent):
  def __init__(self, algorithm: SearchAlgo, heuristic: Optional[Heuristic] = None):
    self.algo = algorithm
    self.heuristic = heuristic

  def getMove(self, gs: GameState):
    return self.algo.searchMove(gs)
  

class EasyAgent(AlgoAgent):
  def __init__(self):
    super().__init__(MinMaxAlgo, MovingMatrixAndMaterialHeuristic)

  
  def getMove(self, gs: GameState):
    return self.algo.searchMove(gs, self.heuristic)
  
  
class MediumAgent(AlgoAgent):
  def __init__(self):
    super().__init__(AlphaBetaAlgo, MovingMatrixAndMaterialHeuristic)


  def getMove(self, gs: GameState):
    return self.algo.searchMove(gs, self.heuristic)


class HardAgent(AlgoAgent):
  # def __init__(self, algorithm: SearchAlgo, heuristic: Optional[Heuristic] = None):
  #   super().__init__(algorithm, heuristic)

  # def getMove(self, gs: GameState):
  #   return self.algo.searchMove(gs)
  def __init__(self):
    super().__init__(AlphaBetaAlgo, MovingMatrixAndMaterialHeuristic)

  def getMove(self, gs: GameState):
    return self.algo.searchMove(gs, self.heuristic)


class Person(Player):
  def __init__(self):
    pass


# Game state checker
class GameFrontEnd:
  # option = {
  #    "cVsp": {
  #       "hard": "HardAgent",
  #       "medium": "MediumAgent",
  #       "easy": "EasyAgent",
  #    }
     
  # }

  def initGame(self):
    pygame.init()
    self.screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    self.controller = chessLogic

  def __init__(self):
    self.width = settings.WINDOW_SIZE[0]
    self.height = settings.WINDOW_SIZE[1]
    self.tile_width = self.width // 8
    self.tile_height = self.height // 8
    self.selected_piece = None

    self.gameState =  GameState()
    self.squares = self.generate_squares()
    self.setup_board()
    
    # TODO: Add options to choose which agent to run
    # self.setUpPlayer()
    self.initGame()
  

  def setUpPlayer(self, side, type):
     if side == 'white':
        if type == 'easy': self.player1 = EasyAgent()
        elif type == 'medium': self.player1 = MediumAgent()
        elif type == 'hard': self.player1 = HardAgent()
        self.player2 = RandomAgent()
     if side == 'black':
        self.player1 = RandomAgent()
        if type == 'easy': self.player2 = EasyAgent()
        elif type == 'medium': self.player2 = MediumAgent()
        elif type == 'hard': self.player2 = HardAgent()
     self.players = [self.player1, self.player2]

  def play(self):
    """
      Control turn between agents or between agent and player
    """
    running = True
    while running:
      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            running = False
      # if self.mode == 'agentvsagent':
      #   for event in pygame.event.get():
      #     # Quit the game if the user presses the close button
      self.draw()
      turn = self.gameState.turn
      curPlayer = self.players[turn.value]
      if isinstance(curPlayer, Agent):
        action = curPlayer.getMove(self.gameState)
        if not self.move(action):
          print("Invalid move")
        time.sleep(1)
      else:
        mx, my = pygame.mouse.get_pos()
        for event in pygame.event.get():
          # Quit the game if the user presses the close button
          if event.type == pygame.QUIT:
            running = False
          elif event.type == pygame.MOUSEBUTTONDOWN: 
            # If the mouse is clicked
            if event.button == 1:
              print("clicked: \n")
              print(mx, my)
              self.handle_click(mx,my)

        # if self.is_in_checkmate(Turn.BLACK): # If black is in checkmate
        #   print('White wins!')
        #   running = False
        # elif board.is_in_checkmate('white'): # If white is in checkmate
        #   print('Black wins!')
        #   running = False
        # # Draw the board
      # self.draw()
      # running = not self.controller.isTerminal(self.gameState)


  def move(self, action:Action):
    for i in self.squares:
      i.highlight = False
    #clear selected piece
    self.selected_piece = None

    # TODO: 
    # check if type of action is Move: 
        # + check valid: is a piece && valid move
        # + move piece to target pos
        # + make move by call controller to update gameState
    # if type of action is QuenPromote:
        # + check valid: is a piece && valid move
        # + move piece to target pos
        # + promote from pawn to Queen
        # + make move by call controller to update gameState
    # if type is EnterTower:
        # + check valid: is a piece && valid move
        # + move those piece to target pos
        # + make move by call controller to update gameState

    # TODO: Check if is valid piece and run valid move
    pos_square =  self.get_square_from_pos(action.pos)
    tar_square = self.get_square_from_pos(action.tar)

    piece =  pos_square.occupying_piece
    if not piece:
      return False
    is_valid_move = self.controller.checkValidMove(self.gameState, action)
    if not is_valid_move:
      return False

    # TODO: Move piece/ promote queen
    pos_square.occupying_piece = None
    piece.pos = action.tar
    piece.x = action.tar[0]
    piece.y = action.tar[1]
    tar_square.occupying_piece = piece

    if isinstance(action, QueenPromote):
      tar_square.occupying_piece = Queen(
              action.tar, Turn.WHITE if piece.side.value == 0 else Turn.BLACK, self
            )
    elif isinstance(action, EnterTower):
      rPos_square =  self.get_square_from_pos(action.rPos)
      rTar_square = self.get_square_from_pos(action.rTar)
      rPiece =  rPos_square.occupying_piece
      if not rPiece:
        return False
      
      rPos_square.occupying_piece = None
      rPiece.pos = action.rTar
      rPiece.x = action.rTar[0]
      rPiece.y = action.rTar[1]
      rTar_square.occupying_piece = rPiece

    tar_square.highlight = True
    # TODO: Update gameState
    self.gameState = self.controller.move(self.gameState, action)
    if self.controller.isTerminal(self.gameState):
      print(f"Player {1-self.gameState.turn.value} win")
      print(self.board_to_string())
      sys.exit()
    print(self.board_to_string())
    print(self.gameState.turn)
    return True
      

  def generate_squares(self):
    output = []
    for x in range(8):
      for y in range(8):
        output.append(
          Square(x,  y, self.tile_width, self.tile_height)
        )
    return output


  def get_square_from_pos(self, pos):
    for square in self.squares:
      if (square.x, square.y) == (pos[0], pos[1]):
        return square


  def get_piece_from_pos(self, pos):
    return self.get_square_from_pos(pos).occupying_piece


  def setup_board(self):
    # iterating 2d list
    for x, row in enumerate(self.gameState.board):
      for y, piece in enumerate(row):
        if piece != '':
          print(x,y,piece)
          square = self.get_square_from_pos((x, y))

          # looking inside contents, what piece does it have
          if piece[1] == 'R':
            square.occupying_piece = Rook(
              (x, y), Turn.WHITE if piece[0] == 'w' else Turn.BLACK, self
            )
          # as you notice above, we put `self` as argument, or means our class Board

          elif piece[1] == 'N':
            square.occupying_piece = Knight(
              (x, y), Turn.WHITE if piece[0] == 'w' else Turn.BLACK, self
            )

          elif piece[1] == 'B':
            square.occupying_piece = Bishop(
              (x, y), Turn.WHITE if piece[0] == 'w' else Turn.BLACK, self
            )

          elif piece[1] == 'Q':
            square.occupying_piece = Queen(
              (x, y), Turn.WHITE if piece[0] == 'w' else Turn.BLACK, self
            )

          elif piece[1] == 'K':
            square.occupying_piece = King(
              (x, y), Turn.WHITE if piece[0] == 'w' else Turn.BLACK, self
            )

          elif piece[1] == 'P':
            square.occupying_piece = Pawn(
              (x, y), Turn.WHITE if piece[0] == 'w' else Turn.BLACK, self
            )
  def printInfoBoard(self):
    for square in self.squares:
      if square.occupying_piece is not None and square.occupying_piece.notation != None:
         print(square.x, square.y)
         print(square.occupying_piece.x, square.occupying_piece.y, square.occupying_piece.side, square.occupying_piece.notation)

  def handlePerSonMove(self, x_column, y_column):
    if self.selected_piece is None:
      return False
    
    # TODO: prepare suitable action to make move
    action = Move(self.selected_piece.pos,(x_column, y_column))
    if self.selected_piece.notation == ' ' and (x_column == 0  or x_column == 7) :
      action = QueenPromote(self.selected_piece.pos,(x_column, y_column))
    elif self.selected_piece.notation == 'K':
      if self.selected_piece.y - y_column == 2:
        action = EnterTower(self.selected_piece.pos, (self.selected_piece.x, 2), (self.selected_piece.x, 0), (self.selected_piece.x, 3))
      elif self.selected_piece.y - y_column == -2:
        action = EnterTower(self.selected_piece.pos, (self.selected_piece.x, 6), (self.selected_piece.x, 7), (self.selected_piece.x, 5))

    return self.move(action)
  
  def handle_click(self, mx, my):
    x = my // self.tile_width
    y = mx // self.tile_height
    print(x, y)
    clicked_square = self.get_square_from_pos((x, y))
    
    if self.selected_piece is None:
      if clicked_square.occupying_piece is not None:
        if clicked_square.occupying_piece.side.value == self.gameState.turn.value:
          self.selected_piece = clicked_square.occupying_piece
          print(self.selected_piece)

    elif self.handlePerSonMove(x, y):
      # self.gameState.turn = Turn.WHITE if self.gameState.turn == Turn.BLACK else Turn.BLACK
      print("Person play success")

    elif clicked_square.occupying_piece is not None:
      if clicked_square.occupying_piece.side.value == self.gameState.turn.value:
        self.selected_piece = clicked_square.occupying_piece


  def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
    output = False
    king_pos = None

    changing_piece = None
    old_square = None
    new_square = None
    new_square_old_piece = None

    if board_change is not None:
      for square in self.squares:
        if square.pos == board_change[0]:
          changing_piece = square.occupying_piece
          old_square = square
          old_square.occupying_piece = None
      for square in self.squares:
        if square.pos == board_change[1]:
          new_square = square
          new_square_old_piece = new_square.occupying_piece
          new_square.occupying_piece = changing_piece

    pieces = [
      i.occupying_piece for i in self.squares if i.occupying_piece is not None
    ]

    if changing_piece is not None:
      if changing_piece.notation == 'K':
        king_pos = new_square.pos
    if king_pos == None:
      for piece in pieces:
        if piece.notation == 'K' and piece.color == color:
            king_pos = piece.pos
    for piece in pieces:
      if piece.color != color:
        for square in piece.attacking_squares(self):
          if square.pos == king_pos:
            output = True

    if board_change is not None:
      old_square.occupying_piece = changing_piece
      new_square.occupying_piece = new_square_old_piece
            
    return output


  def is_in_checkmate(self, color):
    output = False

    for piece in [i.occupying_piece for i in self.squares]:
      if piece != None:
        if piece.notation == 'K' and piece.color == color:
          king = piece

    if king.get_valid_moves(self) == []:
      if self.is_in_check(color):
        output = True

    return output


  def draw(self):
    self.screen.fill('white')
    if self.selected_piece is not None:
      self.get_square_from_pos(self.selected_piece.pos).highlight = True
      # TODO: hightlight valid moves when click piece
      validMoves = self.controller.getValidMoves(self.gameState, (self.selected_piece.x, self.selected_piece.y))
      # Filter actions with pos is not selected pieces pos
      filterActions = [action for action in validMoves if action.pos == self.selected_piece.pos]
      for action in filterActions:
        square = self.get_square_from_pos(action.tar)
        square.highlight = True
    for square in self.squares:
      square.draw(self.screen)
    pygame.display.update()
  
  def board_to_string(self):
        string =  "    A  B  C  D  E  F  G  H\n"
        string += "    -----------------------\n"
        for x in range(8):
            string += str(8 - x) + " | "
            for y in range(8):
                piece = self.gameState.board[x][y]
                if (piece != ''):
                    string += piece + ' '
                else:
                    string += ".. "
            string += "\n"
        return string + "\n"