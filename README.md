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

Real-world platforms like Spotify and YouTube use hybrid recommenders. They combine **collaborative filtering**, which finds patterns across millions of users ("people who liked what you liked also liked this"), with **content-based filtering**, which compares the attributes of songs themselves. They lean heavily on implicit signals such as plays, skips, replays and playlist adds, and then re-rank results for variety and freshness. My version is a simplified **content-based** recommender: it has no data about other listeners, so it judges each song only by how closely its attributes match one user's stated taste. It prioritizes **genre** first, then **mood**, then how close a song's **energy** is to the user's target, with **acoustic preference** as a smaller bonus. A **scoring rule** gives each song a score plus the reasons behind it, and a **ranking rule** sorts all songs by score and returns the top *k*.

**`Song` features used in scoring**

- `genre`: categorical, matched against the user's favorite genre (e.g. lofi, pop, rock)
- `mood`: categorical, matched against the user's favorite mood (e.g. chill, happy, intense)
- `energy`: 0–1, scored by closeness to the user's target energy
- `acousticness`: 0–1, checked against whether the user likes acoustic songs

The `Song` object also stores `id`, `title`, `artist`, `tempo_bpm`, `valence` and `danceability`. They're kept for display and future experiments, but they aren't scored for now: tempo and danceability mostly repeat what energy already measures, and valence has a narrow range in this dataset.

**`UserProfile` features**

- `favorite_genre`: the genre the user wants most
- `favorite_mood`: the mood or vibe they're looking for
- `target_energy`: their ideal energy level, from 0 (calm) to 1 (intense)
- `likes_acoustic`: `True` if they prefer acoustic songs, `False` if they prefer electronic or produced ones

**Point weighting plan**

Each song earns points from four checks, for a maximum of **4.5 points**:

| Check | Max points | How points are earned |
|---|---|---|
| Genre match | 1.5 | Full 1.5 for an exact match; 0.75 for a closely related genre (e.g. `indie pop` vs `pop`) |
| Mood match | 1.0 | Full 1.0 for an exact match; 0.5 for a mood in the same family (see below) |
| Energy closeness | 1.5 | `1.5 × (1 − \|song.energy − target_energy\|)`, so the closest song earns the most, not just the loudest |
| Acoustic preference | 0.5 | `0.5 × acousticness` if `likes_acoustic`, otherwise `0.5 × (1 − acousticness)` |

Mood families used for partial credit:

- **Calm:** chill, relaxed, peaceful, focused
- **High energy:** intense, angry, euphoric, confident
- **Upbeat:** happy, carefree, romantic
- **Reflective:** moody, nostalgic, melancholic

Why these weights:

- **Genre is the biggest single match** because it reflects lasting taste. Someone who dislikes metal won't want a metal song in any mood.
- **Mood is weighted lower than genre** because it describes the moment, and part of it is already captured by energy and acousticness. Weighting it heavily would count the same signal twice.
- **Energy can match genre's 1.5 points, but only for a near-perfect fit.** Most songs earn only part of it, so genre still leads in practice.
- **Genre (1.5) is less than mood + energy (2.5).** This keeps a song that fits the requested vibe from losing to a song that only shares a genre label. Genre or mood matches are rare in this dataset (most genres and moods appear only once), so without this rule one label would decide the whole ranking.
- **Acoustic preference is a tie-breaker**, worth the least.

Example: a user with `genre=pop`, `mood=chill`, `target_energy=0.40` (acoustic points left out for simplicity):

| Song | Genre | Mood | Energy | Total |
|---|---|---|---|---|
| Midnight Coding (lofi, chill, 0.42) | 0 | 1.0 | 1.47 | **2.47** |
| Library Rain (lofi, chill, 0.35) | 0 | 1.0 | 1.43 | **2.43** |
| Sunrise City (pop, happy, 0.82) | 1.5 | 0 | 0.87 | **2.37** |
| Gym Hero (pop, intense, 0.93) | 1.5 | 0 | 0.71 | **2.21** |

With a heavier genre weight (2.0 genre / 1.0 mood / 1.0 energy), both high-energy pop songs ranked above the chill songs. That is the failure these weights are meant to avoid.

**Algorithm Recipe (final)**

1. Load every song from `data/songs.csv` and read the user's `UserProfile`.
2. For each song, start at 0 points and keep a list of reasons.
3. **Genre:** add 1.5 for an exact match, or 0.75 for a related genre.
4. **Mood:** add 1.0 for an exact match, or 0.5 for a mood in the same family.
5. **Energy:** add `1.5 × (1 − |song.energy − target_energy|)`.
6. **Acoustic:** add `0.5 × acousticness` if the user likes acoustic songs, otherwise `0.5 × (1 − acousticness)`.
7. Record a reason for each check that earned points (e.g. "genre match: pop (+1.5)").
8. Sort all songs by total score, highest first, and return the top *k* with their scores and reasons.

**Expected biases**

- **Genre can still win too often.** An exact genre match is the largest single bonus, so a song in the user's genre that only loosely fits their mood can outrank a song that matches the mood but not the genre.
- **Exact labels miss close matches.** Genre and mood are compared as text. Any related genre or mood family I didn't list (e.g. `lofi` and `ambient`) earns nothing.
- **The mood families are my own judgment.** Grouping moods like `confident` with `intense` is a choice, and another person might group them differently.
- **Small or rare genres get worse results.** Lofi has three songs, while metal, jazz, and classical have one each. A jazz fan gets one strong match and then songs from other genres.
- **Ignored features.** Valence, tempo, and danceability aren't scored, so two songs with the same energy but very different feel (sad vs. upbeat) can score alike.
- **No variety check.** The top results can cluster around one genre or artist (e.g. two LoRoom songs), because nothing rewards diversity.

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

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18

============================================================
 Top 5 Recommendations
 Profile -> genre: pop | mood: happy | energy: 0.8
============================================================

 1. Sunrise City  (Neon Echo)
    Score: 3.97
    Reasons:
      - genre match: pop (+1.50)
      - mood match: happy (+1.00)
      - energy 0.82 close to target 0.80 (+1.47)

 2. Rooftop Lights  (Indigo Parade)
    Score: 3.19
    Reasons:
      - related genre: indie pop (+0.75)
      - mood match: happy (+1.00)
      - energy 0.76 close to target 0.80 (+1.44)

 3. Gym Hero  (Max Pulse)
    Score: 2.80
    Reasons:
      - genre match: pop (+1.50)
      - energy 0.93 close to target 0.80 (+1.30)

 4. Island Breeze  (Sunny Roots)
    Score: 1.67
    Reasons:
      - similar mood: carefree (+0.50)
      - energy 0.58 close to target 0.80 (+1.17)

 5. Velvet Hours  (Jaylen Monroe)
    Score: 1.52
    Reasons:
      - similar mood: romantic (+0.50)
      - energy 0.48 close to target 0.80 (+1.02)

============================================================
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



