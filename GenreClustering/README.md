# Capstone Project 1: Genre Clustering

## Data
Free Music Archive. Repo [here](https://github.com/mdeff/fma/)
The data in this repo is divided into two sets:
- tracks_cleaneded.csv: Contains audio features of 13129 tracks, cleaned up from tracks.csv and echonest.csv from the fma repo using DataCleaning.ipynb.  

## Documentation
- Proposal.md: The formal proposal for this project.
- DataWrangling.md: Outlines data-wrangling steps in project. 
- Statistical-Inference-Report.md: Outlines statistical inference techniques used in this project.

## Code
- utils.py: contains some helper functions for dataset. Taken from the FMA repo.
- fma_EDA.ipynb: EDA for each spreadsheet in the dataset. Delved into the data available for this project and explore possibilities. 
- DataCleaning.ipynb: Cleans up tracks.csv and merged the audio features from echonest.csv into tracks_cleaned.csv. Used to be csv_cleaning.ipynb.
- FeatureDistribution.ipynb: Examines the relationship of audio features amongst each other and by genre
- GenreClustering.ipynb: Takes audio features from tracks_cleaned.csv and performs clustering on them. Then, each model is evaluated visually and using clustering metrics. Algorithm(s) used: K-Means, MeanShift, Spectral Clustering. 
- CreateViz.py: When run, creates a Bokeh dashboard that shows the distribution of each track's audio features. To see, enter the following command:
 `
 bokeh serve --show CreateViz.py
 `
 For more information on other ways to view this, see https://bokeh.pydata.org/en/latest/docs/user_guide/server.html
