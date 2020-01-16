import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
import pandas as pd
import plotly.graph_objs as go

#-------------------- DATA -------------------------------

calendar_lisbon = pd.read_csv('calendar_lisbon_clean.csv')
calendar_paris = pd.read_csv('calendar_paris_clean.csv')
calendar_amsterdam = pd.read_csv('calendar_amsterdam_clean.csv')
listings_amsterdam = pd.read_csv('listings_amsterdam_clean.csv')
listings_lisbon = pd.read_csv('listings_lisbon_clean.csv')
listings_paris = pd.read_csv('listings_paris_clean.csv')

superHost = ['Yes', 'No']
roomType = ['Hotel Room', 'Shared Room', 'Private Room', 'Entire Home/Apartment']
superHostCode = [1, 0]
roomTypeCode = ['Hotel room', 'Shared room', 'Private room', 'Entire home/apt']

superHost_options = [dict(label=sh, value=shcode) for sh, shcode in zip(superHost, superHostCode)]
roomType_options = [dict(label=rt, value=rtcode) for rt, rtcode in zip(roomType, roomTypeCode)]

#---------------------------------------------------------

def kpiCheapest(city):
    if city == 'Lisbon':
        kpi_lisbon = pd.DataFrame(listings_lisbon.groupby('neighbourhood')['price'].agg(np.mean))
        kpi_lisbon = kpi_lisbon.sort_values(by=['price'], ascending=True)
        kpi_lisbon.reset_index(inplace=True)
        cheapest = kpi_lisbon.iloc[0,]['neighbourhood']
    elif city == 'Paris':
        kpi_paris = pd.DataFrame(listings_paris.groupby('neighbourhood')['price'].agg(np.mean))
        kpi_paris = kpi_paris.sort_values(by=['price'], ascending=True)
        kpi_paris.reset_index(inplace=True)
        cheapest = kpi_paris.iloc[0,]['neighbourhood']
    elif city == 'Amsterdam':
        kpi_amsterdam = pd.DataFrame(listings_amsterdam.groupby('neighbourhood')['price'].agg(np.mean))
        kpi_amsterdam = kpi_amsterdam.sort_values(by=['price'], ascending=True)
        kpi_amsterdam.reset_index(inplace=True)
        cheapest = kpi_amsterdam.iloc[0,]['neighbourhood']
    return cheapest

def kpiExpensive(city):
    if city == 'Lisbon':
        kpi_lisbon = pd.DataFrame(listings_lisbon.groupby('neighbourhood')['price'].agg(np.mean))
        kpi_lisbon = kpi_lisbon.sort_values(by=['price'], ascending=True)
        kpi_lisbon.reset_index(inplace=True)
        expensive = kpi_lisbon.iloc[-1,]['neighbourhood']
    elif city == 'Paris':
        kpi_paris = pd.DataFrame(listings_paris.groupby('neighbourhood')['price'].agg(np.mean))
        kpi_paris = kpi_paris.sort_values(by=['price'], ascending=True)
        kpi_paris.reset_index(inplace=True)
        expensive = kpi_paris.iloc[-1,]['neighbourhood']
    elif city == 'Amsterdam':
        kpi_amsterdam = pd.DataFrame(listings_amsterdam.groupby('neighbourhood')['price'].agg(np.mean))
        kpi_amsterdam = kpi_amsterdam.sort_values(by=['price'], ascending=True)
        kpi_amsterdam.reset_index(inplace=True)
        expensive = kpi_amsterdam.iloc[-1,]['neighbourhood']
    return expensive

