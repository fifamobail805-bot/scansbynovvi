import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mplsoccer import Radar, grid
import io
import warnings

# Отключаем предупреждения
warnings.filterwarnings("ignore")

# --- НАСТРОЙКИ СТРАНИЦЫ ---
st.set_page_config(page_title="NovviGodly Radar Pro", layout="wide", page_icon="⚽")

# --- ШРИФТЫ (СИСТЕМНЫЕ) ---
# Используем Arial или Helvetica, они есть везде и выглядят профессионально
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# --- SIDEBAR: НАСТРОЙКИ ---
with st.sidebar:
    st.header("1. Детали игрока")
    player_name = st.text_input("Имя Игрока", "Bruno Fernandes")
    team_name = st.text_input("Команда", "Manchester United")
    position_name = st.text_input("Позиция / Роль", "Midfielder")
    details_text = st.text_input("Детали (Мин/Возраст)", "1,272 minutes - 26 years")

    st.divider()
    
    st.header("2. Визуал")
    
    st.subheader("🎨 Цвета")
    radar_face_color = st.color_picker("Заливка Радара", "#d0667a")
    radar_ring_color = st.color_picker("Цвет Колец", "#1d537f")
    text_name_color = st.color_picker("Цвет Имени", "#e4dded")
    text_team_color = st.color_picker("Цвет Команды", "#cc2a3f")
    
    st.subheader("📏 Размеры Шрифтов")
    name_size = st.slider("Размер Имени", 20, 60, 35)
    team_size = st.slider("Размер Команды", 15, 40, 25)
    watermark_size = st.slider("Размер Вотермарки", 20, 80, 35)

# --- ОСНОВНОЕ ОКНО ---
st.title("⚽ NovviGodly Radar Generator (p90)")
st.caption("Введите статистику p90. Low и High — это границы осей (минимум и максимум для сравнения).")

# Данные по умолчанию
default_data = [
    {"Metric": "Progressive Passing", "Value": 8.5, "Low": 0.0, "High": 10.0},
    {"Metric": "xG Shot Creation", "Value": 0.45, "Low": 0.0, "High": 0.8},
    {"Metric": "xG Ball Progression", "Value": 0.35, "Low": 0.0, "High": 0.6},
    {"Metric": "Box Receptions", "Value": 3.2, "Low": 0.0, "High": 5.0},
    {"Metric": "Shot Volume", "Value": 3.5, "Low": 0.0, "High": 4.5},
    {"Metric": "Aerial Wins", "Value": 1.1, "Low": 0.0, "High": 3.0},
    {"Metric": "Defending Impact", "Value": 2.5, "Low": 0.0, "High": 5.0},
    {"Metric": "Defending Intensity", "Value": 4.5, "Low": 0.0, "High": 8.0},
    {"Metric": "Disrupting Moves", "Value": 1.8, "Low": 0.0, "High": 3.0},
    {"Metric": "Ball Recoveries", "Value": 6.5, "Low": 0.0, "High": 10.0},
    {"Metric": "Ball Retention", "Value": 90.0, "Low": 70.0, "High": 100.0},
    {"Metric": "Link-up Play", "Value": 45.0, "Low": 20.0, "High": 60.0},
    {"Metric": "Carries & Dribbles", "Value": 55.0, "Low": 20.0, "High": 80.0},
]

df_input = pd.DataFrame(default_data)
edited_df = st.data_editor(df_input, num_rows="dynamic", use_container_width=True)

# --- ФУНКЦИЯ ОТРИСОВКИ ---
def plot_radar(df):
    params = df["Metric"].tolist()
    values = df["Value"].tolist()
    low = df["Low"].tolist()
    high = df["High"].tolist()

    radar = Radar(params, low, high,
                  round_int=[False]*len(params),
                  num_rings=4, 
                  ring_width=1, 
                  center_circle_radius=1)

    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                    title_space=0, endnote_space=0, grid_key='radar', axis=False)
    
    fig.set_facecolor('#121212')

    radar.setup_axis(ax=axs['radar'], facecolor='None')
    radar.draw_circles(ax=axs['radar'], facecolor='#28252c', edgecolor='#39353f', lw=1.5)

    radar.draw_radar(values, ax=axs['radar'],
                     kwargs_radar={'facecolor': radar_face_color, 'alpha': 0.7},
                     kwargs_rings={'facecolor': radar_ring_color, 'alpha': 0.6})

    # Подписи осей и метрик (стандартный жирный шрифт)
    radar.draw_range_labels(ax=axs['radar'], fontsize=12, color='#fcfcfc', fontweight='bold')
    radar.draw_param_labels(ax=axs['radar'], fontsize=18, color='#fcfcfc', fontweight='bold')

    # --- ТЕКСТА ---
    
    # 1. Имя
    axs['title'].text(0.01, 0.75, player_name, fontsize=name_size,
                      ha='left', va='center', color=text_name_color, fontweight='bold')
    
    # 2. Команда
    axs['title'].text(0.01, 0.20, team_name, fontsize=team_size,
                      ha='left', va='center', color=text_team_color)
    
    # 3. Заголовок справа
    axs['title'].text(0.99, 0.75, 'Statistical Radar', fontsize=25,
                      ha='right', va='center', color='#e4dded', fontweight='bold')
    
    # 4. Детали справа
    axs['title'].text(0.99, 0.20, f"{position_name}\n{details_text}", fontsize=15,
                      ha='right', va='center', color=text_team_color)

    # 5. Вотермарка (Слева внизу)
    axs['endnote'].text(0.01, 0.5, 'NovviGodly', 
                        color='#fcfcfc', fontsize=watermark_size, 
                        ha='left', va='center', weight='bold')

    # 6. Кредитс (Справа внизу)
    axs['endnote'].text(0.99, 0.5, 'Data: p90',
                        color='#fcfcfc', fontsize=26, ha='right', va='center')

    return fig

# --- ВЫВОД ---
st.divider()

# Центрирование через колонки
left_co, cent_co, last_co = st.columns([1, 2, 1])

with cent_co:
    if st.button("Generate Radar", type="primary", use_container_width=True):
        if len(edited_df) < 3:
            st.error("Минимум 3 метрики нужно для радара!")
        else:
            fig = plot_radar(edited_df)
            st.pyplot(fig)

            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', facecolor='#121212', dpi=300)
            st.download_button(
                label="Скачать HD (PNG)",
                data=buf.getvalue(),
                file_name=f"{player_name}_NovviGodly.png",
                mime="image/png",
                use_container_width=True
            )
