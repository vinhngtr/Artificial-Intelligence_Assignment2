from typing import List, Tuple
from logic.attributes import Turn, Action, GameState
from logic.pieces.Rook import Rook
from logic.pieces.Bishop import Bishop
from logic.pieces.Knight import Knight
from logic.pieces.Queen import Queen
from logic.pieces.King import King
from logic.pieces.Pawn import Pawn
from logic.attributes import Action, Move, QueenPromote, EnterTower
import copy
from algorithms import settings


class GameController:
  """
  All logic of the chess game has to communicate to this class
  """

  pieceDict = {
    "R": Rook,
    "B": Bishop,
    "N": Knight,
    "Q": Queen,
    "K": King,
    "P": Pawn,
  }
  def __init__(self):
    pass
  

  def toMove(self, gs: GameState) -> Turn:
    """
    Return player of the state
    """
    return gs.turn
  

  def findPiecesofPlayer(self, gs: GameState, turn: Turn) -> List[Tuple[int]]:
    """
    Find all pieces on board of player in turn
    Return: A tuple with:
      + First ele: An array containing indice of all position of pieces of the player
      + Second ele: A position tuple for the King piece (Used to conveniently check checkmate)
    """
    player_color = "w" if turn == Turn.WHITE else "b"
    player_pieces = []
    king_pos = (None,None)
    for i, row in enumerate(gs.board):
      for j, piece in enumerate(row):
        if piece != "" and piece[0] == player_color:
          if piece[1]=="K":
            king_pos = (i,j)
            continue
          player_pieces.append((i,j))
      
    return (player_pieces, king_pos)

  # def getPiecesFromOpponent(self, gs:GameState) -> List[Tuple[int]]:
  #   opponentColor = "b" if gs.turn.value == 0 else "w"
  #   pieces = []
  #   for i, row in enumerate(gs.board):
  #     for j, piece in enumerate(row):
  #       if piece != '' and piece[0] == opponentColor:
  #         pieces.append((i,j))
  #   return pieces
  def _isKingInEndanger(self, gs:GameState, action: Action) -> bool:
    """
    The function checks if the current position is endangred by "opponentTurn"
    """
    playerColor = "w" if gs.turn == Turn.WHITE else "b"
    gs = copy.deepcopy(gs)
    newGs = self.move(gs, action)
    kRow, kCol = self.findPiecesById(newGs, f"{playerColor}K")[0]
    return self._isEndangered(newGs, (kRow,kCol), newGs.turn)


  def _isEndangered(self, gs:GameState, pos: Tuple, opponentTurn: Turn) -> bool:
    """
    The function checks if the current position is endangered by "opponentTurn"
    """
    opponentPiecesExceptKing, opponentKing = self.findPiecesofPlayer(gs, opponentTurn)
    opponentPieces = opponentPiecesExceptKing + [opponentKing]
    if opponentKing[0] == None: #Opponent does not have a King
      return False
    gs = copy.deepcopy(gs)
    gs.turn = opponentTurn #If it is your turn, Am I endangered ?
    for posRow, posCol  in opponentPieces:
      piece = gs.board[posRow][posCol]
      pieceClass = self.pieceDict[piece[1]]
      if pieceClass == King: # TOFIX: It is a bit odd here 
        for action in pieceClass.getNormalMoves(self, gs, (posRow,posCol), True):
          if action.tar == pos:
            return True       
      else:
        for action in pieceClass.getValidMoves(self, gs, (posRow,posCol), True):
          if action.tar == pos:
            return True 
    return False
    
  
  def actions(self, gs:GameState) -> Action:
    """
    This function returns all moves of pieces, in case "kPos" is given, that means kPos is in danger, only return moves that avoid being captured
    """
    playerPieceIndexes, kingIndex = self.findPiecesofPlayer(gs, gs.turn)
    pieces = playerPieceIndexes + [kingIndex]
    for posRow, posCol  in pieces:
      piece = gs.board[posRow][posCol]
      pieceClass = self.pieceDict[piece[1]]
      
      for action in pieceClass.getValidMoves(self, gs, (posRow,posCol)):
        yield action


  def checkValidMove(self, gs: GameState, action: Action) -> bool:
    row, col = action.pos
    square = gs.board[row][col]
    if square == '':
      return False
    pieceClass = self.pieceDict[square[1]]
    for pieceAction in pieceClass.getValidMoves(self, gs, (row,col)):
      # print(f"{pieceAction.pos} \t {pieceAction.tar}")
      if action == pieceAction:
        return True
    # return True
  
  def move(self, gs: GameState, action: Action) -> GameState:
    turn = Turn.WHITE if gs.turn.value == Turn.BLACK.value else Turn.BLACK
    # TODO: 
    gs = copy.deepcopy(gs)
    pos = action.pos
    tar = action.tar
    board = gs.board
    player_color = "w" if gs.turn.value == 0 else "b"

    piece = board[pos[0]][pos[1]]
    board[pos[0]][pos[1]] = ''
    board[tar[0]][tar[1]] = piece

    # TODO: update value for 
    # self.isEnterTower = [False, False]
    # self.isKingMove = [False,False]
    # self.isRightRockMove = [False, False]
    # self.isLeftRockMove = [False, False]
    if piece.endswith(Rook.NOTATION):
      if pos[1] == 0:
        if player_color == "w":
          gs.isLeftRockMove[0] = True
        else: gs.isLeftRockMove[1] = True
      elif pos[1] == 7:
        if player_color == "w":
          gs.isRightRockMove[0] = True
        else: gs.isRightRockMove[1] = True
    elif piece.endswith(King.NOTATION):
      if isinstance(action, EnterTower):
        if player_color == "w":
          gs.isEnterTower[0] = True
        else: gs.isEnterTower[1] = True
      if player_color == "w":
          gs.isKingMove[0] = True
      else: gs.isKingMove[1] = True

    if isinstance(action, QueenPromote):
      board[tar[0]][tar[1]] = player_color + 'Q'
    elif isinstance(action, EnterTower):
      rPos = action.rPos
      rTar = action.rTar
      rPiece = piece = board[rPos[0]][rPos[1]]
      board[rPos[0]][rPos[1]] = ''
      board[rTar[0]][rTar[1]] = rPiece

    gameState = GameState(board, turn)
    gameState.isEnterTower = gs.isEnterTower
    gameState.isKingMove = gs.isKingMove
    gameState.isLeftRockMove = gs.isLeftRockMove
    gameState.isRightRockMove = gs.isRightRockMove
    
    return gameState
  

  def isTerminal(self, gs:GameState) -> bool:
    """
    Check if the function is terminal
    """  
    # Find the Kings and their positions
    gs = copy.deepcopy(gs)
    for _ in self.actions(gs):
      return False
    return True


  def utility(self, gs:GameState, p:Turn) -> float:
    pass


  def findPiecesById(self, gs:GameState, id: str) -> List[Tuple[int]]:
    """
    + id: "wQ"
    """
    pieces = []
    for i, row in enumerate(gs.board):
      for j, square in enumerate(row):
        if  square == id:
          pieces.append((i,j))
    return pieces


  def getValidMoves(self, gs: GameState, pos:Tuple[int]) -> List[Action]:
    row, col = pos
    board = gs.board
    piece = board[row][col]

    # First check if King is in endanger
    pieceSide, opponentTurn = (Turn.WHITE, Turn.BLACK) if piece[0] == "w" else (Turn.BLACK, Turn.WHITE)
    if piece == '' or gs.turn != pieceSide:
      return []

    pieceClass = self.pieceDict[piece[1]]
    for action in pieceClass.getValidMoves(self, gs, pos):
      yield action

  def isCutOff(self, gs:GameState, depth:int):
    if depth > settings.ALGO_DEPTH:
      return True
    return False 


  def board_to_string(self, board):
    string =  "    A  B  C  D  E  F  G  H\n"
    string += "    -----------------------\n"
    for x in range(8):
        string += str(8 - x) + " | "
        for y in range(8):
            piece = board[x][y]
            if (piece != ''):
                string += piece + ' '
            else:
                string += ".. "
        string += "\n"
    return string + "\n"



chessLogic = GameController()