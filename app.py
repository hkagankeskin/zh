import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Araştırma Paneli", layout="centered")

# Bağlantıyı kur (Secrets'tan otomatik okur)
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS Tasarımı
st.markdown("""
    <style>
    .browser-box { border: 1px solid #d1d1d1; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background: white; margin-bottom: 20px;}
    .browser-header { background: #f1f1f1; padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #d1d1d1; }
    .content { padding: 30px; line-height: 1.8; color: #333; font-family: sans-serif; }
    </style>
    """, unsafe_allow_html=True)

if 'is_started' not in st.session_state:
    st.session_state.is_started = False

# --- EKRAN 1: GİRİŞ ---
if not st.session_state.is_started:
    st.title("Değerlendirme Sistemi")
    ad_soyad = st.text_input("Adınız Soyadınız:")
    
    if st.button("Başla"):
        if ad_soyad:
            try:
                # Veriyi çek (ttl=0 önbelleği kapatır)
                df = conn.read(worksheet="Sheet1", ttl=0)
                if not df.empty and ad_soyad in df['ad_soyad'].values:
                    st.error("Bu isimle daha önce katılım sağlandı.")
                else:
                    st.session_state.user_name = ad_soyad
                    st.session_state.is_started = True
                    st.rerun()
            except:
                st.session_state.user_name = ad_soyad
                st.session_state.is_started = True
                st.rerun()
        else:
            st.warning("İsim giriniz.")

# --- EKRAN 2: TEST ---
else:
    st.markdown(f"""
    <div class="browser-box">
        <div class="browser-header"> <span style="color:#ff5f56">●</span> &nbsp; <div style="background:white; flex-grow:1; border-radius:10px; padding:2px 10px; font-size:12px; border:1px solid #ccc;">https://www.haber-portali.com/makale-01</div></div>
        <div class="content">
            <h2>Metin Başlığı</h2>
            <p>Buraya değerlendirilecek metni yazın.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    puan = st.select_slider("Güvenirlik Puanı (1-6):", options=[1, 2, 3, 4, 5, 6])

    if st.button("Gönder"):
        try:
            df = conn.read(worksheet="Sheet1", ttl=0)
            yeni_satir = pd.DataFrame([{"tarih": datetime.now().strftime("%d/%m/%Y %H:%M"), "ad_soyad": st.session_state.user_name, "puan": puan}])
            updated_df = pd.concat([df, yeni_satir], ignore_index=True)
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("Kaydedildi!")
            st.balloons()
            st.session_state.is_started = False
        except Exception as e:
            st.error(f"Hata: {e}")
