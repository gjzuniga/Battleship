import os
import time
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


class Player:
    """Represent a player in the game Battleship"""

    def __init__(self, player):
        self.player = player
        self.player_board = Board()
        self.opponent_board = Board()
        self.points = 0

    def obtain_hit_coords(self):
        """Prompts the user for coordinates to hit and returns those coordinates"""
        while True:
            try:
                hit_coords = self.opponent_board.convert_coords(
                    input("\nEnter the coordinates that you want to hit. ").title()
                )
                # prevent out of range row coordinates
                if hit_coords[0] > 9:
                    raise ValueError("Row coordinate must be < 9")
                # Prevent user from hitting a coordinate twice
                if self.opponent_board.board[hit_coords[0]][hit_coords[1]] in ['x', -1]:
                    continue
            except KeyError:
                print('\nPlease enter valid hit coordinates.')
            except ValueError:
                print('\nPlease enter valid hit coordinates')
            else:
                return hit_coords

    def hit_opponent_ship(self, hit_coords):
        """Hits the player's opponent's ship, increments player's points if a hit is landed."""
        row = hit_coords[0]
        column = hit_coords[1]

        if self.opponent_board.board[row][column] == 1:
            self.opponent_board.board[row][column] = 'x'
            coordinate = (row, column)
            for ship, coordinate_list in self.opponent_board.ship_coordinates.items():
                if coordinate in coordinate_list and len(coordinate_list) == 1:
                    coordinate_list.remove(coordinate)
                    self.opponent_board.show_board_to_enemy()
                    print(f"\n{self.player} has hit their enemy's {ship}\n!".upper())
                    print(f"\nOpponent's {ship} has been sunken!\n".upper())
                    self.points += 1
                    break
                elif coordinate in coordinate_list and len(coordinate_list) > 1:
                    coordinate_list.remove(coordinate)
                    self.opponent_board.show_board_to_enemy()
                    print(f"\n{self.player} has hit their enemy's {ship}!\n".upper())
                    break
        else:
            self.opponent_board.board[row][column] = -1
            self.opponent_board.show_board_to_enemy()
            print(f"\n{self.player} missed!".upper())

    def hit_player_ship(self, hit_coords):
        row = hit_coords[0]
        column = hit_coords[1]
        if self.player_board.board[row][column] == 1:
            self.player_board.board[row][column] = 'x'
            coordinate = (row, column)
            for ship, coordinate_list in self.player_board.ship_coordinates.items():
                if coordinate in coordinate_list and len(coordinate_list) == 1:
                    coordinate_list.remove(coordinate)
                    break
                elif coordinate in coordinate_list and len(coordinate_list) > 1:
                    coordinate_list.remove(coordinate)
                    break
        else:
            self.player_board.board[row][column] = -1

auto_ships = [('carrier', 'H', (1, 0), (1, 4)), ('battleship', 'H', (2, 0), (2, 3)), ('destroyer', 'H', (3, 0), (3, 2)),
              ('submarine', 'H', (4, 0), (4, 2)), ('patrol boat', 'H', (5, 0), (5, 1))]


def change_turns():
    player_input = input("Enter s to switch players: ").upper()
    while player_input != 'S':
        player_input = input("Enter s to switch players: ").upper()

end_game = False
while not end_game:
    print("*******BATTLESHIP*******")
    player_1 = Player("Player 1")
    player_2 = Player("Player 2")
    is_player_1_turn = True
    is_player_2_turn = False
    # initial board setup
    print("\n### P L A Y E R  1's  T U R N ###")
    player_1.player_board.print_ships()
    # for i in range(5):
    #     player_1.player_board.show_board_to_self()
    #     coordinates = player_1.player_board.get_coordinates()
    #     player_1.player_board.insert_ship(*coordinates)
    #     player_2.opponent_board.insert_ship(*coordinates)
    for atuple in auto_ships:
        player_1.player_board.show_board_to_self()
        player_1.player_board.insert_ship(*atuple)
        player_2.opponent_board.insert_ship(*atuple)
        player_1.player_board.show_board_to_self()
    change_turns()
    os.system('cls')
    print("### P L A Y E R  2's  T U R N ###")
    player_2.player_board.print_ships()
    # for i in range(5):
    #     player_2.player_board.show_board_to_self()
    #     coordinates = player_2.player_board.get_coordinates()
    #     player_2.player_board.insert_ship(*coordinates)
    #     player_1.opponent_board.insert_ship(*coordinates)
    for atuple in auto_ships:
        player_2.player_board.show_board_to_self()
        # coordinates = player_2.player_board.get_coordinates()
        player_2.player_board.insert_ship(*atuple)
        player_1.opponent_board.insert_ship(*atuple)
        player_2.player_board.show_board_to_self()
    change_turns()
    while True:
        os.system('cls')
        if is_player_1_turn:
            print("\n### P L A Y E R  1's  T U R N ###")
            print("\nYour board:\n")
            player_1.player_board.show_board_to_self()
            print("\nPlayer 2's board:\n")
            player_1.opponent_board.show_board_to_enemy()
            hit_coords = player_1.obtain_hit_coords()
            player_1.hit_opponent_ship(hit_coords)
            player_2.hit_player_ship(hit_coords)
            if player_1.points == 5:
                print("\nP L A Y E R  1  W I N S !\n")
                break
            change_turns()
            is_player_1_turn = False
            is_player_2_turn = True

        elif is_player_2_turn:
            print("\n### P L A Y E R  2's  T U R N ###")
            print("\nYour board:\n")
            player_2.player_board.show_board_to_self()
            print("\nPlayer 1's board:\n")
            player_2.opponent_board.show_board_to_enemy()
            hit_coords = player_2.obtain_hit_coords()
            player_2.hit_opponent_ship(hit_coords)
            player_1.hit_player_ship(hit_coords)
            if player_2.points == 5:
                print("\nP L A Y E R  2  W I N S !'n")
                break
            change_turns()
            is_player_2_turn = False
            is_player_1_turn = True
    if input("\nWould you like to play again? Enter Y or N").upper() == 'N':
        end_game = True

