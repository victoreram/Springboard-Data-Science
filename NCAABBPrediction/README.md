# Capstone Project 2: NCAA Basketball Predictions

For detailed documentation of this work, see my [report](https://github.com/victoreram/Springboard-Data-Science/blob/master/NCAABBPrediction/Documents/FinalReport.md)

## Notebooks
- **DataExploration.ipynb**: Includes EDA and initial findings about the distributions of betting lines and the point margin of games. The result is that they're both normally distributed.
- **EloTuning.ipynb**: The main metric used to evaluate a team's strength are Elo Ratings. Here, I tune the parameters which yield the most accurate Elo Ratings based on the results of the 2017-18 NCAA tournaments.
- **MLAdvancedStats.ipynb**: Using the tuned Elo Ratings, as well as some advanced stats calculated from Kaggle's boxscore data, I trained Linear Regressions, LinearSVRs, and Decision Tree Regression models to predict the margin of victory. I then created a betting strategy for each model and compared them to real betting lines. 
