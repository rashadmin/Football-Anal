import pandas as pd
import warnings
warnings.filterwarnings('ignore')



def wrangle_club_data(filename,club):
    df = pd.read_csv(filename).drop('Unnamed: 0',axis=1)
    df = df[(df['home_team'] == club)|(df['away_team']== club)]
    df = df[~df.duplicated()]
    df[['home_team_score','away_team_score']] = df['score'].str.split('-',expand=True).astype(int)
    # Formatting the winning Table
    df['points'] = df['home_team']
    df['points'].mask(((df['home_team_score']-df['away_team_score']) <0),df['away_team'],inplace=True)
    df['points'].mask(((df['home_team_score']-df['away_team_score']) == 0),'Draw',inplace=True)
    df['points'].mask(df['points']==club,'Win',inplace=True)
    df['points'].where(((df['points']=='Win')|(df['points']=='Draw')),'Loss',inplace=True)
    df['points'].replace({'Win':3,'Loss':0,'Draw':1},inplace=True)
    df['Goal Difference'] = (df['home_team_score']-df['away_team_score']).abs()
    df['Goal Difference'].where(df['points']==3,(-1*df['Goal Difference']),inplace=True)
    df['date'] = pd.to_datetime(df['date'],format='%d-%m-%Y')
    df.sort_values('date',inplace=True)
    return df
# Gets Points for the specified club for all seasons or a given season
def get_points(filename,club,season=None,all_seasons=False):
    df = wrangle_club_data(filename,club)
    if all_seasons:
        points = df['points'].sum()
        return points
    df = df[df['season']==season]
    points = df['points'].sum()
    return points
# Gets Goal Difference for the specified club for all seasons or a given season
def get_goal_diff(filename,club,season=None,all_seasons=False):
    df = wrangle_club_data(filename,club)
    if all_seasons:
        goal_diff = df['Goal Difference'].sum()
        return goal_diff
    df = df[df['season']==season]
    goal_diff = df['Goal Difference'].sum()
    return goal_diff
# Gets Club for all seasons or a given season
def season_unique_club(filename,season=None,all_seasons=False):
    df = pd.read_csv(filename).drop('Unnamed: 0',axis=1)
    if (season=='All Seasons')|all_seasons:
        unique_team = df.home_team.unique()
        return unique_team
    unique_team = df[df['season']==season].home_team.unique()
    return unique_team