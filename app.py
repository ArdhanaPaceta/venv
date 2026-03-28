import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# ====== CONFIG ======
st.set_page_config(
    page_title="💰 Money AI App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== CUSTOM CSS ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

/* ===== GLOBAL RESET ===== */
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

.main { background: #0f0f1a; }
.block-container { padding: 2rem 2.5rem 4rem !important; max-width: 1200px; }

/* ===== HEADER ===== */
.hero-header {
    background: linear-gradient(135deg, #1a1a3e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 24px;
    padding: 2.5rem 3rem;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -40px; left: -40px;
    width: 150px; height: 150px;
    background: radial-gradient(circle, rgba(16,185,129,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 2.4rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #34d399 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0 0 0.4rem 0;
}
.hero-subtitle {
    color: rgba(255,255,255,0.5);
    font-size: 0.95rem;
    font-weight: 400;
    margin: 0;
}

/* ===== METRIC CARDS ===== */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    border-radius: 20px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06);
}
.metric-card.balance {
    background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
}
.metric-card.income {
    background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
}
.metric-card.expense {
    background: linear-gradient(135deg, #450a0a 0%, #7f1d1d 100%);
}
.metric-card-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.4rem;
    margin-bottom: 1rem;
}
.balance .metric-card-icon { background: rgba(99,102,241,0.25); }
.income .metric-card-icon { background: rgba(16,185,129,0.25); }
.expense .metric-card-icon { background: rgba(239,68,68,0.25); }
.metric-label {
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
}
.balance .metric-label { color: #a5b4fc; }
.income .metric-label { color: #6ee7b7; }
.expense .metric-label { color: #fca5a5; }
.metric-value {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.7rem;
    font-weight: 700;
    color: #ffffff;
}

/* ===== SECTION TITLES ===== */
.section-title {
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.1rem;
    font-weight: 700;
    color: #e2e8f0;
    margin: 2rem 0 1rem 0;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-title span {
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px;
    padding: 2px 10px;
    font-size: 0.85rem;
    color: #a5b4fc;
}

/* ===== CARDS ===== */
.card {
    background: #1a1a2e;
    border-radius: 20px;
    padding: 1.5rem;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1rem;
}

/* ===== FORM ELEMENTS ===== */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #12122a !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 12px !important;
    color: #e2e8f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    padding: 0.6rem 1rem !important;
}
div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.15) !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
}

/* ===== BUTTONS ===== */
div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.02em !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 20px rgba(99,102,241,0.4) !important;
    background: linear-gradient(135deg, #5b52f0, #8b46f0) !important;
}
div[data-testid="stButton"] button:active {
    transform: translateY(0px) !important;
}

/* ===== ALERTS / MESSAGES ===== */
div[data-testid="stSuccess"],
div[data-testid="stAlert"] {
    border-radius: 14px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}

/* ===== DATAFRAME ===== */
div[data-testid="stDataFrame"] {
    border-radius: 16px !important;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06) !important;
}
.stDataFrame table {
    background: #12122a !important;
    color: #e2e8f0 !important;
}
.stDataFrame thead th {
    background: #1e1b4b !important;
    color: #a5b4fc !important;
    font-size: 0.78rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    border-bottom: 1px solid rgba(99,102,241,0.3) !important;
}
.stDataFrame tbody tr:nth-child(even) {
    background: rgba(255,255,255,0.02) !important;
}
.stDataFrame tbody tr:hover {
    background: rgba(99,102,241,0.08) !important;
}

/* ===== EXPANDER ===== */
div[data-testid="stExpander"] {
    background: #1a1a2e !important;
    border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 16px !important;
    overflow: hidden;
}
div[data-testid="stExpander"] summary {
    color: #a5b4fc !important;
    font-weight: 600 !important;
    padding: 1rem 1.25rem !important;
}
div[data-testid="stExpander"] summary:hover {
    background: rgba(99,102,241,0.08) !important;
}

/* ===== TAB ===== */
div[data-testid="stTabs"] button {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-weight: 600 !important;
    color: #64748b !important;
    border-radius: 10px 10px 0 0 !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #a5b4fc !important;
    border-bottom-color: #6366f1 !important;
}

/* ===== TRANSACTION PILL ===== */
.tx-pill {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.04em;
}
.tx-income { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.25); }
.tx-expense { background: rgba(239,68,68,0.15); color: #f87171; border: 1px solid rgba(239,68,68,0.25); }

/* ===== AI CHAT BUBBLE ===== */
.chat-bubble-user {
    background: linear-gradient(135deg, #312e81, #4f46e5);
    border-radius: 16px 16px 4px 16px;
    padding: 0.9rem 1.2rem;
    color: white;
    margin: 0.5rem 0 0.5rem 20%;
    font-size: 0.92rem;
    line-height: 1.6;
}
.chat-bubble-ai {
    background: #1e1b4b;
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px 16px 16px 4px;
    padding: 0.9rem 1.2rem;
    color: #e2e8f0;
    margin: 0.5rem 20% 0.5rem 0;
    font-size: 0.92rem;
    line-height: 1.6;
}
.ai-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    padding: 4px 12px;
    font-size: 0.75rem;
    font-weight: 600;
    color: #a5b4fc;
    margin-bottom: 0.75rem;
}

/* ===== PROGRESS BAR ===== */
.progress-track {
    background: rgba(255,255,255,0.06);
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
    margin: 0.4rem 0;
}
.progress-fill-green {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #059669, #34d399);
    transition: width 0.6s ease;
}
.progress-fill-red {
    height: 100%;
    border-radius: 100px;
    background: linear-gradient(90deg, #dc2626, #f87171);
    transition: width 0.6s ease;
}

/* ===== SCROLLBAR ===== */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 10px; }

/* ===== DIVIDER ===== */
hr { border-color: rgba(255,255,255,0.06) !important; margin: 1.5rem 0 !important; }

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #12122a !important;
    border-right: 1px solid rgba(255,255,255,0.06) !important;
}
</style>
""", unsafe_allow_html=True)

# ====== DATA FILE ======
DATA_FILE = "data.json"

# ====== LOAD DATA ======
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"balance": 0, "transactions": []}

def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def format_rupiah(amount):
    return f"Rp {int(amount):,}".replace(",", ".")

# ====== HERO HEADER ======
st.markdown("""
<div class="hero-header">
    <div class="hero-title">💰 Money AI App</div>
    <div class="hero-subtitle">Kelola keuangan kamu dengan cerdas — analisis otomatis & saran AI real-time</div>
</div>
""", unsafe_allow_html=True)

# ====== CALCULATE STATS ======
total_income  = sum(t["jumlah"] for t in data["transactions"] if t["tipe"] == "Pemasukan")
total_expense = sum(t["jumlah"] for t in data["transactions"] if t["tipe"] == "Pengeluaran")
total_tx      = len(data["transactions"])

# ====== METRIC CARDS ======
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card balance">
        <div class="metric-card-icon">🏦</div>
        <div class="metric-label">Saldo Saat Ini</div>
        <div class="metric-value">{format_rupiah(data['balance'])}</div>
    </div>
    <div class="metric-card income">
        <div class="metric-card-icon">📈</div>
        <div class="metric-label">Total Pemasukan</div>
        <div class="metric-value">{format_rupiah(total_income)}</div>
    </div>
    <div class="metric-card expense">
        <div class="metric-card-icon">📉</div>
        <div class="metric-label">Total Pengeluaran</div>
        <div class="metric-value">{format_rupiah(total_expense)}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====== MAIN TABS ======
tab1, tab2, tab3, tab4 = st.tabs(["💳 Transaksi", "📊 Analisis", "💬 Tanya AI", "⚙️ Pengaturan"])

# ========================
# TAB 1 — TRANSAKSI
# ========================
with tab1:
    st.markdown('<div class="section-title">➕ Tambah Transaksi Baru <span>Catat pengeluaran & pemasukan</span></div>', unsafe_allow_html=True)

    with st.container():
        c1, c2, c3 = st.columns([1, 1, 2])
        with c1:
            tipe = st.selectbox("Tipe Transaksi", ["Pemasukan", "Pengeluaran"],
                                help="Pilih jenis transaksi")
        with c2:
            kategori_options = {
                "Pemasukan": ["💼 Gaji", "🏪 Bisnis", "💰 Investasi", "🎁 Hadiah", "📦 Lainnya"],
                "Pengeluaran": ["🍔 Makanan", "🚗 Transportasi", "🛍️ Belanja", "💡 Tagihan", "🎮 Hiburan", "🏥 Kesehatan", "📚 Pendidikan", "📦 Lainnya"]
            }
            kategori = st.selectbox("Kategori", kategori_options[tipe])
        with c3:
            deskripsi = st.text_input("Deskripsi", placeholder="Contoh: Gaji bulan Maret, Makan siang...")

        c4, c5 = st.columns([2, 1])
        with c4:
            jumlah = st.number_input("Jumlah (Rp)", min_value=0, step=1000,
                                     format="%d", help="Masukkan nominal transaksi")
        with c5:
            st.markdown("<br>", unsafe_allow_html=True)
            add_btn = st.button("➕ Tambah Transaksi", use_container_width=True)

    if add_btn:
        if jumlah > 0:
            if tipe == "Pemasukan":
                data["balance"] += jumlah
            else:
                data["balance"] -= jumlah
            transaksi = {
                "tipe": tipe,
                "kategori": kategori,
                "jumlah": jumlah,
                "deskripsi": deskripsi if deskripsi else "-",
                "tanggal": datetime.now().strftime("%d %b %Y, %H:%M")
            }
            data["transactions"].append(transaksi)
            save_data()
            icon = "✅" if tipe == "Pemasukan" else "🔴"
            st.success(f"{icon} Transaksi **{format_rupiah(jumlah)}** berhasil ditambahkan!")
            st.rerun()
        else:
            st.error("⚠️ Jumlah transaksi harus lebih dari 0!")

    # ====== RIWAYAT ======
    st.markdown('<div class="section-title">📋 Riwayat Transaksi <span>' + str(total_tx) + ' transaksi</span></div>', unsafe_allow_html=True)

    if data["transactions"]:
        # Filter & Search
        cf1, cf2 = st.columns([1, 2])
        with cf1:
            filter_tipe = st.selectbox("Filter", ["Semua", "Pemasukan", "Pengeluaran"], key="filter_tipe")
        with cf2:
            search_query = st.text_input("🔍 Cari transaksi...", placeholder="Ketik deskripsi atau kategori", key="search_tx")

        txs = data["transactions"].copy()
        if filter_tipe != "Semua":
            txs = [t for t in txs if t["tipe"] == filter_tipe]
        if search_query:
            txs = [t for t in txs if search_query.lower() in t.get("deskripsi","").lower()
                                   or search_query.lower() in t.get("kategori","").lower()]

        # Pastikan semua transaksi punya field "kategori" (data lama mungkin belum)
        for t in txs:
            if "kategori" not in t:
                t["kategori"] = "📦 Lainnya"

        df = pd.DataFrame(txs[::-1])  # Newest first
        if not df.empty:
            df = df[["tipe", "kategori", "jumlah", "deskripsi", "tanggal"]]
            df.columns = ["Tipe", "Kategori", "Jumlah (Rp)", "Deskripsi", "Tanggal"]
            df["Jumlah (Rp)"] = df["Jumlah (Rp)"].apply(lambda x: f"{int(x):,}".replace(",","."))
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Tidak ada transaksi yang cocok dengan filter.")

        # Hapus semua
        with st.expander("🗑️ Hapus Semua Data"):
            st.warning("⚠️ Tindakan ini tidak bisa dibatalkan!")
            if st.button("🗑️ Hapus Semua Transaksi", type="secondary"):
                data["transactions"] = []
                data["balance"] = 0
                save_data()
                st.success("Data berhasil dihapus.")
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center; padding: 3rem 2rem; color: rgba(255,255,255,0.3);">
            <div style="font-size: 3rem; margin-bottom: 1rem;">📭</div>
            <div style="font-size: 1rem; font-weight: 500;">Belum ada transaksi</div>
            <div style="font-size: 0.85rem; margin-top: 0.4rem;">Tambahkan transaksi pertama kamu di atas!</div>
        </div>
        """, unsafe_allow_html=True)

# ========================
# TAB 2 — ANALISIS
# ========================
with tab2:
    st.markdown('<div class="section-title">📊 Ringkasan Keuangan</div>', unsafe_allow_html=True)

    if total_income == 0 and total_expense == 0:
        st.info("Belum ada data untuk dianalisis. Tambahkan transaksi terlebih dahulu!")
    else:
        # Health Score
        if total_income > 0:
            savings_rate = ((total_income - total_expense) / total_income) * 100
        else:
            savings_rate = 0

        if savings_rate >= 30:
            health_color, health_emoji, health_label = "#34d399", "💚", "Sangat Sehat"
        elif savings_rate >= 10:
            health_color, health_emoji, health_label = "#fbbf24", "💛", "Cukup Baik"
        else:
            health_color, health_emoji, health_label = "#f87171", "❤️", "Perlu Perhatian"

        st.markdown(f"""
        <div class="card" style="text-align:center; padding: 2rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">{health_emoji}</div>
            <div style="font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.1em; color: rgba(255,255,255,0.4); margin-bottom: 0.5rem;">Kondisi Keuangan</div>
            <div style="font-size: 1.8rem; font-weight: 800; color: {health_color};">{health_label}</div>
            <div style="font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-top: 0.4rem;">Tingkat tabungan: <b style="color:{health_color}">{savings_rate:.1f}%</b></div>
        </div>
        """, unsafe_allow_html=True)

        # Income vs Expense bars
        col_a, col_b = st.columns(2)

        with col_a:
            max_val = max(total_income, total_expense, 1)
            pct = (total_income / max_val) * 100
            st.markdown(f"""
            <div class="card">
                <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.07em; color: #6ee7b7; font-weight: 600; margin-bottom: 0.6rem;">📈 Total Pemasukan</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #fff; margin-bottom: 0.8rem;">{format_rupiah(total_income)}</div>
                <div class="progress-track"><div class="progress-fill-green" style="width:{pct}%"></div></div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.35); margin-top: 0.4rem;">{total_tx} transaksi total</div>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            pct2 = (total_expense / max_val) * 100
            st.markdown(f"""
            <div class="card">
                <div style="font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.07em; color: #fca5a5; font-weight: 600; margin-bottom: 0.6rem;">📉 Total Pengeluaran</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: #fff; margin-bottom: 0.8rem;">{format_rupiah(total_expense)}</div>
                <div class="progress-track"><div class="progress-fill-red" style="width:{pct2}%"></div></div>
                <div style="font-size: 0.8rem; color: rgba(255,255,255,0.35); margin-top: 0.4rem;">Sisa: {format_rupiah(total_income - total_expense)}</div>
            </div>
            """, unsafe_allow_html=True)

        # Category Breakdown
        if data["transactions"]:
            st.markdown('<div class="section-title">🗂️ Pengeluaran per Kategori</div>', unsafe_allow_html=True)
            expense_by_cat = {}
            for t in data["transactions"]:
                if t["tipe"] == "Pengeluaran":
                    cat = t.get("kategori", "📦 Lainnya")
                    expense_by_cat[cat] = expense_by_cat.get(cat, 0) + t["jumlah"]

            if expense_by_cat:
                sorted_cats = sorted(expense_by_cat.items(), key=lambda x: x[1], reverse=True)
                total_exp_cat = sum(v for _, v in sorted_cats)
                for cat, amt in sorted_cats:
                    pct_cat = (amt / total_exp_cat) * 100 if total_exp_cat > 0 else 0
                    st.markdown(f"""
                    <div style="margin-bottom: 1rem;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                            <span style="color:#e2e8f0; font-size:0.88rem;">{cat}</span>
                            <span style="color:#a5b4fc; font-size:0.88rem; font-weight:600;">{format_rupiah(amt)} <span style="color:rgba(255,255,255,0.3)">({pct_cat:.0f}%)</span></span>
                        </div>
                        <div class="progress-track"><div class="progress-fill-red" style="width:{pct_cat}%"></div></div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Belum ada data pengeluaran per kategori.")

        # Tips
        st.markdown('<div class="section-title">💡 Tips Keuangan</div>', unsafe_allow_html=True)

        tips = []
        if savings_rate < 20:
            tips.append(("🔴", "Coba ikuti aturan 50/30/20", "50% kebutuhan, 30% keinginan, 20% tabungan untuk keuangan yang sehat."))
        if total_expense > total_income * 0.7:
            tips.append(("🟡", "Pengeluaran cukup tinggi", "Identifikasi kategori terbesar dan coba kurangi 10-15% dari sana."))
        if savings_rate >= 20:
            tips.append(("🟢", "Kamu menabung dengan baik!", f"Kamu menyimpan {savings_rate:.0f}% dari pendapatan. Pertimbangkan untuk investasi."))
        if total_tx == 0:
            tips.append(("ℹ️", "Mulai catat keuangan kamu", "Konsistensi mencatat transaksi adalah kunci kendali keuangan."))

        for icon, title, desc in tips:
            st.markdown(f"""
            <div class="card" style="display:flex; gap:1rem; align-items:flex-start; margin-bottom:0.75rem;">
                <div style="font-size:1.4rem; margin-top:2px;">{icon}</div>
                <div>
                    <div style="font-weight:700; color:#e2e8f0; font-size:0.92rem; margin-bottom:0.25rem;">{title}</div>
                    <div style="color:rgba(255,255,255,0.5); font-size:0.84rem; line-height:1.5;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ========================
# TAB 3 — TANYA AI
# ========================
with tab3:
    st.markdown('<div class="section-title">🤖 AI Keuangan Pribadi</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="ai-badge">🤖 AI Powered • Saran keuangan otomatis</div>
    """, unsafe_allow_html=True)

    # Quick ask buttons
    st.markdown("**Pertanyaan cepat:**")
    qcol1, qcol2, qcol3 = st.columns(3)
    quick_qs = [
        "Bagaimana kondisi keuangan saya?",
        "Cara hemat lebih efektif?",
        "Kapan saya bisa investasi?"
    ]

    selected_quick = None
    with qcol1:
        if st.button(quick_qs[0], use_container_width=True, key="q1"):
            selected_quick = quick_qs[0]
    with qcol2:
        if st.button(quick_qs[1], use_container_width=True, key="q2"):
            selected_quick = quick_qs[1]
    with qcol3:
        if st.button(quick_qs[2], use_container_width=True, key="q3"):
            selected_quick = quick_qs[2]

    pertanyaan = st.text_input("💬 Tanya apapun tentang keuanganmu",
                                placeholder="Contoh: Apakah pengeluaran saya terlalu besar bulan ini?",
                                value=selected_quick if selected_quick else "")

    if st.button("🚀 Kirim Pertanyaan", use_container_width=False):
        if pertanyaan:
            st.markdown(f"""
            <div class="chat-bubble-user">{pertanyaan}</div>
            """, unsafe_allow_html=True)

            # Simple rule-based AI response
            p = pertanyaan.lower()
            if any(kw in p for kw in ["kondisi", "bagaimana", "analisis", "analisa", "kesehatan"]):
                if total_income == 0:
                    resp = f"📊 Belum ada data pemasukan. Mulailah mencatat transaksimu agar saya bisa menganalisis kondisi keuanganmu secara akurat."
                elif total_expense > total_income:
                    resp = f"⚠️ Keuanganmu sedang dalam kondisi **defisit**. Pengeluaranmu ({format_rupiah(total_expense)}) melebihi pemasukan ({format_rupiah(total_income)}). Segera kurangi pengeluaran tidak esensial dan cari sumber pendapatan tambahan."
                elif total_expense > total_income * 0.7:
                    resp = f"⚡ Keuanganmu **cukup baik** tapi pengeluaran cukup tinggi ({(total_expense/total_income*100):.0f}% dari pemasukan). Saldo kamu {format_rupiah(data['balance'])}. Coba targetkan hemat 10% lebih banyak bulan depan."
                else:
                    resp = f"✅ Keuanganmu dalam kondisi **sehat**! Kamu berhasil menyimpan {((total_income-total_expense)/total_income*100):.0f}% dari pemasukan. Saldo saat ini {format_rupiah(data['balance'])}. Pertimbangkan untuk mulai berinvestasi!"
            elif any(kw in p for kw in ["hemat", "kurangi", "irit", "efisien"]):
                resp = "💡 Tips hemat yang efektif:\n\n1. **Catat semua pengeluaran** — kesadaran adalah langkah pertama\n2. **Gunakan aturan 24 jam** — tunda pembelian non-esensial sehari\n3. **Meal prep** — masak sendiri bisa hemat 40-60% biaya makan\n4. **Audit langganan** — batalkan yang jarang dipakai\n5. **Pisahkan rekening** — rekening tabungan dan harian yang berbeda"
            elif any(kw in p for kw in ["investasi", "invest", "saham", "reksa"]):
                if data["balance"] > 1_000_000:
                    resp = f"📈 Dengan saldo {format_rupiah(data['balance'])}, kamu sudah bisa mulai investasi! Rekomendasiku:\n\n• **Reksa Dana Pasar Uang** — risiko rendah, cocok untuk pemula\n• **ORI/SBR** — obligasi pemerintah, aman & return bagus\n• **Reksa Dana Indeks** — diversifikasi otomatis jangka panjang\n\nPastikan kamu punya dana darurat 3-6 bulan pengeluaran dulu ya!"
                else:
                    resp = "🏦 Untuk memulai investasi, pastikan:\n1. Dana darurat minimal 3 bulan sudah tersedia\n2. Utang konsumtif sudah lunas\n3. Punya saldo minimal Rp 100.000 untuk mulai reksa dana\n\nFokus dulu perbesar saldo tabunganmu!"
            elif any(kw in p for kw in ["saldo", "berapa", "total"]):
                resp = f"💰 Berikut ringkasan keuanganmu:\n\n• **Saldo:** {format_rupiah(data['balance'])}\n• **Total Pemasukan:** {format_rupiah(total_income)}\n• **Total Pengeluaran:** {format_rupiah(total_expense)}\n• **Jumlah Transaksi:** {total_tx} transaksi"
            else:
                resp = f"🤖 Terima kasih pertanyaannya! Berdasarkan data keuanganmu saat ini (saldo {format_rupiah(data['balance'])}, {total_tx} transaksi), aku siap membantu analisis lebih lanjut. Coba tanya lebih spesifik seperti 'analisis kondisi keuanganku' atau 'tips hemat untuk saya'."

            st.markdown(f"""
            <div class="chat-bubble-ai">{resp}</div>
            """, unsafe_allow_html=True)
        else:
            st.warning("Tulis pertanyaanmu dulu ya!")

# ========================
# TAB 4 — PENGATURAN
# ========================
with tab4:
    st.markdown('<div class="section-title">⚙️ Pengaturan Akun</div>', unsafe_allow_html=True)

    with st.expander("💳 Set Saldo Awal / Reset Saldo"):
        st.markdown("Gunakan ini untuk menetapkan saldo awal atau mengoreksi saldo yang tidak sesuai.")
        saldo_baru = st.number_input("Saldo baru (Rp)", min_value=0, step=10000,
                                      value=int(data["balance"]), format="%d")
        if st.button("💾 Simpan Saldo", key="save_saldo"):
            data["balance"] = saldo_baru
            save_data()
            st.success(f"✅ Saldo berhasil diperbarui ke {format_rupiah(saldo_baru)}!")
            st.rerun()

    with st.expander("📤 Export Data"):
        if data["transactions"]:
            df_export = pd.DataFrame(data["transactions"])
            csv = df_export.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv,
                file_name=f"money_ai_export_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        else:
            st.info("Belum ada data untuk diexport.")

    with st.expander("ℹ️ Tentang Aplikasi"):
        st.markdown("""
        <div style="color: rgba(255,255,255,0.6); font-size: 0.88rem; line-height: 1.8;">
            <b style="color:#a5b4fc">💰 Money AI App</b> — v2.0<br>
            Aplikasi manajemen keuangan pribadi dengan analisis AI sederhana.<br><br>
            <b style="color:#e2e8f0">Fitur:</b><br>
            • Catat pemasukan & pengeluaran<br>
            • Kategorisasi otomatis<br>
            • Analisis kondisi keuangan<br>
            • Saran AI berbasis data kamu<br>
            • Export data CSV
        </div>
        """, unsafe_allow_html=True)

# ====== FOOTER ======
st.markdown("""
<div style="text-align:center; padding: 3rem 0 1rem; color: rgba(255,255,255,0.2); font-size: 0.78rem;">
    💰 Money AI App • Dibuat dengan ❤️ menggunakan Streamlit
</div>
""", unsafe_allow_html=True)