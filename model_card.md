# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeCheck 1.0**

---

## 2. Goal and Intended Use  

**Goal:** VibeCheck suggests songs a user will probably like. It looks at what the user says they like (a genre, a mood, an energy level, and if they like acoustic sound) and picks the 5 songs from the catalog that match best.

**Intended use:** This is a classroom project. It is for learning how recommenders turn data into picks, and for testing how small changes to the rules change the results.

**Not intended for:**

- Real users or a real music app. The catalog is tiny and made up.
- Judging if a song or artist is "good". A low score only means the song does not match one user's settings.
- Learning anything about a person. It does not watch what you play or skip, so it cannot learn your taste over time.

---

## 3. How the Model Works  

Every song gets points, like a judge scoring a contest.

- If the song's genre matches the user's favorite genre, it gets 2 points.
- If the song's mood matches the user's favorite mood, it gets 1 point.
- It gets up to 2 points for energy. The closer the song's energy is to what the user wants, the more points it gets. A song that is too loud or too quiet both lose points.
- It gets up to half a point for sound. Users who like acoustic music get points for acoustic songs, and everyone else gets points for electronic songs.

The best possible score is 5.5. After every song is scored, the system sorts them from highest to lowest and shows the top 5. Each pick comes with a list of reasons, like "genre match: pop (+2.0)", so you can see why it was chosen.

The starter code had no real logic. It just returned the first few songs. I added the CSV loading, the scoring, the ranking, and the reasons.

---

## 4. Data  

- The catalog has 18 songs. The starter file had 10, and I added 8 more.
- My new songs added genres and moods that were missing: hip hop, classical, metal, country, r&b, edm, folk, and reggae, plus moods like sad, angry, peaceful, romantic, and nostalgic.
- Each song has a genre, a mood, and 5 numbers: energy, tempo, valence (how happy it sounds), danceability, and acousticness.
- My system only uses genre, mood, energy, and acousticness.

Limits of the data:

- Most genres only have 1 song. Lofi has the most with 3.
- All the songs and artists are made up, and the numbers were picked by hand.
- It has nothing about lyrics, language, or how popular a song is.
- Each song only gets one mood, but real songs can feel like more than one thing.

---

## 5. Strengths  

- The #1 pick almost always feels right. Sunrise City for happy pop, Library Rain for chill lofi, and Storm Runner for intense rock are the songs I would pick myself.
- It clearly tells opposite users apart. The happy pop list and the chill lofi list share no songs at all.
- The energy rule works the way I wanted. It rewards songs that are close to the target instead of just picking the loudest song.
- It explains itself. Every pick shows exactly where its points came from.
- If a user's genre is not in the catalog, it does not crash. It just uses mood and energy instead.

---

## 6. Limitations and Bias 

My system has a "loud song bubble" for anyone whose favorite genre is small. The catalog only has 1 to 3 songs per genre, so once those are used up, the rest of the list is picked by energy alone, and the same loud, non-acoustic songs (Gym Hero, Storm Runner, Pulse Reactor, Sunrise City) win those spots. In my tests, a sad folk fan and an intense rock fan got 4 of the same 5 songs, and Sunrise City showed up in 6 of my 8 lists. The energy gap only looks at one number, so a user who wants music that is both sad and energetic gets either sad or energetic songs, never both. Exact word matching makes this worse, because a song labeled "indie pop" or a user typing "Pop" gets no genre credit at all.

---

## 7. Evaluation  

I tested 8 user profiles. Three are normal listeners: Happy pop, Chill lofi, and Deep intense rock. Five are edge cases made to trick the system: a fan who wants sad but high energy music, a fan of a genre that is not in the catalog (k-pop), a metal fan who likes acoustic sound, a user who typed "Pop" and "Happy" with capital letters, and a user with an energy target of 1.5, which is outside the 0 to 1 range. For each one I checked if the #1 song made sense and if the rest of the top 5 still matched the user's taste.

What surprised me most was how often the same few loud songs showed up, even for users who are very different. I also did not expect a small thing like a capital letter to quietly break the results, with no error at all.

### Stress test output

I ran `python -m src.main` with 8 profiles: 3 normal ones and 5 edge cases built to trick the scoring.

**Happy pop (default)**

