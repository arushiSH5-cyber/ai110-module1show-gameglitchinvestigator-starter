# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game purpose:** A Streamlit number-guessing game. You pick a difficulty, then guess a secret number in a limited number of attempts. The game gives "higher/lower" hints and keeps score.
- [x] **Bugs found:**
  1. Hints were backwards ("Too High" said "Go HIGHER").
  2. On every even attempt the secret was cast to a string, so guesses were compared alphabetically (`"9" > "50"`).
  3. **New Game** after a loss stayed stuck on "Game over". Status, score and history never reset.
  4. Attempts started at 1, so the first game had one fewer guess than advertised.
  5. Scoring gave +5 for some wrong guesses, and the win bonus was off by one.
  6. Invalid input (`abc`) still used up an attempt. Decimals were truncated (`50.9` won on 50). Negative or out-of-range numbers were accepted.
  7. Changing difficulty kept the old secret (Easy said 1 to 20 but the secret was 38). The banner always said "1 and 100".
  8. Hard's range (1 to 50) was smaller than Normal's (1 to 100).
  9. The starter tests could never pass: they compared a `(outcome, message)` tuple to a string.
- [x] **Fixes applied:** Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` into `logic_utils.py` and fixed them there. `app.py` now only handles UI and session state. A `start_new_game()` helper resets all state and runs on **New Game** or a difficulty change. The secret is always compared as an int. Input is validated before an attempt is counted. Every fix is marked with a `# FIX:` comment.

## 📸 Demo Walkthrough

Normal difficulty (range 1 to 100, 8 attempts). The secret is 50 (visible in "Developer Debug Info").

1. The game opens with "Guess a number between 1 and 100. Attempts left: 8", score 0.
2. User types `abc` and submits. The game shows "That is not a number." and attempts left stays at 8.
3. User enters `40`. The game shows "📈 Go HIGHER!". Score is -5, attempts left 7.
4. User enters `70`. The game shows "📉 Go LOWER!". Score is -10, attempts left 6.
5. User enters `50`. Balloons appear with "You won! The secret was 50. Final score: 70" (80 points for winning on attempt 3, minus 10 for the two misses).
6. Further guesses are blocked with "You already won. Start a new game to play again."
7. User clicks **New Game 🔁**. Score, history and attempts reset (8 left) and a new secret is picked.
8. User switches to **Hard**. The banner updates to "between 1 and 200, Attempts left: 5" and the new secret is within that range.

## 🧪 Test Results

Includes Challenge 1 edge cases (negative, decimal and extremely large inputs):

```
$ pytest
============================= test session starts ==============================
platform darwin -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/arushin/Downloads/game-glitch-investigator
plugins: anyio-4.15.1
collected 17 items

tests/test_game_logic.py .................                               [100%]

============================== 17 passed in 0.02s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
