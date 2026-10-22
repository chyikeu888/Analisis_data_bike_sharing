import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

@st.cache_data
def load_data():
    day = pd.read_csv("day.csv")
    hour = pd.read_csv("hour.csv")
    day["dteday"] = pd.to_datetime(day["dteday"])
    hour["dteday"] = pd.to_datetime(hour["dteday"])
    day["tahun"] = day["yr"].map({0: 2011, 1: 2012})
    hour["tahun"] = hour["yr"].map({0: 2011, 1: 2012})
    return day, hour

day_df, hour_df = load_data()

st.title("🚲 Bike Sharing Dashboard")
st.write("Analisis penyewaan sepeda tahun 2011–2012.")

tahun = st.sidebar.selectbox("Pilih Tahun", ["Semua Tahun", 2011, 2012])

if tahun != "Semua Tahun":
    day_df = day_df[day_df["tahun"] == tahun]
    hour_df = hour_df[hour_df["tahun"] == tahun]

col1, col2, col3 = st.columns(3)
col1.metric("Total Penyewaan", f"{day_df['cnt'].sum():,}")
col2.metric("Rata-rata Harian", f"{day_df['cnt'].mean():,.0f}")
col3.metric("Total Pengguna Terdaftar", f"{day_df['registered'].sum():,}")

st.subheader("Penyewaan Sepeda per Bulan")
monthly = day_df.groupby("mnth")["cnt"].sum()
fig, ax = plt.subplots()
monthly.plot(kind="line", marker="o", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Total Penyewaan")
ax.set_xticks(range(1, 13))
st.pyplot(fig)
plt.close(fig)

st.subheader("Penyewaan Berdasarkan Cuaca")
weather = day_df.groupby("weathersit")["cnt"].mean()
fig, ax = plt.subplots()
weather.plot(kind="bar", ax=ax)
ax.set_xlabel("Kategori Cuaca")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)
plt.close(fig)

st.subheader("Penyewaan Berdasarkan Jam")
hourly = hour_df.groupby("hr")["cnt"].mean()
fig, ax = plt.subplots()
hourly.plot(kind="line", marker="o", ax=ax)
ax.set_xlabel("Jam")
ax.set_ylabel("Rata-rata Penyewaan")
ax.set_xticks(range(0, 24, 2))
st.pyplot(fig)
plt.close(fig)

st.subheader("Penyewaan Berdasarkan Musim")
season = day_df.groupby("season")["cnt"].mean()
fig, ax = plt.subplots()
season.plot(kind="bar", ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Rata-rata Penyewaan")
st.pyplot(fig)
plt.close(fig)

st.caption("Sumber: Bike Sharing Dataset")

