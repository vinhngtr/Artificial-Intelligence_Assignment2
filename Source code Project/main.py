import argparse
from frontend.game import GameFrontEnd
from logic.game import chessLogic
from logic.attributes import Turn, GameState, QueenPromote, EnterTower, Move
from algorithms.heuristic import Heuristic
from algorithms.searchAlgo import MinMaxAlgo

def main():
  # parser = argparse.ArgumentParser(description='Select Agent to fight with Random Agent:')
  # parser.add_argument("-m", '--mode', choices=['personvspersion', 'personvsagent', 'agentvsagent'], default='agentvsagent', help='Specify mode game to run')
  # args = parser.parse_args()

  print("Welcome to the chess!")
  agent_side = input("Please choose number of this chess match (\"white\" and \"black\"): ")
  
  if agent_side != 'white' and agent_side != 'black':
    print("Invalid agent side input!")
    return
  
  agent_type = input("Please choose the agent type (\"easy\", \"medium\" and \"hard\"): ")
  if agent_type != 'easy' and agent_side != 'medium' and agent_side != 'hard':
    print("Invalid agent type input!")

  game = GameFrontEnd()
  game.setUpPlayer(agent_side, agent_type)
  game.printInfoBoard()
  game.play()

  # board = [
  #   ['bR','','','','','bK','','bR'],
  #   ['bP', '','bP','','','bP','',''],
  #   ['bP','','','','','','','bP'],
  #   ['','','bB','','','','',''],
  #   ['','','','bP','','bN','',''],
  #   ['','','','bN','','','wK','bP'],
  #   ['', '','','','','bP','',''],
  #   ['', '','','','','','',''],
  # ]
  # turn = Turn.WHITE

  # gs = GameState(board, turn)
  # # # eval_value = Heuristic.eval(gs)
  # # # print(eval_value)
  # gc = chessLogic
  # # search_algo = MinMaxAlgo()
  # # move = search_algo.searchMove(gs)
  # # print(f"{move.pos} {move.tar}")
  # # hello = gc.isTerminal(gs)
  # # print(hello)
  # print(gc.isTerminal(gs))

if __name__ == '__main__':
  main()


