import random
import streamlit as st

# FIX: Game logic moved to logic_utils.py (refactored with Claude Code) so it can be tested.
from logic_utils import (
    ATTEMPT_LIMITS,
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def start_new_game(difficulty: str):
    # FIX: New Game used to leave status as "won"/"lost" (stuck on "Game over"),
    # skip resetting score/history, and always pick 1-100. Now everything resets
    # together, using the current difficulty's range.
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0  # FIX: was 1 on first load, costing an attempt
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.session_state.difficulty = difficulty


def render_status(info_box, debug_box, low, high, attempts_left, difficulty, dev_mode):
    info_box.info(
        f"Guess a number between {low} and {high}. "
        f"Attempts left: {attempts_left}"
    )
    if dev_mode:
        with debug_box.container():
            with st.expander("Developer Debug Info"):
                st.write("Secret:", st.session_state.secret)
                st.write("Attempts:", st.session_state.attempts)
                st.write("Score:", st.session_state.score)
                st.write("Difficulty:", difficulty)
                st.write("History:", st.session_state.history)


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit = ATTEMPT_LIMITS[difficulty]
low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")
dev_mode = st.sidebar.toggle("Developer mode (show secret)", value=False)

# FIX: Also start a new game when difficulty changes, so the secret matches the new range.
if st.session_state.get("difficulty") != difficulty:
    start_new_game(difficulty)

st.subheader("Make a guess")

# FIX: Range was hardcoded to "1 and 100". The banner is filled in at the bottom of
# the script so "Attempts left" reflects the guess that was just submitted.
info_box = st.empty()

# FIX: Debug panel was drawn before the guess was processed, so it lagged one guess
# behind, and it revealed the secret to every player. It is now filled in at the end
# of the script and only shown when Developer mode is on.
debug_box = st.empty()

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    start_new_game(difficulty)
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    render_status(info_box, debug_box, low, high,
                  attempt_limit - st.session_state.attempts, difficulty, dev_mode)
    st.stop()

if submit:
    ok, guess_int, err = parse_guess(raw_guess, low, high)

    if not ok:
        # FIX: Invalid input no longer uses up an attempt or goes into history.
        st.error(err)
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        # FIX: Removed the even-attempt str() cast. The secret is always compared as an int.
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(
                f"Out of attempts! "
                f"The secret was {st.session_state.secret}. "
                f"Score: {st.session_state.score}"
            )

render_status(info_box, debug_box, low, high,
              attempt_limit - st.session_state.attempts, difficulty, dev_mode)

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
