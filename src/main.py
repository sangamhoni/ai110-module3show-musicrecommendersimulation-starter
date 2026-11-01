"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

from src.recommender import DEFAULT_MODE, SCORING_MODES, load_songs, max_score, recommend_songs

BASIC_PREFS = ("favorite_genre", "favorite_mood", "target_energy", "likes_acoustic")


def print_recommendations(name: str, user_prefs: dict, recommendations: list, mode: str) -> None:
    """Print a profile header and each recommendation with its rank, score, and reasons."""
    best = max_score(user_prefs, mode)
    print("=" * 60)
    print(f"Profile: {name}")
    print(
        f"  genre={user_prefs['favorite_genre']}, mood={user_prefs['favorite_mood']}, "
        f"energy={user_prefs['target_energy']:.2f}, likes_acoustic={user_prefs['likes_acoustic']}"
    )
    extras = {key: value for key, value in user_prefs.items() if key not in BASIC_PREFS}
    if extras:
        print("  " + ", ".join(f"{key}={value}" for key, value in extras.items()))
    print("=" * 60)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / {best:.2f}")
        print("    Because:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument("--mode", choices=SCORING_MODES, default=DEFAULT_MODE,
                        help="ranking strategy to use (default: %(default)s)")
    parser.add_argument("--profile", help="only run profiles whose name contains this text")
    args = parser.parse_args()

    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    print(f"Scoring mode: {args.mode} ({SCORING_MODES[args.mode].description})\n")

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
        # Uses the advanced features (mood tags, decade, popularity, instrumentalness, speechiness)
        "Late-night retro explorer": {
            "favorite_genre": "synthwave",
            "favorite_mood": "moody",
            "target_energy": 0.60,
            "likes_acoustic": False,
            "favorite_mood_tags": ["nostalgic", "nocturnal", "dreamy"],
            "preferred_decade": 1980,
            "target_popularity": 40,
            "likes_instrumental": True,
            "target_speechiness": 0.05,
        },
    }

    for name, user_prefs in profiles.items():
        if args.profile and args.profile.lower() not in name.lower():
            continue
        recommendations = recommend_songs(user_prefs, songs, k=5, mode=args.mode)
        print_recommendations(name, user_prefs, recommendations, args.mode)


if __name__ == "__main__":
    main()
