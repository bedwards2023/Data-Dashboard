"""

Name:Brittany Edwards
Date:02/14/2024
Assignment:Module 6: Assignment: Exploratory Data Analysis
Due Date:02/18/24
About this project: This is my Data Dashboard assignment. I used a data set called "Los Angelos Crimes" from kaggle which looks at crimes in different LA areas.
I created 6 graphs based on the data and then created a Dash site to display the graphs.

Assumptions:(write any assumptions made here N/A
All work below was performed by Brittany Edwards

"""

from dash import Dash, html, dcc
import pandas as pd
import plotly.graph_objects as go
import numpy as np

#I used a data set called "Los_Angeles_Crimes" from Kaggle https://www.kaggle.com/datasets/shayalvaghasiya/los-angeles-crimes

# Load file
file = r"crimes.csv"
df = pd.read_csv(file)

# Count the number of occurrences for each crime. Fig 1
counts = df['Crm Cd Desc'].value_counts()
figure1ds = go.Figure(data=go.Bar(x=counts.index.tolist(),
                                  y=counts.values.tolist(),
                                  marker=dict(color='#8634fb')
                                  ))
figure1ds.update_layout(title='Bar chart of the types of crimes',
                        xaxis_title='Types of crimes',
                        yaxis_title='Number of types of crimes',
                        plot_bgcolor='#2f2f2f',
                        paper_bgcolor='#2f2f2f',
                        font=dict(
                            color="white"
                        )
                    )
# Violin graph for the ages of the victims, Fig 2
figure2ds = go.Figure(data=go.Violin(y=df['Vict Age'],
                                     box_visible=True,
                                     line_color='black',
                                     meanline_visible=True,
                                     fillcolor='#8634fb',
                                     opacity=0.6,
                                     x0='Vict Age',
                                     y0='Age'))
figure2ds.update_layout(title='Violin Plot of Victim Ages',
                        yaxis_zeroline=False,
                        paper_bgcolor='#2f2f2f',
                        plot_bgcolor='#2f2f2f',
                        font=dict(
                            color="white"
                        )
                        )

# Histogram for the number of crimes across the times. Fig 3
time_counts = df['TIME OCC'].value_counts().sort_index()
histogram_trace = go.Bar(x=time_counts.index, y=time_counts.values, marker=dict(color='#8634fb'))
histogram_layout = go.Layout(title='Distribution of Time',
                             xaxis=dict(title='Time'),
                             yaxis=dict(title='Frequency'),
                            paper_bgcolor='#2f2f2f',
                            plot_bgcolor='#2f2f2f',
                            font=dict(
                                color="white"
                            )
                             )
histogram_fig = go.Figure(data=[histogram_trace], layout=histogram_layout)


# Box plot for age and gender. Fig 4
#I had to replace some weird values in this column. Everything that was H,blank or - was replaced with X for unknown.
editeddf = df.replace({'Vict Sex': {'H': 'X', ' ': 'X', '-': 'X'}})
#I also removed the outliers
dropVals = np.where(editeddf['Vict Age'] > 80)
editeddf.drop(dropVals[0], inplace=True)
fig4ds = go.Figure(data=go.Box(x=editeddf['Vict Sex'], y=editeddf['Vict Age'],marker=dict(color='#8634fb')))
fig4ds.update_layout(title='Boxplot of the Victim Age by Victim Sex',
                     xaxis_title='Victim Sex',
                     yaxis_title='Victim Age',
                    paper_bgcolor='#2f2f2f',
                    plot_bgcolor='#2f2f2f',
                    font=dict(
                            color="white"
                        )
                     )

# Area and count of crimes per area. Fig 5
value_counts = df['AREA NAME'].value_counts()
figure5ds = go.Figure(data=go.Bar(x=value_counts.values,
                                  y=value_counts.index,
                                  orientation='h',marker=dict(color='#8634fb')))
figure5ds.update_layout(title='Count of Crimes per Area of LA',
                        xaxis_title='Number of Crimes',
                        yaxis_title='Areas of LA',
                        paper_bgcolor='#2f2f2f',
                        plot_bgcolor='#2f2f2f',
                        font=dict(
                            color="white"
                        )
                        )

# Bar graph for Weapon Description and the number of times it occurred. Fig 6
wepcounts = df['Weapon Desc'].value_counts()
figure6ds = go.Figure(data=go.Bar(x=wepcounts.values,
                                  y=wepcounts.index,
                                  orientation='h',marker=dict(color='#8634fb')))
figure6ds.update_layout(title='Weapon Description Counts',
                        xaxis_title='Count',
                        yaxis_title='Weapon Description',
                        paper_bgcolor='#2f2f2f',
                        plot_bgcolor='#2f2f2f',
                        font=dict(
                            color="white"
                        )
                        )



'''********************DASH PORTION*********************'''
app = Dash(__name__)

app.layout = html.Div(style={'textAlign': 'center', 'margin-left': '100px', 'margin-right': '20px'}, children=[
    html.H1(children="LA Crime Dashboard", className="hello", style={'textAlign':'center'}),

    html.Div([
        html.Div(
            children=[
                html.H2(children='Types of Crimes Occurring', style={'textAlign': 'center'}),
                dcc.Graph(id='Graph', figure=figure1ds)],
            className="box1",
            ),

        html.Div(
            children=[
                html.H2(children='Violin Graph of Ages', style={'textAlign': 'center'}),
                dcc.Graph(id='BoxPlotGraph', figure=figure2ds)],
            className="box1",),
    ]),

    html.Div(
        children=[
            html.H2(children='Histogram of what time crimes are occurring', style={'textAlign': 'center'}),
            dcc.Graph(id='HistGraph', figure=histogram_fig)],
        className="box3",),

    html.Div(
        children=[
            html.H2(children='Count of Crimes per Area of LA', style={'textAlign': 'center'}),
            dcc.Graph(id='AreaCrimeGraph', figure=figure5ds)],
        className="box4",
),
    html.Div(
        children=[
            html.H2(children='Weapon Description Counts', style={'textAlign': 'center'}),
            dcc.Graph(id='WeaponGraph', figure=figure6ds)],
        className="box5",),
    html.Div(
        children=[
            html.H2(children='Age of victims per sex', style={'textAlign': 'center'}),
            dcc.Graph(id='age graph', figure=fig4ds)],
        className="box5",)
])

if __name__ == '__main__':
    app.run_server(debug=True)