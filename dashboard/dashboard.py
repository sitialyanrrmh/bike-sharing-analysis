import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from the CSV file directly
file_path = 'https://raw.githubusercontent.com/sitialyanrrmh/project_analisis_data/5f4e6ceb29ddfb540d650f0df4091c40041649a4/dashboard/main.csv'
hour_df = pd.read_csv(file_path)

# Check if required columns are present
required_columns = ['temp', 'atemp', 'hum', 'windspeed', 'casual', 'registered', 'cnt', 'weekday', 'mnth', 'season']
if not all(col in hour_df.columns for col in required_columns):
    st.error("Missing one or more required columns in the dataset.")
else:
    # Calculate correlation matrix
    variables_x = ['temp', 'atemp', 'hum', 'windspeed']
    variables_y = ['casual', 'registered', 'cnt']
    correlation_matrix = hour_df[variables_y + variables_x].corr().loc[variables_y, variables_x]

    # Visualization functions
    def plot_average_users_per_day(hour_df):
        grouped_data = hour_df.groupby('weekday')['cnt'].mean()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x=grouped_data.index, y=grouped_data.values, marker='o', ax=ax)
        
        ax.set_title('Average Users Per Day in 2011-2012', fontsize=14)
        ax.set_xlabel('Weekday (0=Sunday, 6=Saturday)', fontsize=12)
        ax.set_ylabel('Average Users', fontsize=12)
        ax.grid(True)
        
        st.pyplot(fig)

    def plot_average_users_per_month(hour_df):
        fig, ax = plt.subplots(figsize=(12, 6))
        sns.lineplot(data=hour_df, x='mnth', y='casual', marker='o', label='Casual Users', color='orange')
        sns.lineplot(data=hour_df, x='mnth', y='registered', marker='o', label='Registered Users', color='green')
        sns.lineplot(data=hour_df, x='mnth', y='cnt', marker='o', label='Total Users (cnt)', color='blue')
        
        ax.set_title('Average Users per Month in 2011-2012', fontsize=14)
        ax.set_xlabel('Month (1=January, 12=December)', fontsize=12)
        ax.set_ylabel('Average Users', fontsize=12)
        ax.grid(True)
        
        st.pyplot(fig)

    def plot_users_by_season(hour_df):
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season', y='cnt', data=hour_df, ax=ax)
        
        ax.set_title('Average Total Users by Season in 2011-2012')
        ax.set_xlabel('Season')
        ax.set_ylabel('Average Count')
        
        st.pyplot(fig)

    def plot_correlation_heatmap(correlation_matrix):
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
        
        ax.set_title('Correlation Matrix between Selected Variables')
        ax.set_xlabel('Weather Conditions')
        ax.set_ylabel('Users')
        
        st.pyplot(fig)

    # Main function to layout the dashboard
    st.title('User Analysis Dashboard')
    
    col1, col2 = st.columns(2)
    
    with col1:
        plot_average_users_per_day(hour_df)
    
    with col2:
        plot_users_by_season(hour_df)
    
    with col1:
        plot_average_users_per_month(hour_df)
    
    with col2:
        plot_correlation_heatmap(correlation_matrix)
