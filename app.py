from dash import Dash, html, dcc
import plotly.express as px

import src.data_transformation as dt

app = Dash(__name__)

data_frames = dt.DataTransformation().data_transformation()

figures = []

start_year = 1990
last_year = 2015
fig = px.pie(data_frames[0], values='Value', names='Region', hole=0.05, hover_data={'Region':False},
                             title=f'Mean Post Secandary GAR from {start_year} to {last_year}')
figures.append(fig)

app.layout = html.Div(children=[
    html.H1(children='TESTING'),
    dcc.Graph(figure=figures[0])])


if __name__ == "__main__":
    app.run_server(debug=True)