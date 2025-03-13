# layout.py
import dash_bootstrap_components as dbc
from dash import dcc, html
import pandas as pd

df = pd.read_excel('nc_2024.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()

# Define the desired calendar order for months.
month_order = ["January", "February", "March", "April", "May", "June", 
               "July", "August", "September", "October", "November", "December"]
# Keep only the months present in the data, in calendar order.
unique_months = [m for m in month_order if m in df['Month'].dropna().unique()]

# Create dropdown options for hour and month; add an "All Hours" option.
hour_options = [{'label': 'All Hours', 'value': 'All'}] + [
    {'label': str(hr), 'value': hr} for hr in sorted(df['Hour'].dropna().unique())
]
month_options = [{'label': 'All Months', 'value': 'All'}] + [
    {'label': month, 'value': month} for month in unique_months
]

# Create RadioItems options for the facilities using the 'Facility' column; include "All Facilities"
facility_options = df['Facility'].dropna().unique()
facility_radio_options = [{'label': 'All Facilities', 'value': 'All'}] + [
    {'label': str(facility), 'value': facility} for facility in sorted(facility_options)
]

# Determine default start and end dates from the data
default_start_date = df['Date'].min().date().isoformat()
default_end_date = df['Date'].max().date().isoformat()

# You might also import markdown text or define other constants here.
md = """
# Raleigh-Durham and Charlotte Douglas International Airports Performance Dashboard
"""

layout = dbc.Container([
    # Header row
    dbc.Row([
        dbc.Col(
            dcc.Markdown(md, id='md_text',
                         style={'font': '15px Arial, sans-serif', 'color': 'black', 'font-weight': '500'}),
            width=12
        )
    ], className="mb-3"),
    # Static Instructions Section
    dbc.Row([
        dbc.Col(
            dcc.Markdown(
                """
                ### Dashboard Instructions
                This dashboard allows you to explore the on-time performance of Raleigh-Durham and Charlotte Douglas International Airports. This dashboard is intended for assisting aviation executives with planning new flights selected for North Carolina's largest airports!
                
                You can filter the data by hour, month, date range, and facility. Here's how you can use the filters:
                
                1. **Select Hour(s):** Choose one or multiple hours from the dropdown. Selecting "All Hours" will display data for all hours.
                2. **Select Month:** Pick the month you want to analyze from the dropdown. Selecting "All Months" will not filter by month. If you want to select multiple months (not all), select the date range below.
                3. **Select Date Range:** Use the date picker to specify the start and end dates.
                4. **Select a Facility:** Use the radio buttons to filter by a specific facility or view data for all facilities.
                
                **The charts below will update based on your selections.**
                """,
                id='instructions_static',
                style={'fontSize': '14px', 'color': 'black'}
            ),
            width=12
        )
    ], className="mb-4"),
    
    # Dropdown row for hour selection (multi-select enabled)
    dbc.Row([
        dbc.Col(html.Label('Select Hour(s)',
                           style={'font': '15px Arial, sans-serif', 'color': 'black', 'font-weight': 'bold'}),
                md=3),
        dbc.Col(
            dcc.Dropdown(
                id='hour_selection',
                options=hour_options,
                value='All',
                multi=True
            ),
            md=9
        )
    ], className="mb-4"),
    
    # Dropdown row for month selection
    dbc.Row([
        dbc.Col(html.Label('Select a Month',
                           style={'font': '15px Arial, sans-serif', 'color': 'black', 'font-weight': 'bold'}),
                md=3),
        dbc.Col(
            dcc.Dropdown(
                id='month_selection',
                options=month_options,
                value='All'
            ),
            md=9
        )
    ], className="mb-4"),
    
    # DatePickerRange row for date selection
    dbc.Row([
        dbc.Col(html.Label('Select Date Range',
                           style={'font': '15px Arial, sans-serif', 'color': 'black', 'font-weight': 'bold'}),
                md=3),
        dbc.Col(
            dcc.DatePickerRange(
                id='date_picker_range',
                start_date=default_start_date,
                end_date=default_end_date,
                min_date_allowed=default_start_date,
                max_date_allowed=default_end_date,
                display_format='YYYY-MM-DD'
            ),
            md=9
        )
    ], className="mb-4"),
    
    # RadioItems row for facility selection
    dbc.Row([
        dbc.Col(html.Label('Select a Facility',
                           style={'font': '15px Arial, sans-serif', 'color': 'black', 'font-weight': 'bold'}),
                md=3),
        dbc.Col(
            dcc.RadioItems(
                id='facility_selection',
                options=facility_radio_options,
                value='All',
                labelStyle={'display': 'inline-block', 'margin-right': '10px', 'color': 'black'}
            ),
            md=9
        )
    ], className="mb-4"),
    
    # Row 1: Bar chart (full width)
    dbc.Row([
        dbc.Col(dcc.Graph(id='delay_bar'), width=12)
    ], className="mb-4"),
    
    # Row 2: Gauge chart and Trend line chart side by side
    dbc.Row([
        dbc.Col(dcc.Graph(id='delay_gauge'), md=6),
        dbc.Col(dcc.Graph(id='trend_line'), md=6)
    ], className="mb-4"),
    
], fluid=True, style={'backgroundColor': '#003865', 'padding': '20px'})
