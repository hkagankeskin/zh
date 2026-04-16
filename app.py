import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import streamlit.components.v1 as components  # Sayfa kaydırma için gerekli

# 1. Sayfa Ayarları
st.set_page_config(page_title="Akademik Değerlendirme Paneli", layout="centered")

# --- ARAŞTIRMA İÇERİĞİ ---
if 'METINLER' not in st.session_state:
    st.session_state.METINLER = [
        {"baslik": "Enerji İçecekleri Hakkında", "icerik": "Birinci metnin tam içeriği buraya gelecek...", "url": "nutritionsource.hsph.harvard.edu/energy-drinks/"},
        {"baslik": "İklim Değişikliği Etkileri", "icerik": "İkinci metnin tam içeriği buraya gelecek...", "url": "bilim-dunyasi.org/makale-v2"},
        {"baslik": "Ekonomik Trendler 2026", "icerik": "Üçüncü metnin tam içeriği buraya gelecek...", "url": "ekonomi-gundemi.com/analiz-3"},
        {"baslik": "Eğitimde Yeni Yaklaşımlar", "icerik": "Dördüncü metnin tam içeriği buraya gelecek...", "url": "egitim-arsivi.edu/icerik-04"}
    ]

SORULAR = [
    "Yazarın enerji içecekleri hakkında ne kadar uzmanlığa sahip olduğunu düşünüyorsunuz?",
    "Yazarın doğru bilgiyi paylaşma isteği konusunda ne kadar samimi olduğunu düşünüyorsunuz?",
    "Yazarın kendi iddiasını desteklemede ne kadar iyi olduğunu düşünüyorsunuz?"
]
# ------------------------------------------------------------------------------

