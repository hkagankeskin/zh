import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Zekeriya HAMAMCI'NIN Metin Değerlendirme Paneli", layout="centered")

# --- İÇERİK AYARLARI (Burayı istediğiniz gibi doldurun) ---
METINLER = [
    {"baslik": "Metin 1", "icerik": "Birinci metin buraya gelecek...", "url": "haber-portali.com/analiz-1"},
    {"baslik": "Metin 2", "icerik": "İkinci metin buraya gelecek...", "url": "haber-portali.com/analiz-2"},
    {"baslik": "Metin 3", "icerik": "Üçüncü metin buraya gelecek...", "url": "haber-portali.com/analiz-3"},
    {"baslik": "Metin 4", "icerik": "Dördüncü metin buraya gelecek...", "url": "haber-portali.com/analiz-4"}
]

SORULAR = [
    "Bu metindeki bilgilerin doğruluğuna ne derece güveniyorsunuz?",
    "Yazarın bu konudaki uzmanlığına dair algınız nedir?",
    "Metnin dili ne derece nesnel ve tarafsızdır?"
]
# --------------------------------------------------------

# 2. Bağlantı ve Stil
conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("""
    <style>
    .browser-box { border: 1px solid #d1d1d1; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); background: white; margin-bottom: 25px;}
    .browser-header { background: #f1f1f1; padding: 10px 15px; display: flex; align-items: center; border-bottom: 1px solid #d1d1d1; }
    .content { padding: 30px; line-height: 1.7; color: #333; font-family: 'Georgia', serif; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Oturum (Session State) Yönetimi
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'current_text' not in st.session_state: st.session_state.current_text = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# --- EKRAN 1: GİRİŞ ---
if st.session_state.step == "GIRIS":
    st.title("Araştırma Paneli")
    ad = st.text_input("Adınız Soyadınız:")
    if st.button("Başla"):
        if ad:
            # İsim kontrolü
            df = conn.read(worksheet="Sheet1", ttl=0)
            if not df.empty and ad in df['ad_soyad'].values:
                st.error("Bu isimle daha önce katılım sağlandı.")
            else:
                st.session_state.user_name = ad
                st.session_state.step = "TEST"
                st.rerun()
        else: st.warning("İsim gerekli.")

# --- EKRAN 2: TEST SÜRECİ ---
elif st.session_state.step == "TEST":
    idx = st.session_state.current_text
    st.write(f"**Metin {idx + 1} / 4**")
    
    # Browser Görünümü
    st.markdown(f"""
    <div class="browser-box">
        <div class="browser-header">
            <span style="color:#ff5f56">●</span> &nbsp; <div style="background:white; flex-grow:1; border-radius:10px; padding:2px 10px; font-size:12px; border:1px solid #ccc; color:#888;">https://www.{METINLER[idx]['url']}</div>
        </div>
        <div class="content">
            <h2 style="margin-top:0;">{METINLER[idx]['baslik']}</h2>
            <p>{METINLER[idx]['icerik']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sorular
    p1 = st.radio(SORULAR[0], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s1")
    p2 = st.radio(SORULAR[1], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s2")
    p3 = st.radio(SORULAR[2], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s3")

    # İleri Butonu
    if idx < 3:
        if st.button("Sonraki Metin ➔"):
            st.session_state.answers[f"m{idx+1}_s1"] = p1
            st.session_state.answers[f"m{idx+1}_s2"] = p2
            st.session_state.answers[f"m{idx+1}_s3"] = p3
            st.session_state.current_text += 1
            st.rerun()
    else:
        # Son Sayfa: Gönder Butonu
        if st.button("Testi Tamamla ve Gönder"):
            st.session_state.answers["m4_s1"] = p1
            st.session_state.answers["m4_s2"] = p2
            st.session_state.answers["m4_s3"] = p3
            
            # Veri Hazırlama
            try:
                df = conn.read(worksheet="Sheet1", ttl=0)
                all_vals = list(st.session_state.answers.values())
                yeni_satir = {
                    "tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "ad_soyad": st.session_state.user_name,
                }
                # Dinamik olarak m1_s1, m1_s2... şeklinde ekle
                yeni_satir.update(st.session_state.answers)
                yeni_satir["genel_ortalama"] = round(sum(all_vals) / len(all_vals), 2)
                
                updated_df = pd.concat([df, pd.DataFrame([yeni_satir])], ignore_index=True)
                conn.update(worksheet="Sheet1", data=updated_df)
                
                st.session_state.step = "BITIS"
                st.rerun()
            except Exception as e:
                st.error(f"Hata: {e}")

# --- EKRAN 3: BİTİŞ ---
elif st.session_state.step == "BITIS":
    st.title("Teşekkürler!")
    st.balloons()
    st.success("Tüm yanıtlarınız başarıyla kaydedildi. Katılımınız için teşekkür ederiz.")
    if st.button("Ana Sayfaya Dön"):
        st.session_state.step = "GIRIS"
        st.session_state.current_text = 0
        st.session_state.answers = {}
        st.rerun()
