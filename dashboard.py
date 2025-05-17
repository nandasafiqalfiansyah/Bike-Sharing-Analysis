import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
@st.cache_data
def load_data():
    url_day = "./data/day.csv"
    url_hour = "./data/hour.csv"
    day_df = pd.read_csv(url_day)
    hour_df = pd.read_csv(url_hour)
    
    # Perform the same cleaning as in the notebook
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])
    
    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    day_df['season'] = day_df['season'].map(season_map)
    hour_df['season'] = hour_df['season'].map(season_map)
    
    weather_map = {1: 'Clear/Few clouds', 2: 'Mist/Cloudy', 3: 'Light Snow/Rain', 4: 'Heavy Rain/Ice/Snow'}
    day_df['weathersit'] = day_df['weathersit'].map(weather_map)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)
    
    day_df['workingday'] = day_df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday')
    hour_df['workingday'] = hour_df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday')
    
    return day_df, hour_df

day_df, hour_df = load_data()

# Dashboard title
st.title('Bike Sharing Analysis Dashboard')
st.write('Analisis pola penggunaan sistem berbagi sepeda')

# Tab layout
tab1, tab2 = st.tabs(["Seasonal & Weather Analysis", "Working Day vs Holiday Analysis"])

with tab1:
    st.header("Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")
    
    # Season analysis
    st.subheader("Distribusi Penyewaan berdasarkan Musim")
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='season', y='cnt', data=day_df, ax=ax1)
    ax1.set_title('Bike Rentals by Season')
    ax1.set_xlabel('Season')
    ax1.set_ylabel('Total Rentals')
    st.pyplot(fig1)
    
    # Weather analysis
    st.subheader("Distribusi Penyewaan berdasarkan Kondisi Cuaca")
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='weathersit', y='cnt', data=day_df, ax=ax2)
    ax2.set_title('Bike Rentals by Weather Situation')
    ax2.set_xlabel('Weather Situation')
    ax2.set_ylabel('Total Rentals')
    plt.xticks(rotation=45)
    st.pyplot(fig2)
    
    st.write("""
    **Insight:**
    - Musim gugur (Fall) memiliki jumlah penyewaan tertinggi
    - Cuaca cerah/sedikit awan menghasilkan penyewaan terbanyak
    - Kombinasi musim gugur dengan cuaca cerah adalah kondisi optimal
    """)

with tab2:
    st.header("Perbandingan Penyewaan: Hari Kerja vs Hari Libur")
    
    # Working day vs holiday
    st.subheader("Rata-rata Penyewaan per Jenis Hari")
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.barplot(x='workingday', y='cnt', data=day_df, estimator='mean', ax=ax3)
    ax3.set_title('Average Rentals: Working Day vs Weekend/Holiday')
    ax3.set_xlabel('Day Type')
    ax3.set_ylabel('Average Rentals')
    st.pyplot(fig3)
    
    # Hourly pattern
    st.subheader("Pola Penyewaan Per Jam")
    working_day_hourly = hour_df[hour_df['workingday'] == 'Working Day'].groupby('hr')['cnt'].mean()
    non_working_day_hourly = hour_df[hour_df['workingday'] == 'Weekend/Holiday'].groupby('hr')['cnt'].mean()
    
    fig4, ax4 = plt.subplots(figsize=(12, 6))
    ax4.plot(working_day_hourly.index, working_day_hourly.values, label='Working Day')
    ax4.plot(non_working_day_hourly.index, non_working_day_hourly.values, label='Weekend/Holiday')
    ax4.set_title('Hourly Rental Patterns')
    ax4.set_xlabel('Hour of Day')
    ax4.set_ylabel('Average Rentals')
    ax4.set_xticks(range(0, 24))
    ax4.legend()
    ax4.grid()
    st.pyplot(fig4)
    
    st.write("""
    **Insight:**
    - Hari kerja memiliki total penyewaan lebih tinggi secara keseluruhan
    - Pola berbeda jelas terlihat: 
        - Hari kerja: puncak jam 8 pagi dan 5-6 sore (jam komuter)
        - Hari libur: pola lebih merata dengan puncak tengah hari
    """)

# Run with: streamlit run dashboard.py