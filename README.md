# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Apps like Spotify and YouTube guess what I will like by using two kinds of information. First, they look at what other people with similar taste listen to. If someone who likes the same songs as me also loves a song I have not heard, the app will suggest it to me. Second, they look at the song itself, like its genre, how fast it is, and how happy or calm it sounds. They also watch what I do, such as which songs I like, skip, replay, or add to playlists. These apps have millions of users, so they can mix all of this together to make very good guesses.

My version is much smaller and only uses the song itself. It gives each song a score based on how well it matches what the user likes. Genre matters the most, because people usually stick to the kinds of music they enjoy. Mood comes next. For energy, my system rewards songs that are close to the user's preferred energy level, not just songs with the highest or lowest energy. After every song gets a score, the system sorts them from highest to lowest and recommends the top few.

**Song features used:**

- `genre` (for example pop, lofi, rock)
- `mood` (for example happy, chill, intense)
- `energy` (a number from 0 to 1 for how intense the song feels)
- `acousticness` (a number from 0 to 1 for how acoustic the song sounds)

**UserProfile features used:**

- `favorite_genre`
- `favorite_mood`
- `target_energy`
- `likes_acoustic`

**My test user profile:**

```python
user_prefs = {
    "favorite_genre": "lofi",
    "favorite_mood": "chill",
    "target_energy": 0.40,
    "likes_acoustic": True,
}
```

**Algorithm Recipe:**

My catalog has 18 songs. For each song, the system adds up points like this:

| Rule | Points |
|---|---|
| Genre matches the user's favorite genre | +2.0 |
| Mood matches the user's favorite mood | +1.0 |
| Energy is close to the user's target energy | 2.0 × (1 − the gap between song energy and target energy), so 0 to 2.0 |
| Acoustic sound matches the user's taste | 0.5 × acousticness if the user likes acoustic, or 0.5 × (1 − acousticness) if not, so 0 to 0.5 |

The highest possible score is 5.5. The energy rule gives the most points to songs that are close to the user's target, not to songs that are just the loudest or the quietest. Each time a song earns points, the system saves a short reason, like "genre match (+2.0)", so it can explain its picks.

After every song has a score, the system sorts them from highest to lowest. If two songs tie, the one with the lower id goes first. It then shows the top 5 songs with their scores and reasons.

**Extra features and modes:** I also added 5 optional features (mood tags, release decade, popularity, instrumentalness, and speechiness) that only count if a profile sets them, plus 4 scoring modes you can switch with `python -m src.main --mode <balanced | genre-first | mood-first | energy-focused>`. See `ai_interactions.md` for details.

```
User prefs + songs.csv  ->  score every song  ->  sort by score  ->  top 5 with reasons
```

**Biases I expect:**

- Genre is worth the most points, so the system might push a song just because it has the right genre label, even if the mood is wrong. For example, a pop fan who wants happy music might get an intense gym song ranked above a happy indie pop song.
- Genre and mood only count if the words match exactly. "indie pop" does not count as "pop", and "ambient" gets no credit for a lofi fan, even though they sound close.
- Genres with more songs in the catalog, like lofi, have more chances to show up. Fans of genres with only one song will get songs picked only by energy and sound after that one song.
- The system does not look at valence, so a calm sad song and a calm happy song can score about the same.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Output of `python -m src.main`:

```
Loading songs from data/songs.csv...
Loaded songs: 18
Scoring mode: balanced (The original recipe: genre first, then energy and mood)

============================================================
Profile: Happy pop (default)
  genre=pop, mood=happy, energy=0.80, likes_acoustic=False
============================================================

#1  Sunrise City by Neon Echo
    Score: 5.37 / 5.50
    Because:
      - genre match: pop (+2.0)
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.80 (+1.96)
      - non-acoustic sound: acousticness 0.18 (+0.41)

#2  Gym Hero by Max Pulse
    Score: 4.21 / 5.50
    Because:
      - genre match: pop (+2.0)
      - energy 0.93 vs target 0.80 (+1.74)
      - non-acoustic sound: acousticness 0.05 (+0.47)

#3  Rooftop Lights by Indigo Parade
    Score: 3.25 / 5.50
    Because:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.80 (+1.92)
      - non-acoustic sound: acousticness 0.35 (+0.33)

#4  Concrete Verses by Blockline
    Score: 2.40 / 5.50
    Because:
      - energy 0.78 vs target 0.80 (+1.96)
      - non-acoustic sound: acousticness 0.12 (+0.44)

#5  Night Drive Loop by Neon Echo
    Score: 2.29 / 5.50
    Because:
      - energy 0.75 vs target 0.80 (+1.90)
      - non-acoustic sound: acousticness 0.22 (+0.39)

============================================================
Profile: Chill lofi
  genre=lofi, mood=chill, energy=0.40, likes_acoustic=True
============================================================

#1  Library Rain by Paper Lanterns
    Score: 5.33 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.35 vs target 0.40 (+1.90)
      - acoustic sound: acousticness 0.86 (+0.43)

#2  Midnight Coding by LoRoom
    Score: 5.31 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.42 vs target 0.40 (+1.96)
      - acoustic sound: acousticness 0.71 (+0.35)

#3  Focus Flow by LoRoom
    Score: 4.39 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - energy 0.40 vs target 0.40 (+2.00)
      - acoustic sound: acousticness 0.78 (+0.39)

#4  Spacewalk Thoughts by Orbit Bloom
    Score: 3.22 / 5.50
    Because:
      - mood match: chill (+1.0)
      - energy 0.28 vs target 0.40 (+1.76)
      - acoustic sound: acousticness 0.92 (+0.46)

#5  Coffee Shop Stories by Slow Stereo
    Score: 2.38 / 5.50
    Because:
      - energy 0.37 vs target 0.40 (+1.94)
      - acoustic sound: acousticness 0.89 (+0.45)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



