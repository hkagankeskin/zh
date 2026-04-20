import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime
import random
import time

# 1. Sayfa Ayarları
st.set_page_config(page_title="Online Reading Activity", layout="centered")

# --- MASTER METİN İÇERİKLERİ (KESİNLİKLE DOKUNULMAMIŞ) ---
M1_CONTENT = """Energy drinks are functional beverages marketed with the promise of increasing alertness and energy levels, containing high doses of caffeine and concentrated sugar. These products are distinctly different from traditional sports drinks used for hydration in terms of their fundamental pharmacological structure and metabolic effects. A typical energy drink contains 200 mg of caffeine, equivalent to about two cups of brewed coffee; in some extreme cases, this amount can reach as high as 500 mg. <br><br> Clinical data indicate that while these beverages provide temporary cognitive alertness and improved physical performance in adults, the excessive sucrose and glucose load they contain systematically increases the risk of type 2 diabetes, cardiovascular diseases, and obesity. In individuals with caffeine sensitivity, high doses can lead to severe anxiety, sleep disorders, acute hypertension, and, in extreme cases, serious neurological and cardiovascular complications such as seizures or cardiac arrest. <br><br> From a public health perspective, the most critical issues are the lack of regulation and aggressive marketing tactics targeting adolescents. Many manufacturers classify their products as “dietary supplements” to circumvent legal caffeine limits, thereby weakening regulatory mechanisms. Additionally, the combination of these beverages with alcohol masks the sedative effects of alcohol, preventing individuals from recognizing signs of intoxication and paving the way for excessive alcohol consumption (binge drinking), which poses a life-threatening risk. <br><br> Consequently, authoritative bodies such as the American Academy of Pediatrics (AAP) emphasize that individuals, particularly those in developmental stages, should completely avoid these stimulant-containing products. The uncontrolled consumption of energy drinks is not merely a matter of personal choice but a public health issue that must be addressed with seriousness due to regulatory loopholes and its far-reaching bio-psychosocial effects."""

M2_CONTENT = """In the hectic pace of life, we all hit that invisible wall from time to time; waking up in the morning becomes a struggle, and by the afternoon, our minds start to fog up. In those moments, the reassuring feeling of holding an ice-cold energy drink in your hand is truly priceless. Escaping the unpredictable heat of coffee—whose temperature you can’t quite pin down—or the inconsistent effects that vary from cup to cup, and knowing exactly what to expect in every can is a small yet effective luxury in the chaos of modern life. That refreshing fizz you hear when you open a can is actually the first sign that you’re about to reclaim your day. <br><br> These drinks aren’t just a source of caffeine—they’re also a rich energy cocktail to keep you going. Special ingredients like B vitamins, ginseng, and taurine are combined to help you feel not just awake, but also more vibrant and ready to take on the day. Thanks to their cold and quick-to-drink nature, you don’t have to wait minutes to get that energy boost you need; the refreshing sensation spreads throughout your body in seconds. Especially after a tough workout, rewarding your tired muscles with that light and delicious drink turns the recovery process into a pleasant ritual. <br><br> What’s more, this energy boost is within reach without breaking the bank or compromising your fitness. Instead of the complicated menus at expensive coffee shops, you can recharge your energy guilt-free with these practical, zero-calorie options. Health concerns are usually just simple reminders about knowing your own limits; as long as you know your body, these drinks will be your strongest source of motivation to make your life more dynamic, more productive, and more vibrant. Instead of slowing life down, use this little boost to enjoy every moment to the fullest."""

