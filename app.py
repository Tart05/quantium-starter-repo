import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc

app = Dash(__name__)

df0 = pd.read_csv('quantium-starter-repo/data/daily_sales_data_0.csv')
df1 = pd.read_csv('quantium-starter-repo/data/daily_sales_data_1.csv')
df2 = pd.read_csv('quantium-starter-repo/data/daily_sales_data_2.csv')

df = pd.concat([df0, df1, df2])

df = df[df['product'].str.lower() == 'pink morsel']

df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)

df['sales'] = df['price'] * df['quantity']

df['date'] = pd.to_datetime(df['date'])
df = df.sort_values(by="date")


df_daily = df.groupby('date')['sales'].sum().reset_index()

fig = px.line(
    df_daily, 
    x="date", 
    y="sales", 
    title="Daily Pink Morsel Sales",
    labels={'sales': 'Total Sales ($)', 'date': 'Date'}
)

fig.update_traces(line_color='#ef553b')

app.layout = html.Div(style={
    'backgroundColor': '#111111', # Dark background
    'color': '#7FDBFF',           # Light blue text
    'padding': '40px'
}, children=[
    html.H1(
        children='Pink Morsel Visualisation',
        style={'textAlign': 'center', 'color': '#FFFFFF'}
    ),

    dcc.Graph(
        id='sales-graph',
        figure=fig.update_layout(
            plot_bgcolor='#111111',
            paper_bgcolor='#111111',
            font_color='#FFFFFF'
        )
    )
])

if __name__ == '__main__':
    app.run(debug=True)