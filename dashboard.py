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

    # Data preprocessing
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {
        1: 'Clear/Few clouds',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Ice/Snow'
    }

    day_df['season'] = day_df['season'].map(season_map)
    hour_df['season'] = hour_df['season'].map(season_map)

    day_df['weathersit'] = day_df['weathersit'].map(weather_map)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)

    day_df['workingday'] = day_df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday')
    hour_df['workingday'] = hour_df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday')

    return day_df, hour_df

day_df, hour_df = load_data()

# Judul dashboard
st.title("📊 Bike Sharing Analysis Dashboard")
st.markdown("Analisis data penyewaan sepeda berdasarkan musim, cuaca, dan hari kerja vs libur.")

# Tabs
tab1, tab2 = st.tabs(["Season & Weather", "Working Day vs Holiday"])

# ========================
# TAB 1 - SEASON & WEATHER
# ========================
with tab1:
    st.header("🎯 Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")

    # Filter interaktif
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    date_range = st.date_input("Pilih rentang tanggal:", [min_date, max_date],
                               min_value=min_date, max_value=max_date)

    seasons = day_df['season'].unique().tolist()
    selected_seasons = st.multiselect("Pilih musim:", seasons, default=seasons)

    filtered_day_df = day_df[
        (day_df['dteday'] >= pd.to_datetime(date_range[0])) &
        (day_df['dteday'] <= pd.to_datetime(date_range[1])) &
        (day_df['season'].isin(selected_seasons))
    ]

    # Distribusi penyewaan selama rentang waktu
    st.subheader("🧾 Distribusi Penyewaan Sepeda Selama Rentang Tanggal Dipilih")
    fig_dist, ax_dist = plt.subplots()
    sns.histplot(filtered_day_df['cnt'], bins=20, kde=True, ax=ax_dist, color='coral')
    ax_dist.set_title("Distribusi Penyewaan Sepeda")
    ax_dist.set_xlabel("Jumlah Penyewaan per Hari")
    ax_dist.set_ylabel("Frekuensi")
    st.pyplot(fig_dist)

    st.markdown(f"""
    **📌 Insight:**  
    Grafik ini menunjukkan sebaran penyewaan sepeda per hari dari tanggal **{date_range[0]}** sampai **{date_range[1]}**.  
    Distribusi bisa memperlihatkan apakah penyewaan lebih sering terjadi di angka rendah, sedang, atau tinggi.
    """)

    # Boxplot per musim
    st.subheader("Distribusi Penyewaan berdasarkan Musim (Boxplot)")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x='season', y='cnt', data=filtered_day_df, ax=ax1)
    ax1.set_title('Distribusi Penyewaan Sepeda per Musim')
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Total Penyewaan')
    st.pyplot(fig1)

    # Bar chart total penyewaan per musim
    st.subheader("Total Penyewaan Sepeda per Musim (Bar Chart)")
    season_totals = filtered_day_df.groupby('season')['cnt'].sum()
    fig2, ax2 = plt.subplots()
    season_totals.plot(kind='bar', ax=ax2, color='skyblue')
    ax2.set_ylabel("Total Penyewaan")
    ax2.set_xlabel("Musim")
    ax2.set_title("Total Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(fig2)

    # Boxplot cuaca
    st.subheader("Distribusi Penyewaan berdasarkan Kondisi Cuaca")
    fig3, ax3 = plt.subplots()
    sns.boxplot(x='weathersit', y='cnt', data=filtered_day_df, ax=ax3)
    ax3.set_title('Distribusi Penyewaan per Kondisi Cuaca')
    ax3.set_xlabel('Kondisi Cuaca')
    ax3.set_ylabel('Total Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Pie chart proporsi cuaca
    st.subheader("Proporsi Kondisi Cuaca (Pie Chart)")
    weather_counts = filtered_day_df['weathersit'].value_counts()
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=90)
    ax_pie.axis('equal')
    st.pyplot(fig_pie)

    # Scatter plot: suhu vs jumlah penyewaan
    st.subheader("Hubungan Suhu dan Jumlah Penyewaan Sepeda")
    fig_temp, ax_temp = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', hue='season', data=filtered_day_df, ax=ax_temp, palette='viridis')
    ax_temp.set_title("Suhu vs Jumlah Penyewaan")
    ax_temp.set_xlabel("Suhu")
    ax_temp.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig_temp)

    # Correlation heatmap
    st.subheader("📊 Korelasi Antar Fitur Numerik")
    corr = filtered_day_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
    ax_corr.set_title("Matriks Korelasi")
    st.pyplot(fig_corr)

    # Tren bulanan berdasarkan tahun
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Tahun")
    fig_trend, ax_trend = plt.subplots()
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=filtered_day_df, marker='o', ax=ax_trend)
    ax_trend.set_title("Penyewaan Bulanan per Tahun")
    ax_trend.set_xlabel("Bulan")
    ax_trend.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig_trend)

    st.markdown("""
    **📌 Insight:**
    - Musim **Fall** menghasilkan penyewaan tertinggi.
    - Cuaca **cerah atau sedikit awan** paling optimal untuk penyewaan.
    - Proporsi terbanyak terjadi pada cuaca cerah.
    """)

