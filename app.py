import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional
import json
import os

# Page config
st.set_page_config(
    page_title="Training Tracker",
    page_icon="🏋️",
    layout="wide"
)

# Constants
MUSCLE_GROUPS = {
    "push-ups": "chest",
    "squats": "legs",
    "pull-ups": "back",
    "dips": "triceps",
    "lunges": "legs",
    "plank": "core"
}

# Google Sheets configuration
SPREADSHEET_ID = "YOUR_SPREADSHEET_ID"  # Replace with your spreadsheet ID from the URL

# Initialize session state
if 'training_history' not in st.session_state:
    st.session_state.training_history = pd.DataFrame(columns=[
        'date', 'exercise', 'sets', 'reps', 'muscle_group', 'level'
    ])

def setup_google_sheets():
    """Initialize Google Sheets connection using Streamlit secrets"""
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    try:
        # Get credentials from Streamlit secrets
        creds_dict = st.secrets["GOOGLE_SHEETS_CREDENTIALS"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
        client = gspread.authorize(creds)
        # Open the spreadsheet by ID from secrets
        spreadsheet = client.open_by_key(st.secrets["SPREADSHEET_ID"])
        return spreadsheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {str(e)}")
        st.error("Please check your Streamlit secrets configuration")
        return None

def load_training_data():
    """Load training data from Google Sheets"""
    try:
        spreadsheet = setup_google_sheets()
        if spreadsheet:
            worksheet = spreadsheet.sheet1
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error loading training data: {str(e)}")
        return pd.DataFrame()

def save_training_data(data: pd.DataFrame):
    """Save training data to Google Sheets"""
    try:
        spreadsheet = setup_google_sheets()
        if spreadsheet:
            worksheet = spreadsheet.sheet1
            # Clear existing data
            worksheet.clear()
            # Add headers
            worksheet.append_row(data.columns.tolist())
            # Add data
            for _, row in data.iterrows():
                worksheet.append_row(row.tolist())
            return True
        return False
    except Exception as e:
        st.error(f"Error saving training data: {str(e)}")
        return False

def load_training_progression():
    """Load the training progression table"""
    progression_data = {
        'Level': ['6-10'] * 6,
        'Day': list(range(1, 7)),
        'Set 1': [5, 6, 8, 9, 10, 12],
        'Set 2': [6, 7, 10, 11, 12, 13],
        'Set 3': [4, 6, 7, 8, 9, 10],
        'Set 4': [4, 6, 7, 8, 9, 10],
        'Set 5 Minimum': [5, 7, 10, 11, 13, 15],
        'Rest (hours)': [24, 24, 48, 24, 24, 48],
        'Rest between sets (seconds)': [60, 90, 120, 60, 90, 120]
    }
    return pd.DataFrame(progression_data)

def calculate_estimated_max(reps_history: List[int]) -> float:
    """Calculate estimated max capacity using moving average"""
    if not reps_history:
        return 0
    window_size = min(5, len(reps_history))
    return np.mean(reps_history[-window_size:]) * 1.2

def get_today_recommendation() -> Tuple[bool, str, Dict]:
    """Determine today's training recommendation"""
    today = datetime.now().date()
    last_workout = st.session_state.training_history['date'].max() if not st.session_state.training_history.empty else None
    
    if last_workout:
        days_since_last_workout = (today - last_workout).days
        if days_since_last_workout < 3:
            return False, "rest", {}
    
    # Determine which muscle group to train
    muscle_group_history = st.session_state.training_history.groupby('muscle_group')['date'].max()
    if not muscle_group_history.empty:
        target_muscle = muscle_group_history.idxmin()
        exercises = [ex for ex, mg in MUSCLE_GROUPS.items() if mg == target_muscle]
    else:
        exercises = list(MUSCLE_GROUPS.keys())
    
    selected_exercise = np.random.choice(exercises)
    exercise_history = st.session_state.training_history[
        st.session_state.training_history['exercise'] == selected_exercise
    ]
    
    if exercise_history.empty:
        reps = 5  # Baseline
    else:
        estimated_max = calculate_estimated_max(exercise_history['reps'].tolist())
        reps = int(estimated_max * 0.8)
    
    return True, selected_exercise, {'reps': reps}

def create_heatmap():
    """Create training history heatmap"""
    if st.session_state.training_history.empty:
        return None
    
    # Create a date range for the last 6 months
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=180)
    date_range = pd.date_range(start=start_date, end=end_date)
    
    # Create a DataFrame with all dates
    heatmap_data = pd.DataFrame({'date': date_range})
    heatmap_data['date'] = pd.to_datetime(heatmap_data['date']).dt.date
    
    # Merge with training history
    training_dates = st.session_state.training_history.groupby('date').size().reset_index()
    training_dates.columns = ['date', 'count']
    heatmap_data = heatmap_data.merge(training_dates, on='date', how='left')
    heatmap_data['count'] = heatmap_data['count'].fillna(0)
    
    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data['count'].values.reshape(-1, 7),
        colorscale='YlOrRd',
        showscale=False
    ))
    
    fig.update_layout(
        title='Training History Heatmap',
        xaxis_title='Day of Week',
        yaxis_title='Week',
        height=300
    )
    
    return fig

def main():
    st.title("🏋️ Training Tracker")
    
    # Load training data from Google Sheets
    training_data = load_training_data()
    if not training_data.empty:
        st.session_state.training_history = training_data
    
    # Load training progression table
    progression_table = load_training_progression()
    
    # Get today's recommendation
    should_train, exercise, details = get_today_recommendation()
    
    # Display today's status
    col1, col2 = st.columns(2)
    with col1:
        st.header("Today's Status")
        if should_train:
            st.success("✅ Training Day")
            st.write(f"Exercise: {exercise}")
            st.write(f"Recommended reps: {details['reps']}")
        else:
            st.info("💤 Rest Day")
    
    with col2:
        st.header("Training History")
        heatmap = create_heatmap()
        if heatmap:
            st.plotly_chart(heatmap, use_container_width=True)
    
    # Display training progression table
    st.header("Training Progression")
    st.dataframe(progression_table)
    
    # Save data if there are changes
    if not training_data.equals(st.session_state.training_history):
        if save_training_data(st.session_state.training_history):
            st.success("Training data saved successfully!")
        else:
            st.error("Failed to save training data")

if __name__ == "__main__":
    main()
