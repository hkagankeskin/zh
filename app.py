import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# Sayfa ayarları
st.set_page_config(page_title="Güvenirlik Değerlendirme", layout="centered")

# Google Sheets bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# CSS Tasarımı (Browser Mockup)
st.markdown("""
    <style>
    .browser-box { border: 1px solid #d1d1d1; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); background: white; }
    .browser-header { background: #f1f1f1; padding: 10px; display: flex; align-items: center; border-bottom: 1px solid #d1d1d1; }
    .dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 5px; }
    .address-bar { background: white; flex-grow: 1; margin-left: 10px; border-radius: 15px; padding: 2px 15px; font-size: 12px; color: #888; border: 1px solid #ccc; text-align: left; }
    .content { padding: 30px; line-height: 1.8; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    </style>
    """, unsafe_allow_html=True)

# Oturum Yönetimi
if 'is_started' not in st.session_state:
    st.session_state.is_started = False

# --- GİRİŞ EKRANI ---
if not st.session_state.is_started:
    st.title("Araştırma Katılım Paneli")
    isim = st.text_input("Lütfen Adınızı ve Soyadınızı Giriniz:")
    
    if st.button("Teste Başla"):
        if isim:
            # Daha önce girmiş mi kontrolü (Google Sheets'ten oku)
            existing_data = conn.read(
    spreadsheet="https://docs.google.com/spreadsheets/d/1w9cn8GYm9PvshfpYF-EQ4_ciTsbQhZ5FTSyYtMbZCuQ/edit?usp=sharing",
    worksheet="Sheet1"
            if isim in existing_data["ad_soyad"].values:
                st.error("Bu isimle daha önce bir katılım sağlanmış. Teşekkür ederiz.")
            else:
                st.session_state.user_name = isim
                st.session_state.is_started = True
                st.rerun()
        else:
            st.warning("Devam etmek için isim girmelisiniz.")

# --- TEST EKRANI ---
else:
    st.markdown(f"""
    <div class="browser-box">
        <div class="browser-header">
            <span class="dot" style="background:#ff5f56"></span>
            <span class="dot" style="background:#ffbd2e"></span>
            <span class="dot" style="background:#27c93f"></span>
            <div class="address-bar">https://www.haber-kaynagi.com/arsiv/makale-id-1024</div>
        </div>
        <div class="content">
            <h2 style="margin-top:0">Metin Başlığı Buraya</h2>
            <p>Değerlendirilmesini istediğiniz metni bu alana yapıştırın. 
            Buradaki her şey sanki gerçek bir internet sitesinden okunuyormuş gibi görünecektir.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("---")
    puanlama = st.select_slider(
        "Yukarıdaki metni güvenirlik açısından 1-6 arasında puanlayınız (1: Çok Düşük, 6: Çok Yüksek):",
        options=[1, 2, 3, 4, 5, 6]
    )

    if st.button("Yanıtı Gönder"):
        # Veriyi Hazırla
        new_row = pd.DataFrame([{
            "tarih": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ad_soyad": st.session_state.user_name,
            "puan": puanlama
        }])
        
        # Google Sheets'e Yaz
        updated_df = pd.concat([conn.read(worksheet="Sheet1"), new_row], ignore_index=True)
        conn.update(worksheet="Sheet1", data=updated_df)
        
        st.success("Yanıtınız başarıyla kaydedildi. Katılımınız için teşekkürler!")
        st.balloons()
        st.session_state.is_started = False # Reset
