"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import MAX_SCORE, load_songs, recommend_songs


def print_recommendations(name: str, user_prefs: dict, recommendations: list) -> None:
    """Print a profile header and each recommendation with its rank, score, and reasons."""
    print("=" * 60)
    print(f"Profile: {name}")
    print(
        f"  genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']:.2f}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / {MAX_SCORE:.2f}")
        print("    Because:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    profiles = {
        "Happy pop (default)": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.80,
            "likes_acoustic": False,
        },
        "Chill lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.40,
            "likes_acoustic": True,
        },
        "Deep intense rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.92,
            "likes_acoustic": False,
        },
        # Edge cases: profiles meant to trick the scoring logic
        "Edge: hyped but sad": {
            "favorite_genre": "folk",
            "favorite_mood": "sad",
            "target_energy": 0.90,
            "likes_acoustic": True,
        },
        "Edge: genre not in catalog": {
            "favorite_genre": "k-pop",
            "favorite_mood": "happy",
            "target_energy": 0.75,
            "likes_acoustic": False,
        },
        "Edge: acoustic metalhead": {
            "favorite_genre": "metal",
            "favorite_mood": "angry",
            "target_energy": 0.95,
            "likes_acoustic": True,
        },
        "Edge: capitalized labels": {
            "favorite_genre": "Pop",
            "favorite_mood": "Happy",
            "target_energy": 0.80,
            "likes_acoustic": False,
        },
        "Edge: energy out of range": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 1.50,
            "likes_acoustic": True,
        },
    }

    for name, user_prefs in profiles.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, user_prefs, recommendations)


if __name__ == "__main__":
    main()
