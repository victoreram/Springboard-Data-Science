# Music Genre Clustering Project Report
By Victor Ramirez

## Problem
### Introduction

Music recommendation engines drive the services offered by music streaming companies such as Spotify, Last.fm, and Pandora. A core component of these engines are the genre labels for each track which people apply to tracks or artists. These genre labels offer a rough measure that gauges similarities and differences between tracks. However, how these labels are applied are subjective. One person might label a track 'pop' but be labelled as 'folk' by someone else.

### Music Discovery
Suppose a user wanted to expand their music tastes by listening to similar music in other genres. How would a music recommendation engine go about recommending to this user, if it was bounded by the genre classification imposed by other listeners?  If we recommend music based on subjective genres; that is giving more of genre X to someone because they have listened to genre X in the past, this might not actually give them what they want. This analysis compares genre labels to the actual audio characteristics of the music, to see if we could provide better recommendations this way. One solution is to take the user's listening history and compare it to other users with similar listening histories to recommend new music. But, using this solution alone has some flaws:

1. Listening history data may not be available, especially for smaller companies or for tracks from newer, relatively unknown artists.
2. Other users may subject themselves to a music "bubble", only listening to music that is familiar and limiting the opportunity for discovery.

This project aims to cross the boundaries imposed by genre classification and instead find similarities among music instead of relying on human-assigned labels. By applying clustering techniques on audio features, specific "genres" can be inferred that can describe music differently than conventional music genres. Descriptive subgenres can strengthen a music recommendation engine and give users more options for discovering otherwise unknown music. 

### Potential Clients
Clients with music data are the main target for this projects. These clients would fall under 2 types:
1. A company who already has a robust music recommendation engine and would like to bolster it. E.g. Spotify, Pandora, Last.fm, Youtube
2. A smaller, competing company that has access to music, but doesn't have much user data to base recommendations off of.

Companies under the 1st group likely have something similar in place already. For example, the audio features used for music genre clustering come from Spotify's features. But, there are countless ways to extract audio features from audio files. Data from fma has raw features extracted from audio files, but in-depth analysis of what insights to derive from them require advanced signal-processing knowledge that are beyond the scope of this project. This project is tailored for clients that already have descriptive features in place that can be clustered to describe genres.

