## Project 1: Clustering Music Into Subgenres Using Audio Features
Victor Ramirez
### Problem
Some music recommendation engines rely on user-specified genres, but oftentimes music can’t be pigeonholed into a broad spectrum within a genre. Moreover, relying on users requires enough listeners to classify a song and each listener’s classification is subjective. This creates a seemingly arbitrary way to differentiate between types of music. This project aims to find structure using solely a song's audio features. By removing bias introduced by people's perceptions of music, we could see different ways to categorize music. 
### Deeper Insights Into Genres
Finding tracks with similar features is one factor within music recommendation engines (MRE). Netflix can recommend users, say “visually-striking thrillers from the 80’s”, but such a recommendation engine isn’t present in music platforms like Pandora or Spotify. Instead of relying on assigned genres, it may be more helpful to a music recommendation engine to consider instead songs with similar features. This could improve the recommendatio engine, and having a robust music recommendation engine will allow users to discover music that they may not otherwise have found.
### Data
The data used is from the [Free Music Archive](https://github.com/mdeff/fma). This data contains audio files and metadata for each track.
### Approach
The canonical approach to this problem would be to classify each song in a supervised manner and to check against the given genres. What this project aims to do instead is to find structure within the audio features of music data by various clustering algorithms and see how these compare with music genres. 
### Deliverables
Tentatively, code and a paper.

