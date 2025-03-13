# app.py
from dash import Dash
import dash_bootstrap_components as dbc
from layout import layout  # import the layout from layout.py
import callbacks         # import the callbacks module so they register

# Initialize the app with a Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # for deployment

# Set the layout from the layout.py file
app.layout = layout

# Register callbacks by calling a function from callbacks.py
# (Alternatively, if your callbacks module registers them immediately upon import, you don't need an extra function.)
callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)