## Data Collection
The data is originally sourced from the Free Music Archive. Repo [here](https://github.com/mdeff/fma/). The data files used to create the spreadsheets for this repo come from:
- `tracks.csv`: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks. 
- `genres.csv`: all 163 genre IDs with their name and parent (used to infer the genre hierarchy and top-level genres).
- `echonest.csv`: audio features provided by Echonest (now Spotify) for a subset of 13,129 tracks.

## [Initial Exploration: Genres and Year Released](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/Tracks_by_genre_year.ipynb)
### Tracks by Genre
The first aspect of this project explored was the amount of tracks that were categorized by genre. Note that this was initially done using `tracks.csv` from FMA. The `tracks_cleaned.csv` has a similar structure and was cleaned after knowing some features outlined by this step.

#### All Genres

![Histogram of all genres](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/hist_genres.png)

The histogram above shows that that the music sampled by this dataset has an imbalanced proportion of tracks by genre. The sample is mostly composed of 3 genres: Experimental, Electronic, and Rock, which more than make up the remaining 14 genres. Samples of top genres were taken later on to give an estimated "fair" distribution of features later on. It is worth noting that this is not necessarily a fault of the dataset. Some genres are more popular than others, so it's natural to assume that some genres will have more songs than others.

#### Subgenre: Rock
![Histogram of Rock](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/hist_rock.png)

When examining the subgenres that compose Rock, genres that are direct "children" of rock (see description of `genres.csv` above) were used. Rock has many other subgenres outlined in this dataset, but those are absorbed by the hierarchy level right below Rock. 

The histogram above shows roughly the same Pareto distribution for subgenres as the genres. Punk has the most instances near 10,000 which is roughly 30% of the total instances of Rock. The 2nd most (Lo-Fi) has 2/3 of that amount. There's a healthy enough sample size for the 10 subgenres that it's still possible to see some meaningful disparities between subgenres. 

### Tracks by Year
![Tracks by Year Released Histogram](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/Report/hist_times.png?raw=true)
![Tracks by Year Released Chronologically](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/tracks_release_years.png)

One of the original considerations when separating genres by audio features is to look at when a song is released. After all, some songs and genres are characterized heavily by the times they were released; Rock from the 70's is notably distinct from Rock from the 80's, which are both much different than Indie Rock released in the 2010's. The factors that cause these disparities, whether they be cultural or technology, could in theory be captured by the audio features. In order to prove this hypothesis, one would need a healthy amount of data released over time. 

Unfortunately as we see above, most of the tracks in this dataset are released within the last 2 decades with a lot of them unknown. Thus, any insights from differentiating by decade released may not be all that meaningful. 

## [Data Wrangling](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/DataCleaning.ipynb)
### tracks
`tracks.csv` is the 'meat' of this dataset and contains most of the information needed. This file is multi-indexed into 3 parent indexes: album, artist, track. There are a total of 52 columns initially and not all are relevant for the purpose of this project. The relevant child columns for each parent index are the following:
- track: genres_top, genres, genres_all, id
- artist: name
- album: date_released, title

The multiindex can be sliced as follows: tracks[('parent_index','child_index')]. So, to access track's bit_rate column, you would access it by: tracks[('track', 'bit_rate')]. In DataCleaning.ipynb, Removing unnecessary columns led to the removal the multiindex without loss of important data.

### genres
This spreadsheet is mainly used to translate genre ID's to the name of the genres.

### echonest
This file contains a subset of audio features for each track. Tracks which have the audio features are merged with tracks.

### Merging into a Unified DataFrame
The code is written in the notebook above. Here is a short summary of some of the steps:
- Any track with "genres_all" as null is removed. Since this contains the closest estimation to a target variable, it's best to keep this relatively pure. 
- Convert tracks.csv columns into appropriate types (year to ints, genres_top to lists, etc.)
- Remove data with corrupt metadata, such tracks with genres_all that don't resemble what typical column values should be, which are a list of column ID's. Some of these contain descriptions of the artist for some reason.
- Extract only the tracks with the basic "Spotify" audio features from echonest.
- Merge tracks and echonest audio features together into one cohesive .csv, `tracks_cleaned.csv`. This new .csv file contains 13129 rows and 18 columns. 8 of these columns are audio files, while the rest are metadata (track, artist, album, genre, year released).

## Further Data Analysis: [Feature Distribution](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/FeatureDistribution.ipynb)
### Definition of Audio Features
To better understand what the genres are clustered by, audio features must first be defined. These are taken from Spotify's site: https://developer.spotify.com/web-api/get-audio-features/

- **acousticness:** A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
- **danceability:** Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
- **Energy** is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
- **instrumentalness:** Predicts whether a track contains no vocals. "Ooh" and "aah" sounds are treated as instrumental in this context. Rap or spoken word tracks are clearly "vocal". The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
- **liveness:** Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live. A value above 0.8 provides strong likelihood that the track is live.
- **speechiness:** Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap music. Values below 0.33 most likely represent music and other non-speech-like tracks.
- **tempo:** The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece and derives directly from the average beat duration. The value here is normalized so the max value = 1
- **valence:** A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).

### Relationships Between Audio Features
![Heatmap of Audio Features](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/audio_heatmap.png)

Given the definitions of these features, it's worthwhile to examine how each of them relate to one another. The heatmap indicates indicates 2 significant cross-correlations:
- Acousticness vs. Energy (-0.48). The higher the acousticness, the lower the energy.
- Danceability vs. Valence (0.43). The more danceable a track is, the higher valence/happier it tends to be.

Another reasonable interpretation is that songs that happen to fall under a certain value of a feature, say acousticness, just happens to have low measured energies. This is the null hypothesis. The alternative hypothesis is that the correlation observed does not arise at random. Given these two hypotheses, it was found that the p-values for these two relationships were < 0.001, thus we can accept the alternative hypothesis. 

### Boxplots of Audio Features
One way to neatly see the distribution of audio features is through boxplots. Plotted below are the 6 most prevalent genres: Electronic, Folk, Hip-Hop, Metal, Pop, and Rock and how each genre's distribution differs. 

![Boxplots of Feature Distribution By Genre](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/genre_feature_boxplots.png)
#### Remarks
- **Acousticness**:
    - Metal typically scores low even though the music is heavily reliant on stringed instruments (guitars and bass). This outlines another possible feature that could be useful if extracted: distortion.
    - Folk's distribution is centered towards high acousticness scores (not surprising) but has plenty of outliers that score low.
    - Rock's distribution spans through a large chunk of the available range.
- **Danceability**:
    - For the most part, each genre centers around medium values for danceability.
- **Energy**:
    - Folk's distribution contrasts how it score in acousticness, visibly clustering at lower values than other genres. This is partly
