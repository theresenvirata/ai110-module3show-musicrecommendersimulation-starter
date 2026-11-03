import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Point weights (max 5.25 points)
# Experiment "Weight Shift": genre halved (was 1.5 / 0.75), energy doubled (was 1.5)
GENRE_MATCH_POINTS = 0.75
GENRE_RELATED_POINTS = 0.375
MOOD_MATCH_POINTS = 1.0
MOOD_FAMILY_POINTS = 0.5
ENERGY_MAX_POINTS = 3.0
ACOUSTIC_MAX_POINTS = 0.5

# Moods in the same family earn partial credit
MOOD_FAMILIES = {
    "calm": {"chill", "relaxed", "peaceful", "focused"},
    "high energy": {"intense", "angry", "euphoric", "confident"},
    "upbeat": {"happy", "carefree", "romantic"},
    "reflective": {"moody", "nostalgic", "melancholic"},
}

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
    """Reads songs from a CSV file into dicts, converting numeric columns to int/float."""
    print(f"Loading songs from {csv_path}...")
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores one song against user preferences and returns (score, list of reasons)."""
    score = 0.0
    reasons = []

    # Accept both the short keys used in main.py and the UserProfile field names
    fav_genre = user_prefs.get("genre", user_prefs.get("favorite_genre", "")).lower()
    fav_mood = user_prefs.get("mood", user_prefs.get("favorite_mood", "")).lower()
    target_energy = user_prefs.get("energy", user_prefs.get("target_energy"))
    likes_acoustic = user_prefs.get("likes_acoustic")

    # Genre: exact match, or partial credit when one name contains the other (e.g. "indie pop" / "pop")
    song_genre = song["genre"].lower()
    if fav_genre and song_genre == fav_genre:
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match: {song_genre} (+{GENRE_MATCH_POINTS:.2f})")
    elif fav_genre and (fav_genre in song_genre or song_genre in fav_genre):
        score += GENRE_RELATED_POINTS
        reasons.append(f"related genre: {song_genre} (+{GENRE_RELATED_POINTS:.2f})")

    # Mood: exact match, or partial credit for a mood in the same family
    song_mood = song["mood"].lower()
    if fav_mood and song_mood == fav_mood:
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match: {song_mood} (+{MOOD_MATCH_POINTS:.2f})")
    elif fav_mood and any(fav_mood in family and song_mood in family for family in MOOD_FAMILIES.values()):
        score += MOOD_FAMILY_POINTS
        reasons.append(f"similar mood: {song_mood} (+{MOOD_FAMILY_POINTS:.2f})")

    # Energy: reward closeness to the target, not just high energy
    if target_energy is not None:
        energy_points = ENERGY_MAX_POINTS * (1 - abs(song["energy"] - target_energy))
        score += energy_points
        reasons.append(f"energy {song['energy']:.2f} close to target {target_energy:.2f} (+{energy_points:.2f})")

    # Acoustic: tie-breaker, only scored when the user stated a preference
    if likes_acoustic is not None:
        if likes_acoustic:
            acoustic_points = ACOUSTIC_MAX_POINTS * song["acousticness"]
            label = "acoustic sound"
        else:
            acoustic_points = ACOUSTIC_MAX_POINTS * (1 - song["acousticness"])
            label = "produced/electronic sound"
        score += acoustic_points
        reasons.append(f"{label} (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song and returns the top k as (song, score, explanation), highest first."""
    # Judge every song with score_song -> list of (song, score, reasons)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # sorted() returns a new list, leaving the caller's songs list untouched
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked[:k]]