M3_CONTENT = """Although energy drinks have grown into a multi-billion-dollar global market with the promise of boosting alertness and focus, the temporary energy boost they provide comes at a significant systemic health cost. According to registered dietitian Amber Sommer’s medical perspective, the key factor distinguishing these beverages from traditional caffeine sources like coffee is the synergistic interaction between high doses of caffeine and plant-based stimulants such as taurine, guarana, and ginseng, combined with excessive sugar. <br><br> When examined at the clinical level, the regular consumption of energy drinks leads to reduced insulin sensitivity and unstable blood sugar levels, posing a metabolic risk, particularly for individuals with diabetes. Even more critically, these beverages can trigger “Reversible Cerebral Vasoconstriction Syndrome” (RCVS), causing spasms in brain blood vessels and consequently increasing the risk of stroke. Cardiovascular effects such as high blood pressure and tachycardia directly contribute to these neurological risks. <br><br> When consumed in combination with alcohol, energy drinks mask the sedative effects of alcohol, leading individuals toward “binge drinking” behavior and increasing the risk of dehydration. Additionally, the pharmacological interactions these drinks have with antidepressants and blood thinners can impair the therapeutic efficacy of these medications. <br><br> As a result, children, pregnant women, and individuals with chronic heart or kidney conditions should completely avoid these products. For a healthy and sustainable energy level, alternatives rich in antioxidants and electrolytes—such as black or green tea and coconut water—should be preferred. Scientific data confirms that, for optimal performance, natural physiological supports—such as quality sleep, adequate hydration, and a balanced diet—are of primary importance rather than caffeine supplementation."""

M4_CONTENT = """Energy drinks are functional beverages that are strictly regulated under European Union (EU) regulations regarding ingredients, safety, and labeling. Based on scientific data, the caffeine content of these beverages is comparable to that of a cup of coffee, and in many cases is even lower. The European Food Safety Authority (EFSA) has stated that at least 75 mg of caffeine per serving is required to achieve positive effects on alertness and attention; industry representatives have also established an average of 80 mg of caffeine in 250 ml cans as the standard consumption amount. <br><br> The sugar content of these beverages is comparable to that of natural fruit juices, such as apple or orange juice, and traditional soft drinks of the same volume. Taurine, a common ingredient in these products, is an amino acid found naturally in the body and in various foods. Contrary to common belief, the European Food Safety Authority (EFSA) has confirmed that it has no stimulating effect on the central nervous system. Additionally, the synthetic ingredients used in the products are manufactured to ensure high-quality standards and consistency in composition, in compliance with food regulations. <br><br> Energy drinks are not recommended for children, pregnant women, and breastfeeding women due to their caffeine content; this is stated as a legal requirement on product labels. Regarding mixing with alcohol, organizations such as the EFSA and the UK Committee on Toxicology have reported that there is no scientific evidence of a harmful toxicological or behavioral interaction between caffeine and alcohol. In conclusion, energy drinks have been a part of the food market for over 25 years, and their consumption is intended to be moderate as part of a balanced diet."""

# --- GITHUB IMAGE BASE ---
GITHUB_BASE = "https://raw.githubusercontent.com/hkagankeskin/zh/main/images/"

if 'METINLER_MASTER' not in st.session_state:
    st.session_state.METINLER_MASTER = {
        "m1": {"id": "m1", "yazar": "Anthony L. Komaroff, MD, Harvard Medical School", "baslik": "Energy Drinks: Health Effects and Public Health Concerns", "url": "nutritionsource.hsph.harvard.edu", "resim": GITHUB_BASE + "m1.jpg", "icerik": M1_CONTENT},
        "m2": {"id": "m2", "yazar": "Robert Durfee, Sports and Performance Category Activation Manager", "baslik": "Energy Boost: Reclaim Your Day", "url": "caffeineinformer.com", "resim": GITHUB_BASE + "m2.jpg", "icerik": M2_CONTENT},
        "m3": {"id": "m3", "yazar": "Marc-Alain Babi, MD, Neurocritical Care Specialist for Cleveland Clinic", "baslik": "Are Energy Drinks Bad for You?", "url": "health.clevelandclinic.org", "resim": GITHUB_BASE + "m3.jpg", "icerik": M3_CONTENT},
        "m4": {"id": "m4", "yazar": "Energy Drinks Europe (Industry Association)", "baslik": "Energy Drinks Myths and Facts", "url": "energydrinkseurope.org", "resim": GITHUB_BASE + "m4.jpg", "icerik": M4_CONTENT}
    }

