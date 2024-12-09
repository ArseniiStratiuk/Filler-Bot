#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python bot for the filler game with heat map strategy.
"""
game_state = {
    "player": None,
    "board": [],
    "figure": [],
    "board_height": 0,
    "board_width": 0,
    "figure_height": 0,
    "figure_width": 0,
    "our_char": "",
    "enemy_char": "",
    "heat_map": [],
}


def parse_info_about_player():
    """
    Parse player info and set character markers.
    """
    line = input()
    game_state["player"] = 1 if "p1 :" in line else 2
    game_state["our_char"] = "O" if game_state["player"] == 1 else "X"
    game_state["enemy_char"] = "X" if game_state["player"] == 1 else "O"


def parse_field_info():
    """
    Parse the board dimensions.
    """
    line = input()
    _, height, width = line.split()
    game_state["board_height"] = int(height)
    game_state["board_width"] = int(width[:-1])


def parse_field():
    """
    Parse the current board state.
    """
    input()
    board = []
    for _ in range(game_state["board_height"]):
        line = input()[4:]
        board.append(line)
    game_state["board"] = board


def parse_figure():
    """
    Parse the dimensions and structure of the current figure.
    """
    line = input()
    _, height, width = line.split()
    game_state["figure_height"] = int(height)
    game_state["figure_width"] = int(width[:-1])
    figure = []
    for _ in range(game_state["figure_height"]):
        line = input()
        figure.append(line)
    game_state["figure"] = figure


def initialize_heat_map():
    """
    Initialize a heat map for the board with default values.
    """
    game_state["heat_map"] = [[0] * game_state["board_width"]
                              for _ in range(game_state["board_height"])]


def get_iteration_ranges() -> tuple:
    """
    Determine iteration ranges for x and y based on our_char.
    """
    if game_state["our_char"] == "O":
        return (
            range(game_state["board_height"] - 1, -1, -1),
            range(game_state["board_width"] - 1, -1, -1),
        )
    return range(game_state["board_height"]), range(game_state["board_width"])


def update_heat_map():
    """
    Update the heat map based on the proximity to the opponent's pieces.
    """
    initialize_heat_map()
    x_range, y_range = get_iteration_ranges()

    for x in x_range:
        for y in y_range:
            if game_state["board"][x][y] == game_state["enemy_char"]:
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < game_state["board_height"] and
                            0 <= ny < game_state["board_width"]):
                            game_state["heat_map"][nx][ny] += max(4 - abs(dx) - abs(dy), 0)


def is_valid_placement(x: int, y: int) -> bool:
    """
    Check if placing the figure at (x, y) is valid.
    """
    overlap = 0
    for i in range(game_state["figure_height"]):
        for j in range(game_state["figure_width"]):
            if game_state["figure"][i][j] == "*":
                bx, by = x + i, y + j
                if (bx < 0 or bx >= game_state["board_height"] or
                    by < 0 or by >= game_state["board_width"]):
                    return False
                cell = game_state["board"][bx][by]
                if cell == game_state["enemy_char"]:
                    return False
                if cell == game_state["our_char"]:
                    overlap += 1
    return overlap == 1


def calculate_move_score(x: int, y: int) -> int:
    """
    Calculate the score of placing the figure at (x, y) based on the heat map.
    """
    score = 0
    for i in range(game_state["figure_height"]):
        for j in range(game_state["figure_width"]):
            if game_state["figure"][i][j] == "*":
                bx, by = x + i, y + j
                if (0 <= bx < game_state["board_height"] and
                    0 <= by < game_state["board_width"]):
                    score += game_state["heat_map"][bx][by]
    return score


def find_best_move() -> tuple:
    """
    Find the best move using the heat map for scoring.
    """
    best_move = None
    max_score = float("-inf")
    x_range, y_range = get_iteration_ranges()

    for x in x_range:
        for y in y_range:
            if is_valid_placement(x, y):
                move_score = calculate_move_score(x, y)
                if move_score > max_score:
                    max_score = move_score
                    best_move = (x, y)

    return best_move


def step():
    """
    Perform one step of the game: parse inputs, update the heat map, find a move, and execute it.
    """
    parse_field_info()
    parse_field()
    parse_figure()
    update_heat_map()

    move = find_best_move()
    if move:
        print(f"{move[0]} {move[1]}")
    else:
        print("0 0")


def play():
    """
    Main game loop.
    """
    while True:
        try:
            step()
        except EOFError:
            break


def main():
    """
    Entry point of the bot.
    """
    parse_info_about_player()
    play()


if __name__ == "__main__":
    main()
