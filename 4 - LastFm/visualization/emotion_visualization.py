# !/usr/bin/env python3

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import pandas as pd

def visualize_as_radar_chart(emotion_by_user, emotions):
    chart = _create_radar_chart(emotion_by_user, emotions)

    pyo.plot(chart)

def _create_radar_chart(emotion_by_user, emotions):
    # !: Copy the list and reverse it because plotly flips the categories.
    categories = [emo.capitalize() for emo in emotions]
    categories.reverse()

    # Plot the radar chart.
    fig = go.Figure()

    # Rotate the the axis so Joy is in the 90º position.
    fig.update_layout(
        title_text = 'User emotions spectrum',
        polar = dict(
            angularaxis = dict(rotation=135, direction='counterclockwise')))

    for user in emotion_by_user:
        # !: Copy the list and reverse it because plotly flips the categories.
        user_emotions = emotion_by_user[user]['total'][::-1]

        fig.add_trace(
            go.Scatterpolar(r = user_emotions, name = user, theta = categories, fill = 'toself'))

    return fig

def visualize_as_time_series(username, user_emotions, emotions):
    chart = _create_time_series_chart(username, user_emotions, emotions)

    pyo.plot(chart)

def _create_time_series_chart(username, user_emotions, emotions):
    df = pd.DataFrame.from_dict(user_emotions['days'], orient='index', columns=emotions)
    df = df.sort_index(axis='index', ascending=True)

    chart = px.line(df)

    chart.update_layout(title_text = f'{username} daily emotions.')

    return chart
