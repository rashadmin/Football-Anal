import streamlit as st
import numpy as np
from streamlit_function import league_dataframe,club_matches,club_stats
import pandas as pd
from wrangler import season_unique_club
from plots import points_bar_plot
import streamlit.components.v1 as components
st.set_page_config(layout='wide')
st.title('FOOTBALL ANALYSIS FOR THE TOP 5 LEAGUE IN EUROPE')



league_name =  st.sidebar.radio('SELECT LEAGUE', options = ['England','Spain'])
filename = league_name+'.csv'
df = pd.read_csv(filename)
analysis = st.sidebar.radio('SELECT ANALYSIS', options = ['League Analysis','Club Analysis'])

season_a = df['season'].unique()
seasons = np.append(season_a,'All Seasons')

if analysis =='League Analysis':
    col1,col2,col3 = st.columns([1,3,1])
    col_4,col_5 = st.columns(2)
    with col2:
        season = st.radio('SELECT SEASON',options=seasons,horizontal=True,index=4)
        #components.html('''<hr>''')
        if season!= 'All Seasons':
            league = league_dataframe(filename,all_seasons=False,season=season)
        else:
            league = league_dataframe(filename,all_seasons=True)
        with col_4:
            st.dataframe(league,width=700)
        with col_5:
            fig = points_bar_plot(data=league,league=league_name,season=season)
            st.plotly_chart(fig)
    
    
else:
    club_stat = st.sidebar.radio('Club Information',['Club Position','Club Matches'])
    col1,col2 = st.columns([1,4])
    #components.html('''<hr>''')
    if club_stat == 'Club Matches':
        with col2:
            season = st.radio('SELECT SEASON',options=seasons,horizontal=True,index=4)
        with col1:
            unique_teams = season_unique_club(filename,season=season)
            club =  st.radio('SELECT CLUB', options = unique_teams)
            winner = league_dataframe(filename,all_seasons=False,season=season).head(1)['clubs']
            if club == winner.values:
               st.balloons() 
        with col2:
             club_match = club_matches(filename,season=season,club=club)
             st.dataframe(club_match,width=700)
    else:
        with col1:
            unique_teams = season_unique_club(filename,all_seasons=True)
            club =  st.radio('SELECT CLUB', options = unique_teams)
        with col2:
           stats = club_stats(filename,club=club)
           no_appearance = len(stats)
           string = f"{club}'s Final League Position in the last {no_appearance} {league_name} League Season Appearance."
           st.subheader(string)
           st.dataframe(stats,width=700)
            
        #    
    