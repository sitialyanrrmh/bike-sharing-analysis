import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load data from the CSV file directly
file_path = 'https://raw.githubusercontent.com/sitialyanrrmh/project_analisis_data/5f4e6ceb29ddfb540d650f0df4091c40041649a4/dashboard/main.csv'
day_df = pd.read_csv(file_path)

# Ensure that the 'dteday' column is in datetime format
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

# Add a new column for weekday names
day_df['weekday_name'] = day_df['dteday'].dt.day_name()

# Check if required columns are present
required_columns = ['casual', 'registered', 'cnt', 'weekday', 'mnth', 'season', 'temp', 'atemp', 'hum', 'windspeed', 'dteday', 'weekday_name']
if not all(col in day_df.columns for col in required_columns):
    st.error("Missing one or more required columns in the dataset.")
else:
    # Set up the layout
    st.title('Bicycle Rent Analysis Dashboard')
    st.sidebar.header("Date Range Selection")
    
    # Date selection for filtering
    start_date = st.sidebar.date_input("Start date", pd.to_datetime("2011-01-01"), min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))
    end_date = st.sidebar.date_input("End date", pd.to_datetime("2012-12-31"), min_value=pd.to_datetime("2011-01-01"), max_value=pd.to_datetime("2012-12-31"))

    # Filter the DataFrame based on selected dates
    filtered_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & (day_df['dteday'] <= pd.to_datetime(end_date))]

    # Calculate total renters in the selected date range
    total_renters = filtered_df['cnt'].sum()

    # Display total rentals in a styled container
    with st.container():
        st.markdown(f"<h2 style='color: green;'>Total Bike Rentals from {start_date} to {end_date}:</h2>", unsafe_allow_html=True)
        st.markdown(f"<h1 style='color: blue;'>{total_renters:,}</h1>", unsafe_allow_html=True)

    # Highlight the selected date range
    st.markdown(f"<h3 style='color: orange;'>Selected Date Range:</h3>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='color: gray;'>From: {start_date} To: {end_date}</h4>", unsafe_allow_html=True)

    # Total rentals grouped by weekday
    weekday_total = filtered_df.groupby('weekday_name')['cnt'].sum().reset_index()
    weekday_total = weekday_total.sort_values(by='cnt', ascending=False)

    # Function to plot total rentals per weekday
    def plot_rentals_per_weekday():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='weekday_name', y='cnt', data=weekday_total, ax=ax, palette='viridis')
        ax.set_title('Total Rentals by Weekday', fontsize=16)
        ax.set_xlabel('Day of the Week', fontsize=12)
        ax.set_ylabel('Total Rentals', fontsize=12)

        # Rotate weekday names and format labels
        for label in ax.get_xticklabels():
            label.set_fontsize(12)
            label.set_fontstyle('italic')
            label.set_rotation(45)

        # Annotate the bars with total rentals
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', 
                        fontsize=10, color='black', 
                        rotation=0)

        st.pyplot(fig)

    st.subheader("Total Rentals by Weekday")
    plot_rentals_per_weekday()

    # Best Months
    month_total = filtered_df.groupby('mnth')['cnt'].sum().reset_index()
    month_total['month_name'] = month_total['mnth'].map({
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 
        5: 'May', 6: 'June', 7: 'July', 8: 'August', 
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    })
    
    month_total = month_total.sort_values(by='cnt', ascending=False)  # Sort from largest to smallest

    # Function to plot best months
    def plot_best_months():
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(x='month_name', y='cnt', data=month_total, ax=ax, palette='viridis')
        ax.set_title('Total Rentals per Month', fontsize=16)
        ax.set_xlabel('Month', fontsize=12)
        ax.set_ylabel('Total Rentals', fontsize=12)

        # Set month names to italic and rotate by 45 degrees
        for label in ax.get_xticklabels():
            label.set_fontsize(12)
            label.set_fontstyle('italic')
            label.set_rotation(45)

        # Annotate the bars with total rentals
        for p in ax.patches:
            ax.annotate(f'{int(p.get_height())}', 
                        (p.get_x() + p.get_width() / 2., p.get_height()), 
                        ha='center', va='bottom', 
                        fontsize=10, color='black', 
                        rotation=0)

        st.pyplot(fig)

    st.subheader("Best Months")
    plot_best_months()

  # Average renters per season without filtering
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

    st.subheader("Average Renters per Season")
    plot_average_renters_per_season()

    # Heatmap of correlation
    def plot_heatmap():
        variables_x = ['temp', 'atemp', 'hum', 'windspeed']
        variables_y = ['casual', 'registered', 'cnt']

        correlation_matrix = day_df[variables_y + variables_x].corr().loc[variables_y, variables_x]
        
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
        ax.set_title('Correlation Heatmap of Renters and Weather Variables', fontsize=16)
        st.pyplot(fig)

    st.subheader("Correlation Heatmap")
    plot_heatmap()
