# Capstone Project 1: Subgenre Classification

## Data
Free Music Archive. Repo [here](https://github.com/mdeff/fma/)
The data in this repo is divided into two sets:
- tracks_supervised.csv: Contains audio features of 13129 tracks, cleaned up from tracks.csv and echonest.csv from the fma repo using DataCleaning.ipynb.  

## Documentation
- Proposal.md: The formal proposal for this project.
- Data_Wrangling.md: Outlines data-wrangling steps in project. 

## Code
- utils.py: contains some helper functions for dataset. Taken from the FMA repo.
- fma_EDA.ipynb: EDA for each spreadsheet in the dataset. 
- DataCleaning.ipynb: Cleans up tracks.csv and merged the audio features from echonest.csv into tracks_supervised.csv. Used to be csv_cleaning.ipynb.
- FeatureDistribution.ipynb: Examines the relationship of audio features amongst each other and by genre
- GenreClustering.ipynb: Takes audio featus from tracks_supervised.csv and clusters them. Algorithm(s) used: MeanShift. 
