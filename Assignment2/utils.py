"""
Put the opponent agents and game-running functions in here, they will be used by grader.py

The player's agent is tested against:
1. random agent
2. static evaluation agent

"""
import chess
from math import inf

# Evaluation function used in testing for Q1 and Q2
def evaluation(board: chess.Board, player: bool):
    """
    Simple static evaluation function.
    """
    if board.is_checkmate():
        if player:
            return -inf
        else:
            return inf
    
    SCORES = {
        chess.KING : 200,
        chess.QUEEN : 9,
        chess.ROOK : 5,
        chess.BISHOP : 3,
        chess.KNIGHT : 3,
        chess.PAWN : 1,
    }

    # Creates a dictionary of all the pieces on the board, and counts them
    piece_count = { c : [0] * 7 for c in chess.COLORS }
    for piece in board.piece_map().values():
        piece_count[piece.color][piece.piece_type] += 1

    # Sums the difference in count of each piece type, multiplied by that type's material value
    total = 0
    for piece in chess.PIECE_TYPES:
        if player:
            diff = piece_count[chess.WHITE][piece] - piece_count[chess.BLACK][piece]
        else:
            diff = piece_count[chess.BLACK][piece] - piece_count[chess.WHITE][piece]
        total += SCORES[piece] * diff
    
    return total

# Tests the given adv search and eval function on the given board, returning the chosen top level move
def testAdvSearch(advSearch, evalFunction, board: chess.Board, depth: int):
    # def get_minimax_move(b: chess.Board, eval: function, player: bool, depth: int)
    chosen_move = advSearch(board, evalFunction, True, depth)
    return chosen_move
