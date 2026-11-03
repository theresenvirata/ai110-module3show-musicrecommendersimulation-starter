# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Think of the recommender as a judge at a talent show. It looks at every song in the catalog one at a time, gives each one points based on how well it fits what you asked for, and then lines the songs up from highest score to lowest. The top five are your recommendations.

**What it knows about you**

- Your favorite genre (for example, pop)
- The mood you're in (for example, happy)
- How energetic you want the music to be, on a scale from calm to intense
- Optionally, whether you like acoustic songs or prefer electronic, produced ones

**What it looks at in each song**

Every song has a genre, a mood, an energy level, and an "acousticness" rating. The songs also have tempo, positivity, and danceability, but the judge ignores those for now. Tempo and danceability mostly repeat what energy already says.

**How a song earns points**

1. **Genre (worth the most).** A song in your exact genre gets full points. A song in a closely related genre, like "indie pop" when you asked for "pop," gets half.
2. **Mood.** A song with your exact mood gets full points. A song with a similar mood gets half. For example, if you want "chill," a "relaxed" or "focused" song still earns some credit, because they belong to the same calm family.
3. **Energy.** This is about being *close*, not being *loud*. If you want medium energy, a medium-energy song scores best, and a very calm or very intense song scores lower. The further a song is from what you asked for, the fewer points it gets.
4. **Acoustic sound (a small tie-breaker).** If you said you like acoustic music, more acoustic songs get a little bonus. If you prefer produced music, it works the other way. If you didn't say, this step is skipped.

A song can earn at most 4.5 points. Genre counts the most because it reflects lasting taste. Mood and energy together still outweigh genre, so a song that matches your vibe can beat a song that only shares a genre label.

**Why it shows its reasons**

Next to every recommendation, the judge lists what earned the song its points, such as "genre match: pop (+1.50)." You can see exactly why a song was picked instead of trusting a mystery number.

**Changes from the starter logic**

The starter version returned the first five songs in the file, no matter who was asking. I replaced that with the point system above, added partial credit for related genres and similar moods, and made the energy score reward closeness instead of high energy.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
