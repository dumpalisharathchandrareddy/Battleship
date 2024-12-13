from player import Player
from game_statistics import HighScoreManager, GameStatistics
from ship_placement_manager import ShipPlacementManager
from name_validator import NameValidator
from guess_validator import GuessValidator


class PlayerStatistics:
    """
    Tracks a player's score based on hits, misses, and getting hit.
    """
    def __init__(self):
        self.score = 0

    def update_score(self, points):
        self.score += points

    def get_score(self):
        return self.score


class Game:
    """
    Orchestrates the Battleship game:
    - Live score updates for hits, misses, and getting hit
    - Display scores at the end of each turn
    - Display final scores when the game ends
    """
    def __init__(self):
        self.players = []
        self.high_score_manager = HighScoreManager()
        self.statistics = GameStatistics()
        self.player_statistics = {}

    def setup_game(self):
        # Display high score if it exists
        if self.high_score_manager.high_score:
            print(f"Current High Score: {self.high_score_manager.high_score}")

        print("Welcome to Battleship!")
        existing_names = set()

        # Two players
        for i in range(2):
            name = input(f"Enter Player {i + 1}'s name: ").strip()
            name = NameValidator.validate_name(name, existing_names)
            self.players.append(Player(name))
            self.player_statistics[name] = PlayerStatistics()  # Initialize score tracker for each player

        # Ship placement
        for player in self.players:
            print(f"\n{player.name}, let's get your ships on the board.")
            placement_manager = ShipPlacementManager(player)
            placement_manager.manage_placement()

        print("\nAll ships have been placed. Let's start the game!")
        input("Press Enter to begin...")

    def display_scores(self):
        """
        Displays the current scores of both players.
        """
        print("\nCurrent Scores:")
        for player in self.players:
            print(f"{player.name}: {self.player_statistics[player.name].get_score()}")

    def play_game(self):
        turn_number = 0
        while True:
            current_player_idx = turn_number % 2
            opponent_idx = 1 - current_player_idx
            current_player = self.players[current_player_idx]
            opponent_player = self.players[opponent_idx]

            # Display current player's score and guess board at the start of their turn
            print(f"\n{current_player.name}'s Turn")
            print(f"Current Score: {self.player_statistics[current_player.name].get_score()}")
            print(f"{current_player.name}'s Guess Board:")
            current_player.guess_board.display()

            valid_guess = False
            while not valid_guess:
                try:
                    raw_input_coord = input(f"\n{current_player.name}, enter coordinates (e.g. A5 or A,5): ").upper().replace(" ", "")

                    if "," in raw_input_coord:
                        parts = raw_input_coord.split(",")
                        if len(parts) != 2:
                            raise ValueError("Invalid format. Try A5 or A,5.")
                        row = parts[0]
                        col_str = parts[1]
                    else:
                        if len(raw_input_coord) < 2:
                            raise ValueError("Invalid input. Try something like A5.")
                        row = raw_input_coord[0]
                        col_str = raw_input_coord[1:]

                    if not col_str.isdigit():
                        raise ValueError("Column must be a number (0-9).")
                    col = int(col_str)

                    GuessValidator.validate_input(row, col)

                    row_spot = ord(row) - 65
                    cell = opponent_player.board.ocean_matrix[row_spot][col]

                    if cell.status in ["X", "O"]:
                        print("Already tried that spot. Pick another.")
                    else:
                        # Hit or miss
                        if cell.status == "S":
                            cell.mark_hit()
                            print("Hit!")
                            current_player.guess_board.ocean_matrix[row_spot][col].mark_hit()
                            self.player_statistics[current_player.name].update_score(5)  # +5 points for hit
                        else:
                            cell.mark_miss()
                            print("Miss!")
                            current_player.guess_board.ocean_matrix[row_spot][col].mark_miss()
                            self.player_statistics[current_player.name].update_score(-1)  # -1 point for miss

                        valid_guess = True

                except (ValueError, IndexError) as err:
                    print(f"Error: {err}, try again.")

            # Opponent loses points for getting hit
            self.player_statistics[opponent_player.name].update_score(-1)

            # Check if opponent lost all ships
            if opponent_player.board.remaining_ships() == 0:
                print(f"{current_player.name} wins the game!")
                print("\nFinal Scores:")
                for player in self.players:
                    print(f"{player.name}: {self.player_statistics[player.name].get_score()}")
                break

            # Display scores after each turn
            self.display_scores()

            # Pass turn to other player
            input(f"\n{current_player.name}, press Enter to pass the turn to the other player...")

            turn_number += 1

    def start(self):
        self.setup_game()
        self.play_game()
