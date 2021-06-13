# -*- coding: utf-8 -*-
"""
@author: Gruppe03
"""

import pandas as pd
from pandas import options
import plotly.express as px  # (version 4.7.0)
import numpy as np
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from datetime import date
from dash.dependencies import Input, Output
import math

# Create the app

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

df = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv")
df.replace('', np.NaN, inplace=True)
df.replace(np.NaN, 0, inplace=True)

s_l = df["location"].values.tolist()  # Alle Einträge in Location in einer Liste
suggestions = df["location"].drop_duplicates()  # Duplikate aus der Liste löschen

df_l = df[df["location"] == "World"]
most_recent_date = df_l['date'].max()
t_d = df_l["total_deaths"].max()
t_d = math.trunc(t_d)
t_c = df_l["total_cases"].max()
t_c = math.trunc(t_c)
t_v = df_l["total_vaccinations"].max()
t_v = math.trunc(t_v)
t_f_v = df_l["people_fully_vaccinated"].max()
t_f_v = math.trunc(t_f_v)

df_map = df['date'].max()  # ergibt das höchstmögliche Datum, welches bei der Karte gewählt werden kann

# Liste erstellen mit den relevanten Daten für die Tabelle
col_list1 = ["total_cases", "total_deaths", "total_vaccinations", "location"]
df1 = pd.read_csv("https://covid.ourworldindata.org/data/owid-covid-data.csv", usecols=col_list1)
df1 = df1[df1["location"] != "World"]
df1 = df1[df1["location"] != "South America"]
df1 = df1[df1["location"] != "North America"]
df1 = df1[df1["location"] != "Asia"]
df1 = df1[df1["location"] != "Ozeania"]
df1 = df1[df1["location"] != "European Union"]
df1 = df1[df1["location"] != "Europe"]
df1 = df1[df1["location"] != "Africa"]
df1 = df1.drop_duplicates(subset=["location"], keep='last')


def abstand(number):
    return "{:,}".format(number)


card_total_cases = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Total Cases", className="card-title"),
                html.Div(children=[abstand(t_c)])
            ]
        ),
    ],
    style={
        "color": "light",
        "inverse": "True",
        "outline": "False",
        "card-title": "black",
        "width": "15rem",
        'font-family': 'system-ui',
        'font-weight': '200',
        'text-align': 'center',
        'border-color': 'black',
        'box-shadow': '10px 5px 5px grey',

    },
)

card_total_deaths = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Total Deaths", className="card-title"),
                html.Div(children=[abstand(t_d)])
            ]
        ),
    ],
    style={
        "color": "light",
        "inverse": "True",
        "outline": "False",
        "card-title": "black",
        "width": "15rem",
        'font-family': 'system-ui',
        'font-weight': '200',
        'text-align': 'center',
        'border-color': 'black',
        'box-shadow': '10px 5px 5px grey',
    },
)

card_vaccinations = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Vaccinations", className="card-title"),
                html.Div(children=[abstand(t_v)])
            ]
        ),
    ],
    style={
        "color": "light",
        "inverse": "True",
        "outline": "False",
        "card-title": "black",
        "width": "15rem",
        'font-family': 'system-ui',
        'font-weight': '200',
        'text-align': 'center',
        'border-color': 'black',
        'box-shadow': '10px 5px 5px grey',
    },
)

card_fully_vaccinated = dbc.Card(
    [dbc.CardBody(
        [
            html.H4("Fully vaccinated", className="card-title"),
            html.Div(children=[abstand(t_f_v)])
        ]
    ),
    ],
    style={
        "color": "light",
        "inverse": "True",
        "outline": "False",
        "card-title": "black",
        "width": "15rem",
        'font-family': 'system-ui',
        'font-weight': '200',
        'text-align': 'center',
        'border-color': 'black',
        'box-shadow': '10px 5px 5px grey',

    },
),

