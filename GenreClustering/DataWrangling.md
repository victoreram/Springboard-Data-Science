## Genre Clustering Data Wrangling (See DataCleaning.ipynb)

The data I will be using is from the Free Music Archive (FMA) which can be found [here](https://github.com/mdeff/fma). In particular, I will be extracting features from the following files:

- tracks.csv: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks.
- genres.csv: all 163 genre IDs with their name and parent (used to infer the genre hierarchy and top-level genres).
- features.csv: common features extracted with librosa.
- echonest.csv: audio features provided by Echonest (now Spotify) for a subset of 13,129 tracks.

### tracks
'tracks.csv' is the 'meat' of this dataset and contains most of the information I need. This file is multi-indexed into 3 parent indexes: album, artist, track. There are a total of 52 columns initially and not all are relevant for the purpose of this project. The relevant child columns for each parent index are the following:
- track: genres_top, genres, genres_all, id
- artist: name
- album: date_released, title

The multiindex can be sliced as follows: tracks[('parent_index','child_index')]. So, to access track's bit_rate column, you would access it by: tracks[('track', 'bit_rate')]. In DataCleaning.ipynb, I remove a lot of unnecessary columns which allowed me to remove the multiindex without loss of important data.


### genres
This file is relatively clean, though I have a minor gripe with 'Metal' not being its own genre. I can correct this by making Metal its own genre hierarchy instead of having 'Rock' as its parent.

### features
This file contains statistics of the audio features of a track. There's not much to clean here as this file already contains valuable data.

### echonest
This file contains the audio features I need for each track. Again, the file is already clean and has all the data I need.

## [Data Cleaning](https://github.com/victoreram/Springboard-Data-Science/blob/master/GenreClustering/DataCleaning.ipynb)
The code is written in the notebook above. Here is a short summary of some of the steps:
- Any track with "genres_all" as null is removed. Since this contains the closest estimation to a target variable, it's best to keep this relatively pure. 
- Convert tracks.csv columns into appropriate types (year to ints, genres_top to lists, etc.)
- Remove data with corrupt metadata, such tracks with genres_all that don't resemble what typical column values should be, which are a list of column ID's. Some of these contain descriptions of the artist for some reason.
- Extract only the tracks with the basic "Spotify" audio features from echonest.
- Merge tracks and echonest audio features together into one cohesive .csv
