class Board:
    """Create representation of a Battleship game board and the actions associated with one."""

    def __init__(self):
        self.board = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(10)]  # represent 10x10 board as list of lists
        self.ships = {'carrier': 5, 'battleship': 4, 'destroyer': 3, 'submarine': 3, 'patrol boat': 2}
        self.ships_remaining = self.ships.copy()
        self.ship_coordinates = {'carrier': [], 'battleship': [], 'destroyer': [], 'submarine': [], 'patrol boat': []}

    def convert_coords(self, coords):
        """Takes a coordinate like A1 and converts it to a tuple such as (1,0)"""
        coord_keys = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6, 'H': 7, 'I': 8, 'J': 9}
        column = coord_keys[coords[0]]
        row = int(coords[1:])
        converted_coords = (row, column)
        return converted_coords

    def print_ships(self):
        """Neatly print a list of ships available for placement"""
        print("\nHere are the ships available:")
        for ship, length in self.ships_remaining.items():
            print(f"\n{ship.title()} | Length: {length} units long")
        print('')

    def pick_a_ship(self):
        """Prompts user to enter a ship. Returns said ship."""
        ship = input("\nWhat ship would you like to place on the board?: ").lower()
        while ship not in self.ships_remaining:
            ship = input(
                "\nPlease enter a valid ship name. You may have used that ship already or misspelled its name.")
        return ship

    def get_orientation(self):
        """Outputs a user given orientation"""
        orientation = input("\nEnter the ship's orientation (v or h): ").upper()
        while orientation not in ['V', 'H']:
            orientation = input("\nPlease enter a valid orientation: ").upper()
        return orientation

    def show_board_to_self(self):
        """Displays printed representation of player's board."""
        row_number = 0
        print("   A  B  C  D  E  F  G  H  I  J")
        print(' ' + ('-' * 30))
        for row in self.board:
            row_builder = f'{row_number}| '
            for element in row:
                if element == 0:
                    row_builder += 'o  '
                elif element == 'x':
                    row_builder += 'X  '
                elif element == 1:
                    row_builder += '+  '
                else:
                    row_builder += '-  '
            row_number += 1
            print(row_builder)

    def show_board_to_enemy(self):
        """Displays printed representation of player's board with ships hidden."""
        row_number = 0
        print("   A  B  C  D  E  F  G  H  I  J")
        print(' ' + ('-' * 30))
        for row in self.board:
            row_builder = f'{row_number}| '
            for element in row:
                if element == 'x':
                    row_builder += 'X  '
                elif element == -1:
                    row_builder += '-  '
                else:
                    row_builder += 'o  '
            row_number += 1
            print(row_builder)

    def get_coordinates(self):
        """Prompts user for ship,
         orientation and coordinates and simulates ship placement on board by modifying self.board
        """
        ship = self.pick_a_ship()
        orientation = self.get_orientation()
        ship_length = self.ships[ship]
        # Obtain valid coordinates from user
        while True:
            try:
                start_coords = self.convert_coords(
                    input("\nEnter the ship's starting coordinates (ex. a1): \n").upper())
                end_coords = self.convert_coords(input("\nEnter the ship's ending coordinates (ex. a4): \n").upper())
            except KeyError:
                print('\nPlease enter valid coordinates.')
            except ValueError:
                print('\nPlease enter valid coordinates')
            else:

                # make sure that ship's coordinates are vertical
                if orientation == 'V':
                    if start_coords[1] != end_coords[1]:
                        print("The ship's coordinates aren't in a vertical direction!")
                        continue
                    # prevent ship from being placed in occupied area
                    count_ones = 0
                    for i in range(start_coords[0], end_coords[0] + 1):
                        if self.board[i][start_coords[1]] == 1:
                            count_ones += 1
                    if count_ones != 0:
                        print("That space is occupied!")
                        continue
                    # Handle situation where ship size is different from its designated coordinate range
                    if ((end_coords[0] - start_coords[0] + 1) != ship_length):
                        print("\nEnter valid end coordinates. Your ship does not fit in the given coordinate range!")
                        continue

                # make sure that ship's coordinates are horizontal and that its designated space is open
                elif orientation == 'H':
                    if start_coords[1] == end_coords[1]:
                        print("The ship's coordinates aren't in a horizontal direction!")
                        continue
                    elif start_coords[0] != end_coords[0]:
                        print("The ship's coordinates aren't in a horizontal direction!")
                        continue
                    elif 1 in self.board[start_coords[0]][start_coords[1]: end_coords[1] + 1]:
                        print("That space is occupied!")
                        continue
                    elif ((end_coords[1] - start_coords[1] + 1) != ship_length):
                        print("\nEnter valid coordinates. Your ship does not fit in the given coordinate range!")
                        continue
                return (ship, orientation, start_coords, end_coords,)

    def insert_ship(self, ship, orientation, start_coords, end_coords):
        """Inserts a ship on a player's board by modifying self.board."""
        # insert ship vertically
        if orientation == 'V':
            for i in range(start_coords[0], end_coords[0] + 1):
                self.board[i][start_coords[1]] = 1
                # append every coordinate that a ship occupies to a list in a dictionary with a key corresponding to ship name
                self.ship_coordinates[ship].append((i, start_coords[1]))

        # insert ship horizontally
        elif orientation == 'H':
            # replace a slice of a row with 1's to represent ship occupation
            self.board[start_coords[0]][start_coords[1]: end_coords[1] + 1] = [1] * len(
                self.board[start_coords[0]][start_coords[1]: end_coords[1] + 1])

            for i in range(start_coords[1], end_coords[1] + 1):
                self.ship_coordinates[ship].append((start_coords[0], i))
        del self.ships_remaining[ship]