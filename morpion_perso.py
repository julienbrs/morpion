#!/usr/bin/env python3

"""Un jeu de morpion"""


from random import randint
import os

# Global variables

# list of colors
HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKCYAN = '\033[96m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

#Functions initializing the game
def initialize_playboard():
    "Initialize the playboard 3x3"
    playboard = []
    for i in range(3):
        line = []

        for j in range(3):
            line.append(i* 3 + j)

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
def ask_name(nb_player):
    """
    Ask for name
    """
    while True:
        name = input(OKCYAN + f"Name of player {nb_player} ?\n"+ ENDC)
        if name.isalpha():
            return name
        print(WARNING + "Please use only letters\n"+ ENDC)


def ask_number(player):
    """
    Check if the input is between 0 and 8
    """
    while True:
        digit = input(HEADER + f"\n\n{player}, enter a box to play : \n" + ENDC)
        if digit.isdigit() and len(digit) == 1 and digit != "9":
            return int(digit)
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


def is_win_horizontal(array, symbol):
    """
    Check if the last player won by testing all the horizontal possibilities
    Symbol is the symbol of the last play
    Return a boolean
    """
    for line in array:
        if line[0] == line[1] == line[2] == symbol:
            return True
    return False

def is_win_vertical(array, symbol):
    """
    Check if the last player won by testing all the vertical possibilities
    Symbol is the symbol of the last play
    Return a boolean
    """
    column = 0
    while column < 3:
        if array[0][column] == array[1][column] == array[2][column] == symbol:
            return True
        column += 1
    return False


def is_win_diagonal(array, symbol):
    """
    Check if the last player won by testing all the diagonal possibilities
    Symbol is the symbol of the last play
    Return a boolean
    """
    if (array[0][0] == array[1][1] == array[2][2] == symbol or
        array[0][2] ==array[1][1] == array[2][0] == symbol):
        return True
    return False

def is_win(array, symbol):
    """
    Check if the last player won by testing all the possibilities
    Symbol is the symbol of the last play
    Return a boolean
    """
    val = (is_win_horizontal(array, symbol) or is_win_vertical(array, symbol)
            or is_win_diagonal(array, symbol))
    return val

def is_finished(array, symbol):
    """
    Check if the game is finished
    """
    return (is_full(array) or is_win(array, symbol))


# Graphics functions

def display_gameboard(array):
    """
    display the gameboard
    """
    abscisse = 0
    for lines in array:
        print(HEADER + "         |" + ENDC, end= "")
        for box in lines:
            if box == "X":
                print(FAIL + str(box) + ENDC, end = "")
            elif box == "O":
                print(OKGREEN + str(box) + ENDC, end = "")
            else:
                print(HEADER + str(box) + ENDC, end = "")
            abscisse += 1

            if abscisse == 3:
                print(HEADER + "|" + ENDC)
                abscisse = 0

def start_game(name1, name2, score):
    """
    Main game
    """
    os.system('clear')
    print(HEADER + " ----- START OF THE GAME ----- \n")
    playboard = initialize_playboard()
    symb1 = "X"
    symb2 = "O"
    list_symbol = [symb1, symb2]
    list_name = [name1, name2]

    current_symbol = list_symbol[randint(0,1)]
    index_player = list_symbol.index(current_symbol)
    print(f"   {list_name[index_player]} starts \n" + ENDC)

    while not is_finished(playboard, current_symbol):
        print(HEADER + f" {name1}: {score[0]} ;  {name2}: {score[1]} \n\n" + ENDC)
        display_gameboard(playboard)

        box_to_play = ask_number(list_name[index_player])
        ordonnee, abscisse  = convert(box_to_play)
        while is_occupy(playboard[ordonnee][abscisse]):
            print(WARNING + "The box is already occupied, choose another one : \n" + ENDC)
            box_to_play = ask_number(list_name[index_player])
            ordonnee, abscisse  = convert(box_to_play)

        playboard[ordonnee][abscisse] = current_symbol

        if is_win(playboard, current_symbol):
            os.system('clear')
            print(OKGREEN + f"{list_name[index_player]} won the game! "  + ENDC)
            display_gameboard(playboard)
            return index_player

        if is_full(playboard):
            os.system('clear')
            print(FAIL + "It's a draw!" + ENDC)
            display_gameboard(playboard)
            return None

        index_player = (index_player + 1) %2
        current_symbol = list_symbol[index_player]
        os.system('clear')
        print("\n\n")



if __name__ == "__main__":
    os.system('clear')
    name_p1 = ask_name(1)
    name_p2 = ask_name(2)

    scoreboard = [0,0] #nb points de joueur1 et de joueur 2, respectivement

    while 1:
        index_winner = start_game(name_p1, name_p2, scoreboard)
        scoreboard[index_winner] += 1

        valeur = input(HEADER + "Do u want to continue ? [y] or [n] \n" + ENDC).strip()
        while valeur not in ("y, n"):
            print(WARNING + "\nPlease press [y] or [n]" + ENDC)
            valeur = input(HEADER + "Do u want to continue ? [y] or [n] \n" + ENDC)

        if valeur == "n":
            break
