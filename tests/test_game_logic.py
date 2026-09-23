from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score

# FIX: check_guess returns (outcome, message), so the starter tests that compared the
# whole tuple to a string could never pass. They now unpack the outcome first.


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# --- Bug: hint messages were backwards ---

def test_too_high_message_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message


def test_too_low_message_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message


# --- Bug: secret was compared as a string on even attempts ("9" > "50") ---

def test_single_digit_guess_compares_numerically():
    outcome, _ = check_guess(9, 50)
    assert outcome == "Too Low"


# --- Bug: scoring rewarded wrong guesses and had an off-by-one win bonus ---

def test_wrong_guesses_always_lose_points():
    assert update_score(0, "Too High", attempt_number=2) == -5
    assert update_score(0, "Too Low", attempt_number=2) == -5


def test_first_guess_win_is_worth_100():
    assert update_score(0, "Win", attempt_number=1) == 100


def test_win_points_never_drop_below_10():
    assert update_score(0, "Win", attempt_number=50) == 10


# --- Bug: Hard range was smaller than Normal ---

def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high


# --- Edge cases for parse_guess (Challenge 1) ---

def test_negative_number_is_rejected():
    ok, value, err = parse_guess("-5", 1, 100)
    assert not ok and value is None
    assert "between 1 and 100" in err


def test_decimal_is_rejected_not_truncated():
    ok, value, err = parse_guess("50.9", 1, 100)
    assert not ok and value is None
    assert "whole number" in err


def test_extremely_large_number_is_rejected():
    ok, value, _ = parse_guess("99999999999999999999", 1, 100)
    assert not ok and value is None


def test_non_numeric_input_is_rejected():
    ok, _, err = parse_guess("abc", 1, 100)
    assert not ok
    assert err == "That is not a number."


def test_blank_and_whitespace_input_is_rejected():
    assert parse_guess("", 1, 100)[0] is False
    assert parse_guess("   ", 1, 100)[0] is False


def test_whitespace_around_valid_guess_is_accepted():
    assert parse_guess(" 42 ", 1, 100) == (True, 42, None)


def test_range_boundaries_are_inclusive():
    assert parse_guess("1", 1, 100) == (True, 1, None)
    assert parse_guess("100", 1, 100) == (True, 100, None)
    assert parse_guess("101", 1, 100)[0] is False