- **Instrumentalness**:
    - The distribution for Metal and Electronic are eerily similar, scoring high in instrumentalness with plenty of outliers at low values. 
    - Metal, Folk, Electronic, and Rock all have lower quartiles that extend far past the mean relative to the upper quartile. One way to interpret this is that songs in these genres typically have strong instrumental sounds, but there's a significant minority of songs within these genres where instrumentals are much less prominent. 
- **Liveness**:
    - Plenty of outliers all around. This is a weird audio feature that is track-specific, signifying if the track sounds like it's live or not. There isn't much insight on a per-genre basis because this is dependent on the sample of tracks that happen to be live given a genre.
- **Speechiness**:
    - To nobody's surprise, A genre that is mostly centered around vocals (Hip-Hop) vastly outscore all genres in speechiness.
    - Other genres typically score low but have plenty of outliers outside of its upper quartiles.
- **Tempo**:
    - Each genre seems to share roughly the same distribution here, with some outliers with high tempos. Those Rock outliers may represent Punk songs.
- **Valence**:
    - Hip-Hop takes the honor for happiest genre of this sample. 
    - Metal on the other hand is the saddest / angriest genre of the sample, though there are some outliers that score extremely high. 

### Scatter Plots Between Audio Features
Many scatter plots with selected audio feature comparisons by genre can be found in the FeatureDistributions notebook linked above. Below is just one of those plots, Tempo vs. Energy.
![Tempo vs. Energy](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/tempo_v_energy.png)

There are some distinguishable borders between genres in this plot. The left region (low energy, low-mid tempo) consists mostly of Folk and Old-time Historic. As energy increases to the right, more Rock and Electronic songs show up. Fans familiar with these genres of music can verify that estimation to be roughly accurate. There's also a subtle trend that energy increases with tempo.

## [Clustering](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/GenreClustering.ipynb)
The last step in this project is the application of clustering algorithms on the dataset. The normalized values of the audio columns are the features X. The outputs are newly generated clusters that represent new, descriptive genres based on the audio features. These generated genres are then interpreted and compared to the human-labeled music genres. The generated genres can be augmented to a music recommendation engine so that users can discover music in different human-labeled genres that's similar to the music they already like.

The primary algorithm shown in this report is K-Means, but other algorithms (MeanShift, SpectralClustering) are also tested.  K-Means displayed generated clusters with reasonable boundaries and returns centroids which can be compared to actual subgenres.

### Choosing K
It's desireable to set K >= the number of genres because the goal is to break down the genres into more descriptive pieces. Consolidating genres into larger chunks doesn't give much meaningful insight. 

One method for finding K is the "Elbow Method", a visual comparison of the explained variance with K-Means models of different K values. The optimal K is the value of K where the explained variance plateaus. When plotted, the optimal K value suggested by the Elbow Method was a value < the number of genres. Thus this method was inconclusive.

Another method is comparing Silhouette Scores, which evaluate how close each point within a cluster is compared to other points in other clusters. Silhouette Scores range from 0.0 to 1.0, where 0.0 indicates a lack of structure and 1.0 a strong structure. A Silhouette Score Analysis showed that all K values tested yielded scores close (<0.25) to zero. This again doesn't suggest a conclusive K value. 

As a compromise, K is set to the number of genres. The rationale is that choosing K = to the "expected" number of genres allows for at least a 1 to 1 comparison between actual genres and the generated genres. The disadvantage with using K-Means here is that the cluster sizes are roughly the same size, but the data is imbalanced. For the results from the other algorithms, see the link to the notebook. 
### All tracks
Applying this model yielded the following centroid features:

![K-Means heatmap](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/heatmap_all.png)

#### Genre Cluster Meanings
One of the main purposes of this project is to see if clustering provides any sort of meaning behind any existing structure within the data. Given the cluster centroids from K-Means, we can see the values which characterize each K-Means Label. From eyeballing the values and heatmap, clusters are described based on the meaning behind each feature. In quotes are best-guess interpretations for these genres, meant to resemble Netflix's disturbingly specific genres. 