# --- SORULAR ---
SORULAR = [
    "How much expertise do you think the author has on energy drinks?",
    "How sincere do you think the author is about wanting to share accurate information?",
    "How well do you think the author supports his/her own claim?"
]

# --- TASARIM (CSS) ---
st.markdown("""
    <style>
    .browser-window { border: 1px solid #d1d1d1; border-radius: 12px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); overflow: hidden; background: #ffffff; margin-bottom: 25px; }
    .browser-header { background: #dee1e6; padding: 10px 15px; display: flex; align-items: center; gap: 8px; }
    .dot { width: 12px; height: 12px; border-radius: 50%; }
    .browser-address-bar { background: #f1f3f4; border-radius: 20px; padding: 5px 15px; font-size: 13px; color: #5f6368; flex-grow: 1; border: 1px solid #dfe1e5; margin-left: 10px; }
    .author-box { background: #f8f9fa; border-bottom: 1px solid #eee; padding: 15px 40px; font-style: italic; color: #1a73e8; font-size: 15px; border-left: 5px solid #1a73e8; }
    .browser-body { padding: 40px; line-height: 1.7; color: #202124; font-family: 'Georgia', serif; font-size: 18px; }
    .article-image { width: 100%; max-height: 380px; object-fit: cover; border-radius: 4px; margin-bottom: 25px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .warning-box { background-color: #fff3cd; border-left: 10px solid #ffc107; padding: 25px; border-radius: 8px; margin: 25px 0; font-weight: bold; color: #856404; }
    </style>
    """, unsafe_allow_html=True)

if 'step' not in st.session_state: st.session_state.step = "GIRIS"
if 'current_text' not in st.session_state: st.session_state.current_text = 0
if 'answers' not in st.session_state: st.session_state.answers = {}
if 'warning_seen' not in st.session_state: st.session_state.warning_seen = True
if 'timers' not in st.session_state: st.session_state.timers = {"m1": 0, "m2": 0, "m3": 0, "m4": 0}

conn = st.connection("gsheets", type=GSheetsConnection)

# --- EKRAN 1: GİRİŞ (BAŞLIK GÜNCELLENDİ) ---
if st.session_state.step == "GIRIS":
    st.title("Online Reading Activity") # "Academic Evaluation Panel" -> "Online Reading Activity"
    ad = st.text_input("Name and Surname:")
    sinif = st.text_input("Class / Group:")
    if st.button("Start Activity"):
        if ad and sinif:
            st.session_state.group_code = random.choice(["Grup_A", "Grup_B"])
            master = st.session_state.METINLER_MASTER
            if st.session_state.group_code == "Grup_A":
                st.session_state.active_metinler = [master["m1"], master["m2"], master["m3"], master["m4"]]
            else:
                st.session_state.active_metinler = [master["m2"], master["m1"], master["m4"], master["m3"]]
            st.session_state.user_name, st.session_state.user_class = ad, sinif
            st.session_state.step = "TEST"
            st.session_state.text_start_time = time.time()
            st.rerun()

