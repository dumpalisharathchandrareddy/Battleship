class Ship:
    """
    Represents a single ship on the board.
    Each ship has:
      - A ship_name (for identification)
      - A size (how many cells it occupies)
      - A hits counter (how many times it's been hit)

    If hits >= size, the ship is sunk.
    """
    def __init__(self, ship_name, size):
        self.ship_name = ship_name
        self.size = size
        self.hits = 0

    def is_sunk(self):
        return self.hits >= self.size


class GridCell:
    """
    Represents one cell on the game board.
    Possible states for a cell:
      " " = Empty water
      "S" = Ship present in this cell
      "X" = Cell has been hit
      "O" = Missed shot (no ship here)
    """
    def __init__(self):
        self.status = " "

    def mark_hit(self):
        self.status = "X"

    def mark_miss(self):
        self.status = "O"