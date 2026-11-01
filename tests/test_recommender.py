import pytest

from src.recommender import Song, UserProfile, Recommender, load_songs, max_score, recommend_songs, score_song

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            valence=0.9,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            valence=0.6,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        likes_acoustic=False,
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_load_songs_parses_advanced_features():
    songs = load_songs("data/songs.csv")
    night_drive = next(s for s in songs if s["title"] == "Night Drive Loop")
    assert night_drive["popularity"] == 58
    assert night_drive["release_decade"] == 1980
    assert night_drive["mood_tags"] == ["nostalgic", "nocturnal", "dreamy"]
    assert isinstance(night_drive["instrumentalness"], float)


def test_advanced_features_only_score_when_user_sets_them():
    song = load_songs("data/songs.csv")[7]  # Night Drive Loop
    basic = {"favorite_genre": "synthwave", "favorite_mood": "moody", "target_energy": 0.6, "likes_acoustic": False}
    advanced = {**basic, "favorite_mood_tags": ["nostalgic", "dreamy"], "preferred_decade": 1980}

    basic_score, _ = score_song(basic, song)
    advanced_score, reasons = score_song(advanced, song)

    assert advanced_score == pytest.approx(basic_score + 1.0 + 0.5)  # all tags matched + exact decade
    assert any("mood tags" in r for r in reasons)
    assert max_score(advanced) == max_score(basic) + 1.5


def test_scoring_mode_changes_ranking():
    songs = load_songs("data/songs.csv")
    happy_pop = {"favorite_genre": "pop", "favorite_mood": "happy", "target_energy": 0.8, "likes_acoustic": False}

    balanced = [s["title"] for s, _, _ in recommend_songs(happy_pop, songs, k=3, mode="balanced")]
    mood_first = [s["title"] for s, _, _ in recommend_songs(happy_pop, songs, k=3, mode="mood-first")]

    assert balanced[1] == "Gym Hero"          # genre label wins
    assert mood_first[1] == "Rooftop Lights"  # happy mood wins
