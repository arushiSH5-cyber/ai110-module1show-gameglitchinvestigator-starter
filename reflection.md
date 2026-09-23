# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess `60`, secret `50` (Normal) | "Too High" hint telling me to go lower | Hint says "📈 Go HIGHER!" and score goes **up** by 5 | No error. Outcome is "Too High" but the message is backwards |
| Guess `9` twice in a row (secret `50`) | "Too Low" both times | Guess 2 → "Too Low". Guess 3 → outcome **"Too High"** (+5 score). Same input gives a different result | No error. On even attempts the secret is cast to `str`, so `"9" > "50"` compares alphabetically |
| Lose a game, then click **New Game 🔁** | Fresh game starts | Still shows "Game over. Start a new game to try again." Status never resets | `st.session_state.status` stays `"lost"`. Attempts reset to `0` instead of `1` |
| Start a Normal game | 8 attempts allowed (sidebar says 8) | Banner says "Attempts left: 7". Game ends after 7 guesses | `attempts` initialized to `1` |
| Type `abc` and submit | Error, attempt not consumed | Error shown, but an attempt is used up and `"abc"` is added to history | `That is not a number.` |
| Type `50.9` (secret `50`) | Reject: not a whole number | Truncated to `50`, counts as a win | None |
| Type `-5` | "Out of range" message | Accepted as a normal guess | None |
| Switch difficulty to Easy | Secret within 1 to 20 | Sidebar says 1 to 20 but secret was `38`. Banner still says "between 1 and 100" | None |
| Pick Hard | Harder than Normal | Hard range is 1 to 50, *smaller* than Normal's 1 to 100 | None |
| Run `pytest` on the starter | Tests run | All 3 fail | `NotImplementedError: Refactor this function from app.py into logic_utils.py`. The tests also compare a tuple to a string (`result == "Win"`) |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion you did not accept as written (including what the AI suggested, why you rejected or changed it, and how you verified your version). It does not have to be a suggestion that was wrong: over-engineered, out of scope, harder to read, or a poor fit for this codebase all count.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

**Verification evidence**

- **Unit tests:** `pytest` went from 3 failed (`NotImplementedError`) to 17 passed. Full output is in `test_results.txt` and the README. There is one regression test per bug. For example, `test_single_digit_guess_compares_numerically` checks that `check_guess(9, 50)` is "Too Low", which the string-comparison bug got wrong.
- **Starter tests were buggy too:** they asserted `check_guess(50, 50) == "Win"`, but the function returns `("Win", "🎉 Correct!")`. They now unpack the outcome.
- **Live app:** Reproduced every bug from the log with Streamlit's `AppTest` (a headless driver for `app.py`) before the fix, then re-ran the same script after it. Guess 60 vs 50 now says "Go LOWER" and costs 5 points. `abc`, `50.9` and `-5` show errors without using an attempt. **New Game** after a loss resets to "Attempts left: 8". Switching to Easy gives a secret within 1 to 20.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