# ========================
# TAB 2 - WORKING DAY VS HOLIDAY
# ========================
with tab2:
    st.header("🏖️ Perbandingan Hari Kerja vs Hari Libur")

    # Rata-rata penyewaan per jenis hari
    st.subheader("Rata-rata Penyewaan Sepeda")
    fig4, ax4 = plt.subplots()
    sns.barplot(x='workingday', y='cnt', data=day_df, estimator='mean', ax=ax4)
    ax4.set_title('Rata-rata Penyewaan: Hari Kerja vs Libur')
    ax4.set_xlabel('Jenis Hari')
    ax4.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig4)

    # Pola penyewaan per jam
    st.subheader("Pola Penyewaan per Jam")
    wd_hourly = hour_df[hour_df['workingday'] == 'Working Day'].groupby('hr')['cnt'].mean()
    nwd_hourly = hour_df[hour_df['workingday'] == 'Weekend/Holiday'].groupby('hr')['cnt'].mean()

    fig5, ax5 = plt.subplots()
    ax5.plot(wd_hourly.index, wd_hourly.values, label='Working Day', marker='o')
    ax5.plot(nwd_hourly.index, nwd_hourly.values, label='Weekend/Holiday', marker='s')
    ax5.set_xticks(range(0, 24))
    ax5.set_xlabel("Jam")
    ax5.set_ylabel("Rata-rata Penyewaan")
    ax5.set_title("Pola Penyewaan Sepeda per Jam")
    ax5.legend()
    ax5.grid(True)
    st.pyplot(fig5)

    st.markdown("""
    **📌 Insight:**
    - Hari kerja menunjukkan dua puncak (jam **08:00** dan **17:00** – jam sibuk).
    - Hari libur lebih merata dengan puncak di **tengah hari**.
    """)
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

    # Data preprocessing
    day_df['dteday'] = pd.to_datetime(day_df['dteday'])
    hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

    season_map = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    weather_map = {
        1: 'Clear/Few clouds',
        2: 'Mist/Cloudy',
        3: 'Light Snow/Rain',
        4: 'Heavy Rain/Ice/Snow'
    }

    day_df['season'] = day_df['season'].map(season_map)
    hour_df['season'] = hour_df['season'].map(season_map)

    day_df['weathersit'] = day_df['weathersit'].map(weather_map)
    hour_df['weathersit'] = hour_df['weathersit'].map(weather_map)

    day_df['workingday'] = day_df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday')
    hour_df['workingday'] = hour_df['workingday'].apply(lambda x: 'Working Day' if x == 1 else 'Weekend/Holiday')

    return day_df, hour_df

day_df, hour_df = load_data()

# Judul dashboard
st.title("📊 Bike Sharing Analysis Dashboard")
st.markdown("Analisis data penyewaan sepeda berdasarkan musim, cuaca, dan hari kerja vs libur.")

# Tabs
tab1, tab2 = st.tabs(["Season & Weather", "Working Day vs Holiday"])

