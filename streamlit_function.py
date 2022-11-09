import pandas as pd
from wrangler import season_unique_club,wrangle_club_data,get_goal_diff,get_points
import streamlit as st
#import numpy as np


@st.cache(suppress_st_warning=True)
def league_dataframe(filename,all_seasons=True,season=None):
    clubs = season_unique_club(filename,all_seasons=all_seasons,season=season)
    point = [get_points(filename = filename,all_seasons=all_seasons,season=season,club=club) for club in clubs]
    goal_diff = [get_goal_diff(filename = filename,all_seasons=all_seasons,season=season,club=club) for club in clubs]
    
    league = pd.DataFrame(
        {
            'clubs':clubs,
            'point':point,
            'goal_difference':goal_diff
            })
    league.sort_values('point',inplace=True,ascending=False)
    league.reset_index(inplace=True,drop=True)
    league.index = league.index+1
    return league

@st.cache(suppress_st_warning=True)
def club_matches(filename,club,all_seasons=True,season=None):
    df = wrangle_club_data(filename,club=club)
    #Piechart showing games won/lost/drawn in all season or a particular season
    
    if season != 'All Seasons':
        df = df[df['season']==season]
        col = ['home_team','score','away_team']
    else:
        col = ['home_team','score','away_team','season']
    df = df.sort_values('date').reset_index(drop=True)
    df = df[col]
    return df

@st.cache(suppress_st_warning=True)
def club_stats(filename,club,all_seasons=True):
     club_data = wrangle_club_data(filename, club)
     unique_season = club_data.season.unique()
     position,goal_difference,points =[],[],[]
     for season in unique_season:
         seasonal_club_data = league_dataframe(filename,all_seasons=False,season=season)
         index = seasonal_club_data.index[seasonal_club_data['clubs']==club]
         position.append(index.values[0]+1)
         goal_diff = seasonal_club_data.loc[index,'goal_difference']
         goal_difference.append(goal_diff.values[0])
         point = seasonal_club_data.loc[index,'point']
         points.append(point.values[0])
     stats = pd.DataFrame(
         {
             'season':unique_season,
             'position':position,
             'points':points,
             'goal_difference':goal_difference
             }
         )
     
     return stats
@st.cache(suppress_st_warning=True)
def away_home(filename,club,season=None):
    data =wrangle_club_data(filename, club)
    mapping = {0:'Loss',1:'Draw',3:'Win'}
    data['points'].replace(mapping,inplace=True)
    if season != 'All Seasons':
        home_games = data[(data['home_team']==club)&(data['season']==season)]
        away_games = data[(data['home_team']!=club)&(data['season']==season)]
    else:
        home_games = data[(data['home_team']==club)]
        away_games = data[(data['home_team']!=club)]
    home_games=home_games['points'].value_counts()
    away_games = away_games['points'].value_counts()
    return home_games,away_games
@st.cache(suppress_st_warning=True)
def club_position(filename,match_day=1,season=None,all_seasons=False):
    clubs = season_unique_club(filename,all_seasons=all_seasons,season=season)
    point = [get_points(filename = filename,all_seasons=all_seasons,season=season,club=club,all_point=False,i=match_day) for club in clubs]
    goal_diff = [get_goal_diff(filename = filename,all_seasons=all_seasons,season=season,club=club,all_point=False,i=match_day) for club in clubs]
    
    league = pd.DataFrame(
        {
            'clubs':clubs,
            'point':point,
            'goal_difference':goal_diff
            })
    league.sort_values('point',inplace=True,ascending=False)
    league.reset_index(inplace=True,drop=True)
    league.index = league.index+1
    return league
@st.cache(suppress_st_warning=True)
def points_difference(filename,season=None,all_seasons=False,rank='top'):
    if season == 'All Seasons':
        all_seasons = True
    if season!='All Seasons':
        if rank == 'top':
            diff_1 = [(club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[1,'point']-club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[2,'point']) for i in range(1,39)]
            diff_2 = [(club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[2,'point']-club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[3,'point']) for i in range(1,39)]
            diff_3 = [(club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[3,'point']-club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[4,'point']) for i in range(1,39)]
            data = pd.DataFrame(
                    {
                        'Match_Day':range(1,39),
                        'Point_Difference_1st_2nd':diff_1,
                        'Point_Difference_2nd_3rd':diff_2,  
                        'Point_Difference_3rd_4th':diff_3,  
                        }
                )
        else:
            diff_1 = [(club_position(filename,match_day=i,season=season).loc[17,'point']-club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[18,'point']) for i in range(1,39)]
            diff_2 = [(club_position(filename,match_day=i,season=season).loc[18,'point']-club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[19,'point']) for i in range(1,39)]
            diff_3 = [(club_position(filename,match_day=i,season=season).loc[19,'point']-club_position(filename,match_day=i,season=season,all_seasons=all_seasons).loc[20,'point']) for i in range(1,39)]
            data = pd.DataFrame(
                    {
                        'Match_Day':range(1,39),
                        'Point_Difference_17th_18th':diff_1,   
                        'Point_Difference_18th_19th':diff_2,
                        'Point_Difference_19th_20th':diff_3
                        
                        }
                )
    else:
        n_clubs = len(league_dataframe(filename,all_seasons=True).clubs.unique())
        seasons = ['17/18','18/19','19/20','20/21','21/22']
        if rank == 'top':
            diff_1 = [(club_position(filename,season=sea,all_seasons=all_seasons).loc[1,'point']-club_position(filename,season=sea,all_seasons=all_seasons).loc[2,'point']) for sea in seasons]
            diff_2 = [(club_position(filename,season=sea,all_seasons=all_seasons).loc[2,'point']-club_position(filename,season=sea,all_seasons=all_seasons).loc[3,'point']) for sea in seasons]
            diff_3 = [(club_position(filename,season=sea,all_seasons=all_seasons).loc[3,'point']-club_position(filename,season=sea,all_seasons=all_seasons).loc[4,'point']) for sea in seasons]
            data = pd.DataFrame(
                    {
                        'Match_Day':seasons,
                        'Point_Difference_1st_2nd':diff_1,
                        'Point_Difference_2nd_3rd':diff_2,  
                        'Point_Difference_3rd_4th':diff_3,  
                        }
                )
        else:
            diff_1 = [(club_position(filename,season=sea,all_seasons=all_seasons).loc[(n_clubs-3),'point']-club_position(filename,season=sea,all_seasons=all_seasons).loc[(n_clubs-2),'point']) for sea in seasons]
            diff_2 = [(club_position(filename,season=sea,all_seasons=all_seasons).loc[(n_clubs-2),'point']-club_position(filename,season=sea,all_seasons=all_seasons).loc[(n_clubs-1),'point']) for sea in seasons]
            diff_3 = [(club_position(filename,season=sea,all_seasons=all_seasons).loc[(n_clubs-1),'point']-club_position(filename,season=sea,all_seasons=all_seasons).loc[(n_clubs),'point']) for sea in seasons]
            data = pd.DataFrame(
                    {
                        'Match_Day':seasons,
                        'Point_Difference_1st_2nd':diff_1,
                        'Point_Difference_2nd_3rd':diff_2,  
                        'Point_Difference_3rd_4th':diff_3,  
                        }
                )
        
    return data