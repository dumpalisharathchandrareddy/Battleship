from ship import Ship, GridCell

class Board:
    """
    Represents a player's board (26 rows by 10 columns).
    Also tracks ship positions to allow removing/modifying a single ship without clearing all.
    """
    def __init__(self, name):
        self.name = name
        self.ocean_matrix = [[GridCell() for _ in range(10)] for _ in range(26)]
        self.fleet_manifest = {}       # ship_name -> Ship object
        self.registered_vessels = []   # list of placed ship names
        self.ship_positions = {}       # ship_name -> list of (row, col) tuples

    def display(self, show_ships=False):
        print(f"\n{self.name}'s Board")
        print("    " + " ".join(map(str, range(10))))
        for i, row_line in enumerate(self.ocean_matrix):
            row_label = chr(65 + i)
            displayed_line = [cell.status if (cell.status != 'S' or show_ships) else " " for cell in row_line]
            print(f"{row_label}   " + " ".join(displayed_line))

    def place_ship(self, ship_name, size):
        done_placing = False
        while not done_placing:
            print(f"Place your {ship_name} (size: {size} cells)")
            print("Enter the coordinate for the MIDDLE cell of the ship (e.g., A,5).")
            try:
                coord_input = input("Enter coordinate (e.g., A,5): ").strip()
                if "," not in coord_input:
                    raise ValueError("Coordinate must be in 'A,5' format.")
                parts = coord_input.split(",")
                if len(parts) != 2:
                    raise ValueError("Invalid coordinate format, use 'A,5'.")

                chosen_row = parts[0].upper()
                chosen_col_str = parts[1]
                if chosen_row not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:26]:
                    raise ValueError("Row out of range (A-Z).")
                if not chosen_col_str.isdigit() or not (0 <= int(chosen_col_str) < 10):
                    raise ValueError("Column out of range (0-9).")

                chosen_col = int(chosen_col_str)
                chosen_direction = input("Enter orientation (H for Horizontal, V for Vertical): ").upper()
                if chosen_direction not in ["H", "V"]:
                    raise ValueError("Orientation must be 'H' or 'V'.")

                row_spot = ord(chosen_row) - 65

                if chosen_direction == "H":
                    start_col = chosen_col - (size // 2)
                    end_col = start_col + size
                    if start_col < 0 or end_col > 10 or any(self.ocean_matrix[row_spot][c].status == "S" for c in range(start_col, end_col)):
                        raise ValueError("Invalid placement: off-board or overlapping.")
                    slots_occupied = [(row_spot, c) for c in range(start_col, end_col)]
                else:
                    start_row = row_spot - (size // 2)
                    end_row = start_row + size
                    if start_row < 0 or end_row > 26 or any(self.ocean_matrix[r][chosen_col].status == "S" for r in range(start_row, end_row)):
                        raise ValueError("Invalid placement: off-board or overlapping.")
                    slots_occupied = [(r, chosen_col) for r in range(start_row, end_row)]

                human_readable = [f"{chr(65 + r)}{c}" for r, c in slots_occupied]
                print(f"{ship_name} would occupy: {', '.join(human_readable)}")
                confirm = input("Confirm placement (Y/N) [default=Y]: ").upper().strip()
                if confirm == "":
                    confirm = "Y"
                if confirm == "Y":
                    for (r, c) in slots_occupied:
                        self.ocean_matrix[r][c].status = "S"
                    self.fleet_manifest[ship_name] = Ship(ship_name, size)
                    self.registered_vessels.append(ship_name)
                    self.ship_positions[ship_name] = slots_occupied
                    done_placing = True
                    self.display(show_ships=True)
                else:
                    print("Placement canceled. Try again.")
            except (ValueError, IndexError) as e:
                print(f"Error: {e}. Try again.")

    def reset_all_ships(self):
        for i in range(26):
            for j in range(10):
                if self.ocean_matrix[i][j].status == "S":
                    self.ocean_matrix[i][j].status = " "
        self.fleet_manifest.clear()
        self.registered_vessels.clear()
        self.ship_positions.clear()

    def remove_single_ship(self, ship_name):
        """
        Remove only the specified ship from the board, leaving others intact.
        """
        if ship_name not in self.fleet_manifest:
            return
        for (r, c) in self.ship_positions[ship_name]:
            self.ocean_matrix[r][c].status = " "
        del self.fleet_manifest[ship_name]
        self.registered_vessels.remove(ship_name)
        del self.ship_positions[ship_name]

    def remaining_ships(self):
        return len([shp for shp in self.fleet_manifest.values() if not shp.is_sunk()])

    def sunk_ships(self):
        return len([shp for shp in self.fleet_manifest.values() if shp.is_sunk()])