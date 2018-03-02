# Capstone Project 1: Subgenre Classification

## Data
Free Music Archive. Repo [here](https://github.com/mdeff/fma/)
The data in this repo is divided into two sets:
- supervised_tracks.csv: Contains track and audio features where all genres are labeled
- unsupervised_tracks.csv Contains track and audio features where some genres are unknown, best used for unsupervised clustering methods. 

## Documentation
- Proposal.md: The formal proposal for this project.
- Data_Wrangling.md: Outlines data-wrangling steps in project. 

## Code
- utils.py: contains some helper functions for dataset. Taken from the FMA repo.
- fma_EDA.ipynb: EDA for each spreadsheet in the dataset. 
- csv_cleaning.ipynb: Cleans up tracks.csv and echonest.csv into a smaller subset of data.
- Merging_dfs.ipynb: Notebook that merges cleaned up spreadsheets from csv_cleaning into a unified dataframe and csv file.
- feature_distribution.ipynb: Examines the relationship of audio features amongst each other and by genre
