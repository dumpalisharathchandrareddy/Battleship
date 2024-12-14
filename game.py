from player import Player
from game_statistics import HighScoreManager, GameStatistics
from ship_placement_manager import ShipPlacementManager
from name_validator import NameValidator
from guess_validator import GuessValidator
from game_statistics import PlayerStatistics
from board import Board

class Game:
    """
    Handles the Battleship game:
    - Tracks player scores and turns
    - Runs the game loop
    - Ends the game when one player wins
    """
    def __init__(self):
        self.players = []  # List of players
        self.high_score_manager = HighScoreManager()  # Handles high scores
        self.statistics = GameStatistics()  # Tracks game stats like turns
        self.player_statistics = {}  # Tracks scores for each player

    def setup_game(self):
        """
        Prepares the game:
        - Shows high score
        - Gets player names
        - Handles ship placements
        """
        if self.high_score_manager.high_score:
            print(f"Current High Score: {self.high_score_manager.high_score}")

        print("Welcome to the SHARATH's Battleship!")
        existing_names = set()  # Keeps track of player names to avoid duplicates

        # Set up players
        for i in range(2):
            name = input(f"Please Enter the Player {i + 1}'s name: ").strip()
            name = NameValidator.validate_name(name, existing_names)  # Validate name
            self.players.append(Player(name))  # Create player
            self.player_statistics[name] = PlayerStatistics()  # Initialize score tracker

        # Place ships for each player
        for player in self.players:
            print(f"Heyhe \n{player.name}, it's time to place your ships.")
            placement_manager = ShipPlacementManager(player)
            placement_manager.manage_placement()

        print("\nAll ships have been placed. Let's start the game!")
        input("Press Enter/ Any Key to begin...")

    def display_scores(self):
        
        # Shows current scores for both players.
    
        print("\nCurrent Scores:")
        for player in self.players:
            print(f"{player.name}: {self.player_statistics[player.name].get_score()}")

    def display_final_boards(self):
        """
        Shows both players' boards at the end of the game.
        """
        print("\nFinal Boards:")
        for player in self.players:
            print(f"\n{player.name}'s Board:")
            player.board.display(show_ships=True)

    def play_game(self):
        """
        Runs the game loop:
        - Players take turns guessing
        - Updates boards and scores
        - Ends the game when one player loses all ships
        """
        turn_number = 0  # Keeps track of whose turn it is
        while True:
            self.statistics.increment_turns()  # Increment turn count
            current_player_idx = turn_number % 2  # Get current player's index
            opponent_idx = 1 - current_player_idx  # Get opponent's index
            current_player = self.players[current_player_idx]
            opponent_player = self.players[opponent_idx]

            # Show turn info
            print(f"\n{current_player.name}'s Turn")
            print(f"Current Score: {self.player_statistics[current_player.name].get_score()}")
            
            print(f"\n Remaining Ships of {opponent_player.name}: {opponent_player.board.remaining_ships()}")
            print(f"\n Ships Sunk of {opponent_player.name}: {opponent_player.board.sunk_ships}")
            
            print(f"{current_player.name}'s Guess Board:")
            current_player.guess_board.display()

            # Handle player's guess
            valid_guess = False
            while not valid_guess:
                try:
                    # Get guess input
                    raw_input_coord = input(f"\n{current_player.name}, enter coordinates (e.g. A5 or A,5): ").upper().replace(" ", "")
                    if "," in raw_input_coord:
                        row, col_str = raw_input_coord.split(",")
                    else:
                        row, col_str = raw_input_coord[0], raw_input_coord[1:]
                    col = int(col_str)

                    # Validate the guess
                    GuessValidator.validate_input(row, col)

                    # Check the guessed cell
                    row_spot = ord(row) - 65
                    cell = opponent_player.board.ocean_matrix[row_spot][col]

                    if cell.status in ["X", "O"]:
                        # Guess already made
                        print("Already tried that spot. Pick another.")

                    else:
                        # Process the guess
                        if cell.status == "S":
                            # Hit
                            cell.mark_hit()  # Mark hit on opponent's board
                            print("Hit!")
                            current_player.guess_board.ocean_matrix[row_spot][col].mark_hit()  # Update guess board
                            self.player_statistics[current_player.name].update_score(5)  # Reward for a hit
                            self.player_statistics[opponent_player.name].update_score(-1)  # Penalize opponent for getting hit
                        else:
                            # Miss
                            cell.mark_miss()  # Mark miss on opponent's board
                            print("Miss!")
                            current_player.guess_board.ocean_matrix[row_spot][col].mark_miss()  # Update guess board
                            self.player_statistics[current_player.name].update_score(-1)  # Penalize for a miss

                        valid_guess = True

                except (ValueError, IndexError) as err:
                    # Handle invalid input
                    print(f"Error: {err}, try again.")

            # # Deduct points from the opponent if they got hit
            # self.player_statistics[opponent_player.name].update_score(-1)

            # Check if the opponent has any ships left
            if opponent_player.board.remaining_ships() == 0:
                print(f"\n{current_player.name} wins the game!")
                print("\nFinal Scores:")
                self.display_scores()
                self.display_final_boards()
                
                # Save high score if applicable
                if self.high_score_manager.high_score:
                    high_score_turns = int(self.high_score_manager.high_score.split(": ")[1].split(" ")[0])
                    if self.statistics.get_turns() < high_score_turns:
                        self.high_score_manager.save_high_score(current_player.name, self.statistics.get_turns())
                else:
                    self.high_score_manager.save_high_score(current_player.name, self.statistics.get_turns())
                
                break

            # Show scores and pass the turn
            self.display_scores()
            input(f"\n{current_player.name}, press Enter to pass the turn to the other player...")
            turn_number += 1

    def start(self):
        """
        Starts the game:
        - Sets up players and boards
        - Runs the game loop
        """
        self.setup_game()
        self.play_game()
