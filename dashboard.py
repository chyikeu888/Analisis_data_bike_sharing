from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st


st.set_page_config(
    page_title="Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide"
)

DATA_DIR = Path(__file__).resolve().parent / "data"


@st.cache_data
def load_clean_data():
    day_path = DATA_DIR / "day_clean.csv"
    hour_path = DATA_DIR / "hour_clean.csv"

    if not day_path.exists() or not hour_path.exists():
        raise FileNotFoundError(
            "Dataset hasil cleaning tidak ditemukan. "
            "Jalankan seluruh notebook terlebih dahulu agar "
            "day_clean.csv dan hour_clean.csv terbentuk di folder dashboard/data."
        )

    day = pd.read_csv(day_path, parse_dates=["date"])
    hour = pd.read_csv(hour_path, parse_dates=["date"])
    return day, hour


try:
    day_df, hour_df = load_clean_data()
except (FileNotFoundError, ValueError) as error:
    st.error(str(error))
    st.stop()


st.title("🚲 Bike Sharing Dashboard")
st.write(
    "Dashboard interaktif untuk mengeksplorasi pola penyewaan sepeda "
    "selama periode 2011–2012."
)
st.caption(
    "Sumber: Bike Sharing Dataset. Seluruh visualisasi menggunakan "
    "dataset yang telah melalui proses data cleaning pada notebook."
)

# Sidebar filters
st.sidebar.header("Filter Data")

available_years = sorted(day_df["year"].dropna().unique().tolist())
available_months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

selected_years = st.sidebar.multiselect(
    "Pilih tahun",
    options=available_years,
    default=available_years
)

selected_months = st.sidebar.multiselect(
    "Pilih bulan",
    options=available_months,
    default=available_months
)

if not selected_years or not selected_months:
    st.warning("Pilih minimal satu tahun dan satu bulan untuk menampilkan analisis.")
    st.stop()

day_filtered = day_df[
    day_df["year"].isin(selected_years)
    & day_df["month_name"].isin(selected_months)
].copy()

hour_filtered = hour_df[
    hour_df["year"].isin(selected_years)
    & hour_df["month_name"].isin(selected_months)
].copy()

if day_filtered.empty or hour_filtered.empty:
    st.warning("Tidak ada data untuk kombinasi filter yang dipilih.")
    st.stop()


# KPI section
total_rentals = int(day_filtered["total_rentals"].sum())
average_daily_rentals = day_filtered["total_rentals"].mean()
registered_rentals = int(day_filtered["registered_rentals"].sum())
casual_rentals = int(day_filtered["casual_rentals"].sum())

st.subheader("Ringkasan Penyewaan")
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Total Penyewaan", f"{total_rentals:,.0f}")
kpi2.metric("Rata-rata Penyewaan Harian", f"{average_daily_rentals:,.0f}")
kpi3.metric("Penyewaan Pengguna Terdaftar", f"{registered_rentals:,.0f}")
kpi4.metric("Penyewaan Pengguna Kasual", f"{casual_rentals:,.0f}")


# Monthly analysis
st.subheader("Pola Penyewaan Bulanan")

monthly_summary = (
    day_filtered
    .groupby(["year", "month_number", "month_name"], as_index=False)
    .agg(
        total_rentals=("total_rentals", "sum"),
        average_daily_rentals=("total_rentals", "mean")
    )
    .sort_values(["year", "month_number"])
)
monthly_summary["year_label"] = monthly_summary["year"].astype(str)

left, right = st.columns(2)

with left:
    fig_month_total = px.line(
        monthly_summary,
        x="month_name",
        y="total_rentals",
        color="year_label",
        markers=True,
        category_orders={"month_name": available_months},
        labels={
            "month_name": "Bulan",
            "total_rentals": "Total Penyewaan",
            "year_label": "Tahun"
        },
        title="Total Penyewaan per Bulan"
    )
    fig_month_total.update_layout(legend_title_text="Tahun")
    st.plotly_chart(fig_month_total, use_container_width=True)

