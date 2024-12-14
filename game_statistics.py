class GameStatistics:

    # Tracks overall game stats like turns.
    
    def __init__(self):
        self.turns = 0

    def increment_turns(self):
        self.turns += 1
        
    def get_turns(self):
        return self.turns


class PlayerStatistics:
    
    # Tracks a player's live score based on hits, misses, and getting hit.
    
    def __init__(self):
        self.score = 0
        
    # updates the score

    def update_score(self, points):
        self.score = max(0, self.score + points)
        # this prevents the score going to less than zero zero
        
    def get_score(self):
        return self.score


class HighScoreManager:

    # Manages the high score file (lowest turns to win).

    def __init__(self, filename="high_score.txt"):
        self.filename = filename
        self.high_score = None #hold the current high score
        self.load_high_score()
        
     # loads high score

    def load_high_score(self):
        try:
            with open(self.filename, "r") as file:
                self.high_score = file.read().strip()
        # error handle
        except FileNotFoundError:
            self.high_score = None
    # saves the high score
    def save_high_score(self, name, score, turns):
        with open(self.filename, "w") as file:
            file.write(f"{name}: {score} points, {turns} turns")
        self.high_score = f"{name}: {score} points,{turns} turns"
