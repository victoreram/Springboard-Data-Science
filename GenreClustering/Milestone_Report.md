# Capstone Project 1 Milestone Report
## Problem
Genre Classification is reliant on subjective listening experiences between music fans. This project aims to find boundaries between musical genres using a track's audio features.

## Client
Clustering music is an important mechanism for music recommendation engines. These engines are the backbone of streaming companies like Spotify, Pandora, Last.fm, etc. and allow their users to discover music that they will likely enjoy. 

## Data
The primary dataset used for this project comes from the Free Music Archive (FMA) and the repo can be found [here](https://github.com/mdeff/fma/)
The data is drawn from the following spreadsheets from that repo:

- tracks.csv: per track metadata such as ID, title, artist, genres, tags and play counts, for all 106,574 tracks.
- genres.csv: all 163 genre IDs with their name and parent (used to infer the genre hierarchy and top-level genres).
- features.csv: common features extracted with librosa.
- echonest.csv: audio features provided by Echonest (now Spotify) for a subset of 13,129 tracks.

These spreadsheets are too big to be uploaded on github, and most contain corrupt metadata. So, I replaced missing values and removed rows with un-inferrable data and uploaded cleaner versions of tracks.csv:
- supervised_tracks.csv: A merge of tracks.csv and echonest.csv that contains audio features from echonest and genre labels from tracks.csv
- unsupervised_tracks.csv A merge of tracks.csv and echonest.csv that contains audio features from echonest and genre labels, some unknown, from tracks.csv

## Potential Data
More data can be dug up using Spotify's API, which inherently contains the audio features used in this project. 

## Initial Findings
- There's a strong correlation between 24/28 relationships between the audio features. 
- There's a distinct boundary between genres in when plotting between certain audio features. 

