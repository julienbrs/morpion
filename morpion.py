#!/usr/bin/env python3

"""Little Tic Tac Toe in a shell"""

from random import randint
import os

# Global variables

# List of colors
HEADER = "\033[95m"
OKCYAN = "\033[96m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
RED = "\033[91m"
ENDC = "\033[0m"

# Functions initializing the game
def initialize_playboard():
    """
    Initialize the playboard 3x3 with empty boxes
    Return the initialized playboard as a 2D list
    """
    playboard = []
    for i in range(3):
        line = []
        for j in range(3):
            line.append(i * 3 + j)
        playboard.append(line)
    return playboard


# Tools
def is_occupy(box):
    """
    Check if a box is occupy
    """
    if 48 <= ord(str(box)) <= 56:
        return False
    return True


def convert(number):
    """
    Convert the number to abs/ord
    """
    return number // 3, number % 3


# Functions interacting with user


def ask_name(player_number):
    """
    Ask for name
    """
    while True:
        name = input(OKCYAN + f"Name of player {player_number} ?\n" + ENDC)
        if name.isalpha():
            return name
        print(WARNING + "Please use only letters\n" + ENDC)


def ask_box_number(list_name, index_player, playboard, score):
    """
    Check if the input is between 0 and 8
    """
    player = list_name[index_player]
    while True:
        digit = input(HEADER + f"\n\n{player}, enter a box to play : \n" + ENDC)
        if isinstance(int(digit), int) and 0 <= int(digit) <= 8:
            return int(digit)
        os.system("clear")
        display_game(playboard, list_name, score)
        print(WARNING + f"{player}, please enter a number between 0 and 8\n" + ENDC)


# Functions testing the end of the game


def is_full(array):
    """
    Check if the playboard is full or not
    Return True if full, else False
    """
    for line in array:
        for box in line:
            if not is_occupy(box):
                return False
    return True


def is_win(array, symbol):
    """
    Check if the last player won by testing all the possibilities
    Symbol is the symbol of the last play
    Return a boolean
    """
    # Check if the player has won horizontally
    for line in array:
        if all(box == symbol for box in line):
            return True

    # Check if the player has won vertically
    for column in range(3):
        if all(array[row][column] == symbol for row in range(3)):
            return True

    # Check if the player has won diagonally
    if all(array[i][i] == symbol for i in range(3)) or all(
        array[i][2 - i] == symbol for i in range(3)
    ):
        return True

    # If none of the above checks return True, the player has not won
    return False


def is_finished(array, symbol):
    """
    Check if the game is finished
    """
    return is_full(array) or is_win(array, symbol)


# Graphics functions


def display_gameboard(array):
    """
    Display the gameboard
    """
    print("┏━┳━┳━┓")
    for i in range(len(array)):
        # First line
        for box in array[i]:
            print("┃", end="")  # end="" to not \n
            if box == "X":
                print(OKGREEN + "X" + ENDC, end="")
            elif box == "O":
                print(RED + "O" + ENDC, end="")
            else:
                print(box, end="")
        if i != len(array) - 1:
            print("┃\n┣━╋━╋━┫")
        else:
            print("┃")
    print("┗━┻━┻━┛")


def display_game(gameboard, list_name, score):
    """
    Todo: commentaire
    """
    print(
        "\n\n"
        + HEADER
        + f" {list_name[0]}: {score[0]} ;  {list_name[1]}: {score[1]} ; Draw: {score[2]}\n\n"
        + ENDC
    )
    display_gameboard(gameboard)


def start_game(name1, name2, score):
    """
    Main game
    """
    os.system("clear")
    print(HEADER + " ----- START OF THE GAME ----- \n")
    playboard = initialize_playboard()
    symb1 = "X"
    symb2 = "O"
    list_symbol = [symb1, symb2]
    list_name = [name1, name2]

    current_symbol = list_symbol[randint(0, 1)]
    index_player = list_symbol.index(current_symbol)
    print(f"   {list_name[index_player]} starts \n" + ENDC)

    while not is_finished(playboard, current_symbol):
        display_game(playboard, list_name, score)

        box_to_play = ask_box_number(list_name, index_player, playboard, score)
        ordonnee, abscisse = convert(box_to_play)
        while is_occupy(playboard[ordonnee][abscisse]):
            os.system("clear")
            display_game(playboard, list_name, score)
            print(
                WARNING + "The box is already occupied, choose another one : \n" + ENDC
            )
            box_to_play = ask_box_number(list_name, index_player, playboard, score)
            ordonnee, abscisse = convert(box_to_play)

        playboard[ordonnee][abscisse] = current_symbol

        if is_win(playboard, current_symbol):
            os.system("clear")
            print(OKGREEN + f"{list_name[index_player]} won the game! " + ENDC)
            display_game(playboard, list_name, score)
            return index_player

        if is_full(playboard):
            os.system("clear")
            print(RED + "It's a draw!" + ENDC)
            display_gameboard(playboard)
            return 2

        index_player = (index_player + 1) % 2
        current_symbol = list_symbol[index_player]
        os.system("clear")


if __name__ == "__main__":
    os.system("clear")
    name_p1 = ask_name(1)
    name_p2 = ask_name(2)

    scoreboard = [0, 0, 0]  #  score of player 1, player 2, draws

    while 1:
        index_winner = start_game(name_p1, name_p2, scoreboard)
        scoreboard[index_winner] += 1

        valeur = input(HEADER + "Do u want to continue ? [y] or [n] \n" + ENDC).strip()
        while valeur not in ("y, n"):
            print(WARNING + "\nPlease press [y] or [n]" + ENDC)
            valeur = input(HEADER + "Do u want to continue ? [y] or [n] \n" + ENDC)

        if valeur == "n":
            os.system("clear")
            print(HEADER + "FINAL SCORE: \n")
            print(
                f"{name_p1[0]}: {scoreboard[0]} ;  {name_p1[1]}: {scoreboard[1]} ; Draw: {scoreboard[2]}\n\n"
                + ENDC
            )
            break
