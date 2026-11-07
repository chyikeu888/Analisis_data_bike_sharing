# Bike Sharing Data Analysis Project

Proyek analisis data penyewaan sepeda menggunakan Bike Sharing Dataset periode 2011–2012. Proyek ini mencakup Data Wrangling, EDA, visualisasi, kesimpulan, rekomendasi, dan dashboard Streamlit.

## Struktur Folder

```text
Bike_Sharing_Project_Final/
├── Proyek_Analisis_Data_Final.ipynb
├── day.csv
├── hour.csv
├── requirements.txt
├── README.md
└── dashboard/
    ├── dashboard.py
    └── data/
        ├── day_clean.csv
        └── hour_clean.csv
```

## Persyaratan

- Python 3.10 atau lebih baru
- pip
- Jupyter Notebook untuk menjalankan notebook
- Streamlit untuk menjalankan dashboard

## Instalasi

Jalankan perintah dari direktori utama proyek:

```bash
python -m venv .venv
```

Aktifkan virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install seluruh package:

```bash
pip install -r requirements.txt
```

## Menjalankan Notebook

Pastikan `day.csv` dan `hour.csv` berada di direktori utama proyek, sejajar dengan file notebook.

Jalankan:

```bash
jupyter notebook Proyek_Analisis_Data_Final.ipynb
```

Kemudian jalankan seluruh cell dari atas ke bawah. Pada tahap Cleaning Data, notebook akan membuat atau memperbarui file berikut:

- `dashboard/data/day_clean.csv`
- `dashboard/data/hour_clean.csv`

Dashboard menggunakan kedua file hasil cleaning tersebut, bukan dataset mentah.

## Menjalankan Dashboard Streamlit

Setelah dependencies terpasang dan file hasil cleaning tersedia, masuk ke folder dashboard:

```bash
cd dashboard
streamlit run dashboard.py
```

Jika terminal berada di dalam folder `dashboard` dan dependencies belum dipasang, jalankan:

```bash
pip install -r ../requirements.txt
```

Streamlit akan menampilkan alamat lokal, biasanya `http://localhost:8501`. Buka alamat tersebut melalui browser.

## Fitur Dashboard

- Filter berdasarkan tahun dan bulan.
- Ringkasan total penyewaan.
- Rata-rata penyewaan harian.
- Total penyewaan pengguna terdaftar dan kasual.
- Perbandingan total dan rata-rata penyewaan bulanan.
- Rata-rata penyewaan berdasarkan kondisi cuaca.
- Pola penyewaan per jam pada hari kerja dan nonkerja.
- Perbandingan total dan rata-rata penyewaan berdasarkan musim.
- Hubungan suhu dan jumlah penyewaan.

## Dataset

Bike Sharing Dataset, terdiri dari `day.csv` dan `hour.csv`.

Sumber dataset: https://www.kaggle.com/datasets/lakshmi25npathi/bike-sharing-dataset

## Catatan

- Mapping kategori dilakukan pada tahap Cleaning Data di notebook.
- Kandidat outlier IQR dievaluasi berdasarkan rentang domain dan konsistensi data. Nilai penyewaan yang valid tidak dihapus hanya karena melewati batas IQR.
- Jika dataset mentah berubah, jalankan ulang seluruh notebook agar dashboard menggunakan dataset hasil cleaning terbaru.
