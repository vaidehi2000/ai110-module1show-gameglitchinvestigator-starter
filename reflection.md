# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the secret number kept changing" or "the hints were backwards").
  When I first ran the game, it appeared functional on the surface but had several hidden logic errors. The attempt counter started at 1 instead of 0, which meant every player silently lost one attempt before making a single guess. The hints were reversed on even-numbered attempts — the game would tell you to go higher when the answer was actually lower, and vice versa. The number range shown in the info bar was hardcoded to "1 and 100" regardless of which difficulty was selected, so Easy and Hard showed the wrong range. Finally, clicking "New Game" did not reset the game status or history, which meant a finished game (won or lost) would stay stuck and not let you play again.

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude AI (Claude Code, Chat mode) as my main AI teammate throughout this project.

**Correct suggestion — fixing the string comparison bug:**
Claude identified that on every even-numbered attempt, the code cast `secret` to a string using `str()` before passing it to `check_guess`. This caused Python to compare strings instead of integers, so `"9" > "10"` evaluated to `True` (because `"9"` comes after `"1"` alphabetically), making the hint say "Go LOWER" when the answer was actually higher. Claude suggested removing the `str()` cast entirely and instead casting both `guess` and `secret` to `int` inside `check_guess`. I verified this by writing a pytest regression test: `check_guess(9, "10")` now correctly returns `"Too Low"`, and manually confirmed the hints were correct on even-numbered guesses in the running app.

**Incorrect/misleading suggestion — the conftest.py fix:**
When I got a `ModuleNotFoundError: No module named 'logic_utils'` running tests, Claude suggested creating a `conftest.py` file at the project root to add the root to `sys.path`. This worked, but it was not the real fix — the actual problem was that I was running `python tests/test_game_logic.py` directly instead of `python -m pytest tests/test_game_logic.py`. Running with `python` skips pytest entirely and uses a different `sys.path`. The `conftest.py` file isn't wrong, but Claude's explanation made it sound like a necessary fix when the simpler solution was just to use the right command. I verified this when Claude ran the tests from the terminal and all 4 passed immediately with `python -m pytest`.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I decided a bug was really fixed only when I could reproduce the original broken behavior, apply the fix, and confirm the correct behavior — either through a passing pytest test or manual play in the running app.

**pytest regression test for the string comparison bug:**
Claude helped me write `test_string_secret_does_not_break_comparison` in `tests/test_game_logic.py`. The test calls `check_guess(9, "10")` — passing secret as a string exactly as the old buggy code did on even attempts. Before the fix, string comparison made `"9" > "10"` return `True`, so the outcome would be `"Too High"` instead of `"Too Low"`. After the fix (casting both to `int` in `check_guess`), the test passes and confirms `"Too Low"` is returned. Running `python -m pytest tests/test_game_logic.py -v` showed all 4 tests passing, which gave me confidence the logic was correct.

**Manual test for the difficulty reset fix:**
For the difficulty-change-resets-game fix, there is no pytest test (since it involves Streamlit session state). I verified it manually by opening the app, making a few guesses on Normal difficulty, then switching to Hard in the sidebar. Before the fix, the old secret and attempt count carried over. After the fix, the attempt counter reset to 0, a new secret was generated within the Hard range (1–500), and the history cleared — confirmed by checking the Developer Debug Info expander.

Claude helped design the regression test by explaining exactly which input would trigger the old bug and why, making it easy to write a precise, targeted test case rather than a generic one.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
