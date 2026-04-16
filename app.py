import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="Metin Değerlendirme Sistemi", layout="centered")

# 2. Google Sheets Bağlantısı
# Not: Secrets kısmına spreadsheet linkini eklemeyi unutmayın!
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Görsel Tasarım (CSS)
st.markdown("""
    <style>
    .browser-box {
        border: 1px solid #d1d1d1;
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        overflow: hidden;
        background: #ffffff;
        margin-bottom: 25px;
    }
    .browser-header {
        background: #f1f1f1;
        padding: 12px 18px;
        display: flex;
        align-items: center;
        border-bottom: 1px solid #d1d1d1;
    }
    .dot { height: 12px; width: 12px; border-radius: 50%; display: inline-block; margin-right: 6px; }
    .address-bar {
        background: white;
        flex-grow: 1;
        margin-left: 15px;
        border-radius: 20px;
        padding: 4px 15px;
        font-size: 13px;
        color: #777;
        border: 1px solid #ddd;
        text-align: left;
    }
    .content {
        padding: 40px;
        line-height: 1.8;
        color: #2c3e50;
        font-family: 'Georgia', serif;
        font-size: 18px;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Durum Yönetimi (Session State)
if 'is_started' not in st.session_state:
    st.session_state.is_started = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""

# --- EKRAN 1: GİRİŞ ---
if not st.session_state.is_started:
    st.title("Değerlendirme Testi Giriş Paneli")
    st.write("Lütfen devam etmek için bilgilerinizi giriniz.")
    
    ad_soyad = st.text_input("Adınız Soyadınız:", placeholder="Örn: Ahmet Yılmaz")
    
    if st.button("Sisteme Giriş Yap"):
        if ad_soyad:
            try:
                # Daha önce katılıp katılmadığını kontrol et
                df = conn.read(ttl=0) # ttl=0 önbelleği temiz tutar, güncel veriyi çeker
                
                if not df.empty and ad_soyad in df['ad_soyad'].values:
                    st.error("Bu isimle daha önce katılım sağlandığı görülüyor. Bir kullanıcı sadece bir kez katılabilir.")
                else:
                    st.session_state.user_name = ad_soyad
                    st.session_state.is_started = True
                    st.rerun()
            except Exception as e:
                # Tablo tamamen boşsa hata verebilir, bu durumda girişe izin ver
                st.session_state.user_name = ad_soyad
                st.session_state.is_started = True
                st.rerun()
        else:
            st.warning("Lütfen adınızı ve soyadınızı boş bırakmayınız.")

# --- EKRAN 2: TEST VE DEĞERLENDİRME ---
else:
    st.info(f"Hoş geldiniz, **{st.session_state.user_name}**")
    
    # SAHTE TARAYICI GÖRÜNÜMÜ
    st.markdown(f"""
    <div class="browser-box">
        <div class="browser-header">
            <span class="dot" style="background:#ff5f56"></span>
            <span class="dot" style="background:#ffbd2e"></span>
            <span class="dot" style="background:#27c93f"></span>
            <div class="address-bar">https://www.haber-arsivi.com/guncel/makale-id-124</div>
        </div>
        <div class="content">
            <h1 style="font-size: 26px; margin-bottom: 20px;">Yapay Zeka ve Gelecek</h1>
            <p>
                Buraya değerlendirilmesini istediğiniz asıl metni yapıştırın. 
                Bu metin, yukarıdaki tasarım sayesinde öğrenciye gerçek bir 
                web sitesinden makale okuyormuş hissi verecektir. 
                Metin içinde <b>kalın harfler</b> veya <i>italik</i> vurgular kullanabilirsiniz.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Değerlendirme")
    puanlama = st.select_slider(
        "Okuduğunuz metnin güvenirliğini 1 (En Düşük) ile 6 (En Yüksek) arasında puanlayınız:",
        options=[1, 2, 3, 4, 5, 6],
        value=3
    )

    if st.button("Yanıtı Kaydet ve Bitir"):
        with st.spinner("Verileriniz kaydediliyor..."):
            try:
                # Mevcut veriyi çek
                df = conn.read(ttl=0)
                
                # Yeni satırı hazırla
                yeni_veri = pd.DataFrame([{
                    "tarih": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "ad_soyad": st.session_state.user_name,
                    "puan": puanlama
                }])
                
                # Veriyi birleştir ve güncelle
                if df.empty:
                    updated_df = yeni_veri
                else:
                    updated_df = pd.concat([df, yeni_veri], ignore_index=True)
                
                conn.update(data=updated_df)
                
                st.success("Tebrikler! Yanıtınız başarıyla kaydedildi.")
                st.balloons()
                
                # Kullanıcıyı başa döndürmek veya oturumu kapatmak için
                if st.button("Yeni Katılımcı İçin Çıkış Yap"):
                    st.session_state.is_started = False
                    st.rerun()
                    
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")
