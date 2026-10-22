# Bike Sharing Dashboard 🚲

Dashboard interaktif untuk menganalisis data penyewaan sepeda tahun 2011–2012 menggunakan Streamlit.

## Setup Environment - Anaconda

```bash
conda create --name bike-sharing python=3.9
conda activate bike-sharing
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal

```bash
mkdir bike-sharing
cd bike-sharing
pip install -r requirements.txt
```

Pastikan file `dashboard.py`, `day.csv`, `hour.csv`, dan `requirements.txt` berada dalam folder yang sama.

## Run Streamlit App

```bash
streamlit run dashboard.py
```

## Fitur Dashboard

- Melihat total dan rata-rata penyewaan sepeda.
- Memfilter data berdasarkan tahun.
- Menganalisis penyewaan berdasarkan bulan.
- Menganalisis hubungan kategori cuaca dengan penyewaan.
- Melihat pola penyewaan berdasarkan jam.
- Membandingkan rata-rata penyewaan berdasarkan musim.

## Dataset

Dataset yang digunakan adalah Bike Sharing Dataset yang terdiri dari `day.csv` dan `hour.csv`.

## Tools

- Python
- Pandas
- Matplotlib
- Seaborn
- Streamlit