```
Profile: Happy pop (default)
  genre=pop, mood=happy, energy=0.80, likes_acoustic=False

#1  Sunrise City by Neon Echo
    Score: 5.37 / 5.50
    Because:
      - genre match: pop (+2.0)
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.80 (+1.96)
      - non-acoustic sound: acousticness 0.18 (+0.41)

#2  Gym Hero by Max Pulse
    Score: 4.21 / 5.50
    Because:
      - genre match: pop (+2.0)
      - energy 0.93 vs target 0.80 (+1.74)
      - non-acoustic sound: acousticness 0.05 (+0.47)

#3  Rooftop Lights by Indigo Parade
    Score: 3.25 / 5.50
    Because:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.80 (+1.92)
      - non-acoustic sound: acousticness 0.35 (+0.33)

#4  Concrete Verses by Blockline
    Score: 2.40 / 5.50
    Because:
      - energy 0.78 vs target 0.80 (+1.96)
      - non-acoustic sound: acousticness 0.12 (+0.44)

#5  Night Drive Loop by Neon Echo
    Score: 2.29 / 5.50
    Because:
      - energy 0.75 vs target 0.80 (+1.90)
      - non-acoustic sound: acousticness 0.22 (+0.39)
```

**Chill lofi**

```
Profile: Chill lofi
  genre=lofi, mood=chill, energy=0.40, likes_acoustic=True

#1  Library Rain by Paper Lanterns
    Score: 5.33 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.35 vs target 0.40 (+1.90)
      - acoustic sound: acousticness 0.86 (+0.43)

#2  Midnight Coding by LoRoom
    Score: 5.31 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.42 vs target 0.40 (+1.96)
      - acoustic sound: acousticness 0.71 (+0.35)

#3  Focus Flow by LoRoom
    Score: 4.39 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - energy 0.40 vs target 0.40 (+2.00)
      - acoustic sound: acousticness 0.78 (+0.39)

#4  Spacewalk Thoughts by Orbit Bloom
    Score: 3.22 / 5.50
    Because:
      - mood match: chill (+1.0)
      - energy 0.28 vs target 0.40 (+1.76)
      - acoustic sound: acousticness 0.92 (+0.46)

#5  Coffee Shop Stories by Slow Stereo
    Score: 2.38 / 5.50
    Because:
      - energy 0.37 vs target 0.40 (+1.94)
      - acoustic sound: acousticness 0.89 (+0.45)
```

**Deep intense rock**

```
Profile: Deep intense rock
  genre=rock, mood=intense, energy=0.92, likes_acoustic=False

#1  Storm Runner by Voltline
    Score: 5.43 / 5.50
    Because:
      - genre match: rock (+2.0)
      - mood match: intense (+1.0)
      - energy 0.91 vs target 0.92 (+1.98)
      - non-acoustic sound: acousticness 0.10 (+0.45)

#2  Gym Hero by Max Pulse
    Score: 3.46 / 5.50
    Because:
      - mood match: intense (+1.0)
      - energy 0.93 vs target 0.92 (+1.98)
      - non-acoustic sound: acousticness 0.05 (+0.47)

#3  Pulse Reactor by Kilowatt
    Score: 2.43 / 5.50
    Because:
      - energy 0.95 vs target 0.92 (+1.94)
      - non-acoustic sound: acousticness 0.02 (+0.49)

#4  Iron Tide by Ashen Crown
    Score: 2.39 / 5.50
    Because:
      - energy 0.97 vs target 0.92 (+1.90)
      - non-acoustic sound: acousticness 0.03 (+0.48)

#5  Sunrise City by Neon Echo
    Score: 2.21 / 5.50
    Because:
      - energy 0.82 vs target 0.92 (+1.80)
      - non-acoustic sound: acousticness 0.18 (+0.41)
```

**Edge: hyped but sad**

