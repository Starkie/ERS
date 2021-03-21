# !/usr/bin/env python3

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import numpy as np

def visualize_as_radar_chart(emotions_dataframe):
    # Plot the radar chart.
    fig = px.line_polar(emotions_dataframe, r='r', theta='categories', line_close=True)

    fig.update_traces(fill='toself')

    pyo.plot(fig)
