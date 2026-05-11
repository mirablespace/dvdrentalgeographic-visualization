import streamlit as st
from sidebar_nav import render_sidebar
import re

st.set_page_config(page_title="DVDRental Analytics", layout="wide", page_icon="🎬")
render_sidebar(active="Overview")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family:'Sora',sans-serif; background:#07111a; color:#cae8f0; }
[data-testid="stAppViewContainer"] { background:#07111a; }
[data-testid="stHeader"] { background:transparent !important; }
.block-container { padding:2.5rem 3rem 4rem !important; }

.hero-eyebrow { font-size:10px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:#14b8a6;margin-bottom:14px; }
.hero-title   { font-size:52px;font-weight:800;letter-spacing:-0.03em;color:#f0fdfa;line-height:1.1;margin-bottom:14px; }
.hero-title span { color:#14b8a6; }
.hero-sub     { font-size:15px;color:#4a7c8a;line-height:1.75;max-width:600px;margin-bottom:36px; }

.stat-strip { display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:40px; }
.stat-box   { background:#0d1f2d;border:1px solid #1a3347;border-radius:14px;padding:20px 22px;position:relative;overflow:hidden; }
.stat-box::before { content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#0d9488,#14b8a6); }
.stat-val { font-size:32px;font-weight:800;color:#f0fdfa;line-height:1; }
.stat-lbl { font-size:11px;font-weight:600;letter-spacing:0.1em;text-transform:uppercase;color:#2d5a6a;margin-top:8px; }

.s-label  { font-size:10px;font-weight:700;letter-spacing:0.18em;text-transform:uppercase;color:#14b8a6;margin-bottom:14px; }

.cards-grid { display:grid;grid-template-columns:repeat(2,1fr);gap:14px;margin-bottom:40px; }
.page-card  { background:#0d1f2d;border:1px solid #1a3347;border-radius:16px;padding:26px;position:relative;overflow:hidden; }
.page-card::before { content:'';position:absolute;top:0;left:0;right:0;height:3px;border-radius:16px 16px 0 0; }
.card-tita::before    { background:linear-gradient(90deg,#2563eb,#60a5fa); }
.card-abel::before    { background:linear-gradient(90deg,#059669,#34d399); }
.card-abigail::before { background:linear-gradient(90deg,#0d9488,#14b8a6); }
.card-enja::before    { background:linear-gradient(90deg,#7c3aed,#a78bfa); }
.card-num   { font-size:10px;font-weight:700;letter-spacing:0.14em;text-transform:uppercase;color:#1e4a5a;margin-bottom:12px; }
.card-icon  { font-size:28px;margin-bottom:10px; }
.card-title { font-size:16px;font-weight:700;color:#f0fdfa;margin-bottom:6px; }
.card-badge { display:inline-block;font-size:10px;font-weight:600;padding:3px 10px;border-radius:99px;margin-bottom:12px; }
.badge-tita    { background:rgba(59,130,246,0.12);color:#93c5fd; }
.badge-abel    { background:rgba(52,211,153,0.12);color:#6ee7b7; }
.badge-abigail { background:rgba(20,184,166,0.12);color:#2dd4bf; }
.badge-enja    { background:rgba(167,139,250,0.12);color:#c4b5fd; }
.card-desc  { font-size:13px;color:#2d5a6a;line-height:1.7; }

.team-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:12px; }
.team-card { background:#0d1f2d;border:1px solid #1a3347;border-radius:12px;padding:18px 20px; }
.team-role { font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#1e4a5a;margin-bottom:6px; }
.team-name { font-size:17px;font-weight:700;color:#f0fdfa;margin-bottom:4px; }
.team-topic{ font-size:12px;color:#4a7c8a; }

.ocean-hr  { border:none;border-top:1px solid #0f2535;margin:36px 0; }
.footer    { text-align:center;font-size:12px;color:#1a3347;margin-top:48px;letter-spacing:0.06em; }

/* ── AI CHAT STYLES ── */
.ai-panel {
    background:#0d1f2d;
    border:1px solid #1a3347;
    border-radius:18px;
    padding:0;
    overflow:hidden;
    position:relative;
}
.ai-panel::before {
    content:'';position:absolute;top:0;left:0;right:0;height:3px;
    background:linear-gradient(90deg,#0d9488,#14b8a6,#818cf8);
    border-radius:18px 18px 0 0;
}
.ai-header {
    padding:18px 20px 14px 20px;
    border-bottom:1px solid #0f2535;
}
.ai-header-title {
    font-size:13px;font-weight:700;color:#f0fdfa;
    display:flex;align-items:center;gap:8px;
}
.ai-header-sub { font-size:11px;color:#2d5a6a;margin-top:3px; }
.ai-dot {
    width:7px;height:7px;border-radius:50%;
    background:#14b8a6;
    box-shadow:0 0 6px #14b8a6;
    animation:pulse-dot 2s infinite;
    display:inline-block;
}
@keyframes pulse-dot {
    0%,100% { opacity:1; }
    50%      { opacity:0.4; }
}
.msg-user {
    align-self:flex-end;
    background:rgba(20,184,166,0.12);
    border:1px solid rgba(20,184,166,0.2);
    border-radius:14px 14px 2px 14px;
    padding:9px 13px;
    font-size:13px;color:#cae8f0;
    max-width:85%;line-height:1.55;
}
.msg-ai {
    align-self:flex-start;
    background:#07111a;
    border:1px solid #1a3347;
    border-radius:14px 14px 14px 2px;
    padding:9px 13px;
    font-size:13px;color:#94a3b8;
    max-width:90%;line-height:1.65;
}
.msg-ai b { color:#cae8f0; }
.msg-tag {
    font-size:9px;font-weight:700;letter-spacing:0.12em;
    text-transform:uppercase;color:#1e4a5a;
    margin-bottom:4px;
}
</style>
""", unsafe_allow_html=True)


# ── RULE-BASED AI ENGINE ────────────────────────────────────────────────────────
def get_ai_response(question: str) -> str:
    q = question.lower().strip()

    # ── RFM ──
    if any(w in q for w in ["rfm", "recency", "frequency", "monetary"]):
        return (
            "<b>RFM</b> stands for <b>Recency, Frequency, and Monetary</b> — a classic customer segmentation framework.<br><br>"
            "• <b>Recency</b>: How recently did the customer rent? (0 days = score 3, 1–175 days = score 2, >175 days = score 1)<br>"
            "• <b>Frequency</b>: How often do they rent? (30+ = score 3, 23–29 = score 2, &lt;23 = score 1)<br>"
            "• <b>Monetary</b>: How much do they spend? ($3,439+ = score 3, $2,041–$3,438 = score 2, &lt;$2,041 = score 1)<br><br>"
            "Scores are summed (3–9 total) to place each customer into a segment: <b>Champions (8–9)</b>, <b>Regular (6–7)</b>, <b>At Risk (4–5)</b>, or <b>Low Value (3)</b>."
        )

    # ── CHAMPIONS ──
    if "champion" in q:
        return (
            "<b>Champions</b> are the top-tier customers in the RFM segmentation (score 8–9). They are:<br><br>"
            "• Recently active (rented within the last 175 days)<br>"
            "• High frequency renters (30+ rentals)<br>"
            "• High spenders ($3,439+)<br><br>"
            "In Section 01 (Tita's analysis), Champions are defined as customers who are high revenue + high frequency + still active within 100 days. "
            "Strategy: <b>reward them with VIP perks and early access to new titles</b> to prevent churn."
        )

    # ── DECLINING / TREND ──
    if any(w in q for w in ["declining", "decline", "turun", "trend", "volume", "forecast", "recover"]):
        return (
            "Rental volume <b>peaked in August–September 2005</b> and has been in structural decline since. "
            "The <b>Linear Regression model</b> (Section 03) confirms a <b>negative slope</b>, meaning the downward trend is projected to continue for the next 30 days.<br><br>"
            "Possible reasons: the dataset covers 2005–2006 when digital streaming was emerging, reducing physical DVD demand. "
            "Recommended interventions: <b>weekend flash promotions</b>, <b>bundle offers</b> (rent 5 for the price of 3), and <b>win-back campaigns</b> for inactive customers."
        )

    # ── ML MODEL / RANDOM FOREST ──
    if any(w in q for w in ["ml", "model", "machine learning", "randomforest", "random forest", "classifier", "linear regression", "predict"]):
        return (
            "This dashboard uses <b>two ML models</b>, both in Section 03 (Abigail):<br><br>"
            "1️⃣ <b>RandomForest Classifier</b> (<code>rental_model.pkl</code>)<br>"
            "→ Predicts whether each customer is <b>High Engagement</b> or <b>Low Engagement</b>.<br>"
            "→ Features used: <b>rental frequency</b> (rentals per day) and <b>duration_days</b> (span of rental activity).<br>"
            "→ Result: <b>49.2% of customers</b> are classified as High Engagement.<br><br>"
            "2️⃣ <b>Linear Regression</b> (<code>rental_trend_model.pkl</code>)<br>"
            "→ Forecasts <b>daily rental volume for the next 30 days</b> with a 95% confidence band.<br>"
            "→ Result: confirms a <b>declining trend</b> (negative slope)."
        )

    # ── WEEKEND ──
    if any(w in q for w in ["weekend", "weekday", "saturday", "sunday"]):
        return (
            "<b>29% of all rental transactions</b> happen on weekends (Saturday & Sunday). "
            "This sounds significant, but it's actually <b>proportional</b> — 2 out of 7 days = 28.6%, so there's no natural spike.<br><br>"
            "This is actually an <b>opportunity</b>: because customers don't already prefer weekends, "
            "a targeted <b>Weekend Flash Promotion</b> (e.g. 15% discount Sat–Sun) could create a behavioral shift and boost weekend volume above the baseline."
        )

    # ── DURATION INSIGHT ──
    if any(w in q for w in ["duration", "hidden", "insight", "false", "loyal", "mislead"]):
        return (
            "This is one of the most <b>counterintuitive findings</b> in the dashboard! 🔍<br><br>"
            "Intuitively, you'd think customers with <b>longer duration</b> (more days between first and last rental) are more loyal. "
            "But the data shows <b>At-Risk customers average 177 days</b> of duration vs <b>High Engagement customers at only 83 days</b>.<br><br>"
            "Why? Because At-Risk customers rented <b>sporadically over a long period</b>, then stopped — while High Engagement customers rented <b>frequently and consistently</b>. "
            "<b>Frequency is the real loyalty signal</b>, not duration. Duration alone is a false indicator."
        )

    # ── SEGMENTS ──
    if any(w in q for w in ["segment", "segmen", "at risk", "low value", "regular", "kategori"]):
        return (
            "The dashboard uses <b>two segmentation systems</b>:<br><br>"
            "<b>Section 01 (Tita) — Spending-based:</b><br>"
            "• <b>Champions</b>: High spend + high frequency + active within 100 days<br>"
            "• <b>At Risk</b>: Inactive for more than 100 days<br>"
            "• <b>Regular</b>: Everyone else<br><br>"
            "<b>Section 04 (Enja) — RFM scoring (1–3 per dimension):</b><br>"
            "• <b>Champions</b>: Score 8–9 → retain & reward<br>"
            "• <b>Regular</b>: Score 6–7 → push toward Champions<br>"
            "• <b>At Risk</b>: Score 4–5 → immediate reactivation needed<br>"
            "• <b>Low Value</b>: Score 3 → needs initial engagement"
        )

    # ── GEOGRAPHIC ──
    if any(w in q for w in ["geo", "geograf", "country", "negara", "map", "kota", "city", "abel"]):
        return (
            "Section 02 (Abel) covers the <b>geographic distribution</b> of 599 customers across <b>109 countries and 600 cities</b>.<br><br>"
            "Countries are segmented into 3 market tiers:<br>"
            "• 🏆 <b>Top Market</b>: High customer count AND high transaction volume → focus on retention & upsell<br>"
            "• 💎 <b>High Value Niche</b>: Small market but very high loyalty (transactions per customer) → referral programs<br>"
            "• 🌱 <b>Growth Market</b>: Below-average performance → market penetration tactics, intro offers<br><br>"
            "A choropleth world map and country-vs-global benchmark comparison are available in Section 02."
        )

    # ── CUSTOMERS / TOTAL ──
    if any(w in q for w in ["599", "customer", "pelanggan", "total", "berapa", "how many"]):
        return (
            "The DVDRental database contains <b>599 customers</b> and <b>16,044 total rental transactions</b>.<br><br>"
            "Key facts about the customer base:<br>"
            "• Distributed across <b>2 stores</b> (Store 1 and Store 2)<br>"
            "• Spread across <b>109 countries</b> globally<br>"
            "• The <b>top 10 customers</b> contribute only ~3% of total rentals — a very flat, non-power-law distribution<br>"
            "• <b>49.2%</b> are predicted as High Engagement by the RandomForest model<br>"
            "• Spending distribution is <b>right-skewed</b> — a small group of high spenders pulls the average above the median"
        )

    # ── RECOMMENDATION / STRATEGY ──
    if any(w in q for w in ["rekomendasi", "recommend", "strategi", "strategy", "action", "what should", "apa yang"]):
        return (
            "Based on the dashboard findings, here are the <b>top strategic recommendations</b>:<br><br>"
            "1️⃣ <b>Retain Champions</b>: Launch a VIP Membership with early access to new titles and loyalty rewards.<br>"
            "2️⃣ <b>Re-engage Low Engagement customers</b>: Send a 'We Miss You' email with a free rental voucher — act within 2 weeks before churn is permanent.<br>"
            "3️⃣ <b>Weekend Flash Promo</b>: Offer 15% discount on Sat–Sun rentals to create a behavioral spike above the natural 29% baseline.<br>"
            "4️⃣ <b>Bundle offers</b>: 'Rent 5 for the price of 3' to push Regular customers toward Champion frequency.<br>"
            "5️⃣ <b>Geographic differentiation</b>: Use different strategies for Top Markets (retention), Niche Markets (referrals), and Growth Markets (intro offers)."
        )

    # ── TECH STACK ──
    if any(w in q for w in ["tech", "teknologi", "stack", "tools", "built", "streamlit", "python", "postgresql", "plotly"]):
        return (
            "This dashboard is built with the following tech stack:<br><br>"
            "• <b>Frontend</b>: Streamlit (multi-page app) with custom CSS<br>"
            "• <b>Database</b>: PostgreSQL — dvdrental schema via psycopg2<br>"
            "• <b>Data processing</b>: Pandas + NumPy<br>"
            "• <b>Visualizations</b>: Plotly Express & Plotly Graph Objects<br>"
            "• <b>Machine Learning</b>: scikit-learn (RandomForest + Linear Regression), joblib for model persistence<br>"
            "• <b>Maps</b>: Plotly choropleth with ISO country names"
        )

    # ── WHO MADE / TEAM ──
    if any(w in q for w in ["who", "siapa", "team", "tita", "abel", "abigail", "enja", "analyst"]):
        return (
            "This dashboard was built by a team of <b>4 data science students</b> for a Mid Exam project:<br><br>"
            "👤 <b>Tita (Puspita Tri Rahayu)</b> — Section 01: Customer Profile & Demographics<br>"
            "🗺️ <b>Abel</b> — Section 02: Geographic Analysis<br>"
            "🌊 <b>Abigail</b> — Section 03: Rental Activity & History (+ ML models)<br>"
            "🎯 <b>Enja (Najwa Zhafarina)</b> — Section 04: RFM Customer Segmentation"
        )

    # ── SECTION 01 ──
    if any(w in q for w in ["section 01", "section 1", "tita", "profil", "demografi", "demographics", "profile"]):
        return (
            "<b>Section 01 — Customer Profile & Demographics</b> (by Tita):<br><br>"
            "• 599 total customers across Store 1 and Store 2<br>"
            "• Three segments: <b>Champions</b>, <b>At Risk</b>, <b>Regular</b><br>"
            "• KPIs: Customer Base Health, Customer Equity, Avg Profile Value, Risk Exposure<br>"
            "• Features: spending distribution histogram, customer directory (search, sort, filter), "
            "and a drill-down per customer showing monthly rental timeline + favourite genres<br>"
            "• Spending is <b>right-skewed</b> — mean is higher than median due to a small group of high spenders"
        )

    # ── SECTION 03 ──
    if any(w in q for w in ["section 03", "section 3", "abigail", "rental activity", "aktivitas"]):
        return (
            "<b>Section 03 — Rental Activity & History</b> (by Abigail):<br><br>"
            "• Top renters ranking with a concentration analysis<br>"
            "• Weekend vs weekday split (29% weekend — proportional, not a natural spike)<br>"
            "• Daily rental trend with a 7-day moving average<br>"
            "• <b>RandomForest Classifier</b>: predicts High/Low Engagement per customer<br>"
            "• <b>Linear Regression</b>: 30-day rental volume forecast with 95% confidence band<br>"
            "• <b>Hidden insight</b>: At Risk customers have LONGER duration (177 days) than High Engagement (83 days) — frequency is the real loyalty signal"
        )

    # ── DEFAULT / UNKNOWN ──
    return (
        "Great question! I can answer questions about this dashboard's data, findings, and ML models. Try asking:<br><br>"
        "• <i>What does RFM mean?</i><br>"
        "• <i>Why is rental volume declining?</i><br>"
        "• <i>Who are the Champions?</i><br>"
        "• <i>What ML model is used?</i><br>"
        "• <i>What's the weekend opportunity?</i><br>"
        "• <i>Explain the hidden insight about duration</i><br>"
        "• <i>What are the recommendations?</i>"
    )


# ── INITIALIZE SESSION STATE ────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── LAYOUT ─────────────────────────────────────────────────────────────────────
col_main, col_ai = st.columns([2, 1], gap="large")

with col_main:
    st.markdown("""
    <div class="hero-eyebrow">📊 Data Science · Mid Exam · DVDRental Database</div>
    <div class="hero-title">Understanding Our<br><span>DVD Rental</span> Customers</div>
    <div class="hero-sub">
        Analisis menyeluruh database DVDRental — dari siapa pelanggan kita, di mana mereka berada,
        bagaimana mereka berperilaku, hingga prediksi loyalitas berbasis machine learning.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="stat-strip">
        <div class="stat-box"><div class="stat-val">599</div><div class="stat-lbl">Total Customers</div></div>
        <div class="stat-box"><div class="stat-val">16,044</div><div class="stat-lbl">Total Rentals</div></div>
        <div class="stat-box"><div class="stat-val">109</div><div class="stat-lbl">Countries</div></div>
        <div class="stat-box"><div class="stat-val">4</div><div class="stat-lbl">Analysis Sections</div></div>
    </div>
    <hr class="ocean-hr">
    <div class="s-label">Dashboard Sections</div>
    <div class="cards-grid">
      <div class="page-card card-tita">
        <div class="card-num">Section 01</div><div class="card-icon">👤</div>
        <div class="card-title">Profil & Demografi Pelanggan</div>
        <span class="card-badge badge-tita">Tita</span>
        <div class="card-desc">Siapa pelanggan kita? Status keaktifan, distribusi toko, tren akuisisi dari waktu ke waktu, dan customer segmentation berbasis spending.</div>
      </div>
      <div class="page-card card-abel">
        <div class="card-num">Section 02</div><div class="card-icon">🗺️</div>
        <div class="card-title">Analisis Geografis</div>
        <span class="card-badge badge-abel">Abel</span>
        <div class="card-desc">Dari mana pelanggan kita berasal? Choropleth map global, top country by revenue, dan deep-dive trend per kota & negara.</div>
      </div>
      <div class="page-card card-abigail">
        <div class="card-num">Section 03</div><div class="card-icon">🌊</div>
        <div class="card-title">Aktivitas & Riwayat Sewa</div>
        <span class="card-badge badge-abigail">Abigail</span>
        <div class="card-desc">Siapa yang paling sering menyewa? Kapan waktu tersibuk? Prediksi loyalitas pelanggan dengan RandomForest Classifier ML model.</div>
      </div>
      <div class="page-card card-enja">
        <div class="card-num">Section 04</div><div class="card-icon">🎯</div>
        <div class="card-title">Segmentasi Pelanggan (RFM)</div>
        <span class="card-badge badge-enja">Enja</span>
        <div class="card-desc">Recency · Frequency · Monetary — mengelompokkan pelanggan dari Champions hingga Low Value untuk strategi marketing yang tepat sasaran.</div>
      </div>
    </div>
    <hr class="ocean-hr">
    <div class="s-label">Our Team</div>
    <div class="team-grid">
      <div class="team-card"><div class="team-role">Section 01</div><div class="team-name">Tita</div><div class="team-topic">Profil & Demografi</div></div>
      <div class="team-card"><div class="team-role">Section 02</div><div class="team-name">Abel</div><div class="team-topic">Analisis Geografis</div></div>
      <div class="team-card"><div class="team-role">Section 03</div><div class="team-name">Abigail</div><div class="team-topic">Aktivitas & Riwayat Sewa</div></div>
      <div class="team-card"><div class="team-role">Section 04</div><div class="team-name">Enja</div><div class="team-topic">Segmentasi RFM</div></div>
    </div>
    <div class="footer">DVDRental Customer Intelligence &nbsp;·&nbsp; Data Science &nbsp;·&nbsp; Mid Exam</div>
    """, unsafe_allow_html=True)


# ── AI CHAT PANEL ───────────────────────────────────────────────────────────────
with col_ai:
    st.markdown("""
    <div class="ai-panel">
      <div class="ai-header">
        <div class="ai-header-title">
          <span class="ai-dot"></span>
          Dashboard AI Assistant
        </div>
        <div class="ai-header-sub">Ask anything about this dashboard's data & findings</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── CHAT MESSAGES ────────────────────────────────────────────────────────────
    chat_container = st.container(height=420, border=False)
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style="height:100%;display:flex;flex-direction:column;align-items:center;
                        justify-content:center;text-align:center;padding:24px 12px;gap:10px;">
                <div style="font-size:32px;">🤖</div>
                <div style="font-size:13px;font-weight:700;color:#f0fdfa;">Hi! I know this dashboard.</div>
                <div style="font-size:12px;color:#2d5a6a;line-height:1.65;">
                    Ask me about the findings, segments, ML models, or what any number means.
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div style="display:flex;flex-direction:column;align-items:flex-end;margin-bottom:8px;">
                        <div class="msg-tag" style="text-align:right;">You</div>
                        <div class="msg-user">{msg["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display:flex;flex-direction:column;align-items:flex-start;margin-bottom:8px;">
                        <div class="msg-tag">AI Assistant</div>
                        <div class="msg-ai">{msg["content"]}</div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── QUICK CHIPS ──────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="font-size:10px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;
                color:#1e4a5a;margin-bottom:6px;margin-top:4px;">Quick Questions</div>
    """, unsafe_allow_html=True)

    chips = [
        "What does RFM mean?",
        "Why is rental volume declining?",
        "Who are the Champions?",
        "What is the ML model used for?",
        "What's the weekend opportunity?",
        "Explain the hidden insight about duration",
    ]

    chip_cols = st.columns(2)
    for i, chip in enumerate(chips):
        with chip_cols[i % 2]:
            if st.button(chip, key=f"chip_{i}", use_container_width=True):
                st.session_state._pending_prompt = chip
                st.rerun()

    # ── TEXT INPUT ───────────────────────────────────────────────────────────────
    st.markdown("<div style='margin-top:8px;'></div>", unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        input_col, btn_col = st.columns([5, 1])
        with input_col:
            user_input = st.text_input(
                "message",
                placeholder="Ask about the data, findings, models...",
                label_visibility="collapsed",
                key="chat_input"
            )
        with btn_col:
            send_btn = st.form_submit_button("➤", use_container_width=True)

    if st.session_state.chat_history:
        if st.button("🗑 Clear chat", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

    # ── PROCESS PROMPT ───────────────────────────────────────────────────────────
    prompt_to_send = None

    if send_btn and user_input.strip():
        prompt_to_send = user_input.strip()

    if hasattr(st.session_state, "_pending_prompt"):
        prompt_to_send = st.session_state._pending_prompt
        del st.session_state._pending_prompt

    if prompt_to_send:
        st.session_state.chat_history.append({
            "role": "user",
            "content": prompt_to_send
        })

        # 🔑 Rule-based response — no API needed!
        response = get_ai_response(prompt_to_send)

        st.session_state.chat_history.append({
            "role": "assistant",
            "content": response
        })

        st.rerun()