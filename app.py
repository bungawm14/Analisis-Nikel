import streamlit as st
import numpy as np
import pandas as pd

# --- CONFIG HALAMAN (Wajib di Baris Pertama) ---
st.set_page_config(
    page_title="PBL 3 - Ekonomi SDA & Lingkungan",
    page_icon="📊",
    layout="wide"
)

# --- CUSTOM CSS (Optimasi Header Elegan) ---
st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        margin-bottom: 20px;
    }
    .main-title {
        font-size: 32px !important;
        font-weight: 800;
        color: #1F2937;
        margin-bottom: 0px;
    }
    .sub-title {
        font-size: 18px !important;
        color: #6B7280;
        margin-top: 0px;
        font-weight: 500;
    }
    .info-box {
        background-color: #F8FAFC;
        padding: 25px;
        border-left: 6px solid #1E3A8A;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .info-table td {
        padding: 4px 8px;
        font-size: 16px;
        color: #374151;
        border: none !important;
    }
    .label-cell {
        font-weight: 700;
        color: #111827;
        width: 160px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER SECTION ---
col_logo, col_text = st.columns([1, 5])

with col_logo:
    st.write("##") 
    try:
        st.image("Lambang-Universitas_Islam_Bandung.png", width=150)
    except:
        st.image("https://upload.wikimedia.org/wikipedia/id/2/23/Lambang_Unisba.png", width=150)

with col_text:
    st.markdown('<p class="main-title">Analisis Intertemporal Sumber Daya Alam</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Program Studi Ekonomi Pembangunan - UNISBA</p>', unsafe_allow_html=True)
    
    # BOX IDENTITAS (Tulisan 'Data Nikel' Dihapus)
    st.markdown(f"""
    <div class="info-box">
        <table class="info-table" style="width:100%;">
            <tr>
                <td class="label-cell">KELOMPOK</td>
                <td>: 2</td>
            </tr>
            <tr>
                <td class="label-cell" style="vertical-align: top;">ANGGOTA</td>
                <td style="padding-top: 0px;">
                    <ul style="list-style-type: none; padding: 0; margin: 0;">
                        <li>: 1. Radea Rahman Dwiyana (10090224001)</li>
                        <li>&nbsp;&nbsp; 2. Bunga Wiati Manaki (10090224026)</li>
                        <li>&nbsp;&nbsp; 3. Shidqi Alhamdani Mieftah (10090224032)</li>
                    </ul>
                </td>
            </tr>
            <tr>
                <td class="label-cell">DOSEN</td>
                <td>: Yuhka Sundaya, S.E., M.Si.</td>
            </tr>
            <tr>
                <td class="label-cell">MATA KULIAH</td>
                <td>: Ekonomi SDA dan Lingkungan</td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)

st.write("---")

# --- BAGIAN 1: MEMBACA DATA ---
st.title("📊 Simulasi Alokasi Intertemporal & Dinamika Nikel")
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
    # Parameter disesuaikan dengan laporan [cite: 159, 160, 165]
    a = st.number_input("Intersep Permintaan (a)", value=86500000.0, format="%.1f")
    b = st.number_input("Slope Permintaan (b)", value=0.0702729, format="%.7f")
    mc = st.number_input("Marginal Cost (MC)", value=176566741.2, format="%.1f")
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
        muc_t = lambda_0 * np.exp(r * t) # Aturan Hotelling [cite: 167, 172]
        q_t = (a - (mc/1000000) - (muc_t/1000000)) / (slope_eff * 100) 
        q_t = max(0, q_t)
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        hasil.append({
            "Tahun": t, 
            "MUC": round(muc_t, 2), 
            "Produksi (Ton)": round(produksi, 2), 
            "Sisa Stok (Ton)": round(stok_sisa, 2)
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
    st.write("Tingkat diskonto 5% mencerminkan keseimbangan antar generasi[cite: 169].")
with col_b:
    st.warning(f"**Fenomena Green Paradox:**")
    st.write(f"Dengan r sebesar {r*100:.0f}%, kenaikan r akan mempercepat eksploitasi dan menurunkan nilai T*[cite: 178, 180].")
