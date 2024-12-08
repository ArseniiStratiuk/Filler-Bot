#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Masterpiece bot for the filler game with heat map strategy.
"""

import sys
from logging import DEBUG, getLogger, StreamHandler, INFO

# Debugging logger
logger = getLogger(__name__)
logger.setLevel(INFO)
handler = StreamHandler(sys.stderr)
logger.addHandler(handler)

# Global game state
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
    logger.debug(f"Player info: {line}")
    game_state["player"] = 1 if "p1 :" in line else 2
    game_state["our_char"] = "O" if game_state["player"] == 1 else "X"
    game_state["enemy_char"] = "X" if game_state["player"] == 1 else "O"


def parse_field_info():
    """
    Parse the board dimensions.
    """
    line = input()
    logger.debug(f"Field info: {line}")
    _, height, width = line.split()
    game_state["board_height"] = int(height)
    game_state["board_width"] = int(width[:-1])  # Remove trailing ":"


def parse_field():
    """
    Parse the current board state.
    """
    input()  # Skip the column indices line
    board = []
    for _ in range(game_state["board_height"]):
        line = input()[4:]  # Skip the row number
        board.append(line)
    game_state["board"] = board
    logger.debug("Parsed board:")
    for row in board:
        logger.debug(row)


def parse_figure():
    """
    Parse the dimensions and structure of the current figure.
    """
    line = input()
    logger.debug(f"Figure info: {line}")
    _, height, width = line.split()
    game_state["figure_height"] = int(height)
    game_state["figure_width"] = int(width[:-1])  # Remove trailing ":"

    figure = []
    for _ in range(game_state["figure_height"]):
        line = input()
        figure.append(line)
    game_state["figure"] = figure
    logger.debug("Parsed figure:")
    for row in figure:
        logger.debug(row)


def initialize_heat_map():
    """
    Initialize a heat map for the board with default values.
    """
    game_state["heat_map"] = [[0] * game_state["board_width"] for _ in range(game_state["board_height"])]


def update_heat_map():
    """
    Update the heat map based on the proximity to the opponent's pieces.
    """
    initialize_heat_map()
    for x in range(game_state["board_height"]):
        for y in range(game_state["board_width"]):
            if game_state["board"][x][y] == game_state["enemy_char"]:
                # Increase scores around the opponent's pieces
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < game_state["board_height"] and 0 <= ny < game_state["board_width"]:
                            # Proximity-based weighting (closer cells get higher values)
                            game_state["heat_map"][nx][ny] += max(4 - abs(dx) - abs(dy), 0)
    logger.debug("Updated heat map:")
    for row in game_state["heat_map"]:
        logger.debug(" ".join(map(str, row)))


def is_valid_placement(x, y):
    """
    Check if placing the figure at (x, y) is valid.
    """
    overlap = 0
    for i in range(game_state["figure_height"]):
        for j in range(game_state["figure_width"]):
            if game_state["figure"][i][j] == "*":
                bx, by = x + i, y + j
                if bx < 0 or bx >= game_state["board_height"] or by < 0 or by >= game_state["board_width"]:
                    return False  # Out of bounds
                cell = game_state["board"][bx][by]
                if cell == game_state["enemy_char"]:
                    return False  # Overlaps with enemy cells
                if cell == game_state["our_char"]:
                    overlap += 1
    return overlap == 1  # Must overlap exactly one of our pieces


def calculate_move_score(x, y):
    """
    Calculate the score of placing the figure at (x, y) based on the heat map.
    """
    score = 0
    for i in range(game_state["figure_height"]):
        for j in range(game_state["figure_width"]):
            if game_state["figure"][i][j] == "*":
                bx, by = x + i, y + j
                if 0 <= bx < game_state["board_height"] and 0 <= by < game_state["board_width"]:
                    score += game_state["heat_map"][bx][by]
    return score


def find_best_move():
    """
    Find the best move using the heat map for scoring.
    """
    best_move = None
    max_score = float("-inf")

    for x in range(game_state["board_height"]):
        for y in range(game_state["board_width"]):
            if is_valid_placement(x, y):
                move_score = calculate_move_score(x, y)
                logger.debug(f"Move ({x}, {y}) scored {move_score}.")
                if move_score > max_score:
                    max_score = move_score
                    best_move = (x, y)

    if best_move:
        logger.debug(f"Best move: {best_move} with score {max_score}")
    else:
        logger.debug("No valid moves found.")
    return best_move


def update_board_with_move(move):
    """
    Place the current move on the board using lowercase markers.
    """
    x, y = move
    for i in range(game_state["figure_height"]):
        for j in range(game_state["figure_width"]):
            if game_state["figure"][i][j] == "*":
                bx, by = x + i, y + j
                game_state["board"][bx] = (
                    game_state["board"][bx][:by]
                    + game_state["our_char"].lower()
                    + game_state["board"][bx][by + 1:]
                )


def finalize_board_state():
    """
    Convert lowercase markers to uppercase after placement.
    """
    for i in range(game_state["board_height"]):
        game_state["board"][i] = game_state["board"][i].replace(
            game_state["our_char"].lower(), game_state["our_char"]
        )


def print_board():
    """
    Print the current board state with indices.
    """
    logger.debug("Current board:")
    for i, row in enumerate(game_state["board"]):
        logger.debug(f"{i:02} {row}")


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
        update_board_with_move(move)
        print_board()
        print(f"{move[0]} {move[1]}")
        finalize_board_state()
    else:
        print("0 0")  # No valid moves available


def play():
    """
    Main game loop.
    """
    while True:
        try:
            step()
        except EOFError:
            logger.debug("Game over.")
            break


def main():
    """
    Entry point of the bot.
    """
    parse_info_about_player()
    play()


if __name__ == "__main__":
    main()
