from logic.attributes import Turn, GameState, Action, Move, QueenPromote, EnterTower
from .heuristic import Heuristic
from logic.game import chessLogic
from frontend.settings import TIME_IN_TURN
import time
import copy




class SearchAlgo:
    def __init__():
      pass
    
    def searchMove(gs: GameState) -> Action:
        pass


class AlphaBetaAlgo(SearchAlgo):
    INFINITE = 10000000
    
    # def __init__(self, depth = 2):
    #   pass


    def searchMove(gs: GameState, heuristic: Heuristic) -> Action:
        best_move = None
        turn = chessLogic.toMove(gs)
        best_score = MinMaxAlgo.INFINITE if turn == Turn.BLACK else -MinMaxAlgo.INFINITE
        alpha, beta = -MinMaxAlgo.INFINITE, MinMaxAlgo.INFINITE
        count = 1

        print(f"===================Guess for=============================")
        print(f"============================================================")
        eval_value = heuristic.eval(gs)
        
        print(chessLogic.board_to_string(gs.board))
        print(f"Its heuristic value:{eval_value}")
        start_time = time.time()
        for move in chessLogic.actions(gs):
            if time.time() - start_time >= TIME_IN_TURN:
              return best_move
            gsCopy = chessLogic.move(gs, move)

            if turn == Turn.BLACK:
                # print(f"===================Check move {count}========================")
                # print(chessLogic.board_to_string(gsCopy.board))
                # print(f"Current turn: {'White' if gsCopy.turn == Turn.WHITE else 'Black'}")
                score = AlphaBetaAlgo.maxValue(gsCopy, 1, alpha, beta, heuristic)
                
                count += 1
                if (score < best_score): 
                    best_score = score
                    best_move = move
                    beta = min(beta, score)
                # print(f"===================Traceback to========================")
                # print(chessLogic.board_to_string(gsCopy.board))
                # print(f"Its heuristic value:{score}")
                # print(f"Current best score:{best_score}")
                # print(f"Current best move: {best_move.pos} {best_move.tar}")
                    
            else: 
                score = AlphaBetaAlgo.minValue(gsCopy, 1, alpha, beta, heuristic)
                if (score > best_score):
                    best_score = score
                    best_move = move
                    alpha = max(alpha, score)
            # print(score)

        return best_move
    

    def maxValue(gs: GameState, depth:int, alpha, beta, heuristic: Heuristic):
        if chessLogic.isCutOff(gs, depth): #or chessLogic.isTerminal(gs)
            return heuristic.eval(gs)
        
        best_score = - MinMaxAlgo.INFINITE
        count = 1
        for move in chessLogic.actions(gs):
            newGs = chessLogic.move(gs, move)
            # print(f"===================Check move {count}========================")
            # print(chessLogic.board_to_string(newGs.board))
            # print(f"maxValue")
            # print(f"Current turn: {'White' if newGs.turn == Turn.WHITE else 'Black'}")

            score = AlphaBetaAlgo.minValue(newGs, depth+1, alpha, beta, heuristic)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            # print(f"===================Traceback to========================")
            # print(chessLogic.board_to_string(newGs.board))
            # print(f"Its heuristic value:{score}")
            # print(f"Current best score:{best_score}")
            # print(f"Alpha: {alpha} \t Beta: {beta}")
            count += 1
            if beta <= alpha:
                break  # Beta cutoff

        return best_score
    

    def minValue(gs: GameState, depth, alpha, beta, heuristic):
        if chessLogic.isCutOff(gs, depth):
            return heuristic.eval(gs)
        
        best_score = MinMaxAlgo.INFINITE
        gs = copy.deepcopy(gs)
        count = 1
        for move in chessLogic.actions(gs):
            newGs = chessLogic.move(gs, move)
            # print(f"===================Check move {count}========================")
            # print(chessLogic.board_to_string(newGs.board))
            # print(f"minValue")
            # print(f"Current turn: {'White' if newGs.turn == Turn.WHITE else 'Black'}")
            score = AlphaBetaAlgo.maxValue(newGs, depth+1, alpha, beta, heuristic)
            best_score = min(best_score, score)
            beta = min(beta, score)
            # print(f"===================Traceback to========================")
            # print(chessLogic.board_to_string(newGs.board))
            # print(f"Its heuristic value:{score}")
            # print(f"Current best score:{best_score}")
            # print(f"Alpha: {alpha} \t Beta: {beta}")
            count += 1
            if beta <= alpha:
                break  # Alpha cutoff

        return best_score
    

class MinMaxAlgo(SearchAlgo):
    INFINITE = 10000000

    # def __init__(self):
    #   pass


    def searchMove(gs: GameState, heuristic: Heuristic) -> Action:
        best_move = None
        turn = gs.turn
        best_score = MinMaxAlgo.INFINITE if turn == Turn.BLACK else -MinMaxAlgo.INFINITE
        start_time = time.time()
        for move in chessLogic.actions(gs):
            # if not chessLogic.checkValidMove(gsCopy, move):
            #     continue
            # eval_value = Heuristic.eval(gs)
            
            # print(chessLogic.board_to_string(gs.board))
            # print(eval_value)
            gsCopy = chessLogic.move(gs, move)
            # print(chessLogic.board_to_string(gsCopy.board))

            if turn == Turn.WHITE:
                score = MinMaxAlgo.minValue(gsCopy, 1, heuristic)
                if (score > best_score):
                    best_score = score
                    best_move = move
            else: 
                score = MinMaxAlgo.maxValue(gsCopy, 1, heuristic)
                if (score < best_score):
                    best_score = score
                    best_move = move
            # print(score)

            if time.time() - start_time >= TIME_IN_TURN:
              return best_move

        return best_move
    
    
    def maxValue(gs: GameState, depth, heuristic: Heuristic):
        if chessLogic.isCutOff(gs, depth):
            return heuristic.eval(gs)
        
        best_score = - MinMaxAlgo.INFINITE
        for move in chessLogic.actions(gs):
            newGs = chessLogic.move(gs, move)

            score = MinMaxAlgo.minValue(newGs, depth+1, heuristic)
            best_score = max(best_score, score)

        return best_score
    

    def minValue(gs: GameState, depth, heuristic: Heuristic):
        if chessLogic.isCutOff(gs, depth):
            return heuristic.eval(gs)
        
        best_score = MinMaxAlgo.INFINITE
        for move in chessLogic.actions(gs):
            newGs = chessLogic.move(gs, move)

            score = MinMaxAlgo.maxValue(newGs, depth+1, heuristic)
            best_score = min(best_score, score)

        return best_score