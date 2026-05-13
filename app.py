import streamlit as st
import numpy as np
import pandas as pd

# --- PERBAIKAN 1: CONFIG WAJIB DI BARIS PERTAMA ---
st.set_page_config(page_title="Simulasi PBL 3 - Ekonomi SDA", layout="wide")

# --- PERBAIKAN 2: HEADER & LOGO (DISAMAKAN DENGAN GITHUB) ---
col1, col2 = st.columns([1, 5])

with col1:
    try:
        # Nama file disesuaikan dengan image_3c8072.png (pakai strip '-')
        st.image("Lambang-Universitas_Islam_Bandung.png", width=120)
    except:
        # Cadangan jika file di GitHub tidak terbaca
        st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=120)

with col2:
    st.markdown("# Analisis Intertemporal Sumber Daya Alam")
    st.markdown("### Program Studi Ekonomi Pembangunan - UNISBA")

# --- PERBAIKAN 3: BOX IDENTITAS KELOMPOK ---
st.info("""
**KELOMPOK 2 - DATA NIKEL**
* **Anggota:** Radea Rahman Dwiyana (10090224001), Bunga Wiati Manaki (10090224026), Shidqi Alhamdani Mieftah (10090224032)
* **Dosen Pengampu:** Yuhka Sundaya, S.E., M.Si.
* **Mata Kuliah:** Ekonomi SDA dan Lingkungan
""")

st.title("📊 Simulasi Alokasi Intertemporal & Dinamika Nikel")
st.divider()

# --- BAGIAN 1: MEMBACA DATA ---
try:
    df_historis = pd.read_csv('data_nikel.csv')
    st.subheader("1. Data Historis Produksi & Harga")
    st.dataframe(df_historis, use_container_width=True)
except Exception as e:
    st.error(f"Gagal memuat data_nikel.csv. Error: {e}")

# --- BAGIAN 2: PARAMETER (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Kontrol Simulasi")
    a = st.number_input("Intersep Permintaan (a)", value=1090000000.0)
    b = st.number_input("Slope Permintaan (b)", value=12.31475)
    mc = st.number_input("Marginal Cost (MC)", value=143804.5653)
    r = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    stok_awal = st.number_input("Total Cadangan (S)", value=20000.0)
    lambda_0 = st.number_input("MUC Awal (λ0)", value=15163.0)

# --- BAGIAN 3: LOGIKA SIMULASI ---
def jalankan_simulasi(struktur):
    tahun_sim = np.arange(0, 11)
    slope_eff = b * 2 if struktur == "Monopoli" else (b * 1.5 if struktur == "Oligopoli" else b)
    hasil = []
    stok_sisa = stok_awal
    for t in tahun_sim:
        muc_t = lambda_0 * np.exp(r * t) # Aturan Hotelling
        q_t = (a - mc - muc_t) / slope_eff
        q_t = max(0, q_t)
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        hasil.append({"Tahun": t, "MUC": round(muc_t, 2), "Produksi": round(produksi, 2), "Sisa Stok": round(stok_sisa, 2)})
    return pd.DataFrame(hasil)

# --- BAGIAN 4: OUTPUT ---
st.subheader("2. Hasil Simulasi Per Struktur Pasar")
tab1, tab2, tab3 = st.tabs(["Persaingan Sempurna", "Monopoli", "Oligopoli"])
with tab1: st.table(jalankan_simulasi("Persaingan"))
with tab2: st.table(jalankan_simulasi("Monopoli"))
with tab3: st.table(jalankan_simulasi("Oligopoli"))

st.divider()
st.subheader("3. Analisis Green Paradox")
st.warning(f"Saat ini r = {r*100:.0f}%. Jika r naik, cadangan habis lebih cepat (Green Paradox).")