# 2. Google Sheets Bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Gelişmiş Browser Görünümü İçin CSS
st.markdown("""
    <style>
    .browser-window {
        border: 1px solid #d1d1d1;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        overflow: hidden;
        background: #ffffff;
        margin-bottom: 25px;
    }
    .browser-header-tabs {
        background: #dee1e6;
        height: 42px;
        display: flex;
        align-items: center;
        padding: 0 12px;
        gap: 8px;
    }
    .window-dots { display: flex; gap: 6px; margin-right: 15px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background: #ff5f56; }
    .dot-yellow { background: #ffbd2e; }
    .dot-green { background: #27c93f; }
    
    .active-tab {
        background: #ffffff;
        height: 34px;
        padding: 0 20px;
        border-radius: 8px 8px 0 0;
        display: flex;
        align-items: center;
        font-size: 12px;
        font-family: sans-serif;
        color: #3c4043;
        margin-top: 8px;
    }
    .browser-address-bar {
        background: #ffffff;
        height: 46px;
        display: flex;
        align-items: center;
        padding: 0 12px;
        border-bottom: 1px solid #e8eaed;
        gap: 12px;
    }
    .nav-btn { color: #5f6368; font-size: 18px; cursor: default; }
    .url-box {
        background: #f1f3f4;
        flex-grow: 1;
        border-radius: 20px;
        padding: 6px 16px;
        font-size: 13px;
        color: #202124;
        border: 1px solid #dfe1e5;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .browser-body {
        padding: 40px;
        line-height: 1.8;
        color: #333;
        font-family: 'Georgia', serif;
        min-height: 300px;
        font-size: 18px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Oturum (Session State) Yönetimi
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'current_text' not in st.session_state: st.session_state.current_text = 0
if 'answers' not in st.session_state: st.session_state.answers = {}

# --- EKRAN 1: GİRİŞ ---
if st.session_state.step == "GIRIS":
    st.title("Araştırma Veri Toplama Paneli-Zek Hamamcı :)))")
    st.write("Lütfen devam etmek için isminizi giriniz.")
    ad = st.text_input("Adınız Soyadınız:", placeholder="Örn: Ahmet Yılmaz")
    
    if st.button("Sisteme Giriş Yap"):
        if ad:
            try:
                df = conn.read(worksheet="Sheet1", ttl=0)
                if not df.empty and ad in df['ad_soyad'].values:
                    st.error("Bu isimle daha önce katılım sağlandı. İlginiz için teşekkürler.")
                else:
                    st.session_state.user_name = ad
                    st.session_state.step = "TEST"
                    st.rerun()
            except:
                st.session_state.user_name = ad
                st.session_state.step = "TEST"
                st.rerun()
        else:
            st.warning("Devam etmek için bir isim girmelisiniz.")

# --- EKRAN 2: TEST SÜRECİ ---
elif st.session_state.step == "TEST":
    # 1. Sayfanın en üstüne bir çapa (anchor) koyuyoruz
    st.markdown("<div id='top'></div>", unsafe_allow_html=True)
    
    # 2. Daha kuvvetli bir JS komutu (Hem scrollTo hem scrollIntoView deniyoruz)
    components.html(
        """
        <script>
            // Üstteki elementi bul ve oraya kaydır
            var topElement = window.parent.document.getElementById('top');
            if (topElement) {
                topElement.scrollIntoView({behavior: 'auto'});
            }
            // Alternatif olarak ana pencereyi sıfırla
            window.parent.window.scrollTo(0, 0);
        </script>
        """,
        height=0
    )
    
    idx = st.session_state.current_text
    current_m = st.session_state.METINLER[idx]
    
    st.info(f"Katılımcı: **{st.session_state.user_name}** | İlerleme: **{idx + 1} / 4**")
    
    # BROWSER GÖRÜNÜMÜ VE DİĞER KODLAR AYNI ŞEKİLDE DEVAM EDİYOR...
    st.markdown(f"""
    <div class="browser-window">
        <div class="browser-header-tabs">
            <div class="window-dots"><div class="dot dot-red"></div><div class="dot dot-yellow"></div><div class="dot dot-green"></div></div>
            <div class="active-tab">📄 {current_m['baslik']}</div>
        </div>
        <div class="browser-address-bar">
            <div class="nav-btn">←</div><div class="nav-btn">→</div><div class="nav-btn">↻</div>
            <div class="url-box"><span style="color:#1a73e8;">🔒</span> https://www.{current_m['url']}</div>
            <div class="nav-btn">⋮</div>
        </div>
        <div class="browser-body">
            <h1 style="margin-top:0; font-size:26px;">{current_m['baslik']}</h1>
            <hr style="border:0.5px solid #eee;">
            <p>{current_m['icerik']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ... (Geri kalan radyo düğmeleri ve butonlar aynı kalsın)
    # SORULAR (Likert 1-6)
    st.write("### Değerlendirme")
    st.caption("1 = Hiç katılmıyorum / Çok kötü, 6 = Tamamen katılıyorum / Çok iyi")
    
    p1 = st.radio(SORULAR[0], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s1", index=None)
    p2 = st.radio(SORULAR[1], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s2", index=None)
    p3 = st.radio(SORULAR[2], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s3", index=None)

    st.write("---")
    
    # Navigasyon Butonları
    if idx < 3:
        if st.button("Sonraki Metne Geç ➔"):
            if p1 is None or p2 is None or p3 is None:
                st.warning("Lütfen tüm soruları cevaplamadan ilerlemeyiniz.")
            else:
                st.session_state.answers[f"m{idx+1}_s1"] = p1
                st.session_state.answers[f"m{idx+1}_s2"] = p2
                st.session_state.answers[f"m{idx+1}_s3"] = p3
                st.session_state.current_text += 1
                st.rerun()
    else:
        if st.button("Testi Tamamla ve Verileri Kaydet"):
            if p1 is None or p2 is None or p3 is None:
                st.warning("Lütfen son metindeki tüm soruları da cevaplayınız.")
            else:
                st.session_state.answers["m4_s1"] = p1
                st.session_state.answers["m4_s2"] = p2
                st.session_state.answers["m4_s3"] = p3
                
                with st.spinner("Yanıtlarınız güvenli veritabanına aktarılıyor..."):
                    try:
                        df = conn.read(worksheet="Sheet1", ttl=0)
                        
                        yeni_satir = {
                            "tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),
                            "ad_soyad": st.session_state.user_name
                        }
                        yeni_satir.update(st.session_state.answers)
                        
                        puanlar = list(st.session_state.answers.values())
                        yeni_satir["genel_ortalama"] = round(sum(puanlar) / len(puanlar), 2)
                        
                        updated_df = pd.concat([df, pd.DataFrame([yeni_satir])], ignore_index=True)
                        conn.update(worksheet="Sheet1", data=updated_df)
                        
                        st.session_state.step = "BITIS"
                        st.rerun()
                    except Exception as e:
                        st.error(f"Kayıt sırasında hata oluştu: {e}")

# --- EKRAN 3: BİTİŞ ---
elif st.session_state.step == "BITIS":
    st.balloons()
    st.success("Tebrikler! Tüm metinleri değerlendirdiniz ve yanıtlarınız başarıyla kaydedildi.")
    st.write(f"Sayın **{st.session_state.user_name}**, araştırmamıza katkı sağladığınız için teşekkür ederiz.")
    
    if st.button("Yeni Katılımcı İçin Başa Dön"):
        st.session_state.step = "GIRIS"
        st.session_state.current_text = 0
        st.session_state.answers = {}
        st.rerun()
