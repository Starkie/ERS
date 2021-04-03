# !/usr/bin/env python3

import plotly.express as px
import plotly.graph_objects as go
import plotly.offline as pyo
import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.manifold import MDS

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

    # Change the type of the 'date' column from string to datetime to be able to sort it correctly.
    df.index.names = ['Date']
    df.index = pd.to_datetime(df.index, dayfirst = True)

    df = df.sort_index(axis='index', ascending=True)

    chart = px.line(df)

    chart.update_traces(mode='markers+lines')
    chart.update_layout(title_text = f'{username} daily emotions.')

    return chart

def visualize_as_proximity_matrix(emotion_by_user, emotions):
    chart = _create_proximity_matrix_chart(emotion_by_user, emotions)

    pyo.plot(chart)

def _create_proximity_matrix_chart(emotion_by_user, emotions):
    user_total_emo = {}

    for user in emotion_by_user:
        user_total_emo[user] = emotion_by_user[user]['total']

    df = pd.DataFrame.from_dict(user_total_emo, orient='index', columns=emotions)

    cosine_distances = 1 - cosine_similarity(df)

    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1)
    proximity_matrix = mds.fit_transform(cosine_distances)

    xs, ys = proximity_matrix[:, 0], proximity_matrix[:, 1]

    x_dist = []
    y_dist = []
    names = []

    for x, y, name in zip(xs, ys, emotion_by_user):
        x_dist.append(x)
        y_dist.append(y)
        names.append(name)

    chart = px.scatter(x= x_dist, y= y_dist, color=names, text=names)
    chart.update_layout(title_text = f'Users proximity matrix')
    chart.update_traces(textposition='top center')

    return chart
