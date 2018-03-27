# Music Genre Clustering Project Report
By Victor Ramirez

## Problem
Suppose a user wanted to expand their music tastes by listening to similar music in other genres. How would a music recommendation engine go about recommending to this user, if it was bounded by the genre classification imposed by other listeners? Genre classification is reliant on subjective listening experiences between music fans. One solution is to take the user's listening history and compare it to other users with similar listening histories to recommend new music. But, using this solution alone has some flaws, namely:
1. Listening history data may not be available, especially for smaller companies or for tracks from newer, relatively unknown artists.
2. Other users may subject themselves to a music "bubble", only listening to music that is familiar and limiting the opportunity for discovery.

This project aims to cross the boundaries imposed by genre classification and instead find similarities among music instead of just relying on genres. In doing so, it doesn't aim to rewrite music genres, as music genres have cultural and historical nuances that even the most robust machine learning algorithms can't strip down. Rather, it aims to augment music genres and to derive more descriptive subgenres that are based on the audio features from a track. Descriptive subgenres can strengthen a music recommendation engine and give users more options for discovering otherwise unknown music. Netflix is the gold standard for this in movies, but no music company seems to have matched Netflix's knack for creating eerily descriptive movie genres. 

### Potential Clients
Clients with music data are the main target for this projects. These clients would fall under 2 types:
1. A company who already has a robust music recommendation engine and would like to bolster it. E.g. Spotify, Pandora, Last.fm, Youtube
2. A smaller, competing company that has access to music, but doesn't have much user data to base recommendations off of.

Companies under the 1st group likely have something similar in place already. For example, the audio features I used for music genre clustering come from Spotify's features. But, there are countless ways to extract audio features from audio files. Data from fma has raw features extracted from audio files, but in-depth analysis of what insights to derive from them require advanced signal-processing knowledge that are beyond the scope of this project. This project is tailored for clients that already have descriptive features in place that can be clustered to describe genres.

## Data Collection
The data is originally sourced from the Free Music Archive. Repo [here](https://github.com/mdeff/fma/). The data files used to create the spreadsheets for this repo come from:
- `tracks.csv`: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks. 
- `genres.csv`: all 163 genre IDs with their name and parent (used to infer the genre hierarchy and top-level genres).
- `echonest.csv`: audio features provided by Echonest (now Spotify) for a subset of 13,129 tracks.

## [Initial Exploration: Genres and Year Released](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/Tracks_by_genre_year.ipynb)
### Tracks by Genre
The first aspect of this project I decided to explore was the amount of tracks that were categorized by genre. Note that this was initially done using `tracks.csv` from FMA. The `tracks_cleaned.csv` has a similar structure and was cleaned after knowing some features outlined by this step.

#### All Genres
The histogram above shows that that the music sampled by this dataset has an imbalanced proportion of tracks by genre. The sample is mostly composed of 3 genres: Experimental, Electronic, and Rock, which more than make up the remaining 14 genres. Samples of top genres were taken later on to give an estimated "fair" distribution of features later on. It is worth noting that this is not necessarily a fault of the dataset. Some genres are more popular than others, so it's natural to assume that some genres will have more songs than others.

#### Subgenre: Rock
When examining the subgenres that compose Rock, I used genres that are direct "children" of rock (see description of `genres.csv` above). Rock has many other subgenres outlined in this dataset, but those are absorbed by the hierarchy level right below Rock. 

The histogram above shows roughly the same Pareto distribution for subgenres as the genres. Punk has the most instances near 10,000 which is roughly 30% of the total instances of Rock. The 2nd most (Lo-Fi) has 2/3 of that amount. There's a healthy enough sample size for the 10 subgenres that it's still possible to see some meaningful disparities between subgenres. 

### Tracks by Year
One of the original considerations when separating genres by audio features is to look at when a song is released. After all, some songs and genres are characterized heavily by the times they were released; Rock from the 70's is notably distinct from Rock from the 80's, which are both much different than Indie Rock released in the 2010's. The factors that cause these disparities, whether they be cultural or technology, could in theory be captured by the audio features. In order to prove this hypothesis, one would need a healthy amount of data released over time. 

Unfortunately as we see above, most of the tracks in this dataset are released within the last 2 decades with a lot of them unknown. Thus, any insights from differentiating by decade released may not be all that meaningful. 

## [Data Wrangling](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/DataCleaning.ipynb)
### tracks
`tracks.csv` is the 'meat' of this dataset and contains most of the information I need. This file is multi-indexed into 3 parent indexes: album, artist, track. There are a total of 52 columns initially and not all are relevant for the purpose of this project. The relevant child columns for each parent index are the following:
- track: genres_top, genres, genres_all, id
- artist: name
- album: date_released, title

The multiindex can be sliced as follows: tracks[('parent_index','child_index')]. So, to access track's bit_rate column, you would access it by: tracks[('track', 'bit_rate')]. In DataCleaning.ipynb, I remove a lot of unnecessary columns which allowed me to remove the multiindex without loss of important data.

### genres
This spreadsheet is mainly used to translate genre ID's to the name of the genres.

### echonest
This file contains a subset of audio features I need for each track. Tracks which have the audio features I need are merged with tracks.

### Merging into a Unified DataFrame
The code is written in the notebook above. Here is a short summary of some of the steps:
- Any track with "genres_all" as null is removed. Since this contains the closest estimation to a target variable, it's best to keep this relatively pure. 
- Convert tracks.csv columns into appropriate types (year to ints, genres_top to lists, etc.)
- Remove data with corrupt metadata, such tracks with genres_all that don't resemble what typical column values should be, which are a list of column ID's. Some of these contain descriptions of the artist for some reason.
- Extract only the tracks with the basic "Spotify" audio features from echonest.
- Merge tracks and echonest audio features together into one cohesive .csv, `tracks_cleaned.csv`. This new .csv file contains 13129 rows and 18 columns. 8 of these columns are audio files, while the rest are metadata (track, artist, album, genre, year released).

## Further Data Analysis: Feature Distribution

## Machine Learning