# ========================
# TAB 1 - SEASON & WEATHER
# ========================
with tab1:
    st.header("🎯 Pengaruh Musim dan Cuaca terhadap Penyewaan Sepeda")

    # Filter interaktif
    min_date = day_df['dteday'].min()
    max_date = day_df['dteday'].max()
    date_range = st.date_input("Pilih rentang tanggal:", [min_date, max_date],
                               min_value=min_date, max_value=max_date)

    seasons = day_df['season'].unique().tolist()
    selected_seasons = st.multiselect("Pilih musim:", seasons, default=seasons)

    filtered_day_df = day_df[
        (day_df['dteday'] >= pd.to_datetime(date_range[0])) &
        (day_df['dteday'] <= pd.to_datetime(date_range[1])) &
        (day_df['season'].isin(selected_seasons))
    ]

    # Distribusi penyewaan selama rentang waktu
    st.subheader("🧾 Distribusi Penyewaan Sepeda Selama Rentang Tanggal Dipilih")
    fig_dist, ax_dist = plt.subplots()
    sns.histplot(filtered_day_df['cnt'], bins=20, kde=True, ax=ax_dist, color='coral')
    ax_dist.set_title("Distribusi Penyewaan Sepeda")
    ax_dist.set_xlabel("Jumlah Penyewaan per Hari")
    ax_dist.set_ylabel("Frekuensi")
    st.pyplot(fig_dist)

    st.markdown(f"""
    **📌 Insight:**  
    Grafik ini menunjukkan sebaran penyewaan sepeda per hari dari tanggal **{date_range[0]}** sampai **{date_range[1]}**.  
    Distribusi bisa memperlihatkan apakah penyewaan lebih sering terjadi di angka rendah, sedang, atau tinggi.
    """)

    # Boxplot per musim
    st.subheader("Distribusi Penyewaan berdasarkan Musim (Boxplot)")
    fig1, ax1 = plt.subplots()
    sns.boxplot(x='season', y='cnt', data=filtered_day_df, ax=ax1)
    ax1.set_title('Distribusi Penyewaan Sepeda per Musim')
    ax1.set_xlabel('Musim')
    ax1.set_ylabel('Total Penyewaan')
    st.pyplot(fig1)

    # Bar chart total penyewaan per musim
    st.subheader("Total Penyewaan Sepeda per Musim (Bar Chart)")
    season_totals = filtered_day_df.groupby('season')['cnt'].sum()
    fig2, ax2 = plt.subplots()
    season_totals.plot(kind='bar', ax=ax2, color='skyblue')
    ax2.set_ylabel("Total Penyewaan")
    ax2.set_xlabel("Musim")
    ax2.set_title("Total Penyewaan Sepeda Berdasarkan Musim")
    st.pyplot(fig2)

    # Boxplot cuaca
    st.subheader("Distribusi Penyewaan berdasarkan Kondisi Cuaca")
    fig3, ax3 = plt.subplots()
    sns.boxplot(x='weathersit', y='cnt', data=filtered_day_df, ax=ax3)
    ax3.set_title('Distribusi Penyewaan per Kondisi Cuaca')
    ax3.set_xlabel('Kondisi Cuaca')
    ax3.set_ylabel('Total Penyewaan')
    plt.xticks(rotation=45)
    st.pyplot(fig3)

    # Pie chart proporsi cuaca
    st.subheader("Proporsi Kondisi Cuaca (Pie Chart)")
    weather_counts = filtered_day_df['weathersit'].value_counts()
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(weather_counts, labels=weather_counts.index, autopct='%1.1f%%', startangle=90)
    ax_pie.axis('equal')
    st.pyplot(fig_pie)

    # Scatter plot: suhu vs jumlah penyewaan
    st.subheader("Hubungan Suhu dan Jumlah Penyewaan Sepeda")
    fig_temp, ax_temp = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', hue='season', data=filtered_day_df, ax=ax_temp, palette='viridis')
    ax_temp.set_title("Suhu vs Jumlah Penyewaan")
    ax_temp.set_xlabel("Suhu")
    ax_temp.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig_temp)

    # Correlation heatmap
    st.subheader("📊 Korelasi Antar Fitur Numerik")
    corr = filtered_day_df[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
    fig_corr, ax_corr = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', fmt='.2f', ax=ax_corr)
    ax_corr.set_title("Matriks Korelasi")
    st.pyplot(fig_corr)

    # Tren bulanan berdasarkan tahun
    st.subheader("📅 Tren Penyewaan Sepeda Bulanan Berdasarkan Tahun")
    fig_trend, ax_trend = plt.subplots()
    sns.lineplot(x='mnth', y='cnt', hue='yr', data=filtered_day_df, marker='o', ax=ax_trend)
    ax_trend.set_title("Penyewaan Bulanan per Tahun")
    ax_trend.set_xlabel("Bulan")
    ax_trend.set_ylabel("Jumlah Penyewaan")
    st.pyplot(fig_trend)

    st.markdown("""
    **📌 Insight:**
    - Musim **Fall** menghasilkan penyewaan tertinggi.
    - Cuaca **cerah atau sedikit awan** paling optimal untuk penyewaan.
    - Proporsi terbanyak terjadi pada cuaca cerah.
    """)

# ========================
# TAB 2 - WORKING DAY VS HOLIDAY
# ========================
with tab2:
    st.header("🏖️ Perbandingan Hari Kerja vs Hari Libur")

    # Rata-rata penyewaan per jenis hari
    st.subheader("Rata-rata Penyewaan Sepeda")
    fig4, ax4 = plt.subplots()
    sns.barplot(x='workingday', y='cnt', data=day_df, estimator='mean', ax=ax4)
    ax4.set_title('Rata-rata Penyewaan: Hari Kerja vs Libur')
    ax4.set_xlabel('Jenis Hari')
    ax4.set_ylabel('Rata-rata Penyewaan')
    st.pyplot(fig4)

    # Pola penyewaan per jam
    st.subheader("Pola Penyewaan per Jam")
    wd_hourly = hour_df[hour_df['workingday'] == 'Working Day'].groupby('hr')['cnt'].mean()
    nwd_hourly = hour_df[hour_df['workingday'] == 'Weekend/Holiday'].groupby('hr')['cnt'].mean()

    fig5, ax5 = plt.subplots()
    ax5.plot(wd_hourly.index, wd_hourly.values, label='Working Day', marker='o')
    ax5.plot(nwd_hourly.index, nwd_hourly.values, label='Weekend/Holiday', marker='s')
    ax5.set_xticks(range(0, 24))
    ax5.set_xlabel("Jam")
    ax5.set_ylabel("Rata-rata Penyewaan")
    ax5.set_title("Pola Penyewaan Sepeda per Jam")
    ax5.legend()
    ax5.grid(True)
    st.pyplot(fig5)

    st.markdown("""
    **📌 Insight:**
    - Hari kerja menunjukkan dua puncak (jam **08:00** dan **17:00** – jam sibuk).
    - Hari libur lebih merata dengan puncak di **tengah hari**.
    """)
