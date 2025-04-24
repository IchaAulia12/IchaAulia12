import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Memuat data
@st.cache_data
def load_data():
    combined_data = pd.read_csv('./cleaned_combined_data.csv')
    combined_data['datetime'] = pd.to_datetime(combined_data[['year', 'month', 'day', 'hour']])
    combined_data.set_index('datetime', inplace=True)
    combined_data.sort_index(inplace=True)
    return combined_data

combined_data = load_data()

st.title('Polusi Udara dari Waktu ke Waktu')
with st.sidebar:
    st.title('Kualitas Udara di Beijing')
    frequency = st.selectbox('Frekuensi:', ['Harian', 'Mingguan', 'Bulanan'])
    col1, col2, = st.columns(2)

    # Pilihan frekuensi resampling
    with col1:
        start_date = st.date_input('Tanggal Mulai', value=combined_data.index.min().date())

    # Pilihan rentang tanggal
    with col2:
        end_date = st.date_input('Tanggal Akhir', value=combined_data.index.max().date())

    stations = ['All Stations'] + sorted(combined_data['station'].unique().tolist())
    selected_station = st.selectbox('Stasiun:', stations)

    # Memastikan tanggal mulai tidak lebih besar dari tanggal akhir
    if start_date > end_date:
        st.error('Tanggal mulai harus lebih awal dari tanggal akhir.')
        st.stop()

    # Memilih data berdasarkan rentang tanggal yang dipilih
    filtered_data = combined_data.loc[str(start_date):str(end_date)]

    # Memfilter data berdasarkan stasiun yang dipilih
    if selected_station != 'All Stations':
        filtered_data = filtered_data[filtered_data['station'] == selected_station]

    # Resampling data berdasarkan frekuensi yang dipilih
    if frequency == 'Harian':
        resampled_data = filtered_data.resample('D').mean(numeric_only=True)
    elif frequency == 'Mingguan':
        resampled_data = filtered_data.resample('W').mean(numeric_only=True)
    else:  # Bulanan
        resampled_data = filtered_data.resample('ME').mean(numeric_only=True)  # Updated to 'ME'

    pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']

# Membuat plot
plt.figure(figsize=(12, 8))

for pollutant in pollutants:
    plt.plot(resampled_data.index, resampled_data[pollutant], label=pollutant)  # Ensure labels are set

plt.title(f'Tren Polusi Udara ({frequency}) dari {start_date} hingga {end_date} - {selected_station}')
plt.xlabel('Waktu')
plt.ylabel('Konsentrasi Rata-rata')
plt.legend()  # Ensure legend is displayed
plt.grid(True)

# Menampilkan plot di Streamlit
st.pyplot(plt)

if selected_station == 'All Stations':
    station_grouped = filtered_data.groupby('station').mean(numeric_only=True)
    station_grouped['Average Pollution'] = station_grouped[pollutants].mean(axis=1)
    max_station = station_grouped['Average Pollution'].idxmax()
    min_station = station_grouped['Average Pollution'].idxmin()
else:
    station_grouped = filtered_data.groupby(filtered_data.index.year).mean(numeric_only=True)
    station_grouped['Average Pollution'] = station_grouped[pollutants].mean(axis=1)
    max_station = selected_station
    min_station = selected_station

# Membuat dua kolom utama
col_left, col_right = st.columns([1, 1])

# Kolom kiri: Stasiun dengan Polusi Tertinggi dan Terendah
with col_left:
    if selected_station == 'All Stations':
        with st.container():
            st.subheader('Stasiun dengan Polusi Tertinggi')
            st.markdown(f'<p style="color:red; font-size:24px">{max_station}: <span style="font-size:18px">{station_grouped.loc[max_station, "Average Pollution"]:.2f}</span></p>', unsafe_allow_html=True)

        with st.container():
            st.subheader('Stasiun dengan Polusi Terendah')
            st.markdown(f'<p style="color:green; font-size:24px">{min_station}: <span style="font-size:18px">{station_grouped.loc[min_station, "Average Pollution"]:.2f}</span></p>', unsafe_allow_html=True)
    else:
        with st.container():
            st.subheader('Tingkat Polusi Tertinggi')
            max_pollution = station_grouped['Average Pollution'].max()
            max_year = station_grouped['Average Pollution'].idxmax()
            st.markdown(f'<p style="color:red; font-size:24px">{max_year}: <span style="font-size:18px">{max_pollution:.2f}</span></p>', unsafe_allow_html=True)

        with st.container():
            st.subheader('Tingkat Polusi Terendah')
            min_pollution = station_grouped['Average Pollution'].min()
            min_year = station_grouped['Average Pollution'].idxmin()
            st.markdown(f'<p style="color:green; font-size:24px">{min_year}: <span style="font-size:18px">{min_pollution:.2f}</span></p>', unsafe_allow_html=True)