- **KM0**: Highly acoustic and instrumental. Low danceability, energy tempo, valence. "Slow & Somber Acoustics"
- **KM1**: Highly instrumental and valent. Mid-tempo, mid-energy. Low acousticness and speechiness. "Happy & Danceable Instrumentals"
- **KM2**: Highly instrumental. Mid acousticness. Low valence, speechiness. "Sad Instrumentals"
- **KM3**: Highly valent. Speechy. Mid-instrumental, mid-energy. Low instrumentalness. "Upbeat Songs With Cheerful Vocals"
- **KM4**: Highly instrumental, danceable, fast. Mid-energy. Low acousticness. "Fast & Danceable Instrumentals". 
- **KM5**: High energy, valent, and fast. Relatively high liveness. Low acousticness and instrumentalness. 'Fast, Upbeat & Cheerful"
- **KM6**: Highly acoustic. Mid-high danceable. Speechy. Low energy. "Slow Dance".
- **KM7**: Highly valent and instrumental. Low tempo and speechiness. "Happy & Slow"
- **KM8**: High energy, tempo and instrumentalness. Low acousticness and speechiness. "Happy & Upbeat Instrumentals"
Moreover, we can see how these clusters relate to each genre from the following cell:
```python 
descriptive_labels = ["Slow & Somber Acoustics", "Happy & Danceable Instrumentals", "Sad Instrumentals", 
                     "Upbeat Songs With Cheerful Vocals", "Fast & Danceable Instrumentals", "Fast, Upbeat & Cheerful Songs",
                     "Slow Dance", "Happy & Slow", "Happy & Upbeat Instrumentals"]
unique_labels = np.unique(labels)
translated_labels = dict(zip(unique_labels, descriptive_labels))
tracks['KMeansLabel'] = list(map(lambda x:translated_labels[x], labels))

genre_count = tracks.groupby('genres_top').agg({'genres_top':'count'})['genres_top']

# How many instances of each k-means cluster are there?
print("### Instances of KMeans Cluster ###")
print(tracks[['genres_top', 'KMeansLabel']].groupby('KMeansLabel').agg('count'))

# Which cluster corresponds to the most instances per genre?
print("### Which cluster corresponds to the most instances per genre? ###")
print(tracks[['genres_top', 'KMeansLabel']].groupby('genres_top').agg(lambda x:x.value_counts().index[0]))

# Which genre corresponds to the most instances per cluster?
print("### Which genre corresponds to the most instances per cluster? ###")
print(tracks[['genres_top', 'KMeansLabel']].groupby('KMeansLabel').agg(lambda x:x.value_counts().index[0]))
```
```
### Instances of KMeans Cluster ###
                                   genres_top
KMeansLabel                                  
Fast & Danceable Instrumentals           1071
Fast, Upbeat & Cheerful Songs            1382
Happy & Danceable Instrumentals          1733
Happy & Slow                             1930
Happy & Upbeat Instrumentals             1435
Sad Instrumentals                        1557
Slow & Somber Acoustics                  1983
Slow Dance                                893
Upbeat Songs With Cheerful Vocals        1145
### Which cluster corresponds to the most instances per genre? ###
                                                       KMeansLabel
genres_top                                                        
Classical                                  Slow & Somber Acoustics
Electronic                         Happy & Danceable Instrumentals
Folk/Blues                                 Slow & Somber Acoustics
Hip-Hop/Easy Listening           Upbeat Songs With Cheerful Vocals
Jazz/Experimental/International            Slow & Somber Acoustics
Metal                                 Happy & Upbeat Instrumentals
Old-Time / Historic/Spoken                 Slow & Somber Acoustics
Pop/Country                      Upbeat Songs With Cheerful Vocals
Rock/Instrumental/Soul-RnB                       Sad Instrumentals
### Which genre corresponds to the most instances per cluster? ###
                                                   genres_top
KMeansLabel                                                  
Fast & Danceable Instrumentals                     Electronic
Fast, Upbeat & Cheerful Songs      Rock/Instrumental/Soul-RnB
Happy & Danceable Instrumentals                    Electronic
Happy & Slow                       Rock/Instrumental/Soul-RnB
Happy & Upbeat Instrumentals       Rock/Instrumental/Soul-RnB
Sad Instrumentals                  Rock/Instrumental/Soul-RnB
Slow & Somber Acoustics                            Folk/Blues
Slow Dance                                         Folk/Blues
Upbeat Songs With Cheerful Vocals  Rock/Instrumental/Soul-RnB
```
There are some interesting conclusions that match up with everyday musical intuition.

- In cell 2, The most predominant KMeans Label for Classical, Folk/Blues, and Jazz are Slow & Somber Acoustics. In contrast, the most predominant KMeans Label for Electronic, Pop, and Country are Upbeat Songs With Cheerful Vocals, which make sense. Metal's most predominant KMeans Label is Happy & Upbeat Instrumentals, which may indicate an unfortunately high amount of power metal in our sample.

