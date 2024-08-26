import numpy
from logic.pieces.Rook import Rook
from logic.pieces.Bishop import Bishop
from logic.pieces.Knight import Knight
from logic.pieces.Queen import Queen
from logic.pieces.King import King
from logic.pieces.Pawn import Pawn
from logic.attributes import GameState

class Heuristic:
  @staticmethod
  def eval(gs: GameState):
    pass

class MovingMatrixAndMaterialHeuristic(Heuristic):

    # The tables denote the points scored for the position of the chess pieces on the board.

    PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ])

    # ROOK_TABLE = numpy.array([
    #     [ 0,  0,  0,  0,  0,  0,  0,  0],
    #     [ 5, 10, 10, 10, 10, 10, 10,  5],
    #     [-5,  0,  0,  0,  0,  0,  0, -5],
    #     [-5,  0,  0,  0,  0,  0,  0, -5],
    #     [-5,  0,  0,  0,  0,  0,  0, -5],
    #     [-5,  0,  0,  0,  0,  0,  0, -5],
    #     [-5,  0,  0,  0,  0,  0,  0, -5],
    #     [ 0,  0,  0,  5,  5,  0,  0,  0]
    # ])
    ROOK_TABLE = numpy.array([
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    QUEEN_TABLE = numpy.array([
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ])

    KING_TABLE = numpy.array([
        [ 20, 30, 10,  0,  0, 10, 30, 20],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30]
    ])

    @staticmethod
    def eval(gs: GameState):
        heuristic = MovingMatrixAndMaterialHeuristic
        material = heuristic.get_material_score(gs)
        

        pawns = heuristic.get_piece_position_score(gs, Pawn.NOTATION, heuristic.PAWN_TABLE)
        knights = heuristic.get_piece_position_score(gs, Knight.NOTATION, heuristic.KNIGHT_TABLE)
        bishops = heuristic.get_piece_position_score(gs, Bishop.NOTATION, heuristic.BISHOP_TABLE)
        rooks = heuristic.get_piece_position_score(gs, Rook.NOTATION, heuristic.ROOK_TABLE)
        queens = heuristic.get_piece_position_score(gs, Queen.NOTATION, heuristic.QUEEN_TABLE)
        kings = heuristic.get_piece_position_score(gs, King.NOTATION, heuristic.KING_TABLE)

        pawn_structure_bonus = 0
        for col in range(8):
            white_pawns = sum(1 for row in range(0, 6) if gs.board[row][col] == 'wP')
            black_pawns = sum(1 for row in range(2, 8) if gs.board[row][col] == 'bP')
            pawn_structure_bonus += (white_pawns - black_pawns) * 5
    
        mobility_bonus = 0
        # Calculate mobility bonus for both sides (simple piece count)
        white_mobility = sum(len(list(gs.board[row])) for row in range(8) if gs.board[row][0].startswith("w"))
        black_mobility = sum(len(list(gs.board[row])) for row in range(8) if gs.board[row][0].startswith("b"))
        mobility_bonus += white_mobility - black_mobility
        
        #late game, change heuristic funtion

        return material + pawns + knights + bishops + rooks + queens + kings + pawn_structure_bonus + mobility_bonus

    # Returns the score for the position of the given type of piece.
    # A piece type can for example be: pieces.Pawn.PIECE_TYPE.
    # The table is the 2d numpy array used for the scoring. Example: Heuristics.PAWN_TABLE
    @staticmethod
    def get_piece_position_score(gs: GameState, piece_notation, table):
      white = 0
      black = 0
      for x in range(8):
          for y in range(8):
              piece = gs.board[x][y]
              if (piece != ''):
                  if piece.endswith(piece_notation):
                      if (piece.startswith("w")):
                          white += table[x][y]
                      else:
                          black += table[7 - x][y]

      return white - black

    @staticmethod
    def get_material_score(gs: GameState):
        white = 0
        black = 0
        for x in range(8):
            for y in range(8):
                piece = gs.board[x][y]
                score = 0
                if (piece != ''):
                    if piece.endswith(King.NOTATION):
                        score = King.VALUE
                    elif piece.endswith(Queen.NOTATION):
                        score = Queen.VALUE
                    elif piece.endswith(Rook.NOTATION):
                        score = Rook.VALUE
                    elif piece.endswith(Bishop.NOTATION):
                        score = Bishop.VALUE
                    elif piece.endswith(Knight.NOTATION):
                        score = Knight.VALUE
                    elif piece.endswith(Pawn.NOTATION):
                        score = Pawn.VALUE

                    if (piece.startswith("w")):
                        white += score
                    else:
                        black += score
                    score = 0

        return white - black


        