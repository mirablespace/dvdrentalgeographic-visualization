import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Strategic Customer Intelligence", layout="wide", page_icon="📈")

# --- COLOR PALETTE ---
COLORS = {
    "primary": "#3b82f6",
    "success": "#10b981",
    "warning": "#f59e0b",
    "danger": "#ef4444",
    "navy": "#0f172a",
    "slate": "#1e293b",
    "muted": "#64748b",
    "light": "#94a3b8",
    "border": "#1e293b",
}
PALETTE = ["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#06b6d4"]

# --- 2. CSS MINIMALIS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── BASE ── */
    html, body, [class*="css"], .stApp {
        font-family: 'Inter', sans-serif !important;
        background-color: #0d1117 !important;
        color: #c9d1d9 !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    .main .block-container { background-color: #0d1117 !important; }
    .main .block-container { padding-top: 2rem !important; }

    /* ── HIDE SIDEBAR ── */
    [data-testid="stSidebar"],
    [data-testid="stSidebarNav"],
    section[data-testid="stSidebar"] { display: none !important; }
    .main .block-container { margin-left: 0 !important; }

    /* ── REMOVE STREAMLIT COLUMN WRAPPERS ── */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
    }

    /* ── KPI CARD ── */
    .kpi-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 20px 20px 16px 20px;
        height: 130px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        box-sizing: border-box;
    }
    .kpi-label {
        font-size: 12px;
        font-weight: 500;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: #8b949e;
        margin-bottom: 6px;
    }
    .kpi-value {
        font-size: 26px;
        font-weight: 700;
        color: #e6edf3;
        letter-spacing: -0.02em;
        line-height: 1;
    }
    .kpi-sub {
        font-size: 12px;
        color: #6e7681;
        margin-top: 6px;
    }

    /* ── SECTION HEADER ── */
    .sec-title {
        font-size: 13px;
        font-weight: 600;
        color: #adbac7;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        margin: 36px 0 4px 0;
    }
    .sec-sub {
        font-size: 13px;
        color: #6e7681;
        margin: 2px 0 16px 0;
    }
    .sec-divider {
        border: none;
        border-top: 1px solid #30363d;
        margin: 8px 0 20px 0;
    }

    /* ── BENCHMARK BOX ── */
    .benchmark-box {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 6px;
        padding: 12px 16px;
        margin-bottom: 16px;
        font-size: 13px;
        color: #adbac7;
        line-height: 1.9;
    }
    .benchmark-box b { color: #e6edf3; font-weight: 600; }

    /* ── REC CARDS ── */
    .rec-card-green, .rec-card-red, .rec-card-blue {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 18px;
        min-height: 180px;
        height: auto;
        display: flex;
        flex-direction: column;
    }
    .rec-card-green { border-top: 2px solid #238636; }
    .rec-card-red   { border-top: 2px solid #da3633; }
    .rec-card-blue  { border-top: 2px solid #388bfd; }
    .rec-card-green p, .rec-card-red p, .rec-card-blue p { font-size: 13px; margin: 0; color: #adbac7; line-height: 1.7; }

    /* ── LEADERBOARD CARD ── */
    .leaderboard-card {
        background: #1c2128;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 16px;
        height: 210px;
        box-sizing: border-box;
        overflow: hidden;
        display: flex;
        flex-direction: column;
        gap: 4px;
    }

    /* ── SELECTS & INPUTS ── */
    [data-baseweb="select"] > div {
        background-color: #1c2128 !important;
        border-color: #30363d !important;
        color: #c9d1d9 !important;
        border-radius: 6px !important;
    }
    [data-baseweb="menu"] { background-color: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 6px !important; }
    [data-baseweb="option"] { background-color: #1c2128 !important; color: #c9d1d9 !important; }
    [data-baseweb="option"]:hover { background-color: #30363d !important; }

    /* ── TABS ── */
    [data-testid="stTabs"] [data-baseweb="tab-list"] {
        background: transparent !important;
        border-bottom: 1px solid #21262d !important;
        gap: 0;
    }
    [data-testid="stTabs"] [data-baseweb="tab"] {
        background: transparent !important;
        color: #8b949e !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 10px 18px !important;
        border-radius: 0 !important;
    }
    [data-testid="stTabs"] [aria-selected="true"] {
        color: #e6edf3 !important;
        border-bottom: 2px solid #388bfd !important;
        background: transparent !important;
    }

    /* ── ALERTS ── */
    [data-testid="stAlert"] {
        background: #161b22 !important;
        border: 1px solid #21262d !important;
        border-radius: 6px !important;
        color: #c9d1d9 !important;
    }

    /* ── METRIC FALLBACK ── */
    [data-testid="stMetric"] { background: #1c2128 !important; border: 1px solid #30363d !important; border-radius: 8px !important; padding: 14px !important; }
    [data-testid="stMetricLabel"] { color: #8b949e !important; font-size: 11px !important; text-transform: uppercase !important; letter-spacing: 0.06em !important; }
    [data-testid="stMetricValue"] { color: #e6edf3 !important; font-weight: 600 !important; }

    /* ── MISC ── */
    .stMarkdown p, .stMarkdown li { color: #adbac7 !important; font-size: 13px !important; }
    .stMarkdown h1,.stMarkdown h2,.stMarkdown h3 { color: #e6edf3 !important; }
    .stCaption { color: #6e7681 !important; font-size: 12px !important; }
    [data-testid="stDataFrame"] { border-radius: 8px !important; overflow: hidden; }
    .stDownloadButton button { background: #21262d !important; color: #c9d1d9 !important; border: 1px solid #30363d !important; border-radius: 6px !important; font-weight: 500 !important; }
    </style>
    """, unsafe_allow_html=True)

# Fungsi untuk membaca data dari CSV
def get_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "dvdrental_data.csv")
    df = pd.read_csv(csv_path)
    df['payment_date'] = pd.to_datetime(df['payment_date'])
    return df

# Judul Dashboard
st.title("Customer Geographic Dashboard")

try:
    # 1. Ambil data dari CSV
    df_raw = get_data()
    
    # 2. Kalkulasi Metrik Secara Dinamis (Global)
    total_cust = df_raw['customer_id'].nunique()
    total_rev = df_raw['amount'].sum()
    total_trans = df_raw['payment_id'].count()
    total_city = df_raw['city'].nunique()
    total_country = df_raw['country'].nunique()

    # 2. Kalkulasi Metrik Secara Dinamis
    total_cust = df_raw['customer_id'].nunique()
    total_rev = df_raw['amount'].sum()
    total_trans = df_raw['payment_id'].count()
    total_city = df_raw['city'].nunique()
    total_country = df_raw['country'].nunique()
    
    # ... sisa kode kamu ...

    # --- PERHITUNGAN BENCHMARK ---
    # region_map didefinisikan setelah blok ini, gunakan fixed count 5 region utama + Other
    total_region            = 6  # Asia, Europe, Americas, Africa, Oceania, Other
    avg_cust_per_region     = total_cust    / total_region  if total_region  > 0 else 0
    avg_cust_per_country    = total_cust    / total_country if total_country > 0 else 0
    avg_spending_per_country= total_rev     / total_country if total_country > 0 else 0
    avg_trans_per_country   = total_trans   / total_country if total_country > 0 else 0

    def kpi(label, value, sub=""):
        return f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {"" if not sub else f'<div class="kpi-sub">{sub}</div>'}
        </div>"""

    # --- BARIS 1 — 5 KPI UTAMA ---
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.markdown(kpi("Total Customer",   f"{total_cust:,}",          "unique customers"),          unsafe_allow_html=True)
    m2.markdown(kpi("Total Revenue",    f"${total_rev:,.2f}",        "gross revenue"),             unsafe_allow_html=True)
    m3.markdown(kpi("Total Transaction",f"{total_trans:,}",          "all transactions"),          unsafe_allow_html=True)
    m4.markdown(kpi("Total City",       f"{total_city:,}",           "cities covered"),            unsafe_allow_html=True)
    m5.markdown(kpi("Total Country",    f"{total_country:,}",        "countries reached"),         unsafe_allow_html=True)

    st.markdown("<hr class='sec-divider' style='margin-top:20px;'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Average Performance Benchmarks</div>", unsafe_allow_html=True)

    # --- BARIS 2 — 4 BENCHMARK: region, country, spending, transaction ---
    a1, a2, a3, a4 = st.columns(4)
    a1.markdown(kpi("Avg Customer / Region",  f"{avg_cust_per_region:.1f}",        "per region"),   unsafe_allow_html=True)
    a2.markdown(kpi("Avg Customer / Country", f"{avg_cust_per_country:.1f}",       "per country"),  unsafe_allow_html=True)
    a3.markdown(kpi("Avg Spending / Country", f"${avg_spending_per_country:,.2f}", "per country"),  unsafe_allow_html=True)
    a4.markdown(kpi("Avg Trans / Country",    f"{avg_trans_per_country:.1f}",      "per country"),  unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:28px 0;'>", unsafe_allow_html=True)

    # --- REGION SEGMENTATION (GLOBAL 5 REGION) ---
    region_map = {

        # Asia
        "Afghanistan": "Asia","Bangladesh": "Asia","China": "Asia","India": "Asia",
        "Indonesia": "Asia","Japan": "Asia","Malaysia": "Asia","Pakistan": "Asia",
        "Philippines": "Asia","Singapore": "Asia","South Korea": "Asia",
        "Thailand": "Asia","Vietnam": "Asia","Iran": "Asia","Iraq": "Asia",
        "Israel": "Asia","Saudi Arabia": "Asia","Turkey": "Asia",

        # Europe
        "Austria": "Europe","Belgium": "Europe","Denmark": "Europe","Finland": "Europe",
        "France": "Europe","Germany": "Europe","Greece": "Europe","Ireland": "Europe",
        "Italy": "Europe","Netherlands": "Europe","Norway": "Europe","Poland": "Europe",
        "Portugal": "Europe","Spain": "Europe","Sweden": "Europe","Switzerland": "Europe",
        "United Kingdom": "Europe","Czech Republic": "Europe","Hungary": "Europe",

        # Americas
        "Argentina": "Americas","Brazil": "Americas","Canada": "Americas",
        "Chile": "Americas","Colombia": "Americas","Mexico": "Americas",
        "Peru": "Americas","United States": "Americas","Venezuela": "Americas",

        # Africa
        "Algeria": "Africa","Egypt": "Africa","Ethiopia": "Africa","Ghana": "Africa",
        "Kenya": "Africa","Morocco": "Africa","Nigeria": "Africa",
        "South Africa": "Africa","Tanzania": "Africa",

        # Oceania
        "Australia": "Oceania","New Zealand": "Oceania",
        "Fiji": "Oceania","Papua New Guinea": "Oceania"
    }

    # Tambahkan kolom region ke dataframe
    df_raw["region"] = df_raw["country"].map(region_map)

    # Jika ada negara yang belum masuk mapping
    df_raw["region"] = df_raw["region"].fillna("Other")


    # 3. Siapkan Data untuk Visualisasi (Grouped)
    df_grouped = df_raw.groupby('country').agg({
        'customer_id': 'nunique',   # Total Customer per Country
        'payment_id': 'count',      # Total Transaction per Country
        'amount': 'sum'             # Total Revenue per Country
    }).reset_index().rename(columns={
        'customer_id': 'total_customers', 
        'payment_id': 'total_transactions',
        'amount': 'total_revenue'
    })
    # Menghitung Average Payment (AOV) per Negara
    df_grouped['avg_payment'] = df_grouped['total_revenue'] / df_grouped['total_transactions']

    # Menghitung Average Transaction per Customer per Negara
    df_grouped['avg_trans_per_cust'] = df_grouped['total_transactions'] / df_grouped['total_customers']

    # --- PERSIAPAN DATA UNTUK PERSENTASE ---
    total_cust_all = df_grouped['total_customers'].sum()
    df_grouped['cust_percentage'] = (df_grouped['total_customers'] / total_cust_all) * 100

    # --- VISUALISASI: MAP & BAR CHART DALAM 1 ROW ---
    st.markdown("<div class='sec-title'>Geographic & Top Customer Distribution</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Distribusi customer di seluruh dunia dan 10 negara teratas.</div>", unsafe_allow_html=True)
    
    # Membagi baris menjadi 2 kolom dengan rasio lebar 2:1 (Map lebih lebar)
    col_map, col_bar = st.columns([2, 1])

    with col_map:
        st.write("**Customer Density by Country**")
        fig_map = px.choropleth(
            df_grouped, 
            locations="country", 
            locationmode="country names",
            color="total_customers", 
            hover_name="country",
            # Menampilkan persentase saat kursor diarahkan ke map (hover)
            hover_data={'total_customers': True, 'cust_percentage': ':.2f'}, 
            color_continuous_scale=px.colors.sequential.YlGnBu
        )
        fig_map.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            geo=dict(bgcolor='rgba(0,0,0,0)', showframe=False, showcoastlines=True,
                     coastlinecolor='#21262d', lakecolor='rgba(0,0,0,0)',
                     landcolor='#161b22'),
            coloraxis_colorbar=dict(thickness=10, len=0.5, bgcolor='rgba(0,0,0,0)',
                                    tickfont=dict(color='#8b949e', size=10),
                                    title=dict(font=dict(color='#8b949e', size=10)))
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col_bar:
        st.write("**Top 10 Countries by Total Customers**")
        top_10_cust = df_grouped.nlargest(10, 'total_customers')
        
        fig_cust = px.bar(
            top_10_cust,
            x='total_customers',
            y='country',
            orientation='h',
            color='total_customers',
            color_continuous_scale='Blues',
            # Menampilkan jumlah asli dan persentase di ujung bar
            text=top_10_cust.apply(lambda r: f"{int(r['total_customers'])} ({r['cust_percentage']:.1f}%)", axis=1)
        )
        fig_cust.update_traces(textposition='outside')
        fig_cust.update_layout(
            showlegend=False,
            xaxis_title=None,
            margin=dict(t=0,b=0,l=0,r=8),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#1c2128',
            font=dict(family='Inter', color='#8b949e', size=11),
            xaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
            yaxis=dict(categoryorder='total ascending', showgrid=False, zeroline=False, tickfont=dict(color='#8b949e')),
            coloraxis_showscale=False,
        )
        st.plotly_chart(fig_cust, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:28px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Regional Analysis</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Perbandingan performa antar benua — kontribusi revenue, efisiensi customer, dan tren bulanan.</div>", unsafe_allow_html=True)

    # --- PERSIAPAN DATA REGIONAL ---
    df_region = df_raw.groupby('region').agg(
        total_customers=('customer_id', 'nunique'),
        total_transactions=('payment_id', 'count'),
        total_revenue=('amount', 'sum')
    ).reset_index()
    df_region['avg_spending_per_cust'] = df_region['total_revenue'] / df_region['total_customers']
    df_region['avg_trans_per_cust']    = df_region['total_transactions'] / df_region['total_customers']
    df_region['revenue_pct']           = (df_region['total_revenue'] / df_region['total_revenue'].sum() * 100).round(1)
    df_region['cust_pct']              = (df_region['total_customers'] / df_region['total_customers'].sum() * 100).round(1)

    # Palette region — satu warna netral per region
    REGION_COLORS = {
        'Asia':     '#388bfd',
        'Europe':   '#57ab5a',
        'Americas': '#e3b341',
        'Africa':   '#f47067',
        'Oceania':  '#96d0ff',
        'Other':    '#768390',
    }
    df_region['color'] = df_region['region'].map(REGION_COLORS).fillna('#768390')

    # ── ROW 1: 3 kolom sejajar — Donut Cust | Donut Revenue | Bar Avg Spend ──
    col_dc, col_dr, col_bar = st.columns(3)

    with col_dc:
        st.markdown("<div class='sec-sub' style='margin-bottom:6px;'>Customer Distribution</div>", unsafe_allow_html=True)
        total_cust_region = df_region['total_customers'].sum()
        fig_donut_cust = px.pie(
            df_region.sort_values('total_customers', ascending=False),
            names='region',
            values='total_customers',
            hole=0.65,
            color='region',
            color_discrete_map=REGION_COLORS,
            custom_data=['cust_pct', 'total_customers']
        )
        fig_donut_cust.update_traces(
            textposition='outside',
            texttemplate='%{label} %{customdata[0]:.0f}%',
            textfont=dict(family='Inter', size=10, color='#8b949e'),
            hovertemplate='<b>%{label}</b><br>%{customdata[1]:,} customers (%{customdata[0]:.1f}%)<extra></extra>',
            marker=dict(line=dict(color='#0d1117', width=2)),
            pull=[0.03] * len(df_region)
        )
        fig_donut_cust.add_annotation(
            text=f"<b>{total_cust_region:,}</b><br><span style='font-size:10px;color:#6e7681'>customers</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family='Inter', color='#e6edf3', size=16)
        )
        fig_donut_cust.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=30, l=30, r=30),
            height=260,
            showlegend=False,
            font=dict(family='Inter')
        )
        st.plotly_chart(fig_donut_cust, use_container_width=True)

    with col_dr:
        st.markdown("<div class='sec-sub' style='margin-bottom:6px;'>Revenue Share</div>", unsafe_allow_html=True)
        total_rev_region = df_region['total_revenue'].sum()
        fig_donut_rev = px.pie(
            df_region.sort_values('total_revenue', ascending=False),
            names='region',
            values='total_revenue',
            hole=0.65,
            color='region',
            color_discrete_map=REGION_COLORS,
            custom_data=['revenue_pct', 'total_revenue']
        )
        fig_donut_rev.update_traces(
            textposition='outside',
            texttemplate='%{label} %{customdata[0]:.0f}%',
            textfont=dict(family='Inter', size=10, color='#8b949e'),
            hovertemplate='<b>%{label}</b><br>$%{customdata[1]:,.0f} (%{customdata[0]:.1f}%)<extra></extra>',
            marker=dict(line=dict(color='#0d1117', width=2)),
            pull=[0.03] * len(df_region)
        )
        fig_donut_rev.add_annotation(
            text=f"<b>${total_rev_region:,.0f}</b><br><span style='font-size:10px;color:#6e7681'>total revenue</span>",
            x=0.5, y=0.5, showarrow=False,
            font=dict(family='Inter', color='#e6edf3', size=15)
        )
        fig_donut_rev.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            margin=dict(t=30, b=30, l=30, r=30),
            height=260,
            showlegend=False,
            font=dict(family='Inter')
        )
        st.plotly_chart(fig_donut_rev, use_container_width=True)

    with col_bar:
        st.markdown("<div class='sec-sub' style='margin-bottom:6px;'>Avg Spending / Customer</div>", unsafe_allow_html=True)
        df_region_sorted = df_region.sort_values('avg_spending_per_cust', ascending=True)
        fig_avg_spend = px.bar(
            df_region_sorted,
            x='avg_spending_per_cust',
            y='region',
            orientation='h',
            text=df_region_sorted['avg_spending_per_cust'].apply(lambda v: f"${v:,.2f}"),
            labels={'avg_spending_per_cust': '', 'region': ''}
        )
        fig_avg_spend.update_traces(
            marker_color='#388bfd',
            marker_opacity=0.75,
            textposition='outside',
            textfont=dict(family='Inter', size=11, color='#adbac7'),
            hovertemplate='<b>%{y}</b>  $%{x:,.2f}<extra></extra>'
        )
        fig_avg_spend.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=260,
            showlegend=False,
            font=dict(family='Inter', color='#8b949e', size=11),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#adbac7', size=11)),
            margin=dict(t=0, b=0, l=0, r=60)
        )
        st.plotly_chart(fig_avg_spend, use_container_width=True)

    # ── ROW 3: Monthly Revenue Trend per Region ──────────────────────────────
    st.markdown("<div class='sec-sub' style='margin-top:16px;margin-bottom:8px;'>Monthly Revenue Trend by Region — apakah ada region yang tumbuh atau turun?</div>", unsafe_allow_html=True)

    df_trend = df_raw.copy()
    df_trend['month'] = df_trend['payment_date'].dt.to_period('M').astype(str)
    df_region_trend = df_trend.groupby(['month', 'region']).agg(
        revenue=('amount', 'sum'),
        transactions=('payment_id', 'count')
    ).reset_index().sort_values('month')

    fig_trend = px.line(
        df_region_trend,
        x='month',
        y='revenue',
        color='region',
        color_discrete_map=REGION_COLORS,
        markers=True,
        labels={'month': '', 'revenue': 'Revenue ($)', 'region': 'Region'},
        custom_data=['transactions', 'region']
    )
    fig_trend.update_traces(
        line=dict(width=2),
        marker=dict(size=5),
        hovertemplate='<b>%{customdata[1]}</b><br>%{x}<br>Revenue: $%{y:,.2f}<br>Transactions: %{customdata[0]:,}<extra></extra>'
    )
    fig_trend.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1c2128',
        height=320,
        font=dict(family='Inter', color='#8b949e', size=11),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#8b949e'), tickangle=-30),
        yaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
        legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b949e', size=11, family='Inter'),
                    orientation='h', y=-0.25, x=0),
        margin=dict(t=10, b=40, l=0, r=0),
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:28px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Top 10 Analysis per Country</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Negara dengan performa tertinggi berdasarkan transaksi dan rata-rata per customer.</div>", unsafe_allow_html=True)
    # Membuat 1 blok dengan 3 kolom berjejer
    col_trans, col_rev = st.columns(2)

    with col_trans:
        st.write("**Country With the Highest Total Transactions**")
        fig_trans = px.bar(
            df_grouped.nlargest(10, 'total_transactions'),
            x='total_transactions',
            y='country',
            orientation='h',
            color='total_transactions',
            color_continuous_scale='Viridis',
            text_auto=True
        )
        fig_trans.update_layout(
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1c2128',
            font=dict(family='Inter', color='#8b949e', size=11),
            xaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
            yaxis=dict(categoryorder='total ascending', showgrid=False, zeroline=False, tickfont=dict(color='#8b949e')),
            coloraxis_showscale=False, margin=dict(t=0,b=0,l=0,r=8)
        )
        st.plotly_chart(fig_trans, use_container_width=True)

    with col_rev:
        st.write("**By Avg Transaction per Customer**")
        st.caption("(Country with > 10 Customers)")
        
        # 1. Hitung metrik rata-rata transaksi per customer
        df_grouped['avg_trans_per_cust'] = df_grouped['total_transactions'] / df_grouped['total_customers']
        
        # 2. FILTER: Hanya ambil negara yang punya customer > 10
        df_filtered_avg = df_grouped[df_grouped['total_customers'] > 10].copy()
        
        # 3. Ambil Top 10 dari hasil filter tersebut
        top_10_avg_trans = df_filtered_avg.nlargest(10, 'avg_trans_per_cust')
        
        # 4. Buat Horizontal Bar Chart
        if not top_10_avg_trans.empty:
            fig_avg_trans = px.bar(
                top_10_avg_trans,
                x='avg_trans_per_cust',
                y='country',
                orientation='h',
                color='avg_trans_per_cust',
                color_continuous_scale='Reds',
                text_auto='.2f',
                labels={'avg_trans_per_cust': 'Avg Trans/Cust'}
            )
            
            fig_avg_trans.update_layout(
                showlegend=False,
                xaxis_title=None,
                margin=dict(t=0,b=0,l=0,r=8),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1c2128',
                font=dict(family='Inter', color='#8b949e', size=11),
                xaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
                yaxis=dict(categoryorder='total ascending', showgrid=False, zeroline=False, tickfont=dict(color='#8b949e')),
                coloraxis_showscale=False,
            )
            
            st.plotly_chart(fig_avg_trans, use_container_width=True)
        else:
            st.warning("Tidak ada negara dengan jumlah customer > 10 untuk ditampilkan.")


    # --- 1. PERHITUNGAN METRIK & THRESHOLD GLOBAL ---
    # Pastikan kolom rata-rata transaksi sudah ada
    df_grouped['avg_trans_per_cust'] = df_grouped['total_transactions'] / df_grouped['total_customers']

    # Standar Global (Rata-rata populasi)
    avg_customer = df_grouped['total_customers'].mean()
    avg_transaction = df_grouped['total_transactions'].mean()
    avg_avgtransaction = df_grouped['avg_trans_per_cust'].mean()

    # Kolom untuk ukuran visual agar perbedaan loyalty terlihat menonjol
    df_grouped['visual_size'] = df_grouped['avg_trans_per_cust'] ** 3

    # --- 2. LOGIKA SEGMENTASI NEGARA ---

    # A. TOP MARKET: High Customer (> avg) & High Transaction (> avg)
    df_top_market = df_grouped[
        (df_grouped['total_customers'] > avg_customer) & 
        (df_grouped['total_transactions'] > avg_transaction)
    ].copy()

    # B. HIGH VALUE MARKET: Low Volume (< avg) tapi High Loyalty (> avg_avg)
    df_high_value = df_grouped[
        (df_grouped['total_customers'] <= avg_customer) & 
        (df_grouped['total_transactions'] <= avg_transaction) & 
        (df_grouped['avg_trans_per_cust'] > avg_avgtransaction)
    ].copy()

    # C. GROWTH MARKET: Sisanya (Negara yang belum masuk kedua kategori di atas)
    top_high_countries = np.concatenate([df_top_market['country'].unique(), df_high_value['country'].unique()])
    df_growth_market = df_grouped[~df_grouped['country'].isin(top_high_countries)].copy()

    # --- 3. VISUALISASI DENGAN TABS ---
    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:28px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Strategic Market Segmentation</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Klasifikasi negara berdasarkan volume customer, transaksi, dan loyalitas.</div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="benchmark-box">
        <b>Global Benchmarks:</b><br>
        Average Customer: <b>{avg_customer:.1f}</b> &nbsp;|&nbsp;
        Average Transaction: <b>{avg_transaction:.1f}</b> &nbsp;|&nbsp;
        Global Average Transaction per Customer: <b>{avg_avgtransaction:.2f}</b>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["Top Market", "High Value Market", "Growth Market"])

    def render_segmented_scatter(df, title, color_scale, subtitle):
        if df.empty:
            st.info(f"Belum ada data untuk kategori {title}.")
            return

        st.write(f"### {title}")
        st.caption(subtitle)
        
        # --- LOGIKA UNTUK POSISI TENGAH SEMPURNA ---
        # Kita hitung range sumbu agar 'avg' berada di tengah (Center Padding)
        padding_x = max(df['total_customers'].max() - avg_customer, avg_customer - df['total_customers'].min())
        padding_y = max(df['total_transactions'].max() - avg_transaction, avg_transaction - df['total_transactions'].min())
        
        range_x = [avg_customer - padding_x * 1.1, avg_customer + padding_x * 1.1]
        range_y = [avg_transaction - padding_y * 1.1, avg_transaction + padding_y * 1.1]

        fig = px.scatter(
            df, x="total_customers", y="total_transactions",
            size="visual_size", color="avg_trans_per_cust",
            hover_name="country",
            color_continuous_scale=color_scale,
            template="plotly_dark", 
            height=600,
            range_x=range_x,
            range_y=range_y,
            labels={
                "total_customers": "Total Customers",
                "total_transactions": "Total Transactions",
                "avg_trans_per_cust": "Avg Trans/Cust"
            },
            hover_data={'visual_size': False, 'avg_trans_per_cust': ':.2f'}
        )
        
        # Garis benchmark
        fig.add_vline(x=avg_customer, line_dash="dot", line_color="rgba(255,255,255,0.4)", opacity=0.6)
        fig.add_hline(y=avg_transaction, line_dash="dot", line_color="rgba(255,255,255,0.4)", opacity=0.6)
        
        # Kuadran background
        fig.add_vrect(x0=avg_customer, x1=range_x[1], fillcolor="green", opacity=0.04, line_width=0)
        fig.add_hrect(y0=avg_transaction, y1=range_y[1], fillcolor="green", opacity=0.04, line_width=0)

        fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color='rgba(255,255,255,0.3)')))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='#1c2128',
            font=dict(family='Inter', color='#8b949e', size=11),
            xaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
            yaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
            coloraxis_colorbar=dict(thickness=10, len=0.5, bgcolor='rgba(0,0,0,0)',
                                    tickfont=dict(color='#8b949e', size=10),
                                    title=dict(font=dict(color='#8b949e', size=10))),
            margin=dict(l=0, r=0, t=16, b=0),
        )
        st.plotly_chart(fig, use_container_width=True)

    # Isi masing-masing Tab
    with tab1:
        render_segmented_scatter(
            df_top_market, 
            "Top Market (Priority 1)", 
            "Viridis",
            "Countries with Total Customer and Transaction Above Global Average."
        )
        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:20px 0;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info("###  Segmentation Detail")
            st.write(f"""
            - **Number of Countries:** {len(df_top_market)} countries.
            - **Contribution:** These countries represent the largest contributors to overall business transactions.
            - **Condition:** These markets are well-established, supported by a large and stable customer base.
            """)
        with col2:
            st.success("### Strategic Recommendation")
            st.write("""
            - **Customer Retention:** Focus on loyalty programs (such as memberships) to prevent customer churn.
            - **Upselling:** Offer premium film categories or rental bundle packages.
            - **Operational Excellence:** Ensure the availability of popular film inventory is consistently maintained due to high demand volume.
            """)

    with tab2:
        render_segmented_scatter(
            df_high_value, 
            "High Value Market (Niche)", 
            "Magenta",
            "Countries with a small market size but very high customer loyalty (transactions per customer)."
        )
        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:20px 0;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info("### Segmentation Detail")
            avg_l_niche = df_high_value['avg_trans_per_cust'].mean()
            st.write(f"""
            - **Customer Quality:** Very high ({avg_l_niche:.2f} transactions per customer).
            - **Efficiency:** Lower acquisition costs due to a small but highly active customer base.
            - **Potential:** A profitable “hidden gem” market.
            """)
        with col2:
            st.success("### Strategic Recommendation")
            st.write("""
            - **Community Engagement:** Build communities or host special events for cinephiles in these countries.
            - **Personalized Marketing:** Use highly personalized film recommendations based on their viewing history.
            - **Referral Program:** Encourage these loyal customers to invite friends or family, as they are the best promoters.
            """)

    with tab3:
        render_segmented_scatter(
            df_growth_market, 
            "Growth Market (Standard/New)", 
            "Blues",
            "Countries that fall below the average volume and require further development strategies."
        )
        st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:20px 0;'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.info("### Segmentation Detail")
            st.write(f"""
            - **Challenge:** The number of customers is small and the rental frequency is still low.
            - **Status:** These markets are either new or currently stagnating.
            - **Focus:** Require further market education and awareness efforts.
            """)
        with col2:
            st.success("### Strategic Recommendation")
            st.write("""
            - **Market Penetration:** Offer promotions such as “First Rental Free” or large discounts to attract initial interest.
            - **Content Localization:** Evaluate whether the available film genres match the local preferences in those countries.
            - **Brand Awareness:** Increase marketing investment (advertising) to introduce the service in these regions.
            """)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:20px 0;'>", unsafe_allow_html=True)
    
   # --- PART: DETAIL PER LOCATION ---
    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:28px 0;'>", unsafe_allow_html=True)
    st.markdown("<div class='sec-title'>Deep Dive: Customer Detail by Location</div>", unsafe_allow_html=True)
    st.markdown("<div class='sec-sub'>Filter per negara dan kota untuk analisis granular customer.</div>", unsafe_allow_html=True)

    # 1. Filter Baris
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        selected_country = st.selectbox("Choose Country:", sorted(df_raw['country'].unique()))
    with col_f2:
        available_cities = sorted(df_raw[df_raw['country'] == selected_country]['city'].unique())
        selected_city = st.selectbox(f"Choose City in {selected_country}:", ["All City"] + available_cities)

    # Filter Data Berdasarkan Pilihan
    if selected_city == "All City":
        loc_data = df_raw[df_raw['country'] == selected_country].copy()
        location_name = selected_country
    else:
        loc_data = df_raw[(df_raw['country'] == selected_country) & (df_raw['city'] == selected_city)].copy()
        location_name = f"{selected_city}, {selected_country}"

    # --- 2. LOGIKA PERHITUNGAN RFM (WAJIB DI ATAS SEBELUM VISUALISASI) ---
    loc_data['payment_date'] = pd.to_datetime(loc_data['payment_date'])
    df_raw['payment_date'] = pd.to_datetime(df_raw['payment_date'])
    last_db_date = df_raw['payment_date'].max()

    customer_detail = loc_data.groupby(['customer_id', 'customer_name']).agg({
        'payment_id': 'count',
        'amount': 'sum',
        'payment_date': 'max'
    }).reset_index()

    customer_detail['Recency'] = (last_db_date - customer_detail['payment_date']).dt.days
    customer_detail = customer_detail.rename(columns={
        'customer_id': 'ID',
        'customer_name': 'Name',
        'payment_id': 'Frequency',
        'amount': 'Monetary'
    })

    # --- 3. TAMPILAN METRIK RINGKASAN ---
    st.markdown(f"<div class='sec-title'>Summary — {location_name}</div>", unsafe_allow_html=True)
    st.markdown("<hr class='sec-divider'>", unsafe_allow_html=True)
    m_col1, m_col2, m_col3 = st.columns(3)
    m_col1.markdown(kpi("Total Customer",     f"{len(customer_detail):,}",                 "unique customers"),      unsafe_allow_html=True)
    m_col2.markdown(kpi("Total Revenue",      f"${customer_detail['Monetary'].sum():,.2f}", "gross revenue"),         unsafe_allow_html=True)
    m_col3.markdown(kpi("Total Transactions", f"{customer_detail['Frequency'].sum():,}",    "all transactions"),      unsafe_allow_html=True)

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    a_col1, a_col2, a_col3 = st.columns(3)
    a_col1.markdown(kpi("Avg Frequency", f"{customer_detail['Frequency'].mean():.1f}x",    "per customer"),          unsafe_allow_html=True)
    a_col2.markdown(kpi("Avg Monetary",  f"${customer_detail['Monetary'].mean():,.2f}",     "avg spend / customer"),  unsafe_allow_html=True)
    a_col3.markdown(kpi("Avg Recency",   f"{customer_detail['Recency'].mean():.1f} days",   "since last purchase"),   unsafe_allow_html=True)

    st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.07);margin:28px 0;'>", unsafe_allow_html=True)

    # --- 1. SIAPKAN DATA PERBANDINGAN ---
    # Data Negara yang dipilih
    country_data = df_grouped[df_grouped['country'] == selected_country].iloc[0]
    
    # Data Benchmark (Rata-rata per Negara yang kita buat tadi)
    # avg_trans_per_country dan avg_spending_per_country diambil dari variabel di atas
    
    comparison_data = pd.DataFrame({
        'Category': ['Total Transactions', 'Total Revenue'],
        'Selected Country': [country_data['total_transactions'], country_data['total_revenue']],
        'Global Average': [avg_trans_per_country, avg_spending_per_country]
    })

    # --- 2. VISUALISASI PERBANDINGAN ---
    st.write(f"### {selected_country} Performance vs Global Average")
    
    # Kita buat 2 grafik bersisian agar skalanya tidak jomplang (karena transaksi puluhan vs revenue ribuan)
    comp_col1, comp_col2 = st.columns(2)

    with comp_col1:
        # Grafik Perbandingan Transaksi
        fig_comp_trans = px.bar(
            comparison_data[comparison_data['Category'] == 'Total Transactions'],
            x='Category',
            y=['Selected Country', 'Global Average'],
            barmode='group',
            title=f"Transaction Volume: {selected_country} vs Avg",
            labels={'value': 'Count', 'variable': 'Legend'},
            color_discrete_map={'Selected Country': '#3366CC', 'Global Average': '#AAAAAA'}
        )
        fig_comp_trans.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1c2128',
            font=dict(family='Inter', color='#8b949e', size=11),
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#8b949e')),
            yaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b949e', size=11)),
            title=dict(font=dict(color='#c9d1d9', size=12, family='Inter')),
            margin=dict(t=36, b=0, l=0, r=0),
        )
        st.plotly_chart(fig_comp_trans, use_container_width=True)

    with comp_col2:
        # Grafik Perbandingan Revenue
        fig_comp_rev = px.bar(
            comparison_data[comparison_data['Category'] == 'Total Revenue'],
            x='Category',
            y=['Selected Country', 'Global Average'],
            barmode='group',
            title=f"Revenue Value: {selected_country} vs Avg",
            labels={'value': 'Amount ($)', 'variable': 'Legend'},
            color_discrete_map={'Selected Country': '#FF4B4B', 'Global Average': '#AAAAAA'}
        )
        fig_comp_rev.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='#1c2128',
            font=dict(family='Inter', color='#8b949e', size=11),
            xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color='#8b949e')),
            yaxis=dict(showgrid=True, gridcolor='#30363d', zeroline=False, tickfont=dict(color='#8b949e')),
            legend=dict(bgcolor='rgba(0,0,0,0)', font=dict(color='#8b949e', size=11)),
            title=dict(font=dict(color='#c9d1d9', size=12, family='Inter')),
            margin=dict(t=36, b=0, l=0, r=0),
        )
        st.plotly_chart(fig_comp_rev, use_container_width=True)

    # --- 3. INSIGHT DINAMIS ---
    diff_rev = country_data['total_revenue'] - avg_spending_per_country
    if diff_rev > 0:
        st.success(f"🔥 **{selected_country}** generates ${diff_rev:,.2f} **higher revenue than the global average.**")
    else:
        st.warning(f"⚠️ **{selected_country}** generates ${abs(diff_rev):,.2f} **less revenue than the global average.**")

    # --- 5. TABEL DETAIL ---
    st.write(f"**Individual Customer Data:**")
    st.dataframe(
        customer_detail[['ID', 'Name', 'Frequency', 'Monetary', 'Recency']].sort_values(by='Monetary', ascending=False),
        use_container_width=True,
        hide_index=True
    )

# Penutup blok Try-Except yang sudah ada di kode kamu
except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
    st.info("Pastikan file dvdrental_data.csv ada di root folder project (satu level di atas folder pages/).")
        
        # with col_tab2:
        #     st.write("Data Table (Customer & Transaction)")
        #     # Menampilkan tabel yang bisa di-sort oleh user
        #     st.dataframe(
        #         df_grouped[['country', 'total_customers', 'total_transactions', 'total_revenue']],
        #         use_container_width=True,
        #         hide_index=True 
        #  )
    
# except Exception as e:
#     st.error(f"Gagal koneksi ke database: {e}")
#     st.info("Pastikan database PostgreSQL kamu menyala dan detail login sudah benar.")