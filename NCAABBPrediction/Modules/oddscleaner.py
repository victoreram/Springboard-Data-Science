import numpy as np
import pandas as pd

def assign_team(team_string):
    '''
    Given a string of the team's name (team_string), return its TeamID from the dictionary of Team ID's and spellings
    '''
    team_string = team_string.lower()
    try:
        return team_spelling_dict[team_string]
    except KeyError:
        # Modify string if team_string initially isn't found
        try:
            team_string = team_string.replace(' ', '-')
            return team_spelling_dict[team_string]

        except KeyError:
            print("NOT FOUND:", team_string)
            return np.NaN
        
def round_pt5(number):
    '''
    Round a number to the closest half integer.
    '''

    return round(number * 2) / 2
        
    
def drop_mostly_nans(df, cols, thresh=0.1):
    '''
    Drop columns (cols) from a dataframe (df) that have a percentage of nans > threshold
    Returns new df with dropped columns
    '''
    n = len(df)
    for col in cols:
        nans = df[col].isnull().sum()
        if (nans / n) > thresh:
            df.drop(col, axis=1, inplace=True)
            print("Dropping ", col)
            
    return df

def replace_na(df, na_cols, replace_with):
    series_replacement = df[replace_with]
    for col in na_cols:
        df[col] = df[col].fillna(series_replacement)
    return df



def clean_lines(df, col_starts_with = 'line', avg_line = 'lineavg'):
    
    # Find columns containing lines
    line_cols = [col for col in df if col.startswith(col_starts_with)]
    
    # Drop columns and rows with significant amounts of nans
    df = drop_mostly_nans(df, line_cols)
    line_cols = [col for col in df if col.startswith(col_starts_with)]
    
    # Drop line rows with no average
    df = df.drop(df[df[avg_line].isnull()].index)
    #df[avg_line] = df[avg_line].dropna(0).reset_index().drop('index', axis=1)
    
    # Replace nans with average line
    df = replace_na(df, na_cols=line_cols, replace_with=avg_line)
    
    # Round lines to nearest point 5
    df[line_cols] = df[line_cols].applymap(round_pt5)
      
    return df