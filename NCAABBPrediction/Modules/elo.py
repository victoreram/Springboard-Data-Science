
import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
#from sklearn.linear_model import LogisticRegression
#import matplotlib.pyplot as plt
from sklearn.metrics import explained_variance_score, mean_absolute_error, mean_squared_error, mean_squared_log_error
#from sklearn.linear_model import LinearRegression
from sklearn import linear_model
from sklearn.utils import shuffle
from sklearn.preprocessing import StandardScaler

import itertools
#from sklearn.model_selection import GridSearchCV

#https://www.kaggle.com/lpkirwin/fivethirtyeight-elo-ratings/
#https://en.wikipedia.org/wiki/Elo_rating_system
#https://fivethirtyeight.com/features/how-we-calculate-nba-elo-ratings/

def elo_pred(elo1, elo2):
    '''Calculates expected value E of team'''
    return(1. / (10. ** (-(elo1 - elo2) / 400.) + 1.))

def expected_margin(elo_diff):
    '''Calculates Expected Margin of Victory (see footnote 2 of 538 article)'''
    return((7.5 + 0.006 * elo_diff))

def elo_update(w_elo, l_elo, margin, K=20.):
    elo_diff = w_elo - l_elo
    pred = elo_pred(w_elo, l_elo)
    mult = ((margin + 3.) ** 0.8) / expected_margin(elo_diff)
    update = K * mult * (1 - pred)
    return(pred, update)

def elo_back_update(w_elo, l_elo, margin, K=20.):
    elo_diff = w_elo - l_elo
    pred = elo_pred(w_elo, l_elo)
    mult = ((margin + 3.) ** 0.8) / expected_margin(elo_diff)
    update = -K * mult * (1-pred)
    return(pred, update)

def final_elo_per_season(df, team_id):
    d = df.copy()
    d = d.loc[(d.WTeamID == team_id) | (d.LTeamID == team_id), :]
    d.sort_values(['Season'], inplace=True)
    d.drop_duplicates(['Season'], keep='last', inplace=True)
    w_mask = d.WTeamID == team_id
    l_mask = d.LTeamID == team_id
    d['SeasonElo'] = None
    d.loc[w_mask, 'SeasonElo'] = d.loc[w_mask, 'w_elo']
    d.loc[l_mask, 'SeasonElo'] = d.loc[l_mask, 'l_elo']
    out = pd.DataFrame({
        'TeamID': team_id,
        'Season': d.Season,
        'SeasonElo': d.SeasonElo
    })
    return(out)

def elos_per_season(df, team_id):
    d = df.copy()
    d = d.loc[(d.WTeamID == team_id) | (d.LTeamID == team_id), :]
    d.sort_values(['Season'], inplace=True)
    #d.drop_duplicates(['Season'], keep='last', inplace=True)
    w_mask = d.WTeamID == team_id
    l_mask = d.LTeamID == team_id
    d['SeasonElo'] = None
    d.loc[w_mask, 'SeasonElo'] = d.loc[w_mask, 'w_elo']
    d.loc[l_mask, 'SeasonElo'] = d.loc[l_mask, 'l_elo']
    out = pd.DataFrame({
        'GameID': d.GameID,
        'TeamID': team_id,
        'Season': d.Season,
        'SeasonElo': d.SeasonElo
    })
    return(out)


