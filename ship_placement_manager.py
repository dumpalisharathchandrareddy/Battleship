class ShipPlacementManager:
    
    # This class Manages the initial placement of ships for a player, and allows modifications like changing positions etc.
    
    def __init__(self, player):
        self.player = player

    # THIS function is the placemnet management for all ships
    def manage_placement(self):
        #  List of ships
        ships_to_place = [
            ("Destroyer 1", 3),
            ("Destroyer 2", 3),
            ("Cruiser", 5),
            ("Battleship", 7),
            ("Aircraft Carrier", 9),
        ]

        # Initial placement of all ships
        for ship_name, size in ships_to_place:
            self.player.board.place_ship(ship_name, size)
            
        # Display the board with ships and print message

        print(f"{self.player.name}, all your ships are placed.")
        self.player.board.display(show_ships=True)

        # If placed all
        while True:
            choice = input("Modify ships? (1=Specific, 2=All, N=No): ").upper() #input prompt for modification
            if choice == "1":
                # Modify a single ship
                while True:
                    print("Your placed ships:")
                    for idx, sname in enumerate(self.player.board.registered_vessels):
                        print(f"{idx + 1}. {sname}")
                    try:
                        pick = int(input("Choose a ship number to move: ")) - 1
                        if pick < 0 or pick >= len(self.player.board.registered_vessels):
                            raise ValueError("Invalid choice.")
                        
                        # Get the ship and size
                        chosen_ship = self.player.board.registered_vessels[pick]
                        chosen_size = self.player.board.fleet_manifest[chosen_ship].size

                        # Remove only this ship
                        self.player.board.remove_single_ship(chosen_ship)
                        print(f"Re-placing {chosen_ship}:")
                        self.player.board.place_ship(chosen_ship, chosen_size)
                        
                        # Display the board with ships after modify and print message
                        print(f"{self.player.name}, your updated board after modifying {chosen_ship}:")
                        self.player.board.display(show_ships=True)

                        # Ask if more modifications needed
                        modify_again = input("More modifications? (1=Specific, 2=All, N=No): ").upper()
                        if modify_again == "2":
                            # Reset all and place again
                            self.player.board.reset_all_ships()
                            print("All cleared. Let's place everything again:")
                            
                            # Place all ships again
                            for shp, sz in ships_to_place:
                                self.player.board.place_ship(shp, sz)
                            self.player.board.display(show_ships=True)
                            no_more = input("Modifications complete? (N=No more changes): ").upper()
                            
                            # If no more modifications
                            if no_more == "N" or no_more == "":
                                break
                            else:
                                continue

                        elif modify_again == "1":
                            # Another single ship modification
                            continue
                        elif modify_again == "N" or modify_again == "":
                            # No more modifications
                            break
                        else:
                            # Invalid input treat as no more modifications
                            break
                        break
                    except ValueError as e:
                        print(f"Error: {e}, try again.")

                # After single ship modifications done
                break

            elif choice == "2":
                # Reset all and start all placements over
                self.player.board.reset_all_ships()
                print("All cleared. Let's place everything again:")
                for ship_name, size in ships_to_place:
                    self.player.board.place_ship(ship_name, size)
                self.player.board.display(show_ships=True)
                no_more = input("Modifications complete? (N=No more changes): ").upper()
                if no_more == "N" or no_more == "":
                    break

            elif choice == "N" or choice == "":
                # No modifications
                break
            else:
                print("Invalid choice. Please enter 1, 2, or N.")

        # Done with placement modification
        print("Ship placements finalized.")
        # Display the board with ships and print message
        self.player.board.display(show_ships=True)