def plots(superhost, roomtype):

    ############################################ Line Chart Lisbon ##########################################################
    avg_price_lisbon = pd.DataFrame(calendar_lisbon.groupby('month')['price'].agg(np.mean))
    avg_price_lisbon['month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    avg_price_lisbon['month_num'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    line_data_lisbon = [dict(type='scatter', x=avg_price_lisbon['month_num'], y=avg_price_lisbon['price'])]

    line_layout = dict(title=dict(text='Average Price Per Month', xanchor='center', yanchor='top', y=0.9, x=0.5,
                                  font=dict(color='rgb(255,255,255)')),
                       xaxis=dict(title='Month', showgrid=False, color='rgb(255,255,255)',
                                  tickvals=[i for i in range(1, 13)],
                                  ticktext=list(avg_price_lisbon['month'])),
                       yaxis=dict(title='Price ($)', showgrid=False, color='rgb(255,255,255)'),
                       paper_bgcolor='lightcoral', plot_bgcolor='lightcoral',
                       colorway=['rgb(255,255,255)'])

    ############################################ Bar Chart Lisbon ##########################################################

    count_listings_lisbon = pd.DataFrame(listings_lisbon.groupby('neighbourhood').count())
    count_listings_lisbon = count_listings_lisbon.sort_values(by=['id'], ascending=False)
    count_listings_lisbon.reset_index(inplace=True)
    count_listings_lisbon = count_listings_lisbon.iloc[0:15, 0:2]
    count_listings_lisbon.replace(
        {'Misericrdia': 'Misericórdia', 'So Vicente': 'São Vicente', 'Santo Antnio': 'Santo António',
         'Penha de Frana': 'Penha de França',
         'S.Maria, S.Miguel, S.Martinho, S.Pedro Penaferrim': 'Santa Maria e São Miguel',
         }, inplace=True)

    count_listings_lisbon.columns=['neighbourhood', 'id']
    data_bar_lisbon = dict(type='bar', x=count_listings_lisbon['neighbourhood'], y=count_listings_lisbon['id'])

    layout_bar = dict(title=dict(text='Number of Listings By Neighbourhood (Top 15)', xanchor='center', yanchor='top',
                                 y=0.9, x=0.5, font=dict(color='rgb(255,255,255)')), yaxis=dict(title='# Listings',
                                                                                                showgrid=False,
                                                                                                color='rgb(255,255,255)'),
                      paper_bgcolor='lightcoral', plot_bgcolor='lightcoral', colorway=['rgb(255,255,255)'],
                      xaxis=dict(showgrid=False, color='rgb(255,255,255)'))

    ############################################ Stacked Bar Chart Lisbon ########################################################
    rtype_lisbon = pd.DataFrame(listings_lisbon['room_type'].value_counts())
    rtype_lisbon.columns = ['room_count']
    rtype_lisbon['room_perc'] = round((rtype_lisbon['room_count'] / sum(rtype_lisbon['room_count'])) * 100, 1)
    rtype_lisbon = rtype_lisbon.drop('room_count', axis=1)
    rtype_lisbon = rtype_lisbon.T

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(x=rtype_lisbon['Entire home/apt'],
                             y=['Rooms'],
                             name='Apartment',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='coral',
                                         opacity=0.6,
                                         line=dict(color='coral', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_lisbon['Private room'],
                             y=['Rooms'],
                             name='Private Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='salmon',
                                         opacity=0.6,
                                         line=dict(color='salmon', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_lisbon['Hotel room'],
                             y=['Rooms'],
                             name='Hotel Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='lightcoral',
                                         opacity=0.6,
                                         line=dict(color='lightcoral', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_lisbon['Shared room'],
                             y=['Rooms'],
                             name='Shared Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='lightpink',
                                         opacity=0.6,
                                         line=dict(color='lightpink', width=4))))

    fig_bar.update_layout(title=dict(text="Percentage of Room Types", xanchor="center", yanchor="top", y=0.9, x=0.5),
                          barmode='stack',
                          height=300,
                          plot_bgcolor='whitesmoke',margin=dict(t=100,b=0,r=0,l=0))

    ############################################ Radar Lisbon ########################################################
    scores_lisbon = round(listings_lisbon.mean()[['score_clean', 'score_communication', 'score_location']], 1)
    scores_lisbon = pd.DataFrame(scores_lisbon)
    scores_lisbon = scores_lisbon.T

    rating_lisbon = round(listings_lisbon.mean()['rating'], 1)

    data_radar = [go.Scatterpolar(r=scores_lisbon.iloc[0],
                                  theta=['Clean', 'Communication', 'Location'],
                                  fill='toself',
                                  name='Total Rating: 9.2/10',
                                  hovertemplate='%{theta} Score: %{r}/10',
                                  line=dict(color='lightcoral'),
                                  hoverlabel=dict(bordercolor='white'))]

    layout_radar = go.Layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10]),
                                        bgcolor='whitesmoke'),
                             showlegend=False,margin=dict(t=25,b=50,r=25,l=25))

    lis_local_exact = listings_lisbon[listings_lisbon['is_location_exact'] == 1]

    data = go.Scattermapbox(
        lat=lis_local_exact['latitude'],
        lon=lis_local_exact['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='lightcoral',
            opacity=0.4
        ),
        name='',
        text=lis_local_exact[['name', 'room_type', 'rating', 'price']],
        hoverinfo='text',
        hovertemplate='Name: %{text[0]}<br>' + 'Type: %{text[1]}<br>' + 'Rating: %{text[2]}/10<br>' + 'Price: $%{text[3]}',
        hoverlabel=dict(bordercolor='white')
    )
    fig = go.Figure(data=data)

    x = fig.update_layout(
        title='Lisbon ',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoibWFudWVsdmllZ2FzIiwiYSI6ImNrNWVhYnU1azF3eTEza3JmZng1NnRteWQifQ.R21u1mUs94IiWfF-9F-9sA',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38.720,
                lon=-9.157

            ),
            pitch=0,
            zoom=12,
            style='light'
        ),
        margin=dict(t=25, b=50, r=25, l=25)
    )

    ############################################ Map Lisbon ########################################################
    lis_local_exact = listings_lisbon[listings_lisbon['is_location_exact'] == 1]

    data = go.Scattermapbox(
        lat=lis_local_exact['latitude'],
        lon=lis_local_exact['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='lightcoral',
            opacity=0.4
        ),
        name='',
        text=lis_local_exact[['name', 'room_type', 'rating', 'price']],
        hoverinfo='text',
        hovertemplate='Name: %{text[0]}<br>' + 'Type: %{text[1]}<br>' + 'Rating: %{text[2]}/10<br>' + 'Price: $%{text[3]}',
        hoverlabel=dict(bordercolor='white')
    )
    fig = go.Figure(data=data)

    x = fig.update_layout(
        title='Lisbon ',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoibWFudWVsdmllZ2FzIiwiYSI6ImNrNWVhYnU1azF3eTEza3JmZng1NnRteWQifQ.R21u1mUs94IiWfF-9F-9sA',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38.720,
                lon=-9.157

            ),
            pitch=0,
            zoom=12,
            style='light'
        ),
        margin=dict(t=0,b=0,r=0,l=0)
    )

    #Returns
    return go.Figure(data=line_data_lisbon, layout=line_layout), \
           go.Figure(data=data_bar_lisbon, layout=layout_bar), \
           fig_bar, \
           go.Figure(data=data_radar, layout=layout_radar), \
           fig
