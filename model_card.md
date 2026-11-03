# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeFinder 1.0**

---

## 2. Goal / Task  

VibeFinder suggests songs you will probably like.

You tell it four things: your favorite genre, your mood, how much energy you want, and (optionally) whether you like acoustic music. It gives every song in the catalog a score. Then it shows you the top 5, with the reasons each song was picked.

It does not learn from you over time. It does not know what you listened to before. It only uses what you type in.

---

## 3. Data Used  

- **Size:** 18 songs. The starter file had 10. I added 8 more to cover more genres and moods.
- **Features for each song:** title, artist, genre, mood, energy, tempo, valence (how positive it sounds), danceability, and acousticness.
- **Genres:** 15 different ones, including pop, lofi, rock, jazz, metal, classical, folk, edm, and hip-hop.
- **Moods:** 14 different ones, like happy, chill, intense, melancholic, and romantic.

**Limits of the data**

- It is tiny. A real app has millions of songs.
- Most genres have just one song. Lofi has 3 and pop has 2.
- It leans calm. 10 of the 18 songs have energy below 0.6.
- There are no songs with energy between 0.58 and 0.75.
- Some combinations don't exist at all. For example, there is no song that is both high-energy and sad.
- The labels are my own judgment. Someone else might call a song "chill" that I called "relaxed."

---

## 4. Algorithm Summary  

Think of VibeFinder as a judge at a talent show. It looks at every song, gives it points, and lines them up from highest to lowest.

**How a song earns points**

1. **Genre.** Exact match gets full points. A related genre (like "indie pop" when you asked for "pop") gets half.
2. **Mood.** Exact match gets full points. A similar mood gets half. For example, "relaxed" and "focused" are in the same calm family as "chill."
3. **Energy.** This is about being *close*, not being *loud*. The closer a song's energy is to what you asked for, the more points it gets.
4. **Acoustic sound.** A small bonus. If you like acoustic music, acoustic songs get a little extra. If you like produced music, it flips. If you didn't say, this step is skipped.

**The point values**

| Rule | Original design | Current code ("Weight Shift" experiment) |
|---|---|---|
| Genre (exact / related) | 1.5 / 0.75 | 0.75 / 0.375 |
| Mood (exact / similar) | 1.0 / 0.5 | 1.0 / 0.5 |
| Energy (max) | 1.5 | 3.0 |
| Acoustic (max) | 0.5 | 0.5 |
| **Highest possible score** | 4.5 | 5.25 |

In the original design, genre was the biggest single rule. In the experiment, I doubled energy and cut genre in half to see what would happen. Now energy matters most.

Tempo, valence, and danceability are in the data, but VibeFinder ignores them.

Every recommendation lists its reasons, like "genre match: pop (+0.75)." You can see exactly why a song was picked.

---

## 5. Observed Behavior / Biases  

**What works well**

- When a song matches all your choices, it always wins. Happy Pop gets Sunrise City. Chill Lofi gets Library Rain.
- Opposite users get opposite lists. Happy Pop and Chill Lofi share zero songs.
- The reasons make it easy to check if a pick makes sense.

**Bias: a filter bubble around calm songs**

The catalog has more calm songs than loud ones. So calm songs show up for more people. I tested 2,310 different users (every genre, mood, and energy level). Library Rain made the top 5 for 43% of them. Iron Furnace, the loudest song, made it for only 20%.

**Bias: your favorite genre can get ignored**

With the current weights, energy beats genre. For 62% of the users I tested, the #1 song was not in their favorite genre. A lofi fan who wants high energy gets no lofi at all, because every lofi song is quiet.

**Other limits**

- **It fails silently.** If you ask for something that doesn't exist, it never tells you. It just hands you the closest thing.
- **Unknown words score zero.** If you type "sad" instead of "melancholic," no song gets mood points.
- **Same songs for everyone.** Gym Hero shows up for lots of different users because it is pop and very energetic.
- **No variety.** Two songs by the same artist can both land in your top 5.

---

## 6. Evaluation Process  

**What I did**

1. I ran 7 user profiles and read the top 5 for each.
2. I tried "tricky" profiles with conflicting wishes to see if I could fool the scoring.
3. I ran the "Weight Shift" experiment: doubled energy and halved genre, then compared results.
4. I ran every combination of genre, mood, and energy (2,310 users) to count how often each song appears.

All results below use the current "Weight Shift" weights.

**Profiles I tested**

| Profile | Genre / mood / energy | #1 result |
|---|---|---|
| Happy Pop | pop / happy / 0.8 | Sunrise City |
| Chill Lofi | lofi / chill / 0.35, likes acoustic | Library Rain |
| Deep Intense Rock | rock / intense / 0.9, dislikes acoustic | Storm Runner |
| EDM Euphoric | edm / euphoric / 0.95 | Strobe Horizon |
| Acoustic Folk | folk / melancholic / 0.3, likes acoustic | Letters I Never Sent |
| High-Energy Sad (tricky) | pop / melancholic / 0.9 | Gym Hero |
| Lofi but Intense (tricky) | lofi / intense / 0.95 | Gym Hero |

