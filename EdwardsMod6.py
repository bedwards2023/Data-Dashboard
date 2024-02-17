"""

Name:Brittany Edwards
Date:02/14/2024
Assignment:Module 6: Assignment: Exploratory Data Analysis
Due Date:02/18/24
About this project:

Assumptions:(write any assumptions made here N/A
All work below was performed by Brittany Edwards

"""

from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import xlrd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import numpy as np
import matplotlib.ticker as ticker

#I used a data set called "Los_Angeles_Crimes" from Kaggle https://www.kaggle.com/datasets/shayalvaghasiya/los-angeles-crimes

#Load file
file = r"crimes.csv"
df = pd.read_csv(file)
#print(df.describe())


#Im counting the number of occurences for each crime. Fig 1
counts = df['Crm Cd Desc'].value_counts()

#data structure for figure1
figure1ds = {
    'x': counts.index.tolist(),
    'y': counts.values.tolist(),
    'title': 'Bar chart of the types of crimes',
    'xaxis_title': 'Types of crimes',
    'yaxis_title': 'Number of types of crimes'
}

#print(figure1ds)

typesofcrimesfig1 = px.bar(x=figure1ds['x'], y=figure1ds['y'], title=figure1ds['title'])
typesofcrimesfig1.update_layout(xaxis_title=figure1ds['xaxis_title'], yaxis_title=figure1ds['yaxis_title'])

#typesofcrimesfig1.show()

#I have a violin graph for the ages of the victims, Fig 2
#Data Structure for figure 2, violin graph
figure2ds = go.Figure(data=go.Violin(y=df['Vict Age'],
                               box_visible=True,
                               line_color='black',
                               meanline_visible=True,
                               fillcolor='lightseagreen',
                               opacity=0.6,
                               x0='Vict Age',
                               y0='Age'))
figure2ds.update_layout(yaxis_zeroline=False)

#figure2ds.show()

#I have a histogram for the number of crimes across the times. Fig 3
timecounts = df['TIME OCC'].value_counts().sort_index()

#print(timecounts)
plt.figure(figsize=(20, 6))
plt.hist(df['TIME OCC'],color='skyblue', edgecolor='black')
plt.title('Distribution of Time')
plt.xlabel('Time')
plt.ylabel('Frequency')

#DataStructure for fig 3, histogram
fig3ds = {
    'x': timecounts.index.tolist(),
    'y': timecounts.values.tolist(),
    'title': 'Distribution of Time',
    'xlabel': 'Time',
    'ylabel': 'Frequency'
}
#plt.show()


#box plot for age and gender. Fig 4. There were some funky values in this data set so I had to replace some stuff.
#If H, - , or ' ' was the victim's sex I replaced it with an X, which is suppose to be unknown.
editeddf = df.replace('H','X')
editeddf = editeddf.replace(' ','X')
editeddf = editeddf.replace('-','X')
#I also dropped some outliers to make the graph a little more readable
dropVals = np.where(editeddf['Vict Age'] > 80)
editeddf.drop(dropVals[0], inplace = True)
editeddf.boxplot(column='Vict Age', by='Vict Sex')
#plt.show()

#Data Structure for figure 4 Box Plt
fig4ds = {
    'data': editeddf,
    'column': 'Vict Age',
    'by' : 'Vict Sex',
    'title' : 'Boxplot of the Victim Age by Victim Sex',
    'xlabel' : 'Victim Sex',
    'ylabel' : 'Victim Age'
}


#Now area and count of crimes per area. Fig 5

value_counts = df['AREA NAME'].value_counts()
value_counts.plot(kind='barh')
plt.xlabel('Number of Crimes')
plt.ylabel('Areas of LA')
plt.title('Count of crimes per Area of LA')
#plt.show()

#Data Structure for figure 5 bar graph
figure5ds = {
    'x': value_counts.index.tolist(),
    'y': value_counts.values.tolist(),
    'title': 'Count of crimes per Area of LA',
    'xaxis_title': 'Number of Crimes',
    'yaxis_title': 'Areas of LA'
}


#And another bar graph for Weapon Description and the number of times it occurred. Fig6
wepcounts = df['Weapon Desc'].value_counts()
fig = plt.figure(figsize=(10, 5))
plt.barh(wepcounts.index, wepcounts, color='maroon')
plt.xlabel('Count')
plt.ylabel('Weapon Description')
plt.title('Weapon Description Counts')
plt.gca().yaxis.set_major_locator(ticker.MultipleLocator(3))
plt.tight_layout()
#plt.show()

#Figure 6 Data Structure
figure6ds = {
    'x': wepcounts.index.tolist(),
    'y': wepcounts.values.tolist(),
    'title': 'Weapon Description Counts',
    'xaxis_title': 'Count',
    'yaxis_title': 'Weapon Description'
}


app = Dash(__name__)
app.layout = html.Div([
    html.H1(children="LA Crime Dashboard", className="hello", style={
        'color': '#00361c', 'text-align': 'center'}),

    html.Div([
        html.Div(
            children=[
                html.H2(children='Violin Plot of Fares', style={'textAlign': 'center'}),
                dcc.Graph(id='Graph', figure=typesofcrimesfig1)],
            className="box1",
            style={
                'height': '100px',
                'margin-left': '10px',
                'width': '45%',
                'text-align': 'center',
                'display': 'inline-block'
            }),
        html.Div(children=[
            html.H2(children='Box Plot of Ages', style={'textAlign': 'center'}),
            dcc.Graph(id='BoxPlotGraph', figure=figure2ds)],
            className="box2",
            style={
                'height': '100px',
                'margin-left': '10px',
                'text-align': 'center',
                'width': '40%',
                'display': 'inline-block'
            })






        ])
    ])
if __name__ == '__main__':
    app.run(debug=True)