## Subgenre Classification Data Wrangling

The data I will be using is from the Free Music Archive (FMA) which can be found [here](https://github.com/mdeff/fma). In particular, I will be extracting features from the following files:

- tracks.csv: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks.
- genres.csv: all 163 genre IDs with their name and parent (used to infer the genre hierarchy and top-level genres).
- features.csv: common features extracted with librosa.
- echonest.csv: audio features provided by Echonest (now Spotify) for a subset of 13,129 tracks.

### Tracks
Tracks is the 'meat' of this dataset and contains most of the information I need.This file is multi-indexed into 3 parent indexes: album, artist, track. There are a total of 52 columns initially and not all are relevant for the purpose of this project. The relevant child columns for each parent index are the following:
- track: bit_rate, genres_top, genres, genres_all, language_code, number, tags, title
- artist: id, tags, name, active_year_begin, active_year_end, related_projects, location*
- album: date_released, tags, title, tracks, id, type*, comments*

*indicate possible omission or addition depending on expansion of project.

The multiindex can be sliced as follows: tracks[('parent_index','child_index')]. So, to access track's bit_rate column, you would access it by: tracks[('track', 'bit_rate')].
#### Cleanup
- Right off the bat, any track with "genres_all" as null is removed. Since this contains our target variable, it's important that this be pure and not subject to error from 'best guesses'. This trims our dataset to ~106000, still plenty of data. 
- The time in which a track is released will be converted from datetime into categories / bins by decade, i.e. a track with date_released = 01-01-1986 will instead have a 'decade' column value '1980s'. The exact year is not that relevant for classifying subgenres, but a track 'from the 80's' has a distinct cultural distinction. This will help broaden the subcategories while making a track's subgenres descriptive. 

### genres
This file is relatively clean, though I have a minor gripe with 'Metal' not being its own genre. I can correct this by making Metal its own genre hierarchy instead of having 'Rock' as its parent.

### features
This file contains statistics of the audio features of a track. There's not much to clean here as this file already contains valuable data.

### echonest
This file contains the audio features I need for each track. Again, the file is already clean and has all the data I need.