def plotsParis(superhost, roomtype):

    ############################################ Line Chart Paris ##########################################################
    avg_price_paris = pd.DataFrame(calendar_paris.groupby('month')['price'].agg(np.mean))
    avg_price_paris['month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    avg_price_paris['month_num'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    line_data_paris = [dict(type='scatter', x=avg_price_paris['month_num'], y=avg_price_paris['price'])]

    line_layout = dict(title=dict(text='Average Price Per Month', xanchor='center', yanchor='top', y=0.9, x=0.5,
                                  font=dict(color='rgb(255,255,255)')),
                       xaxis=dict(title='Month', showgrid=False, color='rgb(255,255,255)',
                                  tickvals=[i for i in range(1, 13)],
                                  ticktext=list(avg_price_paris['month'])),
                       yaxis=dict(title='Price ($)', showgrid=False, color='rgb(255,255,255)'),
                       paper_bgcolor='lightcoral', plot_bgcolor='lightcoral',
                       colorway=['rgb(255,255,255)'])

    ############################################ Bar Chart Paris ##########################################################

    count_listings_paris = pd.DataFrame(listings_paris.groupby('neighbourhood').count())
    count_listings_paris = count_listings_paris.sort_values(by=['id'], ascending=False)
    count_listings_paris.reset_index(inplace=True)
    count_listings_paris = count_listings_paris.iloc[0:15, 0:2]
    count_listings_paris.replace(
        {'Misericrdia': 'Misericórdia', 'So Vicente': 'São Vicente', 'Santo Antnio': 'Santo António',
         'Penha de Frana': 'Penha de França',
         'S.Maria, S.Miguel, S.Martinho, S.Pedro Penaferrim': 'Santa Maria e São Miguel',
         }, inplace=True)

    count_listings_paris.columns=['neighbourhood', 'id']
    data_bar_paris = dict(type='bar', x=count_listings_paris['neighbourhood'], y=count_listings_paris['id'])

    layout_bar = dict(title=dict(text='Number of Listings By Neighbourhood (Top 15)', xanchor='center', yanchor='top',
                                 y=0.9, x=0.5, font=dict(color='rgb(255,255,255)')), yaxis=dict(title='# Listings',
                                                                                                showgrid=False,
                                                                                                color='rgb(255,255,255)'),
                      paper_bgcolor='lightcoral', plot_bgcolor='lightcoral', colorway=['rgb(255,255,255)'],
                      xaxis=dict(showgrid=False, color='rgb(255,255,255)'))

    ############################################ Stacked Bar Chart Paris ########################################################
    rtype_paris = pd.DataFrame(listings_paris['room_type'].value_counts())
    rtype_paris.columns = ['room_count']
    rtype_paris['room_perc'] = round((rtype_paris['room_count'] / sum(rtype_paris['room_count'])) * 100, 1)
    rtype_paris = rtype_paris.drop('room_count', axis=1)
    rtype_paris = rtype_paris.T

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(x=rtype_paris['Entire home/apt'],
                             y=['Rooms'],
                             name='Apartment',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='coral',
                                         opacity=0.6,
                                         line=dict(color='coral', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_paris['Private room'],
                             y=['Rooms'],
                             name='Private Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='salmon',
                                         opacity=0.6,
                                         line=dict(color='salmon', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_paris['Hotel room'],
                             y=['Rooms'],
                             name='Hotel Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='lightcoral',
                                         opacity=0.6,
                                         line=dict(color='lightcoral', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_paris['Shared room'],
                             y=['Rooms'],
                             name='Shared Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='lightpink',
                                         opacity=0.6,
                                         line=dict(color='lightpink', width=4))))

    fig_bar.update_layout(title=dict(text="Percentage of Room Types", xanchor="center", yanchor="top", y=0.9, x=0.5),
                          barmode='stack',
                          height=300,
                          plot_bgcolor='whitesmoke',margin=dict(t=100,b=0,r=0,l=0))

    ############################################ Radar Paris ########################################################
    scores_paris = round(listings_paris.mean()[['score_clean', 'score_communication', 'score_location']], 1)
    scores_paris = pd.DataFrame(scores_paris)
    scores_paris = scores_paris.T

    rating_paris = round(listings_paris.mean()['rating'], 1)

    data_radar = [go.Scatterpolar(r=scores_paris.iloc[0],
                                  theta=['Clean', 'Communication', 'Location'],
                                  fill='toself',
                                  name='Total Rating: 9.3/10',
                                  hovertemplate='%{theta} Score: %{r}/10',
                                  line=dict(color='lightcoral'),
                                  hoverlabel=dict(bordercolor='white'))]

    layout_radar = go.Layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10]),
                                        bgcolor='whitesmoke'),
                             showlegend=False,margin=dict(t=25,b=50,r=25,l=25))

    lis_local_exact = listings_paris[listings_paris['is_location_exact'] == 1]

    data = go.Scattermapbox(
        lat=lis_local_exact['latitude'],
        lon=lis_local_exact['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='lightcoral',
            opacity=0.4
        ),
        name='',
        text=lis_local_exact[['name', 'room_type', 'rating', 'price']],
        hoverinfo='text',
        hovertemplate='Name: %{text[0]}<br>' + 'Type: %{text[1]}<br>' + 'Rating: %{text[2]}/10<br>' + 'Price: $%{text[3]}',
        hoverlabel=dict(bordercolor='white')
    )
    fig = go.Figure(data=data)

    x = fig.update_layout(
        title='Paris ',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoibWFudWVsdmllZ2FzIiwiYSI6ImNrNWVhYnU1azF3eTEza3JmZng1NnRteWQifQ.R21u1mUs94IiWfF-9F-9sA',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38.720,
                lon=-9.157

            ),
            pitch=0,
            zoom=12,
            style='light'
        ),
        margin=dict(t=25, b=50, r=25, l=25)
    )

    ############################################ Map Paris ########################################################
    lis_local_exact = listings_paris[listings_paris['is_location_exact'] == 1]

    data = go.Scattermapbox(
        lat=lis_local_exact['latitude'],
        lon=lis_local_exact['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='lightcoral',
            opacity=0.4
        ),
        name='',
        text=lis_local_exact[['name', 'room_type', 'rating', 'price']],
        hoverinfo='text',
        hovertemplate='Name: %{text[0]}<br>' + 'Type: %{text[1]}<br>' + 'Rating: %{text[2]}/10<br>' + 'Price: $%{text[3]}',
        hoverlabel=dict(bordercolor='white')
    )
    fig = go.Figure(data=data)

    x = fig.update_layout(
        title='Paris ',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoibWFudWVsdmllZ2FzIiwiYSI6ImNrNWVhYnU1azF3eTEza3JmZng1NnRteWQifQ.R21u1mUs94IiWfF-9F-9sA',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=48.857,
                lon=2.360

            ),
            pitch=0,
            zoom=12,
            style='light'
        ),
        margin=dict(t=0,b=0,r=0,l=0)
    )

    #Returns
    return go.Figure(data=line_data_paris, layout=line_layout), \
           go.Figure(data=data_bar_paris, layout=layout_bar), \
           fig_bar, \
           go.Figure(data=data_radar, layout=layout_radar), \
           fig