with right:
    fig_month_average = px.line(
        monthly_summary,
        x="month_name",
        y="average_daily_rentals",
        color="year_label",
        markers=True,
        category_orders={"month_name": available_months},
        labels={
            "month_name": "Bulan",
            "average_daily_rentals": "Rata-rata Penyewaan Harian",
            "year_label": "Tahun"
        },
        title="Rata-rata Penyewaan Harian per Bulan"
    )
    fig_month_average.update_layout(legend_title_text="Tahun")
    st.plotly_chart(fig_month_average, use_container_width=True)


# Weather analysis
st.subheader("Penyewaan Berdasarkan Kondisi Cuaca")

weather_summary = (
    day_filtered
    .groupby("weather_condition", as_index=False)
    .agg(
        average_rentals=("total_rentals", "mean"),
        total_rentals=("total_rentals", "sum")
    )
    .sort_values("average_rentals", ascending=False)
)

fig_weather = px.bar(
    weather_summary,
    x="weather_condition",
    y="average_rentals",
    labels={
        "weather_condition": "Kondisi Cuaca",
        "average_rentals": "Rata-rata Penyewaan"
    },
    title="Rata-rata Penyewaan Menurut Kondisi Cuaca",
    text_auto=".0f"
)
st.plotly_chart(fig_weather, use_container_width=True)


# Hourly analysis
st.subheader("Pola Penyewaan Berdasarkan Jam dan Jenis Hari")

hourly_summary = (
    hour_filtered
    .groupby(["day_type", "hour"], as_index=False)
    .agg(average_rentals=("total_rentals", "mean"))
)

fig_hourly = px.line(
    hourly_summary,
    x="hour",
    y="average_rentals",
    color="day_type",
    markers=True,
    labels={
        "hour": "Jam",
        "average_rentals": "Rata-rata Penyewaan",
        "day_type": "Jenis Hari"
    },
    title="Rata-rata Penyewaan per Jam"
)
fig_hourly.update_xaxes(dtick=1)
st.plotly_chart(fig_hourly, use_container_width=True)


# Seasonal analysis
st.subheader("Penyewaan Berdasarkan Musim")

season_order = ["Spring", "Summer", "Fall", "Winter"]
season_summary = (
    day_filtered
    .groupby(["year", "season_name"], as_index=False)
    .agg(
        total_rentals=("total_rentals", "sum"),
        average_daily_rentals=("total_rentals", "mean")
    )
)
season_summary["year_label"] = season_summary["year"].astype(str)

left, right = st.columns(2)

with left:
    fig_season_total = px.bar(
        season_summary,
        x="season_name",
        y="total_rentals",
        color="year_label",
        barmode="group",
        category_orders={"season_name": season_order},
        labels={
            "season_name": "Musim",
            "total_rentals": "Total Penyewaan",
            "year_label": "Tahun"
        },
        title="Total Penyewaan Berdasarkan Musim"
    )
    st.plotly_chart(fig_season_total, use_container_width=True)

with right:
    fig_season_average = px.bar(
        season_summary,
        x="season_name",
        y="average_daily_rentals",
        color="year_label",
        barmode="group",
        category_orders={"season_name": season_order},
        labels={
            "season_name": "Musim",
            "average_daily_rentals": "Rata-rata Penyewaan Harian",
            "year_label": "Tahun"
        },
        title="Rata-rata Penyewaan Harian Berdasarkan Musim"
    )
    st.plotly_chart(fig_season_average, use_container_width=True)


# Environment relationship
st.subheader("Hubungan Suhu dan Jumlah Penyewaan")

fig_temperature = px.scatter(
    day_filtered,
    x="temperature",
    y="total_rentals",
    color="weather_condition",
    opacity=0.65,
    labels={
        "temperature": "Suhu (ternormalisasi)",
        "total_rentals": "Jumlah Penyewaan",
        "weather_condition": "Kondisi Cuaca"
    },
    title="Suhu dan Jumlah Penyewaan Sepeda"
)
st.plotly_chart(fig_temperature, use_container_width=True)


with st.expander("Lihat ringkasan data bulanan"):
    st.dataframe(
        monthly_summary.drop(columns=["year_label"]),
        use_container_width=True,
        hide_index=True
    )

st.caption(
    "Catatan: hubungan antara cuaca, suhu, kelembapan, dan penyewaan "
    "menunjukkan asosiasi pada data historis, bukan bukti sebab-akibat."
)
