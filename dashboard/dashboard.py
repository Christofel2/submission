import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
day_df = pd.read_csv("D:\Belajar\Python\submission\dashboard\day_data_cleaned.csv", parse_dates=["date"])
hour_df = pd.read_csv("D:\Belajar\Python\submission\dashboard\hour_data_cleaned.csv", parse_dates=["date"])

# Sidebar untuk rentang waktu
st.sidebar.image("https://th.bing.com/th/id/OIP._6ZE9i1hNHDnpzaSvgA8RQHaE8?rs=1&pid=ImgDetMain")
min_date, max_date = day_df["date"].min(), day_df["date"].max()
start_date, end_date = st.sidebar.date_input("Rentang Waktu", [min_date, max_date], min_value=min_date, max_value=max_date)

# Filter data berdasarkan rentang waktu
day_df = day_df[(day_df["date"] >= str(start_date)) & (day_df["date"] <= str(end_date))]
hour_df = hour_df[(hour_df["date"] >= str(start_date)) & (hour_df["date"] <= str(end_date))]

st.title("Dashboard Penyewaan Sepeda")

st.subheader("Tren Penyewaan Sepeda dari 2011 -2012")
# Visualisasi Total Penyewaan per Bulan
monthly_counts = day_df.groupby(day_df["date"].dt.to_period("M"))["count"].sum()
monthly_counts.index = monthly_counts.index.astype(str)
monthly_counts.index = pd.to_datetime(monthly_counts.index)

fig, ax = plt.subplots(figsize=(12, 5))
ax.scatter(monthly_counts.index, monthly_counts.values, c="#90CAF9", s=50, marker='o')
ax.plot(monthly_counts.index, monthly_counts.values, linestyle="-", color="b")
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Tren Penyewaan Sepeda per Bulan")
ax.legend()
st.pyplot(fig)

# Statistik
st.write(f"**Total penyewaan sepeda selama periode ini:** {monthly_counts.sum()}")
st.write(f"**Rata-rata penyewaan sepeda per bulan:** {monthly_counts.mean():.2f}")

# Visualisasi Tren Penyewaan Sepeda per Hari
fig, ax = plt.subplots(figsize=(12, 5))
daily_counts = day_df.groupby(day_df["date"])["count"].sum()
ax.scatter(daily_counts.index, daily_counts.values, c="#90CAF9", s=10, marker='o')
ax.plot(daily_counts.index, daily_counts.values, linestyle="-", color="b")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah Peminjaman")
ax.set_title("Tren Penyewaan Sepeda per Hari")
st.pyplot(fig)

# Menampilkan jumlah total penyewaan dalam rentang waktu
st.write(f"**Total penyewaan sepeda selama periode ini:** {daily_counts.sum()}")
st.write(f"**Rata-rata penyewaan sepeda per hari:** {daily_counts.mean():.2f}")

st.write()
st.subheader("Kondisi Cuaca Penyewa Terbanyak")

# Visualisasi Penyewaan Berdasarkan Cuaca
weather_counts = day_df.groupby("weathersit")["count"].sum().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x="weathersit", y="count", data=weather_counts, ax=ax, palette=["#F39C12", "#BDC3C7"])
ax.set_xlabel("Kondisi Cuaca")
ax.set_ylabel("Total Penyewaan Sepeda")
ax.set_title("Total Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
st.pyplot(fig)

st.subheader("Korelasi Kecepatan Angin,Suhu dan Kelembaban terhadap Jumlah Penyewa")
# Visualisasi Hubungan Variabel
fig, axs = plt.subplots(1, 3, figsize=(15, 5))
sns.scatterplot(data=day_df, x="windspeed", y="count", ax=axs[0])
axs[0].set_title("Kecepatan Angin vs Penyewaan")
sns.scatterplot(data=day_df, x="temp", y="count", ax=axs[1])
axs[1].set_title("Suhu vs Penyewaan")
sns.scatterplot(data=day_df, x="hum", y="count", ax=axs[2])
axs[2].set_title("Kelembaban vs Penyewaan")
st.pyplot(fig)

# Heatmap Korelasi
fig, ax = plt.subplots(figsize=(6, 5))
sns.heatmap(day_df[["windspeed", "hum", "temp", "count"]].corr(), annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_title("Heatmap Korelasi")
st.pyplot(fig)

st.subheader("Jam Dengan Aktivitas Penyewaan Tertinggi dan Terendah")
# Visualisasi Total Penyewaan per Jam
hourly_counts = hour_df.groupby("hour")["count"].sum()
top_5_hours = hourly_counts.nlargest(5).reset_index()
bottom_5_hours = hourly_counts.nsmallest(5).reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(18, 6))
top_colors = ["#FF5733", "#FFC300", "#3498DB", "#2ECC71", "#9B59B6"]  
bottom_colors = ["#1ABC9C", "#F39C12", "#E74C3C", "#8E44AD", "#2E86C1"]

sns.barplot(x="hour", y="count", data=top_5_hours, palette=top_colors, ax=ax[0])
ax[0].set_xlabel("Jam")
ax[0].set_title("Jam dengan Aktivitas Penyewaan Tertinggi")
ax[0].tick_params(axis='x', rotation=45)

sns.barplot(x="hour", y="count", data=bottom_5_hours, palette=bottom_colors, ax=ax[1])
ax[1].set_xlabel("Jam")
ax[1].set_title("Jam dengan Aktivitas Penyewaan Terendah")
ax[1].tick_params(axis='x', rotation=45)

st.pyplot(fig)
