import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Scoring weights (see "Algorithm Recipe" in README.md)
GENRE_WEIGHT = 2.0
MOOD_WEIGHT = 1.0
ENERGY_WEIGHT = 2.0
ACOUSTIC_WEIGHT = 0.5
MAX_SCORE = GENRE_WEIGHT + MOOD_WEIGHT + ENERGY_WEIGHT + ACOUSTIC_WEIGHT

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
    """Read songs from a CSV file into dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in ("energy", "tempo_bpm", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user prefs (genre +2, mood +1, energy closeness 0-2, acoustic 0-0.5) and list the reasons."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs.get("favorite_genre"):
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT:.1f})")

    if song["mood"] == user_prefs.get("favorite_mood"):
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT:.1f})")

    # Reward closeness to the target energy, not just high or low energy
    if "target_energy" in user_prefs:
        energy_points = ENERGY_WEIGHT * (1 - abs(song["energy"] - user_prefs["target_energy"]))
        score += energy_points
        reasons.append(
            f"energy {song['energy']:.2f} vs target {user_prefs['target_energy']:.2f} (+{energy_points:.2f})"
        )

    if "likes_acoustic" in user_prefs:
        if user_prefs["likes_acoustic"]:
            acoustic_points = ACOUSTIC_WEIGHT * song["acousticness"]
            label = "acoustic sound"
        else:
            acoustic_points = ACOUSTIC_WEIGHT * (1 - song["acousticness"])
            label = "non-acoustic sound"
        score += acoustic_points
        reasons.append(f"{label}: acousticness {song['acousticness']:.2f} (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort highest first (lower id breaks ties), and return the top k as (song, score, explanation)."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))

    # Highest score first; lower id wins ties so results are stable
    ranked = sorted(scored, key=lambda item: (-item[1], item[0]["id"]))
    return ranked[:k]
