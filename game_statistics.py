class GameStatistics:
    """
    Tracks overall game stats like turns.
    """
    def __init__(self):
        self.turns = 0

    def increment_turns(self):
        self.turns += 1


class PlayerStatistics:
    """
    Tracks a player's live score based on hits, misses, and getting hit.
    """
    def __init__(self):
        self.score = 0

    def update_score(self, points):
        self.score += points

    def get_score(self):
        return self.score


class HighScoreManager:
    """
    Manages the high score file (lowest turns to win).
    """
    def __init__(self, filename="high_score.txt"):
        self.filename = filename
        self.high_score = None
        self.load_high_score()

    def load_high_score(self):
        try:
            with open(self.filename, "r") as file:
                self.high_score = file.read().strip()
        except FileNotFoundError:
            self.high_score = None

    def save_high_score(self, name, turns):
        with open(self.filename, "w") as file:
            file.write(f"{name}: {turns} turns")
        self.high_score = f"{name}: {turns} turns"
