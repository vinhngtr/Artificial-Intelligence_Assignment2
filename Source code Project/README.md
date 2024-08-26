
## 1. How to run
There are three modes 'personvspersion', 'personvsagent', 'agentvsagent' for playing game. 
+ Mode personvspersion: people will play by themself
+ Mode personvsagent: people is white piece, black piece is agent
+ Mode agentvsagent: white piece is random agent, black piece is algorithm agent

From root

To use mode personvspersion run
```bash
python main.py --mode personvspersion
```
To use mode personvsagent run
```bash
python main.py --mode personvsagent
```
To use mode agentvsagent run
```bash
python main.py --mode agentvsagent
```

## 2. Heuristic
A heuristic function consider various aspects of the game like pawn structure analysis, king safety evaluation, piece mobility.

Mỗi piece sẽ có một value mang ý nghĩa cho sức mạnh của nó. Và có các table biểu thị số điểm ghi được cho vị trí của các quân cờ trên bàn cờ. Hàm heristic sẽ tính hiệu số điểm của quân trắng và quân đen. Số điểm của mỗi bên được tính bằng tổng số điểm của quân cờ và tổng số điểm tính toán từ các table.

Piece value
```bash
class Queen(Piece):
  NOTATION = 'Q'
  VALUE = 900

```

Piece table
```bash
 PAWN_TABLE = numpy.array([
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ])

    KNIGHT_TABLE = numpy.array([
        [-50, -40, -30, -30, -30, -30, -40, -50],
        [-40, -20,   0,   5,   5,   0, -20, -40],
        [-30,   5,  10,  15,  15,  10,   5, -30],
        [-30,   0,  15,  20,  20,  15,   0, -30],
        [-30,   5,  15,  20,  20,  15,   0, -30],
        [-30,   0,  10,  15,  15,  10,   0, -30],
        [-40, -20,   0,   0,   0,   0, -20, -40],
        [-50, -40, -30, -30, -30, -30, -40, -50]
    ])

    BISHOP_TABLE = numpy.array([
        [-20, -10, -10, -10, -10, -10, -10, -20],
        [-10,   5,   0,   0,   0,   0,   5, -10],
        [-10,  10,  10,  10,  10,  10,  10, -10],
        [-10,   0,  10,  10,  10,  10,   0, -10],
        [-10,   5,   5,  10,  10,   5,   5, -10],
        [-10,   0,   5,  10,  10,   5,   0, -10],
        [-10,   0,   0,   0,   0,   0,   0, -10],
        [-20, -10, -10, -10, -10, -10, -10, -20]
    ])

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
        [-20, -10, -10, -5, -5, -10, -10, -20],
        [-10,   0,   5,  0,  0,   0,   0, -10],
        [-10,   5,   5,  5,  5,   5,   0, -10],
        [  0,   0,   5,  5,  5,   5,   0,  -5],
        [ -5,   0,   5,  5,  5,   5,   0,  -5],
        [-10,   0,   5,  5,  5,   5,   0, -10],
        [-10,   0,   0,  0,  0,   0,   0, -10],
        [-20, -10, -10, -5, -5, -10, -10, -20]
    ])

    KING_TABLE = numpy.array([
        [20, 30, 10,  0,  0, 10, 30, 20],
        [20, 20,  0,  0,  0,  0, 20, 20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30]
    ])
```


## 3. Todos
+ [ ] Options for running agents.
    + [x] Display UI/UX.
    + [ ] Display time up.
+ [ ] Optimize for searching.
  + [x] unmove()
  + [x] Review heuristic function.
  + [ ] Optimize heuristic function
+ [x] Time up while searching for agent.
+ [x] Utility function. 