card_graph1 = dbc.Card([
    html.H6("Please choose a date", style={'font-family': 'system-ui', 'font-weight': '200', }),
    dcc.DatePickerSingle(
        id='slct_date',
        min_date_allowed=date(2020, 2, 24),
        max_date_allowed=df_map,
        initial_visible_month=df_map,
        date=df_map),

    html.Div(id='output_container', children=[]),
    dcc.Graph(id='my_corona_map', figure={}),

], style={
    'border-color': 'white',

},
),

card_table = dbc.Card([

    # Tabelle erstellen und die Columns umnennen, so dass es für den User einfacher zulesen ist

    dash_table.DataTable(
        id='table',
        columns=[{"name": "Location", "id": "location"},
                 {"name": "Total Cases", "id": "total_cases"},
                 {"name": "Total Deaths", "id": "total_deaths"},
                 {"name": "Vaccinations", "id": "total_vaccinations"}],
        css=[
            {'selector': '.previous-page, .next-page, .last-page, .first-page', 'rule': 'background-color: white',
             'height': 'auto', 'width': 'auto'}
        ],
        data=df1.to_dict('records'),
        page_size=10,
        sort_by=[],
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode='single',
        selected_rows=[],
        page_action='native',
        page_current=0,
        style_header={'backgroundColor': 'white', 'font-family': 'system-ui', 'border': '0.5px solid black'},
        style_cell={'backgroundColor': 'white', 'fontWeight': '200', 'font-family': 'system-ui',
                    'border': '0.5px solid black', 'textAlign': 'left'}
    ),

],

    style={
        'border-color': 'white',

    },
),

card_graph2 = dbc.Card([
    html.H4("New Vaccinations compared to New Cases",
            style={'text-align': 'center', 'font-family': 'system-ui', 'font-weight': '200', 'padding-top': '10px'}),

    # Dropdown-Menü für Landwahl mit Suggest-Funktion, welche auf Grunlage der vorhandenen Ländernamen Vorschläge macht

    dcc.Dropdown(id="trend_country",
                 options=[{'label': k, 'value': k} for k in list(suggestions)[1:]],
                 placeholder="Country",
                 multi=False,
                 value='Switzerland',
                 style={'text-align': 'left', 'font-family': 'system-ui', 'font-weight': '200', 'width': '10rem',
                        'padding-left': '10px'}),
    html.H6("You can choose a time period",
            style={'font-family': 'system-ui', 'font-weight': '200', 'text-align': 'left', 'padding-left': '10px'}),

    dcc.Graph(id='line_chart', figure={}),
],
    style={
        'border-color': 'black',
        'margin': '2rem',

    },
),

card_graph3 = dbc.Card([
    html.H4("Fully vaccinated",
            style={'text-align': 'center', 'font-family': 'system-ui', 'font-weight': '200', 'padding-top': '10px'}),

    # Dropdown-Menü für Landwahl mit Suggest-Funktion, welche auf Grunlage der vorhandenen Ländernamen Vorschläge macht

    dcc.Dropdown(id="vaccination_country",
                 options=[{'label': k, 'value': k} for k in list(suggestions)[1:]],
                 placeholder="Country",
                 multi=False,
                 value='Switzerland',
                 style={'text-align': 'left', 'font-family': 'system-ui', 'font-weight': '200', 'width': '10rem',
                        'padding-left': '10px'}),

    html.H6("You can choose a time period",
            style={'font-family': 'system-ui', 'font-weight': '200', 'text-align': 'left', 'padding-left': '10px'}),

    dcc.Graph(id='bar_chart', figure={}),
],
    style={
        'border-color': 'black',
        'margin': '2rem',
    },

)

