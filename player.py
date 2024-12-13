from board import Board

class Player:
    """
    Represents a player with:
      - a name
      - a personal board (with their ships)
      - a guess board (to track shots at the opponent)
    """
    def __init__(self, player_alias):
        self.name = player_alias
        self.board = Board(player_alias)
        self.guess_board = Board(f"{player_alias}'s Guess Board")
