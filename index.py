import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd
import math

# READING DATA
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

# CREATING DF
confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)

# UNPIVOT DF
date1 = confirmed.columns[4:]
total_confirmed = confirmed.melt(id_vars=['Province/State', 'Country/Region',
                                 'Lat', 'Long'], value_vars=date1, var_name='date', value_name='confirmed')
date2 = deaths.columns[4:]
total_deaths = deaths.melt(id_vars=['Province/State', 'Country/Region',
                           'Lat', 'Long'], value_vars=date2, var_name='date', value_name='deaths')
date3 = recovered.columns[4:]
total_recovered = recovered.melt(id_vars=['Province/State', 'Country/Region',
                                 'Lat', 'Long'], value_vars=date3, var_name='date', value_name='recovered')


# MERGIN DF
covid_data = total_confirmed.merge(right=total_deaths, how='left', on=[
                                   'Province/State', 'Country/Region', 'date', 'Lat', 'Long'])
covid_data = covid_data.merge(right=total_recovered, how='left', on=[
                              'Province/State', 'Country/Region', 'date', 'Lat', 'Long'])


# CONVERTING DATE FORMAT FROM STRING TO PD DATE FORMAT
covid_data['date'] = pd.to_datetime(covid_data['date'])

# REMOVING naN VALUES WITH 0
covid_data['recovered'] = covid_data['recovered'].fillna(0)

# CREATING COLUMN ACTIVE
covid_data['active'] = covid_data['confirmed'] - \
    covid_data['deaths'] - covid_data['recovered']


