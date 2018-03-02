## Applying Statistical Inference
The statistical inference tools are applied toward the audio features in the feature distribution notebook. [feature_distribution.ipynb] (https://github.com/victoreram/Springboard-Data-Science/blob/master/Subgenre_Classification/feature_distribution.ipynb)

### About the audio features
Taken from Spotify's site: https://developer.spotify.com/web-api/get-audio-features/
- **acousticness:** A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
- **danceability:** Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- **Energy** is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- **instrumentalness:** Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- **liveness:** Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
- **speechiness:** Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- **tempo:** The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. The value here is normalized so the max value = 1
- **valence:** A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

### Hypothesis
Assume that we have a null-hypothesis that states that each audio feature is independent. The alternative hypothesis is that for each audio feature, another audio feature is correlated in some way. The statistical analysis in this project is focused on the relationships between each audio feature. 

### P-Values
From the p-value matrix above, most of the audio features are related to one another. Out of 28 relationships ((8 features $\times$ 7 other features)/2), the null-hypothesis can be accepted in 4 relationships if we set our p-value threshold > 0.05. These relationships are:

    -danceability & energy
    -energy & instrumentalness
    -liveness & tempo
    -liveness & valence
    
### Correlations
There's plenty of intuitive observations based on the correlations. 
- Acousticness and energy share the largest negative correlation (-0.48).
- Instrumentalness and acousticness share the largest positive correlation (0.12)
- Energy and danceability are relatively neutral to each other (0.022)

#### By Genre
Audio features were averaged by genre and some of these relationships were plotted. Here is an example from acousticness and energy:
- Hip-hop is the among the most energetic and also the least acoustic
- Spoken word is generelly not energetic but scores high on acousticness
- Most genres are clustered between energy levels 0.5-0.57 and acousticness levels 0.45-0.6

More plots and relationships can be found in the notebook.
