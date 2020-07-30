from board import Board
from player import Player
import os


class Battleship:
    """The well-known game of Battleship written in Python."""
    def change_turns(self):
        """Allows a player to determine when they're done with their turn."""
        player_input = input("\nEnter s to switch players: \n").upper()
        while player_input != 'S':
            player_input = input("\nEnter s to switch players: \n").upper()

    def play(self):
        """Main driver of game."""
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
            for i in range(5):
                player_1.player_board.show_board_to_self()
                coordinates = player_1.player_board.get_coordinates()
                player_1.player_board.insert_ship(*coordinates)
                player_2.opponent_board.insert_ship(*coordinates)
            self.change_turns()
            os.system('cls')
            print("### P L A Y E R  2's  T U R N ###")
            player_2.player_board.print_ships()
            for i in range(5):
                player_2.player_board.show_board_to_self()
                coordinates = player_2.player_board.get_coordinates()
                player_2.player_board.insert_ship(*coordinates)
                player_1.opponent_board.insert_ship(*coordinates)
            self.change_turns()
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
                    self.change_turns()
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
                        print("\nP L A Y E R  2  W I N S !\n")
                        break
                    self.change_turns()
                    is_player_2_turn = False
                    is_player_1_turn = True
            if input("Would you like to play again? Enter Y or N: ").upper() == 'N':
                end_game = True

game = Battleship()
game.play()