def plotsAms(superhost, roomtype):

    ############################################ Line Chart amsterdam ##########################################################
    avg_price_amsterdam = pd.DataFrame(calendar_amsterdam.groupby('month')['price'].agg(np.mean))
    avg_price_amsterdam['month'] = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    avg_price_amsterdam['month_num'] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    line_data_amsterdam = [dict(type='scatter', x=avg_price_amsterdam['month_num'], y=avg_price_amsterdam['price'])]

    line_layout = dict(title=dict(text='Average Price Per Month', xanchor='center', yanchor='top', y=0.9, x=0.5,
                                  font=dict(color='rgb(255,255,255)')),
                       xaxis=dict(title='Month', showgrid=False, color='rgb(255,255,255)',
                                  tickvals=[i for i in range(1, 13)],
                                  ticktext=list(avg_price_amsterdam['month'])),
                       yaxis=dict(title='Price ($)', showgrid=False, color='rgb(255,255,255)'),
                       paper_bgcolor='lightcoral', plot_bgcolor='lightcoral',
                       colorway=['rgb(255,255,255)'])

    ############################################ Bar Chart amsterdam ##########################################################

    count_listings_amsterdam = pd.DataFrame(listings_amsterdam.groupby('neighbourhood').count())
    count_listings_amsterdam = count_listings_amsterdam.sort_values(by=['id'], ascending=False)
    count_listings_amsterdam.reset_index(inplace=True)
    count_listings_amsterdam = count_listings_amsterdam.iloc[0:15, 0:2]

    count_listings_amsterdam.columns=['neighbourhood', 'id']
    data_bar_amsterdam = dict(type='bar', x=count_listings_amsterdam['neighbourhood'], y=count_listings_amsterdam['id'])

    layout_bar = dict(title=dict(text='Number of Listings By Neighbourhood (Top 15)', xanchor='center', yanchor='top',
                                 y=0.9, x=0.5, font=dict(color='rgb(255,255,255)')), yaxis=dict(title='# Listings',
                                                                                                showgrid=False,
                                                                                                color='rgb(255,255,255)'),
                      paper_bgcolor='lightcoral', plot_bgcolor='lightcoral', colorway=['rgb(255,255,255)'],
                      xaxis=dict(showgrid=False, color='rgb(255,255,255)'))

    ############################################ Stacked Bar Chart amsterdam ########################################################
    rtype_amsterdam = pd.DataFrame(listings_amsterdam['room_type'].value_counts())
    rtype_amsterdam.columns = ['room_count']
    rtype_amsterdam['room_perc'] = round((rtype_amsterdam['room_count'] / sum(rtype_amsterdam['room_count'])) * 100, 1)
    rtype_amsterdam = rtype_amsterdam.drop('room_count', axis=1)
    rtype_amsterdam = rtype_amsterdam.T

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(x=rtype_amsterdam['Entire home/apt'],
                             y=['Rooms'],
                             name='Apartment',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='coral',
                                         opacity=0.6,
                                         line=dict(color='coral', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_amsterdam['Private room'],
                             y=['Rooms'],
                             name='Private Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='salmon',
                                         opacity=0.6,
                                         line=dict(color='salmon', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_amsterdam['Hotel room'],
                             y=['Rooms'],
                             name='Hotel Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='lightcoral',
                                         opacity=0.6,
                                         line=dict(color='lightcoral', width=4))))

    fig_bar.add_trace(go.Bar(x=rtype_amsterdam['Shared room'],
                             y=['Rooms'],
                             name='Shared Room',
                             hovertemplate='Percentage: %{x}%',
                             hoverlabel=dict(bordercolor='white'),
                             orientation='h',
                             marker=dict(color='lightpink',
                                         opacity=0.6,
                                         line=dict(color='lightpink', width=4))))

    fig_bar.update_layout(title=dict(text="Percentage of Room Types", xanchor="center", yanchor="top", y=0.9, x=0.5),
                          barmode='stack',
                          height=300,
                          plot_bgcolor='whitesmoke',margin=dict(t=100,b=0,r=0,l=0))

    ############################################ Radar amsterdam ########################################################
    scores_amsterdam = round(listings_amsterdam.mean()[['score_clean', 'score_communication', 'score_location']], 1)
    scores_amsterdam = pd.DataFrame(scores_amsterdam)
    scores_amsterdam = scores_amsterdam.T

    rating_amsterdam = round(listings_amsterdam.mean()['rating'], 1)

    data_radar = [go.Scatterpolar(r=scores_amsterdam.iloc[0],
                                  theta=['Clean', 'Communication', 'Location'],
                                  fill='toself',
                                  name='Total Rating: 9.5/10',
                                  hovertemplate='%{theta} Score: %{r}/10',
                                  line=dict(color='lightcoral'),
                                  hoverlabel=dict(bordercolor='white'))]

    layout_radar = go.Layout(polar=dict(radialaxis=dict(visible=True, range=[0, 10]),
                                        bgcolor='whitesmoke'),
                             showlegend=False,margin=dict(t=25,b=50,r=25,l=25))

    lis_local_exact = listings_amsterdam[listings_amsterdam['is_location_exact'] == 1]

    data = go.Scattermapbox(
        lat=lis_local_exact['latitude'],
        lon=lis_local_exact['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=8,
            color='lightcoral',
            opacity=0.4
        ),
        name='',
        text=lis_local_exact[['name', 'room_type', 'rating', 'price']],
        hoverinfo='text',
        hovertemplate='Name: %{text[0]}<br>' + 'Type: %{text[1]}<br>' + 'Rating: %{text[2]}/10<br>' + 'Price: $%{text[3]}',
        hoverlabel=dict(bordercolor='white')
    )
    fig = go.Figure(data=data)

    x = fig.update_layout(
        title='amsterdam ',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoibWFudWVsdmllZ2FzIiwiYSI6ImNrNWVhYnU1azF3eTEza3JmZng1NnRteWQifQ.R21u1mUs94IiWfF-9F-9sA',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38.720,
                lon=-9.157

            ),
            pitch=0,
            zoom=12,
            style='light'
        ),
        margin=dict(t=25, b=50, r=25, l=25)
    )

    ############################################ Map amsterdam ########################################################
    lis_local_exact = listings_amsterdam[listings_amsterdam['is_location_exact'] == 1]

    data = go.Scattermapbox(
        lat=lis_local_exact['latitude'],
        lon=lis_local_exact['longitude'],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=10,
            color='lightcoral',
            opacity=0.4
        ),
        name='',
        text=lis_local_exact[['name', 'room_type', 'rating', 'price']],
        hoverinfo='text',
        hovertemplate='Name: %{text[0]}<br>' + 'Type: %{text[1]}<br>' + 'Rating: %{text[2]}/10<br>' + 'Price: $%{text[3]}',
        hoverlabel=dict(bordercolor='white')
    )
    fig = go.Figure(data=data)

    x = fig.update_layout(
        title='amsterdam ',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken='pk.eyJ1IjoibWFudWVsdmllZ2FzIiwiYSI6ImNrNWVhYnU1azF3eTEza3JmZng1NnRteWQifQ.R21u1mUs94IiWfF-9F-9sA',
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=52.373,
                lon=4.903

            ),
            pitch=0,
            zoom=12,
            style='light'
        ),
        margin=dict(t=0,b=0,r=0,l=0)
    )

    #Returns
    return go.Figure(data=line_data_amsterdam, layout=line_layout), \
           go.Figure(data=data_bar_amsterdam, layout=layout_bar), \
           fig_bar, \
           go.Figure(data=data_radar, layout=layout_radar), \
           fig


