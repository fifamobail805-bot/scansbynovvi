import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from mplsoccer import Radar, FontManager, grid
import io

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="NovviGodly Radar Pro", layout="wide", page_icon="⚽")

# --- FONTS LOADING ---
try:
    robotto_thin = FontManager('https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Thin.ttf?raw=true')
    robotto_reg = FontManager('https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Regular.ttf?raw=true')
    robotto_bold = FontManager('https://github.com/googlefonts/roboto/blob/main/src/hinted/Roboto-Bold.ttf?raw=true')
except:
    st.error("Error loading fonts. Using default system fonts.")
    robotto_thin = robotto_reg = robotto_bold = None

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("1. Player Details")
    player_name = st.text_input("Player Name", "Bruno Fernandes")
    team_name = st.text_input("Team Name", "Manchester United")
    position_name = st.text_input("Position / Role", "Midfielder")
    details_text = st.text_input("Extra Details (Mins/Age)", "1,272 minutes - 26 years")

    st.divider()
    
    st.header("2. Visual Customization")
    
    st.subheader("🎨 Colors")
    # Color pickers
    radar_face_color = st.color_picker("Radar Fill Color", "#d0667a")
    radar_ring_color = st.color_picker("Inner Rings Color", "#1d537f")
    text_name_color = st.color_picker("Player Name Color", "#e4dded")
    text_team_color = st.color_picker("Team Name Color", "#cc2a3f")
    
    st.subheader("📏 Font Sizes")
    name_size = st.slider("Player Name Size", 20, 60, 35)
    team_size = st.slider("Team Name Size", 15, 40, 25)
    watermark_size = st.slider("Watermark Size", 20, 80, 50)

# --- MAIN AREA: DATA INPUT ---
st.title("⚽ NovviGodly Radar Generator (p90)")
st.markdown("Enter per 90 stats. **Low** and **High** define the boundaries of the chart axis.")

# Default data structure for p90 functionality
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
    # grid_height adjusted slightly to fit larger text if needed
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
    radar.draw_range_labels(ax=axs['radar'], fontsize=12, color='#fcfcfc',
                            fontproperties=robotto_thin.prop if robotto_thin else None)
    
    # Param labels (metric names)
    radar.draw_param_labels(ax=axs['radar'], fontsize=18, color='#fcfcfc',
                            fontproperties=robotto_reg.prop if robotto_reg else None)

    # --- TITLES & TEXT ---
    
    # 1. Player Name (Large, Variable Color)
    axs['title'].text(0.01, 0.65, player_name, fontsize=name_size,
                      fontproperties=robotto_bold.prop if robotto_bold else None,
                      ha='left', va='center', color=text_name_color)
    
    # 2. Team Name (Variable Size & Color)
    axs['title'].text(0.01, 0.25, team_name, fontsize=team_size,
                      fontproperties=robotto_thin.prop if robotto_thin else None,
                      ha='left', va='center', color=text_team_color)
    
    # 3. Chart Title (Right side)
    axs['title'].text(0.99, 0.65, 'Statistical Radar', fontsize=25,
                      fontproperties=robotto_bold.prop if robotto_bold else None,
                      ha='right', va='center', color='#e4dded')
    
    # 4. Details / Position (Right side)
    axs['title'].text(0.99, 0.25, f"{position_name}\n{details_text}", fontsize=15,
                      fontproperties=robotto_thin.prop if robotto_thin else None,
                      ha='right', va='center', color=text_team_color)

    # --- WATERMARK (NovviGodly) ---
    # Using 'title' axis coordinates to place it bottom-left prominently OR 'endnote' axis
    # Placing it big in the bottom left corner similar to "The Athletic" branding
    
    # We use axs['endnote'] for the footer area
    axs['endnote'].text(0.01, 0.5, 'NovviGodly', 
                        color='#fcfcfc', fontproperties=robotto_bold.prop if robotto_bold else None,
                        fontsize=watermark_size, ha='left', va='center', weight='bold')

    # Credits (Small, right side)
    axs['endnote'].text(0.99, 0.5, 'Data: p90 | Visual: Matches StatsBomb/Athletic style',
                        color='#fcfcfc', fontproperties=robotto_thin.prop if robotto_thin else None,
                        fontsize=12, ha='right', va='center')

    return fig

# --- RENDER ---
if st.button("Generate Radar", type="primary"):
    if len(edited_df) < 3:
        st.error("Please add at least 3 metrics to generate a radar.")
    else:
        fig = plot_radar(edited_df)
        st.pyplot(fig)

        # Download
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches='tight', facecolor='#121212', dpi=300)
        st.download_button(
            label="Download High-Res Image",
            data=buf.getvalue(),
            file_name=f"{player_name}_NovviGodly_Radar.png",
            mime="image/png"
        )