app.layout = html.Div([

    # Layout mit Cards

    html.H1("Corona Dashboard",
            style={'text-align': 'center', 'font-family': 'system-ui', 'font-weight': '200', 'padding-top': '12px'}),
    html.Br(),

    dbc.Row([
        dbc.Col(card_total_cases, width=1.5),
        dbc.Col(card_total_deaths, width=1.5),
        dbc.Col(card_vaccinations, width=1.5),
        dbc.Col(card_fully_vaccinated, width=1.5), ], justify="around"),
    html.Br(),
    dbc.Row([
        dbc.Col(card_graph1, width=7),
        dbc.Col(card_table, width=4), ], justify="around"),
    html.Br(),
    dbc.Row([
        dbc.Col(card_graph2, width=6),
        dbc.Col(card_graph3, width=6), ], justify="around"),
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='my_corona_map', component_property='figure')],
    [Input(component_id='slct_date', component_property='date')])
def update_graph(option_slctd):
    print(option_slctd)
    print(type(option_slctd))

    container = '',

    dff = df.copy()
    dff = dff[dff["date"] == option_slctd]

    # Plotly Express
    fig1 = px.choropleth(
        data_frame=dff,
        locationmode='country names',
        locations='location',
        range_color=(0, 90000.0),
        scope="world",
        color='total_cases_per_million',
        hover_data=['new_cases', 'total_cases'],
        color_continuous_scale=px.colors.sequential.Burg,
        labels={'total_cases': 'total cases', 'new_cases': 'new cases', 'location': 'Country',
                'total_cases_per_million': 'Total Cases/Million'},
        template='simple_white',
    )

    fig1.update_geos(
        visible=False,
        showcountries=True, countrycolor="whitesmoke"
    )
    fig1.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="system-ui"),
        height=300,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    ),

    return container, fig1


@app.callback(
    dash.dependencies.Output("trend_country", "options"),
    [dash.dependencies.Input("trend_country", "search_value")],
    [dash.dependencies.State("trend_country", "value")])
def update_multi_options(search_value, value):
    if not search_value:
        raise PreventUpdate

    return [
        o for o in options if search_value in o["label"] or o["value"] in (value or [])
    ]


@app.callback(

    [Output(component_id='line_chart', component_property='figure')],
    [Input(component_id='trend_country', component_property='value')])
def update_line_chart(option_a):
    dff = df.copy()
    dff = dff[dff["location"] == option_a]

    fig2 = px.line(dff, x="date", y=['new_cases', 'new_vaccinations'], template='simple_white',
                   color_discrete_sequence=["#4d0000", "#DB7093"])

    fig2.update_layout(
        font_family="system-ui",
        font_color="black",
        title_font_family="system-ui",
        title_font_color="black",
        hovermode="x unified",
        legend_title_font_color="black",
    )
    fig2.update_yaxes(ticklabelposition="inside top", title=None)
    fig2.update_xaxes(
        title_font_family="system-ui",
        linewidth=3,
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return [fig2]


@app.callback(
    dash.dependencies.Output("vaccination_country", "options"),
    [dash.dependencies.Input("vaccination_country", "search_value")],
    [dash.dependencies.State("vaccination_country", "value")])
def update_options(search_value, value):
    if not search_value:
        raise PreventUpdate

    return [
        o for o in options if search_value in o["label"] or o["value"] in (value or [])
    ]


@app.callback(

    [Output(component_id='bar_chart', component_property='figure')],
    [Input(component_id='vaccination_country', component_property='value')])
def update_bar_chart(option_slctdsa):
    dff = df.copy()
    dff = dff[dff["location"] == option_slctdsa]

    # plotly Express
    fig3 = px.bar(dff, x="date", y="people_fully_vaccinated",
                  template='simple_white')

    fig3.update_layout(
        font_family="system-ui",
        font_color="black",
        title_font_family="system-ui",
        title_font_color="black",
        hovermode="x unified",
        legend_title_font_color="black",
    )
    fig3.update_traces(marker_color='#4d0000')
    fig3.update_yaxes(ticklabelposition="inside top", title=None)
    fig3.update_xaxes(
        title_font_family="system-ui",
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    return [fig3]


if __name__ == '__main__':
    app.server.run()
