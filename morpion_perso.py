#!/usr/bin/env python3

"""Un jeu de morpion"""


from random import randint
import os

class Bcolors:
    "list of colors"
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# def initialize_playboard():
#     playboard = []
#     for i in range(1,4):
#         line = []

#         for j in range(1,4):
#             line.append((i-1) * 3 + j)

#         playboard.append(line)
#     return playboard

def initialize_playboard():
    "Initialize the playboard 3x3"
    playboard = []
    for i in range(3):
        line = []

        for j in range(3):
            line.append(i* 3 + j)

        playboard.append(line)
    return playboard

def is_occupy(box):
    """
    Check if a box is occupy
    """
    if 48 <= ord(str(box)) <= 56:
        return False
    return True

def is_input_legit(val):
    """
    Check if the input is between 0 and 8
    """
    if 48 <= ord(str(val)) <= 56:
        return True
    return False

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

def display_gameboard(array):
    """
    display the gameboard
    """
    abscisse = 0
    for lines in array:
        print(Bcolors.HEADER + "         |" + Bcolors.ENDC, end= "")
        for box in lines:
            if box == "X":
                print(Bcolors.FAIL + str(box) + Bcolors.ENDC, end = "")
            elif box == "O":
                print(Bcolors.OKGREEN + str(box) + Bcolors.ENDC, end = "")
            else:
                print(Bcolors.HEADER + str(box) + Bcolors.ENDC, end = "")
            #print(box, end = "")
            abscisse += 1

            if abscisse == 3:
                print(Bcolors.HEADER + "|" + Bcolors.ENDC)
                abscisse = 0

def convert(number):
    """
    Convert the number to abs/ord
    """
    return number // 3, number % 3

def start_game(name1, name2, pts):
    """
    Main game
    """
    os.system('clear')
    print(Bcolors.HEADER + " ----- START OF THE GAME ----- \n")
    playboard = initialize_playboard()
    joueur1 = "X"
    joueur2 = "O"
    list_symbol = [joueur1, joueur2]
    list_name = [name1, name2]

    current_player = list_symbol[randint(0,1)]
    index_player = list_symbol.index(current_player)
    print(f"   {list_name[index_player]} starts \n" + Bcolors.ENDC)
    while not is_finished(playboard, current_player):
        print(Bcolors.HEADER + f"                                 {name1}: {pts[0]} ;  {name2}: {pts[1]} \n" + Bcolors.ENDC)
        display_gameboard(playboard)

        box_to_play = input(Bcolors.HEADER + f"\n\n{list_name[index_player]}, enter a box to play : \n" + Bcolors.ENDC)

        while not is_input_legit(box_to_play):
            box_to_play = input(Bcolors.WARNING + f"{list_name[index_player]}, please enter a number between 0 and 8\n" + Bcolors.ENDC)

        box_to_play = int(box_to_play)
        ordonnee, abscisse  = convert(box_to_play)
        while is_occupy(playboard[ordonnee][abscisse]):
            print(Bcolors.WARNING + "The box is already occupied, choose another one : \n" + Bcolors.ENDC)
            box_to_play = int(input())
            ordonnee, abscisse  = convert(box_to_play)

        playboard[ordonnee][abscisse] = current_player

        if is_win(playboard, current_player):
            os.system('clear')
            print(Bcolors.OKGREEN + f"{list_name[index_player]} won the game! "  + Bcolors.ENDC)
            display_gameboard(playboard)
            return index_player

        if is_full(playboard):
            os.system('clear')
            print(Bcolors.FAIL + "It's a draw!" + Bcolors.ENDC)
            display_gameboard(playboard)
            return None

        index_player = (index_player + 1) %2
        current_player = list_symbol[index_player]
        os.system('clear')
        print("\n\n")

if __name__ == "__main__":
    os.system('clear')
    name_p1 = input(Bcolors.OKCYAN + "Name of player 1 ?\n"+ Bcolors.ENDC)
    while not len(name_p1) > 2:
        name_p1 = input(Bcolors.WARNING + "Need more than 3 letters, name of Player 1 ?\n"+ Bcolors.ENDC)

    name_p2 = input(Bcolors.OKCYAN + "Name of player 2 ?\n" + Bcolors.ENDC)
    while not len(name_p2) > 2 or name_p1 == name_p2:
        name_p2 = input(Bcolors.WARNING + "Need more than 3 letters, name of Player 2 ?\n" + Bcolors.ENDC)

    nb_pts = [0,0] #nb points de joueur1 et de joueur 2, respectivement

    while 1:
        index_winner = start_game(name_p1, name_p2, nb_pts)
        nb_pts[index_winner] += 1

        valeur = input(Bcolors.HEADER + "Do u want to continue ? [y] or [n] \n" + Bcolors.ENDC).strip()
        while valeur not in ("y, n"):
            print(Bcolors.WARNING + "\nPlease press [y] or [n]" + Bcolors.ENDC)
            valeur = input(Bcolors.HEADER + "Do u want to continue ? [y] or [n] \n" + Bcolors.ENDC)

        if valeur == "n":
            break
