import plotly.express as px


def points_bar_plot(data,league,season):
    top_six = data.head(6)
    if season == 'All Seasons':
        title=f'A Bar Plot showing the Top 6 {league} Clubs for the Last 5 seasons'
    else:
        title=f'A Bar Plot showing the Top 6 {league} Clubs for the season {season}'
    fig = px.bar(top_six,x='point',y='clubs',orientation='h',title=title)
    return fig