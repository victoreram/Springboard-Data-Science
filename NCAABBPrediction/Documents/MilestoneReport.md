# Milestone Report

## Problem
Predicting the outcomes of sporting events is a staple activity in sports that was more art than skill for a long time. It wasn't until the advent of Sports Analytics that the methodology behind sports prediction became quantified. With data becoming increasingly available to everyone, it's now possible for anyone to create a model to predict the outcomes of sports. 

The highly variant nature of college basketball presents an interesting case; the NCAA tournament is dubbed "March Madness" for a reason. [Kaggle](https://www.kaggle.com/c/mens-machine-learning-competition-2018/leaderboard) hosts yearly competitions for predicting March Madness but very few models consistently perform well. Vegas and the Oddsmakers are still the gold standard in predicting sports and March Madness is no different. After all, if they weren't, they wouldn't be profitable. Like a small-school underdog facing a blue-blood powerhouse, this model seeks to answer the question: Can we beat the odds?

### Explaining Betting Lines
Resources: [1](https://www.oddsshark.com/sports-betting/point-spread-betting) 
[2](https://www.pinnacle.com/en/betting-articles/Basketball/Basketball-Bet-Types-Explained/HST2G2NVF267NTS3) (See Handicap Betting)
[3](https://www.quora.com/What-does-covering-the-spread-mean-in-sports-betting) The convention used in the Spurs/Lakers example is flipped in this case. Here, favored teams have positive point spreads.

Suppose two teams play each other, Team A and Team B. Team A is perceived to be stronger than Team B. Oddsmakers will attempt to gauge how much stronger Team A is than Team B by setting how many points Team A is favored to win over Team B. This estimation of how many points Team A is favored by is the "Point spread", or betting line.

Now suppose that the oddsmakers set the betting line to be +5.5 for Team A, which is equivalent to -5.5 for Team B. This means that the oddsmakers value that Team A is a 5 point favorite over Team B. If a better bets that Team A will win by 5 points or less, or for Team B to win, he is betting for Team A to "cover the spread". If another better bets that Team A will win by more than 5 points, he is betting for Team A to "beat the spread". This is also referred to betting "against the spread".  

### Objective: Create a Model That Suggests a Profitable Betting Strategy
The goal of this project is to create a model that can:
1. Accurately predict the outcome of games.
2. Using the predicted outcome, identify bets to make according the Vegas betting lines and develop a profitable betting strategy.

## Clients
### The Underdog Mid-Majors: Sports Betters
Enthusiastic sports betters would be highly interested in a model that gives them an edge over the house. A well-performing model could yield lucrative returns on betting in the long run.

### The Power Conference Staples: Sports Analytics Companies
Sports Analytics companies would be interested in this type of model as well. The companies are often contracted by actual sports teams looking to gain an edge over the competition through analytics.

### The Blue-Bloods: The Oddsmakers
If this model is found to consistently beat The Oddsmakers, then it would be in their best interest to maintain a house advantage over prospective betters by implementing aspects of a high performing model. 

## Initial Data

### Basketball Data - [Kaggle NCAA ML Competition - Men's](https://www.kaggle.com/c/mens-machine-learning-competition-2018/data) 
The basketball data used for this analysis comes from the 2018 March Madness competition hosted by Kaggle. The most important pieces of data include:
- RegularSeason(Compact, Detailed)Results.csv: Contains the results of NCAA regular season games. The compact version contains the winning and losing Team ID's, the season, and score of results since 1985. The detailed version contains all of the columns for the compact version with two differences:
  - The earliest season is 2003.
  - Each row contains boxscore stats for each game, including but not limited to: Field Goals Attempted/Made (FGA/FGM), Rebounds (REB), Blocks (BLK), Steals (STL), Three-Pointers Attempted/Made (TPA/TPM), etc. of each team.
 Advanced statistics that will be feature engineered in the future can only be calculated with the detailed version, so that version is used. The dimensions are (82041 x 8). 
- NCAATourney(Compact, Detailed)Results.csv: Contains the results of NCAA Tournament games. Similar in structure to the Regular Season .csv files, but for tournament games. The results are the key feature for this .csv file so the compact version is used. The dimensions are (1063 x 34)
- Teams.csv and TeamSpellings.csv: Each team is identified by an integer Team ID. Teams.csv contains the most common name of a school in one column, and the corresponding ID in another. For example, "Michigan State University" has a team ID of 1277. TeamSpellings.csv contains common variations of team spellings in one column, and the corresponding ID in another. For example, Michigan State University can also be spelled as "Mich. State University", "Mich-State-University", etc., so each value of those rows would still correspond to the Team ID for Michigan State University, 1277. This is an important piece in future data-wrangling tasks as explained below. 

### Betting Data - [The Prediction Tracker](http://thepredictiontracker.com/)
This dataset contains historical betting lines for many sports including NCAA basketball. There's a spreadsheet for each season and they're named with the convention 'ncaabb{last 2 numbers of season}.csv' For example, the betting odds for the 2017-2018 season is 'ncaabb17.csv'. Each spreadsheet contains the following features:
- Each row is a game. Typically there are ~4000 rows per season.
- There first 5 columns are columns about the game itself, such as the home/road team (home, road), the home/road team score (hscore, rscore) and date.
- The rest of the columns contain information about the betting lines. These have the prefix of "line-" and are followed by the platform that provides these lines. For example, the betting line for the "Fox" platform would be listed under the "linefox". These values are often rounded to the nearest 0.5, but if they're not, they're wrangled in one of the data cleaning steps.

## Data Wrangling

### Basketball Data
This dataset is largely cleaned thanks to Kaggle. It contains just about every basic feature I need. Much of the remaining work is to engineer new features by calculating various advanced metrics from this dataset. 

### Betting Data
#### Assigning Team ID's to Team Names
Each of the betting spreadsheets don't come with the Team ID's generated by the Kaggle dataset. Using `TeamSpellings.csv`, I managed to translate most (~99%) of the teams to their corresponding ID's. The ones that weren't translated were obscure schools that don't factor into the NCAA Tournament anyway, and information on those games are dropped.

#### Dropping Line Columns Populated by a Large Amount of NaNs
Columns containing lines that have >10% NaN values were dropped. This also serves as a filter for more reputable betting platforms, as the more reliable ones will be more likely to have clean data.

#### Rounding to the Nearest 0.5
The convention is to list lines to the nearest 0.5. The lines that don't meet this criteria are rounded to the nearest 0.5. 
These steps are performed using the `clean_lines` function from the module `oddscleaner`. 

## Initial Findings (Using 2017-18 Data)
### Betting Lines are Normally Distributed
![Residuals](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/NCAABBPrediction/Documents/margin_residuals.png)

Based on the residuals and the histograms below, both the betting lines and actual results are normally distributed. The following statistics were calculated for each distribution:

```
Mean betting line for home team: 4.890924741760944 

Mean margin for home team: 5.121495327102804

Standard deviation betting line for home team: 8.616574535963725

Standard deviation result for home team: 13.986181735365248
```
### Betting Lines are Closely Related To Actual Results
![Betting Odds](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/NCAABBPrediction/Documents/odds_distribution.png)

Plotting betting line vs. actual margin of victory shows a correlation (r=0.6) with a very low p-value (<0.01).

### Betting Against The Spread Was Profitable in 2018
![Betting Against The Spread](https://raw.githubusercontent.com/victoreram/Springboard-Data-Science/master/NCAABBPrediction/Documents/bets.png)

Simply betting against the spread performed surprisingly well as a strategy for the 2017-18. However, further analysis of different years may show different conclusions. 

