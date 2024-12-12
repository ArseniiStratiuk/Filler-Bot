# Filler Bot

A Python bot to play the Filler game against other bots, incorporating a heat map to make the best moves.

## Description

The bot is designed to compete in the Filler game by analyzing the game board and using a heat map strategy to determine the most advantageous moves. This bot is implemented in Python, and some components are in Ruby.

## Features

- Heat map analysis for optimal move selection
- Competitive gameplay against other Filler bots
- Easy to set up and configure

## Requirements

- Python 3.x
- Ruby 2.x

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ArseniiStratiuk/Filler-Bot.git
    cd Filler-Bot
    ```

2. Ensure Ruby is installed and configured correctly.

## Usage

To run the bot against the other one, use the following command for Windows OS:
```sh
ruby ./filler_vm -f ./map00 -p1 "py ./player1.py" -p2 "py ./player1.py"
```
And to use a visualizer:
```sh
ruby ./filler_vm -f ./map00 -p1 "py ./player1.py" -p2 "py ./player1.py" | py visualizer.py
```
