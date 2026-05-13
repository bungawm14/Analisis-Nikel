import streamlit as st
import numpy as np
import pandas as pd

# --- HEADER & IDENTITAS ---
# Membuat dua kolom untuk Logo dan Judul
col1, col2 = st.columns([1, 5])

with col1:
    # Mengambil file logo yang ada di folder yang sama
    try:
st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=120)
    except:
        st.write("Logo Belum Ada")

with col2:
    st.markdown("## Analisis Intertemporal Sumber Daya Alam")
    st.markdown("#### Program Studi Ekonomi Pembangunan - UNISBA")

# Kotak Informasi Anggota & Dosen
st.info("""
**KELOMPOK 2 - DATA NIKEL**
* **Anggota:** Radea Rahman Dwiyana (10090224001), Bunga Wiati Manaki (10090224026), Shidqi Alhamdani Mieftah (10090224032)
* **Dosen Pengampu:** Yuhka Sundaya, S.E., M.Si.
* **Mata Kuliah:** Ekonomi SDA dan Lingkungan
""")
st.divider()
# Judul Utama
st.set_page_config(page_title="Simulasi PBL 3 - Ekonomi SDA", layout="wide")
st.title("📊 Simulasi Alokasi Intertemporal & Dinamika Nikel")

# --- BAGIAN 1: MEMBACA DATA DARI CSV ---
try:
    # Membaca data yang baru kamu buat di VSC
    df_historis = pd.read_csv('data_nikel.csv')
    
    st.subheader("1. Data Historis Produksi & Harga (Modul Tahap 1)")
    st.dataframe(df_historis, use_container_width=True)
except Exception as e:
    st.error(f"Gagal memuat data_nikel.csv. Pastikan file sudah dibuat. Error: {e}")

# --- BAGIAN 2: PARAMETER SIMULASI (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    a = st.number_input("Intersep Permintaan (a)", value=1090000000.0)
    b = st.number_input("Slope Permintaan (b)", value=12.31475)
    mc = st.number_input("Marginal Cost (MC)", value=143804.5653)
    r = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)
    stok_awal = st.number_input("Total Cadangan (S)", value=20000.0)
    lambda_0 = st.number_input("MUC Awal (λ0)", value=15163.0)

# --- BAGIAN 3: LOGIKA SIMULASI (TAHAP 3 MODUL) ---
def jalankan_simulasi(struktur):
    tahun_sim = np.arange(0, 11)
    # Penyesuaian MR berdasarkan struktur pasar
    slope_eff = b * 2 if struktur == "Monopoli" else (b * 1.5 if struktur == "Oligopoli" else b)
    
    hasil = []
    stok_sisa = stok_awal
    for t in tahun_sim:
        muc_t = lambda_0 * np.exp(r * t) # Aturan Hotelling
        q_t = (a - mc - muc_t) / slope_eff
        q_t = max(0, q_t)
        
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        
        hasil.append({
            "Tahun Ke-": t,
            "MUC": round(muc_t, 2),
            "Produksi": round(produksi, 2),
            "Sisa Stok": round(stok_sisa, 2)
        })
    return pd.DataFrame(hasil)

# --- BAGIAN 4: TAMPILAN OUTPUT ---
st.divider()
st.subheader("2. Hasil Simulasi Per Struktur Pasar")
tab1, tab2, tab3 = st.tabs(["Persaingan Sempurna", "Monopoli", "Oligopoli"])

with tab1:
    df_p = jalankan_simulasi("Persaingan")
    st.table(df_p)

with tab2:
    st.table(jalankan_simulasi("Monopoli"))

with tab3:
    st.table(jalankan_simulasi("Oligopoli"))

# --- BAGIAN 5: ANALISIS GREEN PARADOX ---
st.divider()
st.subheader("3. Analisis Green Paradox")
st.warning(f"Saat ini r = {r*100:.0f}%. Semakin tinggi nilai ini, stok akan habis lebih cepat karena produsen melakukan 'race to extract' (perlombaan ekstraksi) untuk memaksimalkan nilai sekarang.")