def season_elos(rs, K=20., HOME_ADVANTAGE=100.):
    '''
    Inputs:
    rs = dataframe of regular season results with columns: W/LTeamID, W/LScore
    K = K parameter that measures the volatility of the model. High K means elo ratings change more after one game and vice versa.
    HOME_ADVANTAGE = measures the value of home court advantage. The higher this parameter, the stronger home court advantage is.
    Thus at a high value, if a road team beats a home team, then more elo points are transferred to the road team.
    
    Outputs:
    preds = The estimated predictions of results based on the logistic curve on the 538 site.
    season_elos = the elo ratings at the end of the season for each team
    '''
    team_ids = set(rs.WTeamID).union(set(rs.LTeamID))
    # This dictionary will be used as a lookup for current
    # scores while the algorithm is iterating through each game
    elo_dict = dict(zip(list(team_ids), [1500] * len(team_ids)))
    # Elo updates will be scaled based on the margin of victory
    rs['margin'] = rs.WScore - rs.LScore
    # I'm going to iterate over the games dataframe using 
    # index numbers, so want to check that nothing is out
    # of order before I do that.
    assert np.all(rs.index.values == np.array(range(rs.shape[0]))), "Index is out of order."
    preds = []
    w_elo = []
    l_elo = []

    # Loop over all rows of the games dataframe
    for row in rs.itertuples():

        # Get key data from current row
        w = row.WTeamID
        l = row.LTeamID
        margin = row.margin
        wloc = row.WLoc

        # Does either team get a home-court advantage?
        w_ad, l_ad, = 0., 0.
        if wloc == "H":
            w_ad += HOME_ADVANTAGE
        elif wloc == "A":
            l_ad += HOME_ADVANTAGE

        # Get elo updates as a result of the game
        pred, update = elo_update(elo_dict[w] + w_ad,
                                  elo_dict[l] + l_ad, 
                                  margin,
                                 K)
        elo_dict[w] += update
        elo_dict[l] -= update

        # Save prediction and new Elos for each round
        preds.append(pred)
        w_elo.append(elo_dict[w])
        l_elo.append(elo_dict[l])

    rs['w_elo'] = w_elo
    rs['l_elo'] = l_elo
    df_list = [final_elo_per_season(rs, id) for id in team_ids]
    season_elos = pd.concat(df_list)
    return season_elos, preds

def elo_history(rs, K=20., HOME_ADVANTAGE=100.):

    team_ids = set(rs.WTeamID).union(set(rs.LTeamID))
    # This dictionary will be used as a lookup for current
    # scores while the algorithm is iterating through each game
    elo_dict = dict(zip(list(team_ids), [1500] * len(team_ids)))
    # Elo updates will be scaled based on the margin of victory
    rs['margin'] = rs.WScore - rs.LScore
    # I'm going to iterate over the games dataframe using 
    # index numbers, so want to check that nothing is out
    # of order before I do that.
    assert np.all(rs.index.values == np.array(range(rs.shape[0]))), "Index is out of order."
    preds = []
    w_elo = []
    l_elo = []

    # Loop over all rows of the games dataframe
    for row in rs.itertuples():

        # Get key data from current row
        w = row.WTeamID
        l = row.LTeamID
        margin = row.margin
        wloc = row.WLoc
        game_id = row.GameID
        
        # Does either team get a home-court advantage?
        w_ad, l_ad, = 0., 0.
        if wloc == "H":
            w_ad += HOME_ADVANTAGE
        elif wloc == "A":
            l_ad += HOME_ADVANTAGE

        # Get elo updates as a result of the game
        pred, update = elo_update(elo_dict[w] + w_ad,
                                  elo_dict[l] + l_ad, 
                                  margin,
                                 K)
        elo_dict[w] += update
        elo_dict[l] -= update

        # Save prediction and new Elos for each round
        preds.append(pred)
        w_elo.append(elo_dict[w])
        l_elo.append(elo_dict[l])

    rs['w_elo'] = w_elo
    rs['l_elo'] = l_elo
    df_list = [elos_per_season(rs, team_id) for team_id in team_ids]
    season_elos = pd.concat(df_list)
    return season_elos

def evaluate():
    pass

def training_form(elos):
    df_winelos = elos.rename(columns={'TeamID':'WTeamID', 'SeasonElo':'WElo'})
    df_losselos = elos.rename(columns={'TeamID':'LTeamID', 'SeasonElo':'LElo'})
    df_dummy = pd.merge(left=df_tour, right=df_winelos, how='left', on=['Season', 'WTeamID'])
    df_concat = pd.merge(left=df_dummy, right=df_losselos, on=['Season', 'LTeamID'])
    df_concat['EloDiff'] = df_concat.WElo - df_concat.LElo
    return df_concat

