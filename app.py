import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mplsoccer import Radar, FontManager, grid
import io
import warnings

# Disable warnings
warnings.filterwarnings("ignore")

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NovviGodly Radar Pro", layout="wide", page_icon="⚽")

# --- FONTS (SYSTEM DEFAULT) ---
# Keeping it simple with system fonts to avoid loading errors
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial', 'Helvetica', 'DejaVu Sans']

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("1. Player Details")
    player_name = st.text_input("Player Name", "Bruno Fernandes")
    team_name = st.text_input("Team Name", "Manchester United")
    position_name = st.text_input("Position / Role", "Midfielder")
    details_text = st.text_input("Extra Details (Mins/Age)", "1,272 minutes - 26 years")

    st.divider()
    
    st.header("2. Visual Settings")
    
    st.subheader("🎨 Colors")
    radar_face_color = st.color_picker("Radar Fill Color", "#d0667a")
    radar_ring_color = st.color_picker("Inner Rings Color", "#1d537f")
    text_name_color = st.color_picker("Player Name Color", "#e4dded")
    text_team_color = st.color_picker("Team Name Color", "#cc2a3f")
    
    st.subheader("📏 Font Sizes")
    name_size = st.slider("Name Font Size", 20, 60, 35)
    team_size = st.slider("Team Font Size", 15, 40, 25)
    watermark_size = st.slider("Watermark Size", 20, 80, 35)

# --- MAIN AREA: DATA INPUT ---
st.title("⚽ NovviGodly Radar Generator (p90)")
st.markdown("Enter **per 90** statistics. **Low** and **High** define the minimum and maximum boundaries of the chart axis.")

# Default data structure
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

# --- PLOTTING LOGIC ---
def plot_radar(df):
    # Extract lists from DataFrame
    params = df["Metric"].tolist()
    values = df["Value"].tolist()
    low = df["Low"].tolist()
    high = df["High"].tolist()

    # Create Radar Object
    radar = Radar(params, low, high,
                  round_int=[False]*len(params), # Allow floats for p90
                  num_rings=4, 
                  ring_width=1, 
                  center_circle_radius=1)

    # Setup Grid
    fig, axs = grid(figheight=14, grid_height=0.915, title_height=0.06, endnote_height=0.025,
                    title_space=0, endnote_space=0, grid_key='radar', axis=False)
    
    fig.set_facecolor('#121212') # Dark background

    # Radar Axis
    radar.setup_axis(ax=axs['radar'], facecolor='None')
    
    # Inner Rings
    radar.draw_circles(ax=axs['radar'], facecolor='#28252c', edgecolor='#39353f', lw=1.5)

    # Main Radar Plot
    radar.draw_radar(values, ax=axs['radar'],
                     kwargs_radar={'facecolor': radar_face_color, 'alpha': 0.7},
                     kwargs_rings={'facecolor': radar_ring_color, 'alpha': 0.6})

    # Labels
    # Range labels (axis numbers)
    radar.draw_range_labels(ax=axs['radar'], fontsize=12, color='#fcfcfc', fontweight='bold')
    
    # Param labels (metric names)
    radar.draw_param_labels(ax=axs['radar'], fontsize=18, color='#fcfcfc', fontweight='bold')

    # --- TITLES & TEXT ---
    
    # 1. Player Name
    axs['title'].text(0.01, 0.75, player_name, fontsize=name_size,
                      ha='left', va='center', color=text_name_color, fontweight='bold')
    
    # 2. Team Name
    axs['title'].text(0.01, 0.20, team_name, fontsize=team_size,
                      ha='left', va='center', color=text_team_color)
    
    # 3. Chart Title (Right side)
    axs['title'].text(0.99, 0.75, 'Statistical Radar', fontsize=25,
                      ha='right', va='center', color='#e4dded', fontweight='bold')
    
    # 4. Details / Position (Right side)
    axs['title'].text(0.99, 0.20, f"{position_name}\n{details_text}", fontsize=15,
                      ha='right', va='center', color=text_team_color)

    # --- WATERMARK ---
    axs['endnote'].text(0.01, 0.5, 'NovviGodly', 
                        color='#fcfcfc', fontsize=watermark_size, 
                        ha='left', va='center', weight='bold')

    # --- CREDITS ---
    axs['endnote'].text(0.99, 0.5, 'Data: p90',
                        color='#fcfcfc', fontsize=26, ha='right', va='center')

    return fig

# --- RENDER ---
st.divider()

# Centering using columns
left_co, cent_co, last_co = st.columns([1, 2, 1])

with cent_co:
    if st.button("Generate Radar", type="primary", use_container_width=True):
        if len(edited_df) < 3:
            st.error("Please add at least 3 metrics to generate a radar.")
        else:
            fig = plot_radar(edited_df)
            st.pyplot(fig)

            # Download
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches='tight', facecolor='#121212', dpi=300)
            st.download_button(
                label="Download HD Image (PNG)",
                data=buf.getvalue(),
                file_name=f"{player_name}_NovviGodly_Radar.png",
                mime="image/png",
                use_container_width=True
            )