```
Profile: Edge: hyped but sad
  genre=folk, mood=sad, energy=0.90, likes_acoustic=True

#1  Empty Train Station by Willow Gray
    Score: 4.12 / 5.50
    Because:
      - genre match: folk (+2.0)
      - mood match: sad (+1.0)
      - energy 0.24 vs target 0.90 (+0.68)
      - acoustic sound: acousticness 0.88 (+0.44)

#2  Storm Runner by Voltline
    Score: 2.03 / 5.50
    Because:
      - energy 0.91 vs target 0.90 (+1.98)
      - acoustic sound: acousticness 0.10 (+0.05)

#3  Gym Hero by Max Pulse
    Score: 1.96 / 5.50
    Because:
      - energy 0.93 vs target 0.90 (+1.94)
      - acoustic sound: acousticness 0.05 (+0.03)

#4  Sunrise City by Neon Echo
    Score: 1.93 / 5.50
    Because:
      - energy 0.82 vs target 0.90 (+1.84)
      - acoustic sound: acousticness 0.18 (+0.09)

#5  Pulse Reactor by Kilowatt
    Score: 1.91 / 5.50
    Because:
      - energy 0.95 vs target 0.90 (+1.90)
      - acoustic sound: acousticness 0.02 (+0.01)
```

**Edge: genre not in catalog**

```
Profile: Edge: genre not in catalog
  genre=k-pop, mood=happy, energy=0.75, likes_acoustic=False

#1  Rooftop Lights by Indigo Parade
    Score: 3.31 / 5.50
    Because:
      - mood match: happy (+1.0)
      - energy 0.76 vs target 0.75 (+1.98)
      - non-acoustic sound: acousticness 0.35 (+0.33)

#2  Sunrise City by Neon Echo
    Score: 3.27 / 5.50
    Because:
      - mood match: happy (+1.0)
      - energy 0.82 vs target 0.75 (+1.86)
      - non-acoustic sound: acousticness 0.18 (+0.41)

#3  Night Drive Loop by Neon Echo
    Score: 2.39 / 5.50
    Because:
      - energy 0.75 vs target 0.75 (+2.00)
      - non-acoustic sound: acousticness 0.22 (+0.39)

#4  Concrete Verses by Blockline
    Score: 2.38 / 5.50
    Because:
      - energy 0.78 vs target 0.75 (+1.94)
      - non-acoustic sound: acousticness 0.12 (+0.44)

#5  Storm Runner by Voltline
    Score: 2.13 / 5.50
    Because:
      - energy 0.91 vs target 0.75 (+1.68)
      - non-acoustic sound: acousticness 0.10 (+0.45)
```

**Edge: acoustic metalhead**

```
Profile: Edge: acoustic metalhead
  genre=metal, mood=angry, energy=0.95, likes_acoustic=True

#1  Iron Tide by Ashen Crown
    Score: 4.97 / 5.50
    Because:
      - genre match: metal (+2.0)
      - mood match: angry (+1.0)
      - energy 0.97 vs target 0.95 (+1.96)
      - acoustic sound: acousticness 0.03 (+0.01)

#2  Pulse Reactor by Kilowatt
    Score: 2.01 / 5.50
    Because:
      - energy 0.95 vs target 0.95 (+2.00)
      - acoustic sound: acousticness 0.02 (+0.01)

#3  Gym Hero by Max Pulse
    Score: 1.99 / 5.50
    Because:
      - energy 0.93 vs target 0.95 (+1.96)
      - acoustic sound: acousticness 0.05 (+0.03)

#4  Storm Runner by Voltline
    Score: 1.97 / 5.50
    Because:
      - energy 0.91 vs target 0.95 (+1.92)
      - acoustic sound: acousticness 0.10 (+0.05)

#5  Sunrise City by Neon Echo
    Score: 1.83 / 5.50
    Because:
      - energy 0.82 vs target 0.95 (+1.74)
      - acoustic sound: acousticness 0.18 (+0.09)
```

**Edge: capitalized labels**

```
Profile: Edge: capitalized labels
  genre=Pop, mood=Happy, energy=0.80, likes_acoustic=False

#1  Concrete Verses by Blockline
    Score: 2.40 / 5.50
    Because:
      - energy 0.78 vs target 0.80 (+1.96)
      - non-acoustic sound: acousticness 0.12 (+0.44)

#2  Sunrise City by Neon Echo
    Score: 2.37 / 5.50
    Because:
      - energy 0.82 vs target 0.80 (+1.96)
      - non-acoustic sound: acousticness 0.18 (+0.41)

#3  Night Drive Loop by Neon Echo
    Score: 2.29 / 5.50
    Because:
      - energy 0.75 vs target 0.80 (+1.90)
      - non-acoustic sound: acousticness 0.22 (+0.39)

#4  Rooftop Lights by Indigo Parade
    Score: 2.25 / 5.50
    Because:
      - energy 0.76 vs target 0.80 (+1.92)
      - non-acoustic sound: acousticness 0.35 (+0.33)

#5  Storm Runner by Voltline
    Score: 2.23 / 5.50
    Because:
      - energy 0.91 vs target 0.80 (+1.78)
      - non-acoustic sound: acousticness 0.10 (+0.45)
```

