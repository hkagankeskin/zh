import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components

# 1. Sayfa Ayarları
st.set_page_config(page_title="Akademik Değerlendirme Paneli", layout="centered")

# --- ARAŞTIRMA İÇERİĞİ ---
if 'METINLER' not in st.session_state:
    st.session_state.METINLER = [
        {"baslik": "Enerji İçecekleri Hakkında", "icerik": "Enerji içecekleri, genellikle yüksek miktarda kafein, şeker ve taurin gibi uyarıcılar içeren içeceklerdir. Harvard Health verilerine göre, bu içeceklerin aşırı tüketimi kalp ritim bozuklukları ve uyku sorunlarına yol açabilir. Ayrıca, bu içeceklerin içindeki şeker miktarının tip 2 diyabet riskini artırdığı bilinmektedir. Özellikle sporcuların bu içecekleri su yerine tüketmemesi gerektiği vurgulanmaktadır...", "url": "nutritionsource.hsph.harvard.edu/energy-drinks/"},
        {"baslik": "İklim Değişikliği Etkileri", "icerik": "Küresel ısınma, kutup buzullarının erimesine ve deniz seviyelerinin yükselmesine neden olmaktadır. Bilim insanları, karbon emisyonunun azaltılmaması durumunda 2050 yılına kadar ekosistemde geri dönülemez hasarlar oluşacağını öngörmektedir. Fırtınaların şiddetinin artması ve kuraklık gibi ekstrem hava olayları tarımsal üretimi de tehdit etmektedir...", "url": "bilim-dunyasi.org/makale-v2"},
        {"baslik": "Ekonomik Trendler 2026", "icerik": "Dijital paralar ve yapay zeka tabanlı ticaret sistemleri, klasik bankacılık anlayışını kökten değiştiriyor. 2026 yılında küresel ekonominin %30'unun blokzincir altyapısına geçmesi bekleniyor. Bu değişim, geleneksel finans kurumlarının rollerini yeniden tanımlamasına neden olurken, bireysel yatırımcılar için yeni fırsatlar sunmaktadır...", "url": "ekonomi-gundemi.com/analiz-3"},
        {"baslik": "Eğitimde Yeni Yaklaşımlar", "icerik": "Hibrit eğitim modelleri ve kişiselleştirilmiş öğrenme algoritmaları, sınıf içi eğitimi daha verimli hale getiriyor. Öğrenciler artık kendi hızlarında öğrenirken, öğretmenler rehber rolünü üstleniyor. Teknolojinin eğitime entegrasyonu, coğrafi engelleri kaldırarak bilgiye erişimi demokratikleştiriyor...", "url": "egitim-arsivi.edu/icerik-04"}
    ]

SORULAR = [
    "Yazarın enerji içecekleri hakkında ne kadar uzmanlığa sahip olduğunu düşünüyorsunuz?",
    "Yazarın doğru bilgiyi paylaşma isteği konusunda ne kadar samimi olduğunu düşünüyorsunuz?",
    "Yazarın kendi iddiasını desteklemede ne kadar iyi olduğunu düşünüyorsunuz?"
]

