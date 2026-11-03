"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

from recommender import load_songs, recommend_songs

# Resolve data path relative to this file so the script works from any directory
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "songs.csv")


def main() -> None:
    songs = load_songs(DATA_PATH)
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print_recommendations(user_prefs, recommendations)


def print_recommendations(user_prefs: dict, recommendations: list) -> None:
    """Prints ranked recommendations with their score and the reasons behind it."""
    width = 60
    profile = " | ".join(f"{key}: {value}" for key, value in user_prefs.items())

    print()
    print("=" * width)
    print(f" Top {len(recommendations)} Recommendations")
    print(f" Profile -> {profile}")
    print("=" * width)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print()
        print(f" {rank}. {song['title']}  ({song['artist']})")
        print(f"    Score: {score:.2f}")
        print("    Reasons:")
        for reason in explanation.split("; "):
            print(f"      - {reason}")

    print()
    print("=" * width)


if __name__ == "__main__":
    main()
