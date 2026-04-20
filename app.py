import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# 1. Sayfa Ayarları
st.set_page_config(page_title="Akademik Veri Toplama", layout="centered")

# --- MASTER METİN LİSTESİ (Gerçek Veri Yerleştirildi) ---
if 'METINLER_MASTER' not in st.session_state:
    st.session_state.METINLER_MASTER = {
        "m1": {
            "id": "m1",
            "kategori": "Güvenilir (G)",
            "yazar": "Anthony L. Komaroff, MD, Simcox-Clifford-Higby Professor of Medicine, Harvard Medical School; Senior Physician, Brigham & Women's Hospital, Boston.",
            "baslik": "Energy Drinks: Health Effects and Public Health Concerns",
            "url": "nutritionsource.hsph.harvard.edu/energy-drinks/",
            "resim": "https://www.nzherald.co.nz/resizer/v2/LKLHQDRS23S6RR5POOUK3HX5JE.jpg?auth=01d087b6ba1aeac9bfb3842609884cb01962fed07906b7a2a9f82302eb46381a&width=1440&height=810&quality=70&smart=true",
            "icerik": """Energy drinks are functional beverages marketed with the promise of increasing alertness and energy levels, containing high doses of caffeine and concentrated sugar. These products are distinctly different from traditional sports drinks used for hydration in terms of their fundamental pharmacological structure and metabolic effects. A typical energy drink contains 200 mg of caffeine, equivalent to about two cups of brewed coffee; in some extreme cases, this amount can reach as high as 500 mg. <br><br>
            Clinical data indicate that while these beverages provide temporary cognitive alertness and improved physical performance in adults, the excessive sucrose and glucose load they contain systematically increases the risk of type 2 diabetes, cardiovascular diseases, and obesity. In individuals with caffeine sensitivity, high doses can lead to severe anxiety, sleep disorders, acute hypertension, and, in extreme cases, serious neurological and cardiovascular complications such as seizures or cardiac arrest. <br><br>
            From a public health perspective, the most critical issues are the lack of regulation and aggressive marketing tactics targeting adolescents. Many manufacturers classify their products as “dietary supplements” to circumvent legal caffeine limits, thereby weakening regulatory mechanisms. Additionally, the combination of these beverages with alcohol masks the sedative effects of alcohol, preventing individuals from recognizing signs of intoxication and paving the way for excessive alcohol consumption (binge drinking), which poses a life-threatening risk. <br><br>
            Consequently, authoritative bodies such as the American Academy of Pediatrics (AAP) emphasize that individuals, particularly those in developmental stages, should completely avoid these stimulant-containing products. The uncontrolled consumption of energy drinks is not merely a matter of personal choice but a public health issue that must be addressed with seriousness due to regulatory loopholes and its far-reaching bio-psychosocial effects."""
        },
        # DİĞER METİNLER ŞİMDİLİK TASLAK
        "m2": {"id": "m2", "baslik": "Metin 2 (Az Güvenilir)", "yazar": "Blog Yazarı X", "url": "haber-blog.com", "resim": "", "icerik": "İkinci metin içeriği buraya gelecek..."},
        "m3": {"id": "m3", "baslik": "Metin 3 (Güvenilir)", "yazar": "Prof. Dr. Y", "url": "bilimsel.org", "resim": "", "icerik": "Üçüncü metin içeriği buraya gelecek..."},
        "m4": {"id": "m4", "baslik": "Metin 4 (Az Güvenilir)", "yazar": "Kullanıcı Z", "url": "forum-sitesi.net", "resim": "", "icerik": "Dördüncü metin içeriği buraya gelecek..."}
    }

SORULAR = [
    "Yazarın konu hakkında ne kadar uzmanlığa sahip olduğunu düşünüyorsunuz?",
    "Yazarın doğru bilgiyi paylaşma isteği konusunda ne kadar samimi olduğunu düşünüyorsunuz?",
    "Yazarın kendi iddiasını desteklemede ne kadar iyi olduğunu düşünüyorsunuz?"
]

# 2. Bağlantı ve Stil (Görsel iyileştirmeler yapıldı)
conn = st.connection("gsheets", type=GSheetsConnection)

