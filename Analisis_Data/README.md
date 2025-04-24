# Air Quality Dashboard ✨

Project ini adalah dashboard visualisasi data kualitas udara menggunakan Streamlit.

## Struktur Proyek
```
submission
├───dashboard
|   ├───cleaned_combined_data.csv
|   └───Air_Quality.py
├───PRSA_Data_20130301-20170228
|   ├───data_1.csv
|   └───data_2.csv
├───Proyek_Analisis_Data_Air_Quality.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Persiapan Lingkungan - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt
```

## Persiapan Lingkungan - Shell/Terminal (Tanpa Anaconda)
```bash
# Buat direktori proyek
mkdir air_quality
cd air_quality

# Buat virtual environment
python -m venv env

# Aktivasi environment
# Untuk Linux/Mac
source env/bin/activate
# Untuk Windows (PowerShell)
# .\env\Scripts\activate

# Install dependensi
pip install -r requirements.txt
```

## Menjalankan Aplikasi Streamlit
```bash
cd dashboard
streamlit run Air_Quality.py
```

## Catatan
- Pastikan file `requirements.txt` berisi semua library yang dibutuhkan.
- File `cleaned_combined_data.csv` digunakan sebagai sumber data utama dalam visualisasi.
- `Proyek_Analisis_Data_Air_Quality.ipynb` berisi proses data wrangling dan analisis data sesuai format.
- 'data_Wrangling.ipynb' dan 'Exploratory.ipynb' berisi proses saya dalam menyelesaikan proyek ini sebelum masuk kedalam format yang diberikan.
- Jangan lupa mengaktifkan environment sebelum menjalankan perintah apapun.
- File `url.txt` berisi referensi atau sumber data yang digunakan dalam proyek ini.

Selamat mencoba! 🚀