# Kolom kanan: Tabel Keterangan Urutan Setiap Stasiun
with col_right:
    if selected_station == 'All Stations':
        st.subheader('Urutan Setiap Stasiun')
        sorted_stations = station_grouped[['Average Pollution']].sort_values(by='Average Pollution', ascending=False)
        st.dataframe(sorted_stations.style.format({'Average Pollution': '{:.2f}'}))
    else:
        st.subheader('Urutan Polusi dari Tahun ke Tahun')
        sorted_years = station_grouped[['Average Pollution']].sort_values(by='Average Pollution', ascending=False)
        st.dataframe(sorted_years.style.format({'Average Pollution': '{:.2f}'}))

tabs = st.tabs(["Correlation Matrix", "Data Distribution", "Rain vs Pollution"])

with tabs[0]:
    st.header("Correlation Matrix of Air Pollutants and Weather Variables")
    correlation_matrix = combined_data[['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP']].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title('Correlation Matrix')
    st.pyplot(fig)

with tabs[1]:
    st.header("Data Distribusi Polusi Udara")
    fig, axes = plt.subplots(4, 3, figsize=(15, 10))
    axes = axes.ravel()

    for i, column in enumerate(['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN']):
        sns.histplot(combined_data[column], kde=True, ax=axes[i])
        axes[i].set_title(f'Distribution of {column}')

    plt.tight_layout()
    st.pyplot(fig)

with tabs[2]:
    st.header("Rain vs Pollution")
    rain_grouped = combined_data.groupby('RAIN').mean(numeric_only=True)

    fig, axes = plt.subplots(3, 2, figsize=(15, 10))
    axes = axes.ravel()

    for i, pollutant in enumerate(['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']):
        sns.lineplot(x=rain_grouped.index, y=rain_grouped[pollutant], ax=axes[i])
        axes[i].set_xlabel('Rain')
        axes[i].set_ylabel(pollutant)
        axes[i].set_title(f'{pollutant} vs Rain')

    plt.tight_layout()
    st.pyplot(fig)
# Menghitung outlier PM2.5
Q1 = combined_data['PM2.5'].quantile(0.25)
Q3 = combined_data['PM2.5'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

extreme_pollution = combined_data[combined_data['PM2.5'] > upper_bound]
extreme_times = extreme_pollution.groupby('station')['PM2.5'].idxmax()
extreme_times_df = pd.DataFrame(extreme_times).reset_index()
extreme_times_df.columns = ['station', 'datetime']
extreme_times_df['datetime'] = pd.to_datetime(extreme_times_df['datetime'])

extreme_weather = combined_data.loc['2017-02-14':'2017-02-16']
weather_summary = extreme_weather.groupby('datetime')[['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']].mean()

    # Judul aplikasi
st.title('Terjadi Polusi Udara Ekstrem')

    # Menampilkan waktu dengan PM2.5 tertinggi per stasiun
st.subheader('Waktu dengan PM2.5 Tertinggi per Stasiun')
fig1, ax1 = plt.subplots(figsize=(15, 8))
sns.barplot(x='station', y='datetime', data=extreme_times_df, ax=ax1)
ax1.set_title('Waktu dengan PM2.5 Tertinggi per Stasiun')
ax1.set_xlabel('Stasiun')
ax1.set_ylabel('Waktu')
ax1.tick_params(axis='x', rotation=45)
st.pyplot(fig1)

    # Menampilkan rangkuman kondisi cuaca di sekitar waktu polusi ekstrem
st.subheader('Rangkuman Kondisi Cuaca di Sekitar Waktu Polusi Ekstrem')
fig2, ax2 = plt.subplots(figsize=(15, 10))

    # Plotting TEMP
plt.subplot(3, 2, 1)
sns.lineplot(data=weather_summary, x=weather_summary.index, y='TEMP')
plt.title('Temperature (TEMP)')

    # Plotting PRES
plt.subplot(3, 2, 2)
sns.lineplot(data=weather_summary, x=weather_summary.index, y='PRES')
plt.title('Pressure (PRES)')

    # Plotting DEWP
plt.subplot(3, 2, 3)
sns.lineplot(data=weather_summary, x=weather_summary.index, y='DEWP')
plt.title('Dew Point (DEWP)')

    # Plotting RAIN
plt.subplot(3, 2, 4)
sns.lineplot(data=weather_summary, x=weather_summary.index, y='RAIN')
plt.title('Rain (RAIN)')

    # Plotting WSPM
plt.subplot(3, 2, 5)
sns.lineplot(data=weather_summary, x=weather_summary.index, y='WSPM')
plt.title('Wind Speed (WSPM)')

plt.tight_layout()
st.pyplot(fig2)