- In cell 3, we see Rock/Instrumental/Soul-RnB dominate 4 out of 5 "Happy/Cheerful" KMeans Labels. Folk/Blues, which tends to be slower, does end up categorized as typically slow.

Applying PCA to reduce the data to 2-D allows the data to be visualized. The "x" and "y" axis in these plots represent the newly reduced audio features generated by PCA. First, here is the 2-D space containing just the genres. 

![PCA Scatter Plot](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/pca_scatter_genres.png)

*A scatter plot of the distribution of tracks based on audio features, with x and y being the new features constructed by PCA. Each track is colored by their actual genre.*

The reduced dimensional space showed some well-defined clusters from genres. Folk/Blues, Classical and Old-Time clustered together towards strong acoustic values and weak energy values. Metal seemed to straddle along the instrumentalness axis but skewed towards higher energy values. Compare this to the plot where points are instead colored by their KMeans label:

![PCA K-Means All Genres Plot](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/pca_scatter_km.png)

*A scatter plot of the distribution of tracks based on audio features, with x and y being the new features constructed by PCA. Each track is colored by the assigned K-Means label.*

K-Means labels crossed genre boundaries with few exceptions. Perhaps the most striking compatibility between labels is Metal - "Happy & Upbeat Instrumentals" straddling along the top left edge. Another one is Classical with "Slow & Somber Acoustics". 

### Rock
The same process is repeated, this time only examining the top 5 most prevalent Rock subgenres as our genres. 

#### Rock Subgenre Cluster Meanings
![K-Means heatmap for rock](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/KM5_heatmap.png)

The best guess interpretations are:
- **KM0**: High Energy, Valence, Tempo, Danceablity. Low acousticness, instrumentalness. Probably just described Pop. "Upbeat Rock with Synths to Dance to"
- **KM1**: High Acousticness and Instrumentalness. Not Danceable. Low Speechiness, Tempo, and Valence. "Slow & Depressing Rock"
- **KM2**: High Acousticness, Instrumentalness and Valence. Lowest Speechiness and Tempo. "Slow & Cheerful Rock"
- **KM3**: High Acousticness and Danceability. Low Energy. "Slow Dance Rock"
- **KM4**: High Instrumentalness, Tempo and Energy. Low Acousticness, Danceability. "Fast & Energetic Rock"

Again, tallying up the instances from both subgenres and K-Means clusters yields the following pairings:
```python
### Assign K-Means Label to Descriptive Labels
descriptive_labels = ["Upbeat Rock with Synths to Dance to", "Slow & Depressing Rock", "Slow & Cheerful Rock",
                     "Slow Dance Rock", "Fast & Energetic Rock"]
unique_labels = np.unique(rock_tracks["KMeansLabel"].values)
translated_labels = dict(zip(unique_labels, descriptive_labels))
rock_tracks['KMeansLabel'] = list(map(lambda x:translated_labels[x], (rock_tracks["KMeansLabel"].values)))

genre_count = rock_tracks.groupby('subgenre').agg({'subgenre':'count'})['subgenre']

# How many instances of each subgenre of rock are there?
print("### Instances of subgenre ###")
print(rock_tracks[['subgenre', 'KMeansLabel']].groupby('subgenre').agg('count'))

# How many instances of each k-means cluster are there?
print("### Instances of KMeans Cluster ###")
print(rock_tracks[['subgenre', 'KMeansLabel']].groupby('KMeansLabel').agg('count'))

# Which cluster corresponds to the most instances per genre?
print("### Which cluster corresponds to the most instances per genre? ###")
print(rock_tracks[['subgenre', 'KMeansLabel']].groupby('subgenre').agg(lambda x:x.value_counts().index[0]))

# Which genre corresponds to the most instances per cluster?
print("### Which genre corresponds to the most instances per cluster? ###")
print(rock_tracks[['subgenre', 'KMeansLabel']].groupby('KMeansLabel').agg(lambda x:x.value_counts().index[0]))
```
```
### Instances of subgenre ###
            KMeansLabel
subgenre               
Indie-Rock          730
Pop                 400
Psych-Rock          447
Punk               1474
Rock               1790
### Instances of KMeans Cluster ###
                                     subgenre
KMeansLabel                                  
Fast & Energetic Rock                     734
Slow & Cheerful Rock                     1157
Slow & Depressing Rock                   1106
Slow Dance Rock                           526
Upbeat Rock with Synths to Dance to      1318
### Which cluster corresponds to the most instances per genre? ###
                                    KMeansLabel
subgenre                                       
Indie-Rock               Slow & Depressing Rock
Pop         Upbeat Rock with Synths to Dance to
Psych-Rock                 Slow & Cheerful Rock
Punk        Upbeat Rock with Synths to Dance to
Rock        Upbeat Rock with Synths to Dance to
### Which genre corresponds to the most instances per cluster? ###
                                    subgenre
KMeansLabel                                 
Fast & Energetic Rock                   Punk
Slow & Cheerful Rock                    Rock
Slow & Depressing Rock                  Rock
Slow Dance Rock                         Rock
Upbeat Rock with Synths to Dance to     Rock
```
More interesting and intuitive conclusions can be made from the cluster groupings.

