import pygame

class Piece:
	def __init__(self, pos, side, board):
		self.pos = pos
		self.x = pos[0]
		self.y = pos[1]
		# self.side = "w" if side.value == 0 else "b"
		self.side = side
		self.has_moved = False

class Queen(Piece):
	def __init__(self, pos, side, board):
		super().__init__(pos, side, board)

		img_path = 'frontend/imgs/' + ('w' if self.side.value == 0 else 'b') + '_queen.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'Q'

class Rook(Piece):
	def __init__(self, pos, side, board):
		super().__init__(pos, side, board)

		img_path = 'frontend/imgs/' + ('w' if self.side.value == 0 else 'b') + '_rook.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'R'
		
class Pawn(Piece):
	def __init__(self, pos, side, board):
		super().__init__(pos, side, board)

		img_path = 'frontend/imgs/' + ('w' if self.side.value == 0 else 'b') + '_pawn.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 35, board.tile_height - 35))

		self.notation = ' '
		
class Knight(Piece):
	def __init__(self, pos, side, board):
		super().__init__(pos, side, board)

		img_path = 'frontend/imgs/' + ('w' if self.side.value == 0 else 'b') + '_knight.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'N'
		

class King(Piece):
  def __init__(self, pos, side, board):
    super().__init__(pos, side, board)

    img_path = 'frontend/imgs/' + ('w' if self.side.value == 0 else 'b') + '_king.png'
    self.img = pygame.image.load(img_path)
    self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

    self.notation = 'K'


  def get_valid_moves(self, board):
    output = []
    # for square in self.get_moves(board):
    # 	if not board.is_in_check(self.side, board_change=[self.pos, square.pos]):
    # 		output.append(square)

    # if self.can_castle(board) == 'queenside':
    # 	output.append(
    # 		board.get_square_from_pos((self.x - 2, self.y))
    # 	)
    # if self.can_castle(board) == 'kingside':
    # 	output.append(
    # 		board.get_square_from_pos((self.x + 2, self.y))
    # 	)
    output.append(board.get_square_from_pos((1,2)))
    return output
		

class Bishop(Piece):
	def __init__(self, pos, side, board):
		super().__init__(pos, side, board)

		img_path = 'frontend/imgs/' + ('w' if self.side.value == 0 else 'b') + '_bishop.png'
		self.img = pygame.image.load(img_path)
		self.img = pygame.transform.scale(self.img, (board.tile_width - 20, board.tile_height - 20))

		self.notation = 'B'