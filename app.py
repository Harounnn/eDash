from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px

import src.data_transformation as dt

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

data_frames = dt.DataTransformation().data_transformation()

figures = []

start_year = 1990
last_year = 2015
fig = px.pie(data_frames[0], values='Value', names='Region', hole=0.05, hover_data={'Region':False},
                             title=f'Mean Post Secandary GAR from {start_year} to {last_year}',
                             template='plotly_dark',color_discrete_sequence=px.colors.qualitative.Set3)
figures.append(fig)

fig = px.bar(data_frames[1], x='Years', y='Value', color='Gender', barmode='group',
             title='Proportion of out of school in Primary Education (Male and Female)',
             hover_data={'Gender':False,'Years':False,'Value':False},
             hover_name='Value', template='plotly_dark',color_discrete_sequence=px.colors.qualitative.Set3)

figures.append(fig)

fig = px.scatter_geo(data_frames[2], locations="Country Code", color="Region",
                     title='GAR change through the years and over the globe',
                     hover_name="Short Name", size="Value",
                     projection="natural earth",animation_frame='Epoch', template='plotly_dark',
                     color_discrete_sequence=px.colors.qualitative.Set3)

figures.append(fig)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([dcc.Graph(figure=figures[0])], width=6),
        dbc.Col([dcc.Graph(figure=figures[2])], width=6)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(figure=figures[1])])
    ])
])


if __name__ == "__main__":
    app.run_server(debug=True)