import pandas as pd
import warnings
warnings.filterwarnings('ignore')

season_list = ['17/18','18/19','19/20','20/21','21/22','All Seasons']

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
def get_points(filename,club,season=None,all_seasons=False,all_point=True,i=1):
    df = wrangle_club_data(filename,club)
    
    df.index = df.index+1
    if all_point:
        if all_seasons:
            points = df['points'].sum()
            return points
        df = df[df['season']==season]
        points = df['points'].sum()
        return points
    else:
        if all_seasons:
            index = season_list.index(season)
            selected_season = season_list[:index+1]
            df = df[df['season'].isin(selected_season)]
            points = df['points'].sum()
            return points
        df = df[df['season']==season]
        df.reset_index(inplace=True,drop=True)
        df.index = df.index+1
        points = df.loc[:i,'points'].sum()
        return points
# Gets Goal Difference for the specified club for all seasons or a given season
def get_goal_diff(filename,club,season=None,all_seasons=False,all_point=True,i=1):
    df = wrangle_club_data(filename,club)
    df.index = df.index+1
    if all_point:
        if all_seasons:
            goal_diff = df['Goal Difference'].sum()
            return goal_diff
        df = df[df['season']==season]
        goal_diff = df['Goal Difference'].sum()
        return goal_diff
    else:
        if all_seasons:
            index = season_list.index(season)
            if season != 'All Seasons':
                index = season_list.index(season)+1
            selected_season = season_list[:index]
            df = df[df['season'].isin(selected_season)]
            goal_diff = df['Goal Difference'].sum()
            return goal_diff
        df = df[df['season']==season]
        df.reset_index(inplace=True,drop=True)
        df.index = df.index+1
        goal_diff = df.loc[:i,'Goal Difference'].sum()
        return goal_diff
# Gets Club for all seasons or a given season
def season_unique_club(filename,season=None,all_seasons=False):
    df = pd.read_csv(filename).drop('Unnamed: 0',axis=1)
    df.sort_values('home_team',inplace=True)
    if (season=='All Seasons')|all_seasons:
        unique_team = df.home_team.unique()
        return unique_team
    unique_team = df[df['season']==season].home_team.unique()
    unique_team.sort()
    return unique_team