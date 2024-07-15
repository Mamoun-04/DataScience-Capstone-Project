# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
file_path = '/Users/maamounmraish/Downloads/spacex_launch_dash.csv'
spacex_df = pd.read_csv(file_path)
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# Calculate min and max payload values from your data

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                                {"label": "All", "value": "ALL"},
                                                {"label": "CCAFS LC-40", "value": 'CCAFS LC-40'},
                                                {"label": "VAFB SLC-4E", "value": 'VAFB SLC-4E'},
                                                {"label": "KSC LC-39A", "value": "KSC LC-39A"},
                                                {"label": "CCAFS SLC-40", "value": "CCAFS SLC-40"}
                                             ],
                                             value='ALL',
                                             placeholder="Select A Launch Site Here:",
                                             searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=500,
                                                marks={0: '0', 1000: '1000',2000:'2000',3000:'3000',4000:'4000',5000:'5000',
                                                       6000:'6000',7000:'7000',8000:'8000',9000:'9000',10000:'10000',},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Connect the Plotly graphs with Dash Components
# Callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    [Input('site-dropdown', 'value')]
)
def update_pie_chart(entered_site):
    spacex_df_copy = spacex_df.copy()
    
    if entered_site == 'ALL':
        # Calculate success counts by launch site
        success_counts = spacex_df_copy[spacex_df_copy['class'] == 1].groupby('Launch Site').size()
        
        # Calculate total launches by launch site
        launch_counts = spacex_df_copy.groupby('Launch Site').size()
        
        # Calculate success percentage for each launch site
        success_percentage = (success_counts / launch_counts) * 100
        
        # Create a pie chart using Plotly Express with explicit colors
        fig = px.pie(values=success_percentage, names=success_percentage.index, title='Success Percentage by Launch Site')
    else:
        # Filter data for the selected launch site
        filtered_df = spacex_df_copy[spacex_df_copy['Launch Site'] == entered_site]
        
        # Calculate success and failure counts for the selected launch site
        success_counts = filtered_df[filtered_df['class'] == 1].shape[0]
        failure_counts = filtered_df[filtered_df['class'] == 0].shape[0]
        
        # Create pie chart with explicit color mapping
        fig = px.pie(values=[success_counts, failure_counts], names=['Success', 'Failure'],
                     title=f'Launch Outcome for {entered_site}', 
                     color_discrete_map={'Success': 'green', 'Failure': 'red'})
    return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [Input('site-dropdown', 'value'), Input('payload-slider', 'value')]
)
def update_scatter_chart(entered_site, payload_range):
    spacex_df_copy = spacex_df.copy()
    
    # Filter data based on selected site
    if entered_site != 'ALL':
        spacex_df_copy = spacex_df_copy[spacex_df_copy['Launch Site'] == entered_site]
    
    # Filter data based on payload range
    min_payload, max_payload = payload_range
    spacex_df_copy = spacex_df_copy[(spacex_df_copy['Payload Mass (kg)'] >= min_payload) & 
                                    (spacex_df_copy['Payload Mass (kg)'] <= max_payload)]
    
    # Create scatter plot
    fig = px.scatter(spacex_df_copy, x='Payload Mass (kg)', y='class', color='Booster Version Category', 
                     title='Payload vs. Launch Success by Booster Version Category')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()