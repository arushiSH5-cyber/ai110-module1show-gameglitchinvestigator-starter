# FIX: Core game logic refactored out of app.py into this module with Claude Code,
# so it can be unit-tested without running Streamlit.

ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Hard":
        # FIX: Hard was 1-50 (easier than Normal). Widened so difficulty actually increases.
        return 1, 200
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw.strip() == "":
        return False, None, "Enter a guess."

    raw = raw.strip()

    # FIX: Decimals used to be truncated ("50.9" -> 50 and counted as a win).
    # Now only whole numbers are accepted.
    try:
        value = int(raw)
    except ValueError:
        try:
            float(raw)
        except ValueError:
            return False, None, "That is not a number."
        return False, None, "Please enter a whole number."

    # FIX: Added range check so -5 or 500 aren't accepted as real guesses.
    if value < low or value > high:
        return False, None, f"Your guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess: int, secret: int):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    # FIX: Messages were swapped ("Too High" said "Go HIGHER"). Also removed the
    # str() fallback that compared numbers alphabetically ("9" > "50").
    if guess == secret:
        return "Win", "🎉 Correct!"
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number (1 = first guess).

    A win on the first guess is worth 100, minus 10 per extra attempt (minimum 10).
    Every wrong guess costs 5 points.
    """
    # FIX: Win bonus was off by one, and "Too High" gave +5 on even attempts.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in ("Too High", "Too Low"):
        return current_score - 5

    return current_score
