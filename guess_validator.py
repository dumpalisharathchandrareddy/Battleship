class GuessValidator:
    
    # Checks whether a guess (row, col) is valid.
    # Rows: A-Z (first 26 letters) and Columns: 0-9
    
    @staticmethod
    def validate_input(row, col):
        if row not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:26] or not (0 <= col < 10):
            raise ValueError("Coordinates out of range. Use A-Z for row and 0-9 for column.")
        return True
