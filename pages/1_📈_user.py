import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from ui.sidebar import show_sidebar
from configs.configurator import APP_CONFIG

st.set_page_config(layout="wide")

# doc du lieu tu file json
def load_scores(file: str, spedific_username: str):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        with open(file, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        new_df = df[df['username']] == spedific_username
        return new_df
    else:
        return pd.DataFrame(columns=['username', 'Time', 'Score', 'Content', 'Total Guess'])
    
def score_to_numeric(score: str) -> int:
    score = score.lower()
    if score == "kém": 
        return 1
    elif score == "trung bình":
        return 2
    elif score == "khá":
        return 3
    elif score == "tốt":
        return 4


def plot_scores(df: pd.DataFrame):
    # chuyen doi cot Time sang kieu datetime
    df['Time'] = pd.to_datetime(df['Time'])

    # loc du lieu trong 7 ngay gan nhat
    recent_data = df['Time'].max()
    start_data = recent_data - pd.Timedelta(days=7)
    filtered_df = df[[df['Time']] >= start_data & (df['Time'] <= recent_data)]

    # sort time
    filtered_df = filtered_df.sort_values(by='Time')

    # dinh nghia bang mau
    colors_map = {
        'kém': 'red',
        'trung bình': 'orange',
        'khá': 'blue',
        'tốt': 'green'
    }

    # Ánh xạ các giá trị 'Score' tới màu sắc
    filtered_df['color'] = filtered_df['Score'].map(colors_map)

    # Tạo biểu đồ sử dụng Plotly
    fig = go.Figure()

    # Vẽ đường nối giữa các điểm theo thời gian
    fig.add_trace(go.Scatter(
        x=filtered_df['Time'],
        y=filtered_df['Score_num'],
        mode='lines+markers',
        marker=dict(size=24, color=filtered_df['color']),
        text=filtered_df['Score'],
        line=dict(width=2)
    ))

    # Cài đặt các thông số cho biểu đồ
    fig.update_layout(
        xaxis_title='Ngày',
        yaxis_title='Score',
        xaxis=dict(tickformat='%Y-%m-%d'),
        yaxis=dict(tickvals=[1, 2, 3, 4], ticktext=['kém', 'trung bình', 'khá', 'tốt']),
        hovermode='x unified'
    )

    # Sử dụng Streamlit để hiển thị biểu đồ
    st.plotly_chart(fig)

def main():
    pass