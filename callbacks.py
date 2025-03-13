# callbacks.py
import json
from dash import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load your data (or import it from another module)
df = pd.read_excel('nc_2024.xlsx')
df['Date'] = pd.to_datetime(df['Date'])
df['Month'] = df['Date'].dt.month_name()

def register_callbacks(app):
    print("Callbacks registered")
    @app.callback(
        Output('delay_bar', 'figure'),
        Output('delay_gauge', 'figure'),
        Input('hour_selection', 'value'),
        Input('facility_selection', 'value'),
        Input('date_picker_range', 'start_date'),
        Input('date_picker_range', 'end_date')
    )
    def update_content(selected_hours, selected_facility, start_date, end_date):
        print('Updating content')
        filtered = df.copy()
        if start_date and end_date:
            filtered = filtered[(filtered['Date'] >= start_date) & (filtered['Date'] <= end_date)]
        
        if selected_hours and "All" not in selected_hours:
            filtered = filtered[filtered['Hour'].isin(selected_hours)]
        
        if selected_facility != 'All':
            filtered = filtered[filtered['Facility'] == selected_facility]
        
        if filtered.empty:
            return go.Figure(), go.Figure()
        
        # Update the bar chart
        if len(selected_hours) == 1 and selected_hours[0] != 'All':
            categories = ["% On-Time Gate Departures", "% On-Time Airport Departures", "% On-Time Gate Arrivals"]
            values = [filtered[cat].iloc[0] for cat in categories]
            fig = px.bar(x=categories, y=values,
                         labels={'x': 'On-Time Performance', 'y': 'Percentage'},
                         title=f"On-Time Performance at Hour {selected_hours[0]} for {selected_facility}")
            fig.update_layout(yaxis_range=[0, 110])
        else:
            # Aggregate by facility or otherwise as needed
            if selected_facility == 'All':
                group_df = filtered.groupby('Facility')[["% On-Time Gate Departures",
                                                          "% On-Time Airport Departures",
                                                          "% On-Time Gate Arrivals"]].mean().reset_index()
            else:
                group_df = filtered[["% On-Time Gate Departures",
                                     "% On-Time Airport Departures",
                                     "% On-Time Gate Arrivals"]].mean().to_frame().T
                group_df.insert(0, "Facility", selected_facility)
            
            melt_df = group_df.melt(id_vars=['Facility'],
                                    value_vars=["% On-Time Gate Departures",
                                                "% On-Time Airport Departures",
                                                "% On-Time Gate Arrivals"],
                                    var_name="Metric",
                                    value_name="Percentage")
            fig = px.bar(melt_df, x="Facility", y="Percentage", color="Metric", barmode="group",
                         title="On-Time Performance by Facility for Selected Hours")
        
        # Update the gauge chart:
        if len(selected_hours) == 1 and selected_hours[0] != 'All':
            gauge_value = filtered["Average Taxi Out Delay"].iloc[0]
        else:
            gauge_value = filtered["Average Taxi Out Delay"].mean()
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=gauge_value,
            title={"text": "Avg. Taxi Out Delay (min)"},
            gauge={
                "axis": {"range": [0, 100]},
                "steps": [
                    {"range": [0, 50], "color": "lightgreen"},
                    {"range": [50, 75], "color": "yellow"},
                    {"range": [75, 100], "color": "red"}
                ]
            }
        ))
        return fig, gauge_fig

    @app.callback(
        Output('trend_line', 'figure'),
        Input('month_selection', 'value'),
        Input('facility_selection', 'value'),
        Input('date_picker_range', 'start_date'),
        Input('date_picker_range', 'end_date')
    )
    def update_trend_line(selected_month, selected_facility, start_date, end_date):
        filtered = df.copy()
        if start_date and end_date:
            filtered = filtered[(filtered['Date'] >= start_date) & (filtered['Date'] <= end_date)]
        
        if selected_month != 'All':
            filtered = filtered[filtered['Month'] == selected_month]
        
        if selected_facility != 'All':
            filtered = filtered[filtered['Facility'] == selected_facility]
        
        if filtered.empty:
            return go.Figure()
        
        agg_df = filtered.groupby("Hour")[["Scheduled Departures", "Scheduled Arrivals"]].sum().reset_index()
        fig = px.line(agg_df, x="Hour", y=["Scheduled Departures", "Scheduled Arrivals"],
                      labels={"value": "Flight Count", "Hour": "Hour of Day"},
                      title=f"Scheduled Departures & Arrivals by Hour for Month: {selected_month}\nAirport: {selected_facility}")
        return fig
