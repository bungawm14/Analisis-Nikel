print("Halo, saya sedang mengerjakan Tugas PBL 3!")
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Konfigurasi Tampilan (User Friendly)
st.set_page_config(page_title="Simulasi PBL 3 - Ekonomi SDA", layout="wide")
st.title("📊 Simulasi Alokasi Intertemporal Sumber Daya Nikel")
st.markdown("Aplikasi ini mensimulasikan ekstraksi optimal berdasarkan Aturan Hotelling.")

# 1. Input Parameter di Sidebar (Data dari Modul Praktikum)
with st.sidebar:
    st.header("⚙️ Konfigurasi Parameter")
    a = st.number_input("Intersep Permintaan (a)", value=1090000000.0) # [cite: 120, 129]
    b = st.number_input("Slope Permintaan (b)", value=12.31475)       # [cite: 120, 129]
    mc = st.number_input("Marginal Cost (MC)", value=143804.5653)    # [cite: 125, 129]
    r = st.slider("Tingkat Diskonto (r)", 0.01, 0.20, 0.05)           # [cite: 129, 149]
    stok_awal = st.number_input("Total Cadangan (S)", value=20000.0) # [cite: 130]
    lambda_0 = st.number_input("MUC Awal (λ0)", value=15163.0)       # [cite: 131]

# 2. Fungsi Logika Perhitungan per Struktur Pasar
def jalankan_simulasi(struktur):
    tahun = np.arange(0, 11) # Simulasi 10 tahun [cite: 141]
    
    # Penyesuaian MR berdasarkan Teori Ekonomi:
    # Monopoli memiliki MR yang lebih curam (2x slope b) dibanding Persaingan 
    if struktur == "Monopoli":
        slope_eff = b * 2
    elif struktur == "Oligopoli":
        slope_eff = b * 1.5
    else: # Persaingan Sempurna
        slope_eff = b
        
    hasil = []
    stok_sisa = stok_awal
    
    for t in tahun:
        # Aturan Hotelling: MUC tumbuh eksponensial [cite: 133, 180]
        muc_t = lambda_0 * np.exp(r * t) 
        
        # Rumus Ekstraksi: q = (a - MC - MUC) / slope
        q_t = (a - mc - muc_t) / slope_eff
        q_t = max(0, q_t) # Produksi tidak bisa negatif
        
        # Update Stok
        produksi = min(q_t, stok_sisa)
        stok_sisa -= produksi
        
        hasil.append({
            "Tahun": t,
            "MUC": round(muc_t, 2),
            "Harga": round(a - b * produksi, 2),
            "Produksi": round(produksi, 2),
            "Sisa Stok": round(stok_sisa, 2)
        })
    return pd.DataFrame(hasil)

# 3. Menampilkan Informasi Dampak (Poin 3.a, 3.b, 3.c)
tab1, tab2, tab3 = st.tabs(["Persaingan Sempurna", "Monopoli", "Oligopoli"])

with tab1:
    df_p = jalankan_simulasi("Persaingan")
    st.dataframe(df_p, use_container_width=True)

with tab2:
    df_m = jalankan_simulasi("Monopoli")
    st.dataframe(df_m, use_container_width=True)

with tab3:
    df_o = jalankan_simulasi("Oligopoli")
    st.dataframe(df_o, use_container_width=True)

# 4. Grafik Perbandingan (User Friendly)
st.subheader("📈 Grafik Tren Ekstraksi dan Sisa Stok")
col1, col2 = st.columns(2)
with col1:
    st.line_chart(df_p.set_index("Tahun")[["Produksi"]].rename(columns={"Produksi": "Persaingan"}))
with col2:
    st.line_chart(df_p.set_index("Tahun")[["Sisa Stok"]])

# 5. Analisis Green Paradox (Poin 4)
st.divider()
st.subheader("🌿 Analisis Green Paradox")
st.info(f"""
**Teori:** Ketika tingkat diskonto ($r$) dinaikkan (saat ini: {r*100:.0f}%), nilai masa depan kehilangan bobotnya secara drastis[cite: 151]. 
Hal ini menyebabkan produsen melakukan eksploitasi lebih cepat dan agresif di tahun-tahun awal[cite: 153]. 
Dampaknya, waktu habis cadangan ($T^*$) akan mengecil, yang mencerminkan perilaku eksploitasi dibandingkan keberlanjutan.
""")