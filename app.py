import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG HALAMAN (Wajib di Baris Pertama) ---
st.set_page_config(
    page_title="PBL 3 - Ekonomi SDA & Lingkungan",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM CSS (Untuk Sentuhan Elegan) ---
st.markdown("""
    <style>
    .main-title {
        font-size: 38px !important;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 20px !important;
        color: #4B5563;
        margin-top: -10px;
        margin-bottom: 20px;
    }
    .info-card {
        background-color: #F3F4F6;
        padding: 20px;
        border-left: 5px solid #1E3A8A;
        border-radius: 5px;
        margin-bottom: 25px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
# Menggunakan ratio 1:4 agar logo tidak terlalu dominan tapi tetap jelas
col_logo, col_text = st.columns([1, 4])

with col_logo:
    try:
        # Menampilkan logo dengan padding atas agar sejajar dengan teks
        st.write("") 
        st.image("Lambang-Universitas_Islam_Bandung.png", width=140)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=140)

with col_text:
    st.markdown('<p class="main-title">Analisis Intertemporal Sumber Daya Alam</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Program Studi Ekonomi Pembangunan - UNISBA</p>', unsafe_allow_html=True)
    
    # Identitas dalam box yang elegan menggunakan columns di dalam box
    with st.container():
        st.markdown("""
        <div class="info-card">
            <table style="width:100%; border:none; border-collapse: collapse;">
                <tr style="border:none;">
                    <td style="width:15%; font-weight:bold; vertical-align:top; border:none;">KELOMPOK</td>
                    <td style="border:none;">: 2 - Data Nikel</td>
                </tr>
                <tr style="border:none;">
                    <td style="font-weight:bold; vertical-align:top; border:none;">ANGGOTA</td>
                    <td style="border:none;">: Radea Rahman Dwiyana, Bunga Wiati Manaki, Shidqi Alhamdani Mieftah</td>
                </tr>
                <tr style="border:none;">
                    <td style="font-weight:bold; vertical-align:top; border:none;">DOSEN</td>
                    <td style="border:none;">: Yuhka Sundaya, S.E., M.Si.</td>
                </tr>
                <tr style="border:none;">
                    <td style="font-weight:bold; vertical-align:top; border:none;">MATA KULIAH</td>
                    <td style="border:none;">: Ekonomi SDA dan Lingkungan</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

st.divider()
st.title("📊 Simulasi Alokasi Intertemporal & Dinamika Nikel")

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
    st.markdown("---")
    a = st.number_input("Intersep Permintaan (a)", value=1090000000.0, format="%.2f")
    b = st.number_input("Slope Permintaan (b)", value=12.31, format="%.2f")
    mc = st.number_input("Marginal Cost (MC)", value=143804.57, format="%.2f")
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
        hasil.append({
            "Tahun": t, 
            "MUC": round(muc_t, 2), 
            "Produksi": round(produksi, 2), 
            "Sisa Stok": round(stok_sisa, 2)
        })
    return pd.DataFrame(hasil)

# --- BAGIAN 4: OUTPUT ---
st.subheader("2. Hasil Simulasi Per Struktur Pasar")
tab1, tab2, tab3 = st.tabs(["🏛️ Persaingan Sempurna", "🏢 Monopoli", "🏪 Oligopoli"])

with tab1:
    st.table(jalankan_simulasi("Persaingan"))

with tab2:
    st.table(jalankan_simulasi("Monopoli"))

with tab3:
    st.table(jalankan_simulasi("Oligopoli"))

st.divider()
st.subheader("3. Analisis Ekonomi")
col_a, col_b = st.columns(2)
with col_a:
    st.info(f"**Tingkat Diskonto (r): {r*100:.0f}%**")
with col_b:
    st.warning(f"**Fenomena Green Paradox:** Dengan r sebesar {r*100:.0f}%, produsen cenderung mempercepat ekstraksi hari ini karena nilai uang di masa depan menyusut lebih cepat.")
