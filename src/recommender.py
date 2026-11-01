import csv
from typing import Callable, List, Dict, Tuple, Optional
from dataclasses import dataclass, field

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    popularity: int = 50
    release_decade: int = 2020
    mood_tags: List[str] = field(default_factory=list)
    instrumentalness: float = 0.0
    speechiness: float = 0.0

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read songs from a CSV file into dicts, converting numeric columns and splitting mood tags."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field_name in ("id", "popularity", "release_decade"):
                row[field_name] = int(row[field_name])
            for field_name in ("energy", "tempo_bpm", "valence", "danceability", "acousticness",
                               "instrumentalness", "speechiness"):
                row[field_name] = float(row[field_name])
            row["mood_tags"] = row["mood_tags"].split(";") if row["mood_tags"] else []
            songs.append(row)
    return songs

# ---------------------------------------------------------------------------
# Feature rules: each one scores a single feature.
# A rule gets the user prefs, the song, and its weight from the active mode,
# and returns (points, reason), or None if it adds no points.
# ---------------------------------------------------------------------------

Rule = Callable[[Dict, Dict, float], Optional[Tuple[float, str]]]

def genre_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Full points when the song's genre equals the favorite genre."""
    if song["genre"] == user_prefs["favorite_genre"]:
        return weight, f"genre match: {song['genre']} (+{weight:.1f})"
    return None

def mood_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Full points when the song's mood equals the favorite mood."""
    if song["mood"] == user_prefs["favorite_mood"]:
        return weight, f"mood match: {song['mood']} (+{weight:.1f})"
    return None

def energy_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Reward closeness to the target energy, not just high or low energy."""
    target = user_prefs["target_energy"]
    points = weight * (1 - abs(song["energy"] - target))
    return points, f"energy {song['energy']:.2f} vs target {target:.2f} (+{points:.2f})"

def acoustic_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Reward acoustic songs for acoustic fans, and electronic songs for everyone else."""
    if user_prefs["likes_acoustic"]:
        points = weight * song["acousticness"]
        label = "acoustic sound"
    else:
        points = weight * (1 - song["acousticness"])
        label = "non-acoustic sound"
    return points, f"{label}: acousticness {song['acousticness']:.2f} (+{points:.2f})"

def mood_tags_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Points for the share of the user's mood tags that the song also has."""
    wanted = user_prefs["favorite_mood_tags"]
    shared = [tag for tag in wanted if tag in song["mood_tags"]]
    if not wanted or not shared:
        return None
    points = weight * len(shared) / len(wanted)
    return points, f"mood tags: {', '.join(shared)} (+{points:.2f})"

def decade_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Full points for the preferred decade, half points for a neighboring decade."""
    gap = abs(song["release_decade"] - user_prefs["preferred_decade"])
    if gap == 0:
        points = weight
    elif gap == 10:
        points = weight / 2
    else:
        return None
    return points, f"from the {song['release_decade']}s (+{points:.2f})"

def popularity_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Reward closeness to the target popularity (0-100), so fans of hidden gems get them."""
    target = user_prefs["target_popularity"]
    points = weight * (1 - abs(song["popularity"] - target) / 100)
    return points, f"popularity {song['popularity']} vs target {target} (+{points:.2f})"

def instrumental_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Reward instrumental songs for users who want them, and songs with vocals for everyone else."""
    if user_prefs["likes_instrumental"]:
        points = weight * song["instrumentalness"]
        label = "instrumental"
    else:
        points = weight * (1 - song["instrumentalness"])
        label = "has vocals"
    return points, f"{label}: instrumentalness {song['instrumentalness']:.2f} (+{points:.2f})"

def speechiness_rule(user_prefs: Dict, song: Dict, weight: float) -> Optional[Tuple[float, str]]:
    """Reward closeness to the target amount of spoken words (rap is high, singing is low)."""
    target = user_prefs["target_speechiness"]
    points = weight * (1 - abs(song["speechiness"] - target))
    return points, f"speechiness {song['speechiness']:.2f} vs target {target:.2f} (+{points:.2f})"

# Feature name -> (user pref key that turns the rule on, rule function)
FEATURE_RULES: Dict[str, Tuple[str, Rule]] = {
    "genre": ("favorite_genre", genre_rule),
    "mood": ("favorite_mood", mood_rule),
    "energy": ("target_energy", energy_rule),
    "acoustic": ("likes_acoustic", acoustic_rule),
    "mood_tags": ("favorite_mood_tags", mood_tags_rule),
    "decade": ("preferred_decade", decade_rule),
    "popularity": ("target_popularity", popularity_rule),
    "instrumental": ("likes_instrumental", instrumental_rule),
    "speechiness": ("target_speechiness", speechiness_rule),
}

# ---------------------------------------------------------------------------
# Scoring modes (Strategy pattern): every mode uses the same rules,
# but gives each feature a different weight.
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class ScoringMode:
    """A named ranking strategy: how many points each feature is worth."""
    name: str
    description: str
    weights: Dict[str, float]

_EXTRA_WEIGHTS = {"mood_tags": 1.0, "decade": 0.5, "popularity": 0.5, "instrumental": 0.5, "speechiness": 0.5}

SCORING_MODES: Dict[str, ScoringMode] = {
    mode.name: mode
    for mode in (
        ScoringMode("balanced", "The original recipe: genre first, then energy and mood",
                    {"genre": 2.0, "mood": 1.0, "energy": 2.0, "acoustic": 0.5, **_EXTRA_WEIGHTS}),
        ScoringMode("genre-first", "Stick to the favorite genre above everything else",
                    {"genre": 4.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5, **_EXTRA_WEIGHTS}),
        ScoringMode("mood-first", "Match the feeling, even across genres",
                    {"genre": 1.0, "mood": 2.5, "energy": 1.5, "acoustic": 0.5,
                     **_EXTRA_WEIGHTS, "mood_tags": 2.0}),
        ScoringMode("energy-focused", "Match the intensity level above labels",
                    {"genre": 1.0, "mood": 1.0, "energy": 4.0, "acoustic": 0.5, **_EXTRA_WEIGHTS}),
    )
}
DEFAULT_MODE = "balanced"

def max_score(user_prefs: Dict, mode: str = DEFAULT_MODE) -> float:
    """Highest score possible for this profile: the sum of weights for every feature the user set."""
    weights = SCORING_MODES[mode].weights
    return sum(weights[name] for name, (pref_key, _) in FEATURE_RULES.items() if pref_key in user_prefs)

def score_song(user_prefs: Dict, song: Dict, mode: str = DEFAULT_MODE) -> Tuple[float, List[str]]:
    """Score one song by running every feature rule the user has a preference for, weighted by the mode."""
    weights = SCORING_MODES[mode].weights
    score = 0.0
    reasons = []
    for name, (pref_key, rule) in FEATURE_RULES.items():
        if pref_key not in user_prefs:
            continue
        result = rule(user_prefs, song, weights[name])
        if result is not None:
            points, reason = result
            score += points
            reasons.append(reason)
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5,
                    mode: str = DEFAULT_MODE) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first (lower id breaks ties), and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, mode)
        scored.append((song, score, "; ".join(reasons)))

    # Highest score first; lower id wins ties so results are stable
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["id"]))
    return ranked[:k]