def winloss_features(df_teams, df_feature, feature_cols, merge_on=['Season'], team_id='TeamID'):
    '''
    Takes input:
    df_teams: a dataframe with columns that specify the winning and losing team, identified by arg team_id
    df_feature: a dataframe with features (e.g. stats) that each team has.
    feature_cols: the columns from df_features to extract
    merge_on: the common columns from df_teams and df_features to merge to. Default is 'Season'
    team_id: The name of the column that contains the team identifier for both df_teams and df_features. Default is 'TeamID'.
    Outputs: 
    df_concat: a dataframe containing the original info from df_teams with columns that contain the features for each team
    from df_feature
    '''
    
    # Separate teams by win/loss
    w_team_id = 'W'+team_id
    l_team_id = 'L'+team_id
    
    # Prepare columns for feature dataframe
    w_cols = ['W{}'.format(feature) for feature in feature_cols]
    l_cols = ['L{}'.format(feature) for feature in feature_cols]
    diff_cols = ['{}Diff'.format(feature) for feature in feature_cols]
    
    # Create a dict with key = feature, value = Wfeature or Lfeature
    w_dict = dict(zip(feature_cols, w_cols))
    w_dict[team_id] = w_team_id
    
    l_dict = dict(zip(feature_cols, l_cols))
    l_dict[team_id] = l_team_id
    
    df_wins = df_feature.rename(columns=w_dict)
    df_losses = df_feature.rename(columns=l_dict)
    
    # Prepare common columns to merge on
    w_merge_on = merge_on + [w_team_id]
    l_merge_on = merge_on + [l_team_id]
    
    # Merge the dataframes that contain the winning team's features with the losing team's features
    df_dummy = pd.merge(left=df_teams, right=df_wins, how='left', on=w_merge_on)
    df_concat = pd.merge(left=df_dummy, right=df_losses, on=l_merge_on)
    df_concat = df_concat.reindex(columns=list(df_concat.columns)+diff_cols)
    df_concat[diff_cols] = df_concat[w_cols].values - df_concat[l_cols].values
    
    return df_concat
    
def mirror_df(df, x, y):
    df_pos = df.copy()
    df_pos[x] = df[x]
    df_pos[y] = df[y]
    
    df_neg = df.copy()
    df_neg[x] = -df[x]
    df_neg[y] = -df[y]

    df_mirrored = pd.concat((df_pos, df_neg))
    
    return df_mirrored

def elo_tune(rs, tourney, Ks, HCAs, x_col='SeasonEloDiff', y_col='WMargin', season_cutoff=2017):
    params = list(itertools.product(Ks, HCAs))
    n_params = len(params)
    scores_all = []
    coefs = []
    for i in range(n_params):
        K, HCA = params[i]
        param_string = "K{}HCA{}".format(K,HCA)
        ### Calculate elos
        elos, rs_preds = season_elos(rs, K, HCA)
        #elos.to_csv(elo_out_dir+"SeasonElos{}.csv".format(param_string))
        
        ### Preprocess elos into [[X][y], [-X],[-y]] form
        elos_tourney = winloss_features(df_teams=tourney, df_feature=elos, feature_cols=['SeasonElo'])
        
        ### Mirror dfs
        elos_tourney = mirror_df(elos_tourney, x=x_col, y=y_col).reset_index(drop=True)
        #elos_tourney.to_csv(elo_out_dir+"EloTrain{}.csv".format(param_string))
        
        ### Evaluate
        scores, coef = elo_lr(elos_tourney, x_col, y_col)
        scores_all.append(scores)
        coefs.append(coef)
        
    return list(zip(params, scores_all)), list(zip(params, coefs))

def elo_lr(elos_tourney, x, y, season_cutoff=2017, metrics=[mean_squared_error, explained_variance_score]):
    lr = lm.LinearRegression()
    scores = []
    X_train = elos_tourney.loc[elos_tourney.Season<season_cutoff, x].values.reshape(-1,1)
    X_train = StandardScaler().fit_transform(X_train)
    X_test = elos_tourney.loc[elos_tourney.Season>=season_cutoff, x].values.reshape(-1,1)
    X_test = StandardScaler().fit_transform(X_test)
    y_train = elos_tourney.loc[elos_tourney.Season<season_cutoff, y].values.reshape(-1,1)
    y_train = StandardScaler().fit_transform(y_train)
    y_true = elos_tourney.loc[elos_tourney.Season>=season_cutoff, y].values.reshape(-1,1)
    y_true = StandardScaler().fit_transform(y_true)

    lr.fit(X_train,y_train)
    y_pred = lr.predict(X_test)
    coef = lr.coef_
    
    for metric in metrics:
        scores.append(metric(y_true, y_pred))
        
    return scores, coef
        