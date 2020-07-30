from board import Board
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
                    input("\nEnter the coordinates that you want to hit: \n").title()
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
                    print(f"\n{self.player} has hit their enemy's {ship}!".upper())
                    print(f"\nOpponent's {ship} has been sunken!".upper())
                    self.points += 1
                    break
                elif coordinate in coordinate_list and len(coordinate_list) > 1:
                    coordinate_list.remove(coordinate)
                    self.opponent_board.show_board_to_enemy()
                    print(f"\n{self.player} has hit their enemy's {ship}!".upper())
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