# --- EKRAN 2: TEST SÜRECİ ---
elif st.session_state.step == "TEST":
    idx = st.session_state.current_text
    m = st.session_state.active_metinler[idx]
    
    if 'text_start_time' not in st.session_state:
        st.session_state.text_start_time = time.time()
    
    st.info(f"Participant: {st.session_state.user_name} | Session: {idx+1}/4")
    
    st.markdown(f"""
    <div class="browser-window">
        <div class="browser-header">
            <div class="dot" style="background:#ff5f56;"></div><div class="dot" style="background:#ffbd2e;"></div><div class="dot" style="background:#27c93f;"></div>
            <div class="browser-address-bar">🔒 https://www.{m['url']}</div>
        </div>
        <div class="author-box"><b>Author:</b> {m['yazar']}</div>
        <div class="browser-body">
            <h1 style="margin-top:0; font-size:30px; color:#1a1a1a; line-height:1.2;">{m['baslik']}</h1>
            <img src="{m['resim']}" class="article-image">
            <div style="font-size:19px; color:#333;">{m['icerik']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.warning_seen:
        st.markdown('<div class="warning-box">⚠️ ATTENTION: New article loaded!</div>', unsafe_allow_html=True)
        if st.button("I have read it, show questions"):
            st.session_state.warning_seen = True
            st.rerun()
    else:
        st.write("### Evaluation (1: Lowest - 6: Highest)")
        a1, a2, a3 = [st.session_state.answers.get(f"{m['id']}_s{i}") for i in [1,2,3]]
        p1 = st.radio(SORULAR[0], [1,2,3,4,5,6], horizontal=True, key=f"p1_{m['id']}", index=(a1-1) if a1 else None)
        p2 = st.radio(SORULAR[1], [1,2,3,4,5,6], horizontal=True, key=f"p2_{m['id']}", index=(a2-1) if a2 else None)
        p3 = st.radio(SORULAR[2], [1,2,3,4,5,6], horizontal=True, key=f"p3_{m['id']}", index=(a3-1) if a3 else None)

        c1, c2 = st.columns(2)
        with c1:
            if idx > 0:
                if st.button("⬅️ Previous"):
                    elapsed = time.time() - st.session_state.text_start_time
                    st.session_state.timers[m['id']] += elapsed
                    st.session_state.text_start_time = time.time()
                    
                    st.session_state.answers.update({f"{m['id']}_s1":p1, f"{m['id']}_s2":p2, f"{m['id']}_s3":p3})
                    st.session_state.current_text -= 1
                    st.session_state.warning_seen = True
                    st.rerun()
        with c2:
            if idx < 3:
                if st.button("Next ➔"):
                    if p1 and p2 and p3:
                        elapsed = time.time() - st.session_state.text_start_time
                        st.session_state.timers[m['id']] += elapsed
                        st.session_state.text_start_time = time.time()
                        
                        st.session_state.answers.update({f"{m['id']}_s1":p1, f"{m['id']}_s2":p2, f"{m['id']}_s3":p3})
                        st.session_state.current_text += 1
                        nxt_id = st.session_state.active_metinler[idx+1]['id']
                        st.session_state.warning_seen = (f"{nxt_id}_s1" in st.session_state.answers)
                        st.rerun()
                    else: st.warning("Please answer all questions.")
            else:
                if st.button("✅ Complete and Save"):
                    if p1 and p2 and p3:
                        elapsed = time.time() - st.session_state.text_start_time
                        st.session_state.timers[m['id']] += elapsed
                        
                        st.session_state.answers.update({f"{m['id']}_s1":p1, f"{m['id']}_s2":p2, f"{m['id']}_s3":p3})
                        with st.spinner("Saving..."):
                            try:
                                df = conn.read(worksheet="Sheet1", ttl=0)
                                row = {"timestamp": datetime.now().strftime("%d/%m/%Y %H:%M"), "name": st.session_state.user_name, "class": st.session_state.user_class, "group": st.session_state.group_code}
                                row.update(st.session_state.answers)
                                for mid, duration in st.session_state.timers.items():
                                    row[f"{mid}_time_sec"] = round(duration, 2)
                                
                                vals = [v for k,v in st.session_state.answers.items() if "_s" in k]
                                row["total_avg"] = round(sum(vals)/len(vals), 2)
                                updated = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
                                conn.update(worksheet="Sheet1", data=updated)
                                st.session_state.step = "BITIS"
                                st.rerun()
                            except Exception as e: st.error(f"Error: {e}")

# --- EKRAN 3: BİTİŞ ---
elif st.session_state.step == "BITIS":
    st.balloons()
    st.success("Thank you! Recorded successfully.")
    if st.button("New Participant"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
