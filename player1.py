#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from copy import deepcopy
from logging import DEBUG, debug, getLogger

# We use the debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    l = input()
    _, height, width = l.split()
    return int(height), int(width[:-1])


def parse_field(height: int):
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowecase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    :param player int: Represents whether we're the first or second player
    """

    _ = input()
    field = []
    for _ in range(height):
        _, line = input().split()
        field.append(line)
    field = [list(line) for line in field]
    return field


def parse_figure():
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    piece = input()
    height, width = int(piece.split()[1]), int(piece.split()[2][:-1])
    figure = []
    for _ in range(height):
        l = input()
        figure.append(l)
    # debug(f'figure: {figure}')
    return height, width, figure

def where_to_put(my_positions_on_field, field, h_figure, w_figure, figure, symbol):
    """
    Checks possible placements by overlapping the figure with each player's symbol on the field.

    :param my_positions_on_field: List of (row, column) positions 
        of the player's symbols on the field.
    :param field: Current game field as a 2D list.
    :param h_figure: Height of the figure.
    :param w_figure: Width of the figure.
    :param figure: The figure to be placed as a 2D list.
    :param symbol: Current player's symbol ('O' or 'X').

    :return: List of valid field configurations after placing the figure.
    """
    lst_of_correct_coordinates = []
    lst_of_correct_fields = []
    opponent_symbols = 'Xx' if symbol == 'O' else 'Oo'
    top_left_x, top_left_y = 0, 0

    coordinates_of_figure_stars = [(fx, fy) for fx in range(h_figure) for fy in range(w_figure) \
                                   if figure[fx][fy] == '*']

    candidates = []
    for field_x, field_y in my_positions_on_field:
        for fx, fy in coordinates_of_figure_stars:
            top_left_x = field_x - fx
            top_left_y = field_y - fy

            if  0 <= top_left_x < len(field) - h_figure + 1 and \
                0 <= top_left_y < len(field[0]) - w_figure + 1:
                candidates.append((top_left_x, top_left_y))

    for top_left_x, top_left_y in candidates:
        new_field = deepcopy(field)
        correct_placement = True
        overlaps_count = 0

        for field_x, field_y in coordinates_of_figure_stars:
            curr_x = top_left_x + field_x
            curr_y = top_left_y + field_y

            if field[curr_x][curr_y] in opponent_symbols:
                correct_placement = False
                break

            if field[curr_x][curr_y] == symbol:
                overlaps_count += 1

            new_field[curr_x][curr_y] = symbol

        if correct_placement and overlaps_count == 1:
            lst_of_correct_coordinates.append((top_left_x, top_left_y))
            lst_of_correct_fields.append(new_field)

    return lst_of_correct_coordinates, lst_of_correct_fields

def get_manhattan_distance(height, width, field, symbol):
    """Calculates manhattan_distance from my point to opponent closest point"""
    list_of_distances = []
    opponent_symbols = 'Xx' if symbol == 'O' else 'Oo'
    my_positions_on_field = [(r, c) for r in range(height) for c in range(width) \
                            if field[r][c] == symbol]
    oponent_positions_on_field = [(r, c) for r in range(height) for c in range(width) \
                            if field[r][c] in opponent_symbols]
    for mine_x, mine_y in my_positions_on_field:
        for opponent_x, opponent_y in oponent_positions_on_field:
            distance = abs(mine_x - opponent_x) + abs(mine_y - opponent_y)
            list_of_distances.append(distance)
    list_of_distances = sorted(list_of_distances)
    return list_of_distances[0]


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    symbol = 'O' if player == 1 else 'X'
    height, width = parse_field_info()
    field = parse_field(height)
    h_figure, w_figure, figure = parse_figure()

    my_positions_on_field = [(r, c) for r in range(height) for c in range(width) \
                            if field[r][c] == symbol]

    list_of_possible_coordinates, lst_of_correct_fields = where_to_put(my_positions_on_field, \
                                                                        field, h_figure, \
                                                                        w_figure, figure, \
                                                                        symbol)
    lst_of_calculated_coordinates = []

    length = len(lst_of_correct_fields)
    for i in range(length):
        smallest_distance = get_manhattan_distance(height, width, lst_of_correct_fields[i], symbol)
        lst_of_calculated_coordinates.append((list_of_possible_coordinates[i], smallest_distance))
    lst_of_calculated_coordinates = sorted(lst_of_calculated_coordinates, key = lambda x: x[1])

    return lst_of_calculated_coordinates[0][0]



def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        print(*move)

def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    i = input()
    return 1 if "p1" in i else 2


def main():
    """main"""

    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        debug("Cannot get input. Seems that we've lost ):")


if __name__ == "__main__":
    main()