# 2. Bağlantı ve Stil
conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("""
    <style>
    .browser-window { border: 1px solid #d1d1d1; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); background: #ffffff; margin-bottom: 25px; }
    .browser-header-tabs { background: #dee1e6; height: 42px; display: flex; align-items: center; padding: 0 12px; gap: 8px; }
    .window-dots { display: flex; gap: 6px; margin-right: 15px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background: #ff5f56; }
    .dot-yellow { background: #ffbd2e; }
    .dot-green { background: #27c93f; }
    .active-tab { background: #ffffff; height: 34px; padding: 0 20px; border-radius: 8px 8px 0 0; display: flex; align-items: center; font-size: 12px; color: #3c4043; margin-top: 8px; }
    .browser-address-bar { background: #ffffff; height: 46px; display: flex; align-items: center; padding: 0 12px; border-bottom: 1px solid #e8eaed; gap: 12px; }
    .url-box { background: #f1f3f4; flex-grow: 1; border-radius: 20px; padding: 6px 16px; font-size: 13px; color: #202124; border: 1px solid #dfe1e5; display: flex; align-items: center; gap: 8px; }
    
    /* GİZLİ FOCUS ALANI */
    .stTextInput { position: absolute; top: -100px; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'current_text' not in st.session_state: st.session_state.current_text = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# --- EKRAN 1: GİRİŞ ---
if st.session_state.step == "GIRIS":
    st.title("Araştırma Paneli - Zek Hamamcı :)))")
    ad = st.text_input("Adınız Soyadınız:")
    if st.button("Başla"):
        if ad:
            st.session_state.user_name = ad
            st.session_state.step = "TEST"
            st.rerun()
        else: st.warning("İsim giriniz.")

# --- EKRAN 2: TEST ---
elif st.session_state.step == "TEST":
    idx = st.session_state.current_text
    current_m = st.session_state.METINLER[idx]

    # HACK 1: Sayfanın en tepesine gizli bir input koyup odağı oraya çekiyoruz
    st.text_input("focus_hack", key=f"focus_{idx}", label_visibility="collapsed")
    
    # HACK 2: JavaScript ile agresif kaydırma
    components.html(f"""<script>window.parent.document.querySelector('section.main').scrollTo(0,0);</script>""", height=0)

    st.info(f"Katılımcı: **{st.session_state.user_name}** | Metin: **{idx + 1} / 4**")

    # BROWSER GÖRÜNÜMÜ
    st.markdown(f"""
    <div class="browser-window">
        <div class="browser-header-tabs">
            <div class="window-dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
            <div class="active-tab">📄 {current_m['baslik']}</div>
        </div>
        <div class="browser-address-bar">
            <div class="url-box"><span style="color:#1a73e8;">🔒</span> https://www.{current_m['url']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # HACK 3: Metin Kutusu (Internal Scroll) 
    # Bu metin kutusu kendi içinde kayar, böylece sayfanın kaymasına gerek kalmaz.
    with st.container(height=350, border=True):
        st.markdown(f"### {current_m['baslik']}")
        st.write(current_m['icerik'])

    st.write("### Değerlendirme")
    p1 = st.radio(SORULAR[0], [1,2,3,4,5,6], horizontal=True, key=f"m{idx}s1", index=None)
    p2 = st.radio(SORULAR[1], [1,2,3,4,5,6], horizontal=True, key=f"m{idx}s2", index=None)
    p3 = st.radio(SORULAR[2], [1,2,3,4,5,6], horizontal=True, key=f"m{idx}s3", index=None)

    if idx < 3:
        if st.button("Sonraki Metin ➔"):
            if p1 and p2 and p3:
                st.session_state.answers[f"m{idx+1}_s1"] = p1
                st.session_state.answers[f"m{idx+1}_s2"] = p2
                st.session_state.answers[f"m{idx+1}_s3"] = p3
                st.session_state.current_text += 1
                st.rerun()
            else: st.warning("Eksik cevap!")
    else:
        if st.button("Testi Bitir"):
            if p1 and p2 and p3:
                st.session_state.answers["m4_s1"] = p1
                st.session_state.answers["m4_s2"] = p2
                st.session_state.answers["m4_s3"] = p3
                try:
                    df = conn.read(worksheet="Sheet1", ttl=0)
                    yeni = {"tarih": datetime.now().strftime("%d/%m/%Y %H:%M"), "ad_soyad": st.session_state.user_name}
                    yeni.update(st.session_state.answers)
                    updated_df = pd.concat([df, pd.DataFrame([yeni])], ignore_index=True)
                    conn.update(worksheet="Sheet1", data=updated_df)
                    st.session_state.step = "BITIS"
                    st.rerun()
                except Exception as e: st.error(f"Hata: {e}")
            else: st.warning("Eksik cevap!")

# --- EKRAN 3: BİTİŞ ---
elif st.session_state.step == "BITIS":
    st.balloons()
    st.success("Kaydedildi. Teşekkürler!")
    if st.button("Başa Dön"):
        st.session_state.step = "GIRIS"
        st.session_state.current_text = 0
        st.session_state.answers = {}
        st.rerun()
