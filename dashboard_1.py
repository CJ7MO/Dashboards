import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc

# cargando los datos en un dataframe
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/airline_data.csv',
                   encoding='ISO-8859-1',
                   dtype={'Div1Airport': str, 'Div1TailNum': str,
                          'Div2Airport': str, 'Div2TailNum': str})

# Escogiendo 500 filas de datos al azar
df = data.sample(n=500, random_state=42)

# Creando un grafico de Pie
fig = px.pie(df, values='Flights', names='DistanceGroup', title='Distance Group Proportion by flights')

# aplicacion dash
app = dash.Dash(__name__)

# haciendo el diseño de la aplicacion y ajustandolo
# creando una division usando html.div y agregandole titulo con html.h1 una decripcion con html.P y un componente gráfico
app.layout = html.Div(children=[html.H1('Airline Dashboard', style={'textAlign': 'center', 'color': '%503d36', 'font-size': 77}),
                                html.P('Proportion of distance group (250 mile distance interval group) by flights.',
                                       style={'textAlign': 'center', 'color': '#F57241'}),
                                dcc.Graph(figure=fig)])

# ejecutando la aplicación
if __name__ == '__main__':
    app.run_server()