**Edge: energy out of range**

```
Profile: Edge: energy out of range
  genre=lofi, mood=chill, energy=1.50, likes_acoustic=True

#1  Midnight Coding by LoRoom
    Score: 3.19 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.42 vs target 1.50 (+-0.16)
      - acoustic sound: acousticness 0.71 (+0.35)

#2  Library Rain by Paper Lanterns
    Score: 3.13 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - mood match: chill (+1.0)
      - energy 0.35 vs target 1.50 (+-0.30)
      - acoustic sound: acousticness 0.86 (+0.43)

#3  Focus Flow by LoRoom
    Score: 2.19 / 5.50
    Because:
      - genre match: lofi (+2.0)
      - energy 0.40 vs target 1.50 (+-0.20)
      - acoustic sound: acousticness 0.78 (+0.39)

#4  Spacewalk Thoughts by Orbit Bloom
    Score: 1.02 / 5.50
    Because:
      - mood match: chill (+1.0)
      - energy 0.28 vs target 1.50 (+-0.44)
      - acoustic sound: acousticness 0.92 (+0.46)

#5  Iron Tide by Ashen Crown
    Score: 0.95 / 5.50
    Because:
      - energy 0.97 vs target 1.50 (+0.94)
      - acoustic sound: acousticness 0.03 (+0.01)
```

### What I noticed

- **The #1 picks for normal profiles feel right.** Sunrise City for happy pop, Library Rain for chill lofi, and Storm Runner for intense rock are the songs I would pick myself.
- **Spots #3 to #5 are mostly decided by energy alone.** Each genre only has 1 to 3 songs, so after those run out, any song with a close energy level gets almost 2 points. That is why Sunrise City (a happy pop song) shows up at #5 for the rock fan, and why it appears in 6 of the 8 lists.
- **Metal ranks below EDM for the rock fan.** Iron Tide is #4, behind Pulse Reactor. The system does not know that metal is close to rock.
- **Hyped but sad:** a sad folk song with energy 0.24 still wins, because genre and mood together (3 points) beat the energy gap. Every song after it is a loud, non-acoustic song, so the user never gets anything that is both sad and energetic.
- **Acoustic metalhead:** the acoustic preference barely matters. It is worth at most 0.5 points, so the list looks almost the same as a normal metal fan's list.
- **Genre not in catalog:** this works fine. With no genre match, mood and energy take over and the results still make sense.
- **Capitalized labels:** "Pop" does not match "pop", so genre and mood give 0 points. Sunrise City drops from #1 to #2 behind a hip hop song. The system fails without any warning.
- **Energy out of range:** a target of 1.50 makes the energy points negative (shown as "+-0.16"). The system does not check that the target is between 0 and 1.

### Comparing profiles

