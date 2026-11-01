# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Claude Code (running in VS Code) to add 5 or more new song features to the dataset, update the scoring so it uses them, and add multiple scoring modes that I can switch between in `main.py`.

**Prompts used:**

My main prompt was the challenge text itself:

> Challenge 1: Add Advanced Song Features. Introduce 5 or more complex attributes to your dataset that are not currently present in the baseline data, such as Song Popularity (0-100), Release Decade, or Detailed Mood Tags (e.g., "nostalgic," "aggressive," "euphoric"). Update both data/songs.csv and the scoring logic in src/recommender.py so scoring accounts for the new attributes.
>
> Challenge 2: Create Multiple Scoring Modes. Build two or more different ranking strategies (e.g., "Genre-First," "Mood-First," or "Energy-Focused") so a user can switch between modes in main.py. ... brainstorm a design pattern (like a simple "Strategy" pattern) that keeps your code modular.

**What did the agent generate or change?**

- **Before changing anything**, it saved the program's full output so it could compare against it later.
- **`data/songs.csv`:** added 5 new columns to all 18 songs.
  - `popularity`: 0 to 100
  - `release_decade`: for example 1980
  - `mood_tags`: 3 tags per song, like `nostalgic;nocturnal;dreamy`
  - `instrumentalness`: 0 to 1
  - `speechiness`: 0 to 1, where rap is high
- **`src/recommender.py`:**
  - `load_songs` now converts the new number columns and splits `mood_tags` into a list.
  - Each feature now has its own small scoring function (a "rule"). There are 4 old rules and 5 new ones:

    | New rule | How it gives points |
    |---|---|
    | Mood tags | Points for the share of the user's tags the song also has |
    | Decade | Full points for the exact decade, half for the decade next to it |
    | Popularity | More points the closer the song is to the target |
    | Instrumental | Points for instrumental songs if the user wants them, or for songs with vocals if not |
    | Speechiness | More points the closer the song is to the target |

  - A rule only runs if the user set that preference. That way old profiles keep their old scores.
  - It added 4 scoring modes (see the Design Pattern section) and a `max_score()` function.
  - The `Song` class got the 5 new fields with default values, so the old tests still work.
- **`src/main.py`:**
  - Added a `--mode` option to switch modes, and a `--profile` option to run just one profile.
  - Shows the right maximum score for each profile and mode.
  - Added a new "Late-night retro explorer" profile that uses all the new features.
- **`tests/test_recommender.py`:** added 3 tests:
  - the new columns load correctly
  - the new features only add points when the user sets them
  - switching modes changes the ranking
- **`README.md`:** added the new "Scoring mode" line to the sample output.

**What did you verify or fix manually?**

- **Old results did not change.** The output for my 8 old profiles is exactly the same as before. The only difference is the new "Scoring mode: balanced" line at the top.
- **Checked one score by hand.** Night Drive Loop gets 7.79 out of 8.50 for the retro profile:

  | Points | Reason |
  |---|---|
  | 2.0 | genre |
  | 1.0 | mood |
  | 1.70 | energy |
  | 0.39 | acoustic |
  | 1.0 | all 3 mood tags |
  | 0.5 | 1980s |
  | 0.41 | popularity |
  | 0.30 | instrumental |
  | 0.49 | speechiness |
  | **7.79** | **total** |

- **Checked the max scores.** They add up correctly: 8.50 in balanced mode and 9.50 in the other three modes for the retro profile.
- **Tried a bad mode name.** `--mode nope` gives a clear error that lists the real modes.
- **Ran the tests.** All 5 pass. One new test first compared decimal numbers with `==`, which can break because of rounding. It was changed to `pytest.approx`.
- **Checked if the modes really behave differently.** For happy pop, `balanced` and `genre-first` put Gym Hero at #2, while `mood-first` and `energy-focused` put Rooftop Lights at #2. That matches what I expected from my earlier weight experiment.
- **One thing I noticed:** for the retro profile, every mode picks Night Drive Loop at #1, because it is the only synthwave song. The rest of the list barely changes. The modes matter more when a user's favorite genre has several songs.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

The Strategy pattern. Each scoring mode is a strategy that can be swapped in when the program runs.

**How did AI help you brainstorm or implement it?**

I asked the AI how to add modes without making `score_song` a mess. It gave me three options:

1. **An `if`/`elif` for each mode inside `score_song`.** This is the easiest, but every new mode or feature makes the function longer. Changing one mode could break another one by accident.
2. **The classic Strategy pattern: one class per mode, each with its own `score()` method.** This is very flexible, but all my modes use the same math and only the weights change. So every class would repeat almost the same code.
3. **Strategy as data.** Each mode is a small `ScoringMode` object that only stores a name, a description, and a weight for each feature. The scoring math lives in separate feature rules that every mode shares.

I picked option 3 because my modes only differ in weights. With it:

- A new mode is just a new set of weights.
- A new feature is one new rule function plus one line in the list of rules.
- `score_song` never needs to change for either one.

The AI also pointed out that keeping the old weights as the `balanced` default would keep all my earlier results and documentation correct.

**How does the pattern appear in your final code?**

- **`ScoringMode`** in `src/recommender.py` is the strategy object (name, description, weights).
- **`SCORING_MODES`** holds the 4 strategies:

  | Mode | Focus |
  |---|---|
  | `balanced` | The original recipe |
  | `genre-first` | Genre is worth 4 points |
  | `mood-first` | Mood and mood tags count more |
  | `energy-focused` | Energy is worth 4 points |

- **`FEATURE_RULES`** links each feature to its rule function (`genre_rule`, `energy_rule`, `mood_tags_rule`, and so on).
- **`score_song(user_prefs, song, mode)`** gets the weights for the chosen mode and runs every rule. It does not care which mode it is using.
- **`main.py`** picks the strategy from the command line: `python -m src.main --mode mood-first`.