# CREATING DF WITH SUM OF CASES
covid_data_SUM = covid_data.groupby(
    ['date'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()


def recuperados():
    resultado = round(((covid_data_SUM['recovered'].iloc[-1] - covid_data_SUM['recovered'].iloc[-2]) / (
        covid_data_SUM['recovered'].iloc[-1])) * 100, 2)

    if math.isnan(resultado) == True:
        return 0
    else:
        return resultado


app = dash.Dash(__name__,)

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo.png'), id='corona-image',
                     style={'height': '60px', 'width': 'auto', 'margin-botton': '25px'})
        ], className='one-third column'),
        html.Div([
            html.Div([
                html.H3('Covid 19', style={
                        'margin-botton': '0px', 'color': 'red'}),
                html.H5('Track Covid 19 cases', style={
                        'margin-botton': '0px', 'color': 'black'})
            ])
        ], className='one-half column', id='title'),
        html.Div([
            html.H6('Last Updated: ' + str(covid_data['date'].iloc[-1].strftime('%d/%m/%y')),
                    style={'color': 'orange'})
        ], className='one-third column', id='title1')
    ], id='header', className='row flex-display', style={'margin-botton': '25px'}),
    html.Div([

        html.Div([
            html.H6(children='Global Cases',
                    style={'textAlign': 'center', 'color': 'white'}),
            html.P(f"{covid_data_SUM['confirmed'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center', 'color': 'orange', 'fontSize': '40px'}),
            html.P(
                'New: ' +
                f"{covid_data_SUM['confirmed'].iloc[-1] - covid_data_SUM['confirmed'].iloc[-2]:,.0f}" +
                ' (' + str(round(((covid_data_SUM['confirmed'].iloc[-1] - covid_data_SUM['confirmed'].iloc[-2]) / (
                    covid_data_SUM['confirmed'].iloc[-1])) * 100, 2)) + '%) ',
                style={'textAlign': 'center', 'color': 'orange', 'fontSize': '15px', 'margin-top': '-18px'})
        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Deaths',
                    style={'textAlign': 'center', 'color': 'white'}),
            html.P(f"{covid_data_SUM['deaths'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center', 'color': 'red', 'fontSize': '40px'}),
            html.P(
                'New: ' +
                f"{covid_data_SUM['deaths'].iloc[-1] - covid_data_SUM['deaths'].iloc[-2]:,.0f}" +
                ' (' + str(round(((covid_data_SUM['deaths'].iloc[-1] - covid_data_SUM['deaths'].iloc[-2]) / (
                    covid_data_SUM['deaths'].iloc[-1])) * 100, 2)) + '%) ',
                style={'textAlign': 'center', 'color': 'red', 'fontSize': '15px', 'margin-top': '-18px'})
        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Recovered',
                    style={'textAlign': 'center', 'color': 'white'}),
            html.P(f"{covid_data_SUM['recovered'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center', 'color': 'green', 'fontSize': '40px'}),
            html.P(
                'New: ' +
                f"{covid_data_SUM['recovered'].iloc[-1] - covid_data_SUM['recovered'].iloc[-2]:,.0f}" +
                ' (' + str(recuperados()) + '%) ',
                style={'textAlign': 'center', 'color': 'green', 'fontSize': '15px', 'margin-top': '-18px'})
        ], className='card_container three columns'),

        html.Div([
            html.H6(children='Global Cases',
                    style={'textAlign': 'center', 'color': 'white'}),
            html.P(f"{covid_data_SUM['active'].iloc[-1]:,.0f}",
                   style={'textAlign': 'center', 'color': 'CornflowerBlue', 'fontSize': '40px'}),
            html.P(
                'New: ' +
                f"{covid_data_SUM['active'].iloc[-1] - covid_data_SUM['active'].iloc[-2]:,.0f}" +
                ' (' + str(round(((covid_data_SUM['active'].iloc[-1] - covid_data_SUM['active'].iloc[-2]) / (
                    covid_data_SUM['active'].iloc[-1])) * 100, 2)) + '%) ',
                style={'textAlign': 'center', 'color': 'CornflowerBlue', 'fontSize': '15px', 'margin-top': '-18px'})
        ], className='card_container three columns')


    ], className='row flex display'),
    html.Div([

        html.Div([

            html.P('Select country: ', className='fix_label',
                   style={'color': 'white'}),
            dcc.Dropdown(id='w_countries', multi=False, searchable=True, value='Brazil',
                         placeholder='Select Country', options=[{'label': c, 'value': c} for c in (covid_data['Country/Region'].unique())], className='dcc_compon'),

            html.P('New cases: ' + '' + str(covid_data['date'].iloc[-1].strftime(
                '%d %B de %Y')), className='fix_label', style={'text-align': 'center', 'color': 'white'}),

            dcc.Graph(id='confirmed', config={
                      'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}
                      ),

            dcc.Graph(id='death', config={
                      'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}
                      ),

            dcc.Graph(id='recovered', config={
                      'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}
                      ),

            dcc.Graph(id='active', config={
                      'displayModeBar': False}, className='dcc_compon',
                      style={'margin-top': '20px'}
                      )

        ], className='create_container three columns'),

        html.Div([
            dcc.Graph(id='pie_chart', config={
                'displayModeBar': 'hover'}
            ),

        ], className='create_container four columns'),

        html.Div([
            dcc.Graph(id='line_chart', config={
                'displayModeBar': 'hover'}
            ),

        ], className='create_container four columns', style={'width': '35%'})

    ], className='row flex-display')
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


@app.callback(Output('confirmed', 'figure'), [Input('w_countries', 'value')])
def update_confirmed(w_countries):
    covid_data_byCountry = covid_data.groupby(
        ['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

    value_confirmed = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['confirmed'].iloc[-1] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['confirmed'].iloc[-2]

    delta_confirmed = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['confirmed'].iloc[-2] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['confirmed'].iloc[-3]

    return{'data': [go.Indicator(
        mode='number+delta',
        value=value_confirmed,
        delta={'reference': delta_confirmed, 'position': 'right',
               'valueformat': ',g', 'relative': False, 'font': {'size': 15}},
        number={'valueformat': ',', 'font': {'size': 20}},
        domain={'y': [0, 1], 'x':[0, 1]}
    )],
        'layout': go.Layout(title={'text': 'New confirmed', 'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                            height=50,
                            font=dict(color='orange'),
                            paper_bgcolor='#1f2c56',
                            plot_bgcolor='#1f2c56'
                            )
    }


@app.callback(Output('death', 'figure'), [Input('w_countries', 'value')])
def update_death(w_countries):
    covid_data_byCountry = covid_data.groupby(
        ['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

    value_death = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['deaths'].iloc[-1] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['deaths'].iloc[-2]

    delta_death = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['deaths'].iloc[-2] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['deaths'].iloc[-3]

    return{'data': [go.Indicator(
        mode='number+delta',
        value=value_death,
        delta={'reference': delta_death, 'position': 'right',
               'valueformat': ',g', 'relative': False, 'font': {'size': 15}},
        number={'valueformat': ',', 'font': {'size': 20}},
        domain={'y': [0, 1], 'x':[0, 1]}
    )],
        'layout': go.Layout(title={'text': 'New deaths', 'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                            height=50,
                            font=dict(color='red'),
                            paper_bgcolor='#1f2c56',
                            plot_bgcolor='#1f2c56'
                            )
    }


@app.callback(Output('recovered', 'figure'), [Input('w_countries', 'value')])
def update_recovered(w_countries):
    covid_data_byCountry = covid_data.groupby(
        ['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

    value_recovered = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['recovered'].iloc[-1] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['recovered'].iloc[-2]

    delta_recovered = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['recovered'].iloc[-2] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['recovered'].iloc[-3]

    return{'data': [go.Indicator(
        mode='number+delta',
        value=value_recovered,
        delta={'reference': delta_recovered, 'position': 'right',
               'valueformat': ',g', 'relative': False, 'font': {'size': 15}},
        number={'valueformat': ',', 'font': {'size': 20}},
        domain={'y': [0, 1], 'x':[0, 1]}
    )],
        'layout': go.Layout(title={'text': 'New recoveries', 'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                            height=50,
                            font=dict(color='green'),
                            paper_bgcolor='#1f2c56',
                            plot_bgcolor='#1f2c56'
                            )
    }


@app.callback(Output('active', 'figure'), [Input('w_countries', 'value')])
def update_active(w_countries):
    covid_data_byCountry = covid_data.groupby(
        ['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

    value_active = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['active'].iloc[-1] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['active'].iloc[-2]

    delta_active = covid_data_byCountry[covid_data_byCountry['Country/Region'] == w_countries]['active'].iloc[-2] - \
        covid_data_byCountry[covid_data_byCountry['Country/Region']
                             == w_countries]['active'].iloc[-3]

    return{'data': [go.Indicator(
        mode='number+delta',
        value=value_active,
        delta={'reference': delta_active, 'position': 'right',
               'valueformat': ',g', 'relative': False, 'font': {'size': 15}},
        number={'valueformat': ',', 'font': {'size': 20}},
        domain={'y': [0, 1], 'x':[0, 1]}
    )],
        'layout': go.Layout(title={'text': 'New active cases', 'y': 1, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                            height=50,
                            font=dict(color='CornflowerBlue'),
                            paper_bgcolor='#1f2c56',
                            plot_bgcolor='#1f2c56'
                            )
    }


@app.callback(Output('pie_chart', 'figure'), [Input('w_countries', 'value')])
def update_graph(w_countries):
    covid_data_byCountry = covid_data.groupby(
        ['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

    confirmed_values = covid_data_byCountry[covid_data_byCountry['Country/Region']
                                            == w_countries]['confirmed'].iloc[-1]

    deaths_values = covid_data_byCountry[covid_data_byCountry['Country/Region']
                                         == w_countries]['deaths'].iloc[-1]

    recovered_values = covid_data_byCountry[covid_data_byCountry['Country/Region']
                                            == w_countries]['recovered'].iloc[-1]

    active_values = covid_data_byCountry[covid_data_byCountry['Country/Region']
                                         == w_countries]['active'].iloc[-1]

    colors = ['orange', 'red', 'green', 'CornflowerBlue']

    return{'data': [go.Pie(labels=['Confirmed', 'Deaths', 'Recovered', 'Active'],
                           values=[confirmed_values, deaths_values,
                                   recovered_values, active_values],
                           marker=dict(colors=colors),
                           hoverinfo='label+value+percent',
                           textinfo='label+value',
                           rotation=45
                           )],
           'layout': go.Layout(title={'text': 'Total cases in ' + (w_countries), 'y': 0.93, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                               titlefont={'color': 'white', 'size': 20},
                               font=dict(family='sans-serif',
                                         color='white', size=12),
                               paper_bgcolor='#1f2c56',
                               plot_bgcolor='#1f2c56',
                               hovermode='closest',
                               legend={
                                   'orientation': 'h', 'bgcolor': '#1f2c56', 'xanchor': 'center', 'x': 0.5, 'y': -0.7}
                               )
           }


@app.callback(Output('line_chart', 'figure'), [Input('w_countries', 'value')])
def update_graph(w_countries):
    covid_data_byCountry = covid_data.groupby(
        ['date', 'Country/Region'])[['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()

    daily_confirmed = covid_data_byCountry[covid_data_byCountry['Country/Region']
                                           == w_countries][['Country/Region', 'date', 'confirmed']].reset_index()

    daily_confirmed['daily confirmed'] = daily_confirmed['confirmed'] - \
        daily_confirmed['confirmed'].shift(1)

    daily_confirmed['rolling average'] = daily_confirmed['daily confirmed'].rolling(
        window=7).mean()

    colors = ['orange', 'red', 'green', 'CornflowerBlue']

    return{'data': [go.Bar(x=daily_confirmed['date'].tail(30),
                           y=daily_confirmed['daily confirmed'].tail(30),
                           name='Daily confirmed cases',
                           marker=dict(color='orange'),
                           hoverinfo='text',
                           hovertext='<b>Date</b>: ' + daily_confirmed['date'].tail(30).astype(str) + '</br>' +
                           '<b>Daily confirmed cases</b>: ' + [f'{x:,.0f}' for x in daily_confirmed['daily confirmed'].tail(30)] + ' </br >' +
                           '<b>Country</b>: ' +
                           daily_confirmed['Country/Region'].tail(
                               30).astype(str) + '<br>'
                           ),

                    go.Scatter(x=daily_confirmed['date'].tail(30),
                               y=daily_confirmed['rolling average'].tail(30),
                               mode='lines',
                               name='Rolling average',
                               marker=dict(color='CornflowerBlue'),
                               hoverinfo='text',
                               hovertext=[
                                   f'{x:,.0f}' for x in daily_confirmed['rolling average'].tail(30)]
                               )],
           'layout': go.Layout(title={'text': 'Last 30 days in ' + (w_countries), 'y': 0.93, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                               titlefont={'color': 'white', 'size': 20},
                               font=dict(family='sans-serif',
                                         color='white', size=12),
                               paper_bgcolor='#1f2c56',
                               plot_bgcolor='#1f2c56',
                               hovermode='closest',
                               legend={'orientation': 'h', 'bgcolor': '#1f2c56',
                                       'xanchor': 'center', 'x': 0.5, 'y': -0.7},
                               margin=dict(r=0, l=55),
                               xaxis=dict(title='<b>Date</b>',
                                          color='white',
                                          showline=True,
                                          showgrid=True,
                                          showticklabels=True,
                                          linecolor='white',
                                          linewidth=1,
                                          ticks='outside',
                                          tickfont=dict(family='Arial', color='white', size=12)),
                               yaxis=dict(title='<b>Daily cases</b>',
                                          color='white',
                                          showline=True,
                                          showgrid=True,
                                          showticklabels=True,
                                          linecolor='white',
                                          linewidth=1,
                                          ticks='outside',
                                          tickfont=dict(family='Arial', color='white', size=12))
                               )
           }


if __name__ == '__main__':
    app.run_server(debug=True)
