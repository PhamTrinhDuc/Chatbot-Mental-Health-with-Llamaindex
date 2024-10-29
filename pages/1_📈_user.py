import os
import json
import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
from ui import sidebar
from configs.config import APP_CONFIG

st.set_page_config(layout="wide")

# doc du lieu tu file json
def load_scores(file: str, spesific_username: str):
    if os.path.exists(file) and os.path.getsize(file) > 0:
        with open(file, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data)
        new_df = df[df['username']] == spesific_username
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
    sidebar.show_sidebar()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if st.session_state.logged_in:
        st.markdown("# Theo dõi thông tin sức khỏe của bạn")

        df  = load_scores(file=APP_CONFIG.scores_file_path, 
                          spesific_username=st.session_state.username)

        if not df.empty:
            df['Time'] = pd.to_datetime(df['Time'])
            df['Score_num'] = df['Score'].apply(score_to_numeric)
            df['Score'] = df['Score'].str.lower()
            st.markdown("## Biểu đồ sức khỏe tinh thần 7 ngày qua của bạn")
            plot_scores(df)

        st.markdown("## Truy xuất thông tin sức khỏe tinh thần theo ngày")
        date = st.date_input("Chọn ngày", datetime.now().date())
        selected_date = pd.to_datetime(date)

        if not df.empty:
            filtered_df = [df['Time'].dt.date == selected_date.date()]
            if not filtered_df.empty:
                st.write(f"Thông tin ngày {selected_date.date()}:")
                for index, row in filtered_df.iterrows():
                    st.markdown(f"""
                    **Thời gian:** {row['Time']}  
                    **Điểm:** {row['Score']}  
                    **Nội dung:** {row['Content']}  
                    **Tổng dự đoán:** {row['Total guess']}  
                    """)
            else:
                st.write(f"Không có dữ liệu cho ngày {selected_date.date()}")
        st.markdown("## Bảng dữ liệu chi tiết")
        st.table(df)    

if __name__ == "__main__":
    main()