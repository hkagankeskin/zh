import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

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

# 2. Google Sheets Bağlantısı
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. Görsel Tasarım (CSS)
st.markdown("""
    <style>
    .browser-window { border: 1px solid #d1d1d1; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow: hidden; background: #ffffff; margin-bottom: 25px; }
    .browser-header-tabs { background: #dee1e6; height: 42px; display: flex; align-items: center; padding: 0 12px; gap: 8px; }
    .window-dots { display: flex; gap: 6px; margin-right: 15px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .dot-red { background: #ff5f56; } .dot-yellow { background: #ffbd2e; } .dot-green { background: #27c93f; }
    .active-tab { background: #ffffff; height: 34px; padding: 0 20px; border-radius: 8px 8px 0 0; display: flex; align-items: center; font-size: 12px; color: #3c4043; margin-top: 8px; }
    .browser-address-bar { background: #ffffff; height: 46px; display: flex; align-items: center; padding: 0 12px; border-bottom: 1px solid #e8eaed; gap: 12px; }
    .url-box { background: #f1f3f4; flex-grow: 1; border-radius: 20px; padding: 6px 16px; font-size: 13px; color: #202124; border: 1px solid #dfe1e5; display: flex; align-items: center; gap: 8px; }
    .browser-body { padding: 40px; line-height: 1.8; color: #333; font-family: 'Georgia', serif; min-height: 300px; font-size: 18px; }
    
    /* Uyarı Kutusu */
    .warning-box { background-color: #fff3cd; border-left: 6px solid #ffc107; padding: 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 4. Durum Yönetimi (Session State)
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'current_text' not in st.session_state: st.session_state.current_text = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'warning_seen' not in st.session_state: st.session_state.warning_seen = True # İlk metinde çıkmasın

# --- EKRAN 1: GİRİŞ ---
if st.session_state.step == "GIRIS":
    st.title("Araştırma Veri Toplama Paneli - Zek Hamamcı :)))")
    st.write("Hoş geldiniz. Lütfen adınızı ve soyadınızı girerek teste başlayınız.")
    ad = st.text_input("Adınız Soyadınız:", placeholder="Örn: Ahmet Yılmaz")
    
    if st.button("Sisteme Giriş Yap"):
        if ad:
            st.session_state.user_name = ad
            st.session_state.step = "TEST"
            st.session_state.warning_seen = True # İlk metin hemen gösterilir
            st.rerun()
        else:
            st.warning("Devam etmek için bir isim girmelisiniz.")

# --- EKRAN 2: TEST SÜRECİ ---
elif st.session_state.step == "TEST":
    idx = st.session_state.current_text
    current_m = st.session_state.METINLER[idx]
    
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
        <div class="browser-body">
            <h1 style="margin-top:0; font-size:26px;">{current_m['baslik']}</h1>
            <hr style="border:0.5px solid #eee;">
            <p>{current_m['icerik']}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- KONTROL MEKANİZMASI ---
    if not st.session_state.warning_seen:
        st.markdown("""
            <div class="warning-box">
                <h3 style="color: #856404; margin-top:0;">⚠️ DİKKAT: Metin Değişti!</h3>
                <p style="color: #856404;">Soruları görmeden önce lütfen sayfanın <b>en üstüne çıkın</b> ve yeni metni dikkatlice okuyun. Hazır olduğunuzda aşağıdaki butona tıklayın.</p>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("⬆️ Metni okudum, soruları cevaplamaya hazırım", key=f"warn_btn_{idx}"):
            st.session_state.warning_seen = True
            st.rerun()
    else:
        # Sorular (Eski yanıtlar varsa hatırlanır)
        st.write("### Değerlendirme")
        
        # Mevcut yanıtları session_state'den çek
        ans1 = st.session_state.answers.get(f"m{idx+1}_s1")
        ans2 = st.session_state.answers.get(f"m{idx+1}_s2")
        ans3 = st.session_state.answers.get(f"m{idx+1}_s3")
        
        p1 = st.radio(SORULAR[0], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s1", 
                      index=(ans1-1) if ans1 else None)
        p2 = st.radio(SORULAR[1], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s2", 
                      index=(ans2-1) if ans2 else None)
        p3 = st.radio(SORULAR[2], [1, 2, 3, 4, 5, 6], horizontal=True, key=f"m{idx}s3", 
                      index=(ans3-1) if ans3 else None)

        st.write("---")
        
        # NAVİGASYON BUTONLARI (Yan yana)
        col1, col2 = st.columns([1, 1])
        
        with col1:
            if idx > 0:
                if st.button("⬅️ Önceki Metne Dön"):
                    # Mevcutları kaydet ve geri git
                    st.session_state.answers[f"m{idx+1}_s1"] = p1
                    st.session_state.answers[f"m{idx+1}_s2"] = p2
                    st.session_state.answers[f"m{idx+1}_s3"] = p3
                    st.session_state.current_text -= 1
                    st.session_state.warning_seen = True # Geri giderken uyarıya gerek yok
                    st.rerun()

        with col2:
            if idx < 3:
                if st.button("Sonraki Metne Geç ➔"):
                    if p1 is None or p2 is None or p3 is None:
                        st.warning("Lütfen tüm soruları cevaplayınız.")
                    else:
                        st.session_state.answers[f"m{idx+1}_s1"] = p1
                        st.session_state.answers[f"m{idx+1}_s2"] = p2
                        st.session_state.answers[f"m{idx+1}_s3"] = p3
                        st.session_state.current_text += 1
                        # Yeni sayfa daha önce cevaplanmadıysa uyarıyı aç
                        if f"m{idx+2}_s1" not in st.session_state.answers:
                            st.session_state.warning_seen = False
                        else:
                            st.session_state.warning_seen = True
                        st.rerun()
            else:
                if st.button("✅ Testi Tamamla ve Kaydet"):
                    if p1 is None or p2 is None or p3 is None:
                        st.warning("Lütfen soruları cevaplayınız.")
                    else:
                        st.session_state.answers["m4_s1"] = p1
                        st.session_state.answers["m4_s2"] = p2
                        st.session_state.answers["m4_s3"] = p3
                        
                        with st.spinner("Verileriniz güvenli bir şekilde kaydediliyor..."):
                            try:
                                df = conn.read(worksheet="Sheet1", ttl=0)
                                yeni_satir = {
                                    "tarih": datetime.now().strftime("%d/%m/%Y %H:%M"),
                                    "ad_soyad": st.session_state.user_name
                                }
                                yeni_satir.update(st.session_state.answers)
                                # Ortalama hesapla
                                puanlar = [v for k,v in st.session_state.answers.items() if v is not None]
                                yeni_satir["genel_ortalama"] = round(sum(puanlar) / len(puanlar), 2)
                                
                                updated_df = pd.concat([df, pd.DataFrame([yeni_satir])], ignore_index=True)
                                conn.update(worksheet="Sheet1", data=updated_df)
                                st.session_state.step = "BITIS"
                                st.rerun()
                            except Exception as e:
                                st.error(f"Kayıt hatası: {e}")

# --- EKRAN 3: BİTİŞ ---
elif st.session_state.step == "BITIS":
    st.balloons()
    st.success("Harika! Tüm metinleri değerlendirdiniz ve yanıtlarınız başarıyla kaydedildi.")
    st.write(f"Teşekkürler Sayın **{st.session_state.user_name}**, araştırmaya katkınız bizim için değerli.")
    if st.button("Yeni Katılımcı İçin Başa Dön"):
        st.session_state.step = "GIRIS"
        st.session_state.current_text = 0
        st.session_state.answers = {}
        st.rerun()