- **Happy pop vs Chill lofi:** these two lists share no songs at all. The pop list is all loud, electronic songs (energy 0.75 to 0.93), and the lofi list is all quiet, acoustic songs (energy 0.28 to 0.42). This makes sense because the two users want opposite energy levels and opposite sounds.
- **Chill lofi vs Deep intense rock:** again no shared songs. The rock fan gets the loudest songs in the catalog and the lofi fan gets the softest. The system clearly tells "intense rock" and "chill lofi" apart.
- **Happy pop vs Deep intense rock:** both lists have Gym Hero at #2, and both include Sunrise City. Gym Hero gets there for different reasons: for the pop fan it is the genre (pop), and for the rock fan it is the mood (intense). Both users want loud music, so some overlap makes sense.
- **Happy pop vs Genre not in catalog (k-pop):** the k-pop list looks like the pop list without the genre bonus. Rooftop Lights moves up to #1 because it is happy, and Gym Hero drops out because it is not happy. This shows that the genre label is the only thing keeping Gym Hero high for the pop fan.
- **Happy pop vs Capitalized labels:** this is really the same user, but typing "Pop" instead of "pop" changes the list. A hip hop song takes #1 and Gym Hero disappears. This output is not valid, it is a bug.
- **Deep intense rock vs Acoustic metalhead:** the lists are almost the same. Both have Pulse Reactor, Gym Hero, and Sunrise City, and the rock song and the metal song just swap places (each one is #1 for its own fan and lower for the other). Liking acoustic sound did almost nothing, because it is only worth half a point.
- **Deep intense rock vs Hyped but sad:** a sad folk fan and an intense rock fan share 4 of their 5 songs. After the one sad folk song, the system only looks at energy, so the sad fan gets the rock fan's list. This is the clearest example of the loud song bubble.
- **Chill lofi vs Energy out of range:** the same three lofi songs stay on top, but every score drops, and a metal song (Iron Tide) sneaks in at #5 for a lofi fan. The bad energy number is what caused this.

**Why does Gym Hero keep showing up for people who just want Happy Pop?** Think of the system as a judge handing out points. Gym Hero is labeled "pop", and a matching genre is the biggest prize (2 points). It is also loud, and the happy pop fan asked for loud music, so it earns almost all of the energy points too. The only thing it gets wrong is the mood ("intense" instead of "happy"), and a wrong mood only costs 1 point. So Gym Hero beats Rooftop Lights, a happy song that sounds like what the user wants, just because Rooftop Lights is labeled "indie pop" instead of "pop."

### Experiment: weight shift

I doubled the energy weight (2.0 to 4.0) and cut the genre weight in half (2.0 to 1.0). The highest possible score went from 5.5 to 6.5, and the top score in any list was 6.41, so the math still stays inside the limit.

| Profile | Before (top 3) | After (top 3) | Better or just different? |
|---|---|---|---|
| Happy pop | Sunrise City, Gym Hero, Rooftop Lights | Sunrise City, Rooftop Lights, Gym Hero | Better. The happy song now beats the intense one. |
| Chill lofi | Library Rain, Midnight Coding, Focus Flow | Midnight Coding, Library Rain, Focus Flow | Just different. The top two swapped. |
| Deep intense rock | Storm Runner, Gym Hero, Pulse Reactor | Same order | No change. |
| Hyped but sad | Empty Train Station, Storm Runner, Gym Hero | Storm Runner, Gym Hero, Pulse Reactor | Worse. The only sad folk song fell to #4. |
| Energy out of range | Midnight Coding, Library Rain, Focus Flow | Midnight Coding, Iron Tide, Library Rain | Worse. A metal song jumped to #2 for a lofi fan. |

Overall the change made results mostly different, not more accurate. It fixed the Gym Hero problem, but it made the loud song bubble stronger, because energy now matters more than who the user is. The scores also got bunched together (spots #2 to #5 were often within 1 point), so the lists felt less personal. I went back to the original weights.

---

## 8. Future Work  

- **Fix the two bugs I found.** Make genre and mood matching ignore capital letters, and keep energy points from ever going below zero.
- **Give partial credit for similar genres.** "indie pop" should count a little for a pop fan, and metal should count a little for a rock fan.
- **Add variety to the top 5.** For example, do not show the same artist twice, and use valence so a sad song and a happy song with the same energy are not treated the same.

---

## 9. Personal Reflection  

My biggest learning moment was seeing that the hard part is not the code. The scoring function is only about 30 lines. The hard part was picking the weights, because every choice helps one user and hurts another. When I doubled the energy weight, Gym Hero stopped beating Rooftop Lights for the pop fan, but the sad folk fan lost the only sad folk song. There was no setting that made everyone happy.

AI tools helped me a lot with planning, writing the first version of the code, and coming up with tricky test profiles I would not have thought of, like the capital letters one. But I still had to double check things. The tests passed even before the ranking worked, because the starter test happened to put the right song first, so passing tests did not prove my code was right. During my experiment, the first run gave the exact same output as before, because Python was using an old saved copy of the code. If I had trusted that, I would have written that changing the weights did nothing. I also had to check that the AI's wording matched what really happened in the output.

I was surprised how much a few simple rules can feel like a real recommendation. Seeing "Because: genre match, mood match, energy close to target" makes the pick feel smart, even though it is just adding up points. It made me think that apps like Spotify feel personal partly because they show you a reason, not only because their math is fancy.

If I kept going, I would add more songs so each genre has more than one or two, and then try using other users' likes, so the system could find songs I would never find by genre alone.