The five normal profiles got the #1 song I expected. The two tricky ones did not.

**Comparing pairs of profiles**

- **Happy Pop vs. Chill Lofi:** Happy Pop gets upbeat songs (energy 0.75–0.93). Chill Lofi gets quiet study music (energy 0.28–0.42). No songs overlap. That makes sense: they asked for opposite energy.
- **Chill Lofi vs. Acoustic Folk:** Both get soft, acoustic songs. Three songs show up in both lists. Only the #1 song is different, and it's the one in each user's genre. After that, a calm user just gets "calm songs." There's only one folk song, so there isn't much else to give.
- **Deep Intense Rock vs. EDM Euphoric:** Same five songs, different order. Each user's own genre comes first. That's fair: both want very loud music, and "intense" and "euphoric" are in the same mood family.
- **Happy Pop vs. Deep Intense Rock:** Gym Hero is in both lists. For Rock it fits well. For Happy Pop it's a weaker fit, but it still gets points for being pop and energetic.
- **Happy Pop vs. High-Energy Sad:** Both chose pop. The sad user still gets happy and intense pop, with Gym Hero at #1. There's no loud sad song in the catalog, so the mood just gets dropped.
- **Chill Lofi vs. Lofi but Intense:** Both love lofi. The intense user gets zero lofi songs. All lofi songs are quiet, and energy points now outweigh genre points.

**Why "Gym Hero" keeps showing up**

Gym Hero was in the top 5 for 5 of my 7 profiles. VibeFinder scores songs like a checklist, and Gym Hero checks a lot of boxes. It's pop, so pop fans give it genre points. It's very energetic (0.93), and energy is now worth the most. Its mood, "intense," is close to other energetic moods. It's never a *perfect* match for someone who wants happy pop. But it's "close enough" on everything, and there aren't many other loud pop songs to beat it.

**What surprised me**

I thought favorite genre would matter most. With the current weights, it often doesn't. I was also surprised that VibeFinder never admits when it can't find what you want. The High-Energy Sad user gets confident picks, and none of them are sad.

---

## 7. Intended Use and Non-Intended Use  

**Intended use**

- A classroom project to learn how recommenders work.
- Exploring how changing weights changes the results.
- Finding a few songs from a small, fixed list that roughly match a mood.

**Not intended for**

- Real users or a real music app. The catalog is far too small.
- Judging whether a genre or artist is "good." Scores only measure fit to one person's inputs.
- Anything important, like mental health support. A "sad" request doesn't mean the system understands how someone feels.
- Learning someone's taste over time. It has no memory and no listening history.

---

## 8. Ideas for Improvement  

1. **Balance the weights and the data.** Bring genre back up so it isn't drowned out by energy. Add more songs, especially loud songs in quiet genres (like upbeat lofi) and songs in the 0.6–0.75 energy range.
2. **Say when there's no good match.** If no song fits the mood, tell the user. Also warn when they type a mood or genre the system doesn't know, like "sad."
3. **Add variety.** Limit each artist to one song in the top 5. Use valence so "sad" vs. "happy" is measured by sound, not just by a label.

---

## 9. Personal Reflection  

**My biggest learning moment**

It was the "Weight Shift" experiment. I changed just two numbers: energy went up and genre went down. That one change completely flipped who the system served well. A lofi fan who wanted high energy suddenly got no lofi at all. I learned that the weights aren't small details. They *are* the recommender's opinion about what matters.

**How AI tools helped, and when I double-checked**

AI helped me come up with tricky test profiles I wouldn't have thought of, like "high energy but sad." It also found real bugs. Typing " Pop " with extra spaces gave a lower score than "pop." An energy of 5.0 made every score negative. It also wrote quick scripts to test thousands of users at once.

But I had to double-check it. Its numbers only applied to the weights in the code at that moment. When I changed the weights, the results changed too. Some of its first explanations also went further than the data showed, so I re-ran the profiles and checked each claim against the real output before keeping it.

**What surprised me about simple algorithms**

VibeFinder is just adding up points. There's no learning and no AI inside it. But when it lists reasons like "mood match: happy," it feels smart and personal. That's also a little dangerous. It sounds just as confident when it's wrong, like giving happy pop to someone who asked for sad songs. Showing reasons makes a system *feel* trustworthy, even when it isn't.

**What I'd try next**

- Use valence (how positive a song sounds) so "sad" is measured by the music, not just a label.
- Add a "no good match found" message so the system is honest when it can't help.
- Grow the catalog, and limit each artist to one song in the top 5 for more variety.