- In cell 2, Psych-Rock mostly fell under the Slow & Depressing Rock cluster which is on point. Punk tends to be fast & energetic subset of rock as well, but Pop and "Plain" Rock also fall under the same cluster. Indie Rock does tend to be slower, but is differentiated by Psych Rock with its mood.

- In cell 3, we see that 4 out of 5 KMeans Labels are dominated by Rock. This is partially due to the imbalanced sampling of plain Rock, which takes up over a third of the dataset. Fast & Energetic Rock is dominated by Punk, matching the intuition behind the typical features of punk.

The reduced dimensional space for just the subgenres is represented below. 

![subgenre PCA](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/GenreClustering/Report/subgenreClustering1.png)

*A scatter plot of the distribution of rock tracks based on audio features, with x and y being the new features constructed by PCA. Each track is colored by their actual genre.*

The subgenres within Rock show even less structure than all genres. The only decipherable subgenre is Psych-Rock straddling along the bottom left edge. The K-Means model shows more bounded structures:

![subgenre PCA KMeans](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/Report/KMeansClustering.png)

*A scatter plot of the distribution of rock tracks based on audio features, with x and y being the new features constructed by PCA. Each track is colored by their K-Means label.*

These clusters did capture some similarities. "Slow & Depressing Rock" managed to capture some Psych-Rock. "Slow & Cheerful Rock" captures some Indie-Rock as well. 

## Conclusions

### Describing Music in a New Way
Clustering music into genres based on audio features allow music to be described in new ways. Combining these genres with the conventions already employed by human-labeled genres, new and more descriptive genres can be generated and labeled onto music. These descriptive genres allow listeners to describe a specific type of music they're looking for. Another insight worth mentioning is that the lack of conclusive K parameter, as noted by the attempts of applying The Elbow Method and Silhouette Scores, indicate a subjective approach to breaking down music. Thus, a music recommendation engine can describe and break down music in many ways. Given more structured data, more optimal K values may be used to solidify generated genre boundaries.

### Compatibility Between Generated Genres and Human-Labeled Genres
Although the generated genres allow music to be viewed in a different perspective, the generated music genres were found to be compatible with human-labeled genres. For example, a punk fan will agree that punk tends to be fast and energetic, and a psych-rock fan will agree that psych-rock is slow and depressing. This is an important result because a model that's too separated from actual music would be meaningless.

### Generated Genres Make Recommending Music From Different Human-Labeled Genres Easier
A user who listens to mostly, say Classical, may discover Folk/Blues songs they like that otherwise wouldn't be discovered if music recommendation engines drew the line within boundaries. By taking into account important audio features, a user can discover music from different genres similar to their current taste.

## Future Work And Recommendations

This project is a largely contained model that is only meant to generate descriptive subgenres and be augmented to an existing music recommendation engine. This model can be further enhanced with the following additions:

- Implementation of more tracks. This would allow further breakdowns of main genres and can allow for more structure based on audio features to arise.
- Creation of different audio features extracted from audio files (Distortion, Percussion, etc.). This model relies on the audio features provided, interpreted, and extracted by Spotify. More audio features will allow more ways to describe music.
- Augmentation with contextual features. For example, one of the initial goals of this project was to see if the differences between songs released in different decades (70's, 80's, 90's, etc.) were prominent enough to show up in clusters. Adding a different set of clustering based on social features could highlight a different dimension that can be added to a music recommendation engine.

A fully realized version of this enhanced model could generate numerous (in the thousands) descriptive genres like Netflix for movies. Then, when augmented to a music recommendation engine, can represent categories of music that specific users may be interested in. For example, a user who is generally found to like relaxing music may be recommended music labeled as "Soothing Classical" to "Ambient Instrumentals". Thus, a user can discover music that can describe the type of music they like, rather than sticking to just genres.