figs = plots('ds','sd')
figs2 = plotsParis('ds', 'sd')
figs3 = plotsAms('ds', 'sd')

tab_selected_style = {
    'borderTop': '1px solid lightcoral',
    'backgroundColor': 'lightcoral',
    'color': 'white',
}


app = dash.Dash(__name__, assets_folder='Assets')
server = app.server

app.layout = html.Div([
    dcc.Tabs(id="tabs-example", value='tablisbon', children=[
        dcc.Tab(label='Lisbon', value='tablisbon', selected_style=tab_selected_style),
        dcc.Tab(label='Paris', value='tabparis', selected_style=tab_selected_style),
        dcc.Tab(label='Amsterdam', value='tabamsterdam', selected_style=tab_selected_style),

    ]),
    html.Div(id='tabs-content-example'),
    #end tabs


])


#------------------------------------------------------------------------------------------------------
#@app.callback(
#    [
#        Output("priceVariation", "figure"),
#        Output("barChart", "figure"),
#        Output("stackedBarChart", "figure"),
#        Output("radar", "figure"),
#        Output("map", "figure")
#    ],
#    [
#        Input("superhost_drop", "value"),
#        Input("roomtype_drop", "value")
#    ]
#)
#------------------------------------------------------------------------------------------------------
#callbacks tabs
@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tabparis':
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=figs2[4], id='map')
                ], className='two-thirds big_map_container'),

                html.Div([
                    html.Img(
                        src=app.get_asset_url('logo.png'),
                        id="aibnb_image",
                        style={"height": "60px", "width": "auto", "margin-bottom": "20px", "margin-top": "20px"}
                    ),
                    html.H1("Airbnb Dashboard", style={"text-align": "center", "margin-bottom": "10px"}),
                    html.H6(
                        "Each day that goes by, travelling is easier. Low cost airlines are emerging and housing abroad is "
                        "cheaper. This created a huge boom in the tourism industry. The goal of this dashboard is to "
                        "show how a tourism related company - Airbnb - is working in cities with big flows "
                        "of tourist arrivals.", style={"margin-left": "20px", "margin-right": "20px"})
                ], className='row', style={"text-align": "center", "margin-bottom": "100px"}),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H6("Average Cheapest Neighborhood", style={"text-align": "center",
                                                                            "color": "lightcoral"}),
                            html.H4(kpiCheapest("Paris"), style={"text-align": "center"})
                        ], className='six columns'),
                        html.Div([
                            html.H6("Average Most Expensive Neighborhood", style={"text-align": "center",
                                                                                  "color": "lightcoral"}),
                            html.H4(kpiExpensive("Paris"), style={"text-align": "center"})
                        ], className='six columns'),
                    ], className='row', style={"margin-bottom": "75px"}),
                    html.Div([
                        dcc.Graph(figure=figs2[0], id='priceVariation')
                    ], className='row'),
                    html.Div([
                        html.Div([
                            html.H6("Average Dimension Rating", style={"text-align": "center"}),
                            dcc.Graph(figure=figs2[3])
                        ], className='six columns'),
                        html.Div([
                            dcc.Graph(figure=figs2[2])
                        ], className='six columns'),
                    ], className='row')
                ], className='offset one-third'),
            ], className='row'),
            html.Div([
                dcc.Graph(figure=figs2[1], id='barChart')
            ], className='row')
        ])
    elif tab == 'tablisbon':
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=figs[4], id='map')
                ], className='two-thirds big_map_container'),

                html.Div([
                    html.Img(
                        src=app.get_asset_url('logo.png'),
                        id="aibnb_image",
                        style={"height": "60px", "width": "auto", "margin-bottom": "20px", "margin-top": "20px"}
                    ),
                    html.H1("Airbnb Dashboard", style={"text-align": "center", "margin-bottom": "10px"}),
                    html.H6(
                        "Each day that goes by, travelling is easier. Low cost airlines are emerging and housing abroad is "
                        "cheaper. This created a huge boom in the tourism industry. The goal of this dashboard is to "
                        "show how a tourism related company - Airbnb - is working in cities with big flows "
                        "of tourist arrivals.", style={"margin-left": "20px", "margin-right": "20px"})
                ], className='row', style={"text-align": "center", "margin-bottom": "100px"}),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H6("Average Cheapest Neighborhood", style={"text-align": "center",
                                                                            "color": "lightcoral"}),
                            html.H4(kpiCheapest("Lisbon"), style={"text-align": "center"})
                        ], className='six columns'),
                        html.Div([
                            html.H6("Average Most Expensive Neighborhood", style={"text-align": "center",
                                                                                  "color": "lightcoral"}),
                            html.H4(kpiExpensive("Lisbon"), style={"text-align": "center"})
                        ], className='six columns'),
                    ], className='row', style={"margin-bottom": "75px"}),
                    html.Div([
                        dcc.Graph(figure=figs[0], id='priceVariation')
                    ], className='row'),
                    html.Div([
                        html.Div([
                            html.H6("Average Dimension Rating", style={"text-align": "center"}),
                            dcc.Graph(figure=figs[3])
                        ], className='six columns'),
                        html.Div([
                            dcc.Graph(figure=figs[2])
                        ], className='six columns'),
                    ], className='row')
                ], className='offset one-third'),
            ], className='row'),
            html.Div([
                dcc.Graph(figure=figs[1], id='barChart')
            ], className='row')
        ])
    elif tab == 'tabamsterdam':
        return html.Div([
            html.Div([
                html.Div([
                    dcc.Graph(figure=figs3[4], id='map')
                ], className='two-thirds big_map_container'),

                html.Div([
                    html.Img(
                        src=app.get_asset_url('logo.png'),
                        id="aibnb_image",
                        style={"height": "60px", "width": "auto", "margin-bottom": "20px", "margin-top": "20px"}
                    ),
                    html.H1("Airbnb Dashboard", style={"text-align": "center", "margin-bottom": "10px"}),
                    html.H6(
                        "Each day that goes by, travelling is easier. Low cost airlines are emerging and housing abroad is "
                        "cheaper. This created a huge boom in the tourism industry. The goal of this dashboard is to "
                        "show how a tourism related company - Airbnb - is working in cities with big flows "
                        "of tourist arrivals.", style={"margin-left": "20px", "margin-right": "20px"})
                ], className='row', style={"text-align": "center", "margin-bottom": "100px"}),

                html.Div([
                    html.Div([
                        html.Div([
                            html.H6("Average Cheapest Neighborhood", style={"text-align": "center",
                                                                            "color": "lightcoral"}),
                            html.H4(kpiCheapest("Amsterdam"), style={"text-align": "center"})
                        ], className='six columns'),
                        html.Div([
                            html.H6("Average Most Expensive Neighborhood", style={"text-align": "center",
                                                                                  "color": "lightcoral"}),
                            html.H4(kpiExpensive("Amsterdam"), style={"text-align": "center"})
                        ], className='six columns'),
                    ], className='row', style={"margin-bottom": "75px"}),
                    html.Div([
                        dcc.Graph(figure=figs3[0], id='priceVariation')
                    ], className='row'),
                    html.Div([
                        html.Div([
                            html.H6("Average Dimension Rating", style={"text-align": "center"}),
                            dcc.Graph(figure=figs3[3])
                        ], className='six columns'),
                        html.Div([
                            dcc.Graph(figure=figs3[2])
                        ], className='six columns'),
                    ], className='row')
                ], className='offset one-third'),
            ], className='row'),
            html.Div([
                dcc.Graph(figure=figs3[1], id='barChart')
            ], className='row')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
