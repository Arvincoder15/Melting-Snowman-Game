# Melting-Snowman-Game
Hangman-style Clue Guessing Game built with Python and Pygame 🎮⛄

## Features
- Playable categories:
  - Famous Movies
  - Famous Athletes
  - Soccer Teams
- Clue-based word puzzles loaded from `puzzle.txt`
- On-screen A–Z buttons with hover states
- 9-frame snowman melting animation
- Sound effects for correct/incorrect guesses and win/lose screens
- Keyboard shortcuts for quick replay or category change

## How to Play
1. Launch the game and choose a category.
2. Click letters (A–Z) to guess the hidden word.
3. Each wrong guess melts the snowman.
4. You lose after 8 wrong guesses.
5. Solve the word before the snowman melts to win!

## Controls
- **Mouse**: Click on letters to guess
- **A**: Play again (new puzzle)
- **C**: Back to category menu
- **Esc**: Quit the game

## Requirements
- Python 3.8+
- Pygame 2.x

Install dependencies:
```bash
pip install pygame
