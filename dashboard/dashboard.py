import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from the CSV file directly
file_path = 'https://raw.githubusercontent.com/sitialyanrrmh/project_analisis_data/5f4e6ceb29ddfb540d650f0df4091c40041649a4/dashboard/main.csv'
day_df = pd.read_csv(file_path)

# Check if required columns are present
required_columns = ['casual', 'registered', 'cnt', 'weekday', 'mnth', 'season', 'temp', 'atemp', 'hum', 'windspeed']
if not all(col in day_df.columns for col in required_columns):
    st.error("Missing one or more required columns in the dataset.")
else:
    # Average renters per day
    weekday_total = day_df.groupby('weekday')[['casual', 'registered', 'cnt']].sum().reset_index()
    weekday_average = weekday_total.copy()
    weekday_average[['casual', 'registered', 'cnt']] = weekday_total[['casual', 'registered', 'cnt']] / (52 * 2)  # jumlah bulan dalam 2 tahun * jumlah minggu
    weekday_average.columns = ['weekday', 'avg_casual', 'avg_registered', 'avg_cnt']
    weekday_average[['avg_casual', 'avg_registered', 'avg_cnt']] = weekday_average[['avg_casual', 'avg_registered', 'avg_cnt']].astype(int)

    # Define the week names for x-axis labels
    weeks = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    # Function to plot average renters per day
    def plot_average_renters_per_day():
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(weekday_average['weekday'], weekday_average['avg_cnt'], marker='o', label='Avg Total Renters', color='green')
        ax.set_title('Average Total Renters per Week', fontsize=16)
        ax.set_xlabel('Day', fontsize=12)
        ax.set_ylabel('Average Total Renters', fontsize=12)
        ax.set_xticklabels(weeks, rotation=45)
        ax.legend()
        ax.grid(True)

              
        # Annotate the points with average total renters
        for i in range(len(weekday_average)):
            ax.annotate(weekday_average['avg_cnt'].iloc[i], 
                        (weekday_average['weekday'].iloc[i], weekday_average['avg_cnt'].iloc[i]),
                        textcoords="offset points", 
                        xytext=(0,5), 
                        ha='center')

        st.pyplot(fig)

    # Average renters per season
    season_total = day_df.groupby('season')[['casual', 'registered', 'cnt']].sum().reset_index()
    season_average = season_total.copy()
    season_average[['casual', 'registered', 'cnt']] = season_total[['casual', 'registered', 'cnt']] / 2  # jumlah season dalam 2 tahun
    season_average.columns = ['season', 'avg_casual', 'avg_registered', 'avg_cnt']
    season_average[['avg_casual', 'avg_registered', 'avg_cnt']] = season_average[['avg_casual', 'avg_registered', 'avg_cnt']].astype(int)

    # Define the week seasons for x-axis labels
    seasons = ['Winter', 'Spring', 'Summer', 'Fall']
    
    # Function to plot average renters per season
    def plot_average_renters_per_season():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='season', y='avg_cnt', data=season_average, ax=ax, palette='viridis')
        ax.set_title('Average Total Renters per Season', fontsize=16)
        ax.set_xlabel('Season', fontsize=12)
        ax.set_ylabel('Average Total Renters', fontsize=12)
        ax.set_xticklabels(seasons, rotation=45)

        # Annotate the bars with average total renters
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', 
                        fontsize=10, color='black', 
                        rotation=0)

        st.pyplot(fig)

    # Average renters per month
    month_total = day_df.groupby('mnth')[['casual', 'registered', 'cnt']].sum().reset_index()
    month_average = month_total.copy()
    month_average[['casual', 'registered', 'cnt']] = month_total[['casual', 'registered', 'cnt']] / 2  # membagi dengan jumlah bulan dalam 2 tahun
    month_average.columns = ['month', 'avg_casual', 'avg_registered', 'avg_cnt']
    month_average[['avg_casual', 'avg_registered', 'avg_cnt']] = month_average[['avg_casual', 'avg_registered', 'avg_cnt']].astype(int)

    # Define the month names for x-axis labels
    months = ['January', 'February', 'March', 'April', 'May', 'June', 
              'July', 'August', 'September', 'October', 'November', 'December']

    # Function to plot average renters per month
    def plot_average_renters_per_month():
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(month_average['month'], month_average['avg_cnt'], marker='o', label='Avg Total Renters (cnt)', color='blue')
        ax.set_title('Average Renters per Month', fontsize=16)
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Average Renters', fontsize=12)
        ax.set_xticks(month_average['month'])
        ax.set_xticklabels(months, rotation=45)
        ax.grid(True)
        ax.legend()

        # Annotate the points with average total renters
        for i in range(len(month_average)):
            ax.annotate(month_average['avg_cnt'].iloc[i], 
                        (month_average['month'].iloc[i], month_average['avg_cnt'].iloc[i]),
                        textcoords="offset points", 
                        xytext=(0,5), 
                        ha='center')

        st.pyplot(fig)

    # Heatmap of correlation
    def plot_heatmap():
        # Pilih kolom yang diinginkan
        variables_x = ['temp', 'atemp', 'hum', 'windspeed']
        variables_y = ['casual', 'registered', 'cnt']

        # Menghitung korelasi hanya antara variabel-variabel yang diinginkan
        correlation_matrix = day_df[variables_y + variables_x].corr().loc[variables_y, variables_x]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
        ax.set_title('Correlation Heatmap of Renters and Weather Variables', fontsize=16)
        st.pyplot(fig)

    # Main function to layout the dashboard
    st.title('Bicycle Rent Analysis Dashboard')

    col1, col2 = st.columns(2)

    with col1:
        plot_average_renters_per_day()
    
    with col2:
        plot_average_renters_per_season()
    
    with col1:
        plot_average_renters_per_month()
    
    with col2:
        plot_heatmap()
