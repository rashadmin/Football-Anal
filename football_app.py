import streamlit as st
import numpy as np
from streamlit_function import league_dataframe,club_matches,club_stats,away_home,club_position,points_difference
import pandas as pd
from wrangler import season_unique_club
from plots import club_points_bar_plot,club_goal_bar_plot,home_away_plot,diff_plot
st.set_page_config(layout='wide')
st.title('FOOTBALL ANALYSIS FOR THE TOP 5 LEAGUE IN EUROPE')

league_name =  st.sidebar.radio('SELECT LEAGUE', options = ['England','Spain'])
filename = 'data/'+league_name+'.csv'
df = pd.read_csv(filename)
analysis = st.sidebar.radio('SELECT ANALYSIS', options = ['League Analysis','Club Analysis'])

season_a = df['season'].unique()
seasons = np.append(season_a,'All Seasons')

if analysis =='League Analysis':
    col1,col2,col3 = st.columns([1,3,1])
    col_4,col_5,col_mid,col_6,col_7 = st.columns([1,45,1,45,8])
    col_8,col_9=st.columns(2)
    with col2:
        st.write('SELECT SEASON')
        season = st.radio('',options=seasons,horizontal=True,index=4,label_visibility='collapsed')
        #components.html('''<hr>''')
    if season!= 'All Seasons':
        league = league_dataframe(filename,all_seasons=False,season=season)
    else:
        league = league_dataframe(filename,all_seasons=True)
    with col_5:
        #components.html('''<br>''')
        st.title('')
        st.header('')
        st.subheader(f'{league_name} League table for {season} Season')
        st.dataframe(league,width=700,height=700)
    with col_6:
        st.header('')
        rank =st.radio('Select Top or Bottom 6',['top','bottom'],key='goal',horizontal=True)
    with col_6:
        data = points_difference(filename,season,all_seasons=False,rank=rank)
        fig = diff_plot(data,rank=rank,league=league_name,season=season)
        st.plotly_chart(fig)
    
    if season != 'All Seasons':
        with col_6:
            match_day = st.slider('Slide to Get League Table for each Matchday',min_value=1,max_value=38,value=1)
            st.subheader(f'{league_name} League Table as at Matchday {match_day}')
            match = club_position(filename,match_day=match_day,season=season)
    else:
        with col_6:
            season_year = st.select_slider('Select Matchday',options=season_a,value=season_a[0])
            st.subheader(f'{league_name} League Table as at {season_year} Season')
            match = club_position(filename,season=season_year,all_seasons=True)
    with col_6:
        st.dataframe(match,width=800)
        
        
        
        
    
    
       
    
else:
    club_stat = st.sidebar.radio('Club Information',['Club Position','Club Matches'])
    col0,col9,col8 = st.columns([2,6,2])
    col1,col2,col3,col4,col5 = st.columns([15,45,1,25,25])
    col_1,col_2 = st.columns([15,65])
    #components.html('''<hr>''')
    
        
    if club_stat == 'Club Matches':
        with col9:
            season = st.radio('SELECT SEASON',options=seasons,horizontal=True,index=4)
        with col1:
            unique_teams = season_unique_club(filename,season=season)
            club =  st.radio('SELECT CLUB', options = unique_teams)
            winner = league_dataframe(filename,all_seasons=False,season=season).head(1)['clubs']
            if (club == winner.values) & (season!='All Seasons'):
               st.balloons() 
        with col2:
             club_match = club_matches(filename,season=season,club=club)
             st.dataframe(club_match,width=900,height=700)
        with col2:
            home,away = away_home(filename, club,season=season)
        with col4:
            fig = home_away_plot(home)
            st.plotly_chart(fig)
        with col4:
            fig = home_away_plot(away)
            st.plotly_chart(fig)
    else:
        with col_1:
            unique_teams = season_unique_club(filename,all_seasons=True)
            club =  st.radio('SELECT CLUB', options = unique_teams)
        with col_2:
           df_plot = st.radio('SELECT',['DataFrame','Plot'],horizontal=True)
           stats = club_stats(filename,club=club)
           if df_plot=='DataFrame':
               no_appearance = len(stats)
               string = f"{club}'s Final League Position in the last {no_appearance} {league_name} League Season Appearance."
               st.subheader(string)
               st.dataframe(stats,width=1000)
               
           elif df_plot == 'Plot':
               with col_2:
                    point_figs = club_points_bar_plot(stats, league=league_name, club=club)
                    goal_figs = club_goal_bar_plot(stats, league=league_name, club=club)
                    st.plotly_chart(point_figs)
               with col_2:
                    st.plotly_chart(goal_figs)
    