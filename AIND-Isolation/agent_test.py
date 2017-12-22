"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import unittest

import isolation
import game_agent

from importlib import reload


class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        


if __name__ == '__main__':
    from isolation import Board
    from game_agent import MinimaxPlayer
    from game_agent import AlphaBetaPlayer
    player1 = AlphaBetaPlayer()
    player2 = MinimaxPlayer()
    game = Board(player1, player2)

    game.apply_move((3,3))
    game.apply_move((0,1))
    game.apply_move((4,5))
    game.apply_move((1,3))
    
    print(game.to_string())
    assert(player1 == game.active_player)
    print(game.get_legal_moves())
    print(player1.get_move(game, 15))