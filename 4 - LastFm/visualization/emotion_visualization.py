# !/usr/bin/env python3

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo

def visualize_as_radar_chart(emotion_by_user, emotions):
    # !: Copy the list and reverse it because plotly flips the categories.
    categories = [emo.capitalize() for emo in emotions]
    categories.reverse()

    # Plot the radar chart.
    fig = go.Figure()

    # Rotate the the axis so Joy is in the 90º position.
    fig.update_layout(
        polar = dict(
            angularaxis = dict(rotation=135, direction='counterclockwise')))

    for user in emotion_by_user:
        # !: Copy the list and reverse it because plotly flips the categories.
        user_emotions = emotion_by_user[user][::-1]

        fig.add_trace(
            go.Scatterpolar(r = user_emotions, name = user, theta = categories, fill = 'toself'))

    pyo.plot(fig)