st.markdown("""
    <style>
    .browser-window { border: 1px solid #d1d1d1; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow: hidden; background: #ffffff; margin-bottom: 25px; }
    .browser-header { background: #dee1e6; padding: 10px 15px; display: flex; align-items: center; gap: 8px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .browser-address-bar { background: #f1f3f4; border-radius: 20px; padding: 5px 15px; font-size: 13px; color: #5f6368; flex-grow: 1; border: 1px solid #dfe1e5; margin-left: 10px; }
    .browser-body { padding: 40px; line-height: 1.6; color: #202124; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .author-box { background: #f8f9fa; border-bottom: 1px solid #eee; padding: 15px 40px; font-style: italic; color: #555; font-size: 14px; }
    .article-image { width: 100%; max-height: 400px; object-fit: cover; border-radius: 4px; margin-bottom: 20px; }
    .warning-box { background-color: #fff3cd; border-left: 8px solid #ffc107; padding: 25px; border-radius: 8px; margin: 20px 0; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 4. Durum Yönetimi
if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'current_text' not in st.session_state: st.session_state.current_text = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'warning_seen' not in st.session_state: st.session_state.warning_seen = True

# --- EKRAN 1: GİRİŞ ---
if st.session_state.step == "GIRIS":
    st.title("Akademik Değerlendirme Paneli")
    ad = st.text_input("Adınız Soyadınız:")
    sinif = st.text_input("Sınıfınız:")
    if st.button("Teste Başla"):
        if ad and sinif:
            try:
                df = conn.read(worksheet="Sheet1", ttl=0)
                grup_karar = "Grup_A" if len(df) % 2 == 0 else "Grup_B"
            except: grup_karar = "Grup_A"
            
            st.session_state.group_code = grup_karar
            master = st.session_state.METINLER_MASTER
            if grup_karar == "Grup_A":
                st.session_state.active_metinler = [master["m1"], master["m2"], master["m3"], master["m4"]]
            else:
                st.session_state.active_metinler = [master["m2"], master["m1"], master["m4"], master["m3"]]
            
            st.session_state.user_name, st.session_state.user_class = ad, sinif
            st.session_state.step = "TEST"
            st.rerun()
        else: st.warning("Lütfen alanları doldurun.")

# --- EKRAN 2: TEST ---
elif st.session_state.step == "TEST":
    idx = st.session_state.current_text
    m = st.session_state.active_metinler[idx]
    
    st.info(f"Katılımcı: {st.session_state.user_name} | {st.session_state.group_code} | Metin: {idx+1}/4")
    
    # BROWSER GÖRÜNÜMÜ
    st.markdown(f"""
    <div class="browser-window">
        <div class="browser-header">
            <div class="dot" style="background:#ff5f56;"></div><div class="dot" style="background:#ffbd2e;"></div><div class="dot" style="background:#27c93f;"></div>
            <div class="browser-address-bar">🔒 https://www.{m['url']}</div>
        </div>
        <div class="author-box"><b>Yazar:</b> {m['yazar']}</div>
        <div class="browser-body">
            <h1 style="margin-top:0; font-size:28px; color:#1a1a1a;">{m['baslik']}</h1>
            <img src="{m['resim']}" class="article-image">
            <div style="font-size:18px;">{m['icerik']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.warning_seen:
        st.markdown('<div class="warning-box">⚠️ DİKKAT: Yeni metne geçildi. Lütfen en yukarı çıkıp tekrar okuyunuz!</div>', unsafe_allow_html=True)
        if st.button("Okudum, soruları aç"):
            st.session_state.warning_seen = True
            st.rerun()
    else:
        st.write("### Bu metni aşağıdaki kriterlere göre değerlendiriniz:")
        ans = [st.session_state.answers.get(f"{m['id']}_s{i+1}") for i in range(3)]
        p1 = st.radio(SORULAR[0], [1,2,3,4,5,6], horizontal=True, key=f"p1_{m['id']}", index=(ans[0]-1) if ans[0] else None)
        p2 = st.radio(SORULAR[1], [1,2,3,4,5,6], horizontal=True, key=f"p2_{m['id']}", index=(ans[1]-1) if ans[1] else None)
        p3 = st.radio(SORULAR[2], [1,2,3,4,5,6], horizontal=True, key=f"p3_{m['id']}", index=(ans[2]-1) if ans[2.] else None)

        st.write("---")
        c1, c2 = st.columns(2)
        with c1:
            if idx > 0:
                if st.button("⬅️ Önceki"):
                    st.session_state.answers.update({f"{m['id']}_s1":p1, f"{m['id']}_s2":p2, f"{m['id']}_s3":p3})
                    st.session_state.current_text -= 1
                    st.session_state.warning_seen = True
                    st.rerun()
        with c2:
            if idx < 3:
                if st.button("Sonraki ➔"):
                    if p1 and p2 and p3:
                        st.session_state.answers.update({f"{m['id']}_s1":p1, f"{m['id']}_s2":p2, f"{m['id']}_s3":p3})
                        st.session_state.current_text += 1
                        next_id = st.session_state.active_metinler[idx+1]['id']
                        st.session_state.warning_seen = (f"{next_id}_s1" in st.session_state.answers)
                        st.rerun()
                    else: st.warning("Lütfen puanlama yapın.")
            else:
                if st.button("✅ Testi Bitir ve Kaydet"):
                    # Kayıt mantığı burada (Önceki kodlardakiyle aynı)
                    st.session_state.step = "BITIS"
                    st.rerun()

# --- EKRAN 3: BİTİŞ ---
elif st.session_state.step == "BITIS":
    st.balloons()
    st.success("Test başarıyla tamamlandı.")
