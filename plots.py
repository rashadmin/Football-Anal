import plotly.express as px
import streamlit as st
@st.cache(suppress_st_warning=True)
def points_bar_plot(data,league,season,rank='top'):
    if rank == 'top':
        top_six = data.head(6)
    elif rank=='bottom':
        top_six = data.tail(6)
    
    if season == 'All Seasons':
        title=f'A Bar Plot showing the Points for the Top 6 {league} Clubs for the Last 5 seasons'
    else:
        title=f'A Bar Plot showing the Points for the Top 6 {league} Clubs for the season {season}'
    fig = px.bar(top_six,x='point',y='clubs',orientation='h',title=title)
    return fig
@st.cache(suppress_st_warning=True)
def goal_diff_bar_plot(data,league,season,rank='top'):
    if rank == 'top':
        top_six = data.sort_values('goal_difference',ascending=False).head(6)
    elif rank=='bottom':
        top_six = data.sort_values('goal_difference',ascending=True).head(6)
    if season == 'All Seasons':
        title=f'A Bar Plot showing the Goal Difference for the Top 6 {league} Clubs for the Last 5 seasons'
    else:
        title=f'A Bar Plot showing the Goal Difference for the Top 6 {league} Clubs for the season {season}'
    fig = px.bar(top_six,x='goal_difference',y='clubs',orientation='h',title=title)
    return fig
@st.cache(suppress_st_warning=True)
def club_points_bar_plot(data,league,club):
    data.sort_values('season',inplace=True)
    title=f'A Bar Plot showing the Points of {club} for the  Last 5 seasons in {league} League'
    figs = px.bar(data_frame= data,y='points',x='season',orientation='v',title=title,width=1000)
    figs.update_yaxes(range=[0,144])
    return figs
@st.cache(suppress_st_warning=True)
def club_goal_bar_plot(data,league,club):
    #data.sort_values('points',inplace=True)
    title=f'A Bar Plot showing the Goal Difference of {club} for the  Last 5 seasons in {league} League'
    figs = px.bar(data_frame= data,y='goal_difference',x='season',orientation='v',title=title,width=1000)
    #figs.update_layout(yaxis=dict(tickvals=np.arange(144)))
    return figs
@st.cache(suppress_st_warning=True)
def home_away_plot(data):
    fig = px.pie(data,names=data.index,values='points',width=600)
    return fig
@st.cache(suppress_st_warning=True)
def diff_plot(data,league,season,rank='top'):
    if rank =='top':
        title = f'A Line Plot showing the difference in point between the Top 4 team in the {league} League in {season}'
    else:
        title = f'A Line Plot showing the difference in point between the Relegation Threatened Bottom 4 team in the {league} League in {season}'
    fig = px.line(data_frame=data,x='Match_Day',y=data.columns[1:],title=title)
    return fig