import streamlit as st
import pandas as pd
from datetime import datetime
from supabase import create_client, Client

# ====== CONFIG ======
st.set_page_config(
    page_title="💰 Money AI App",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ====== CUSTOM CSS (RESPONSIVE) ======
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif !important; }
.main { background: #0f0f1a; }

.block-container { padding: 1rem 0.8rem 4rem !important; max-width: 1200px; }
@media (min-width: 768px) { .block-container { padding: 2rem 2.5rem 4rem !important; } }

.hero-header {
    background: linear-gradient(135deg, #1a1a3e 0%, #16213e 50%, #0f3460 100%);
    border-radius: 16px; padding: 1.3rem 1.3rem; margin-bottom: 1rem;
    border: 1px solid rgba(255,255,255,0.08); position: relative; overflow: hidden;
}
@media (min-width: 768px) { .hero-header { border-radius: 24px; padding: 2.5rem 3rem; margin-bottom: 2rem; } }
.hero-header::before {
    content: ''; position: absolute; top: -60px; right: -60px; width: 180px; height: 180px;
    background: radial-gradient(circle, rgba(99,102,241,0.3) 0%, transparent 70%); border-radius: 50%;
}
.hero-title {
    font-family: 'Space Grotesk', sans-serif !important; font-size: 1.5rem; font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #a5b4fc 50%, #34d399 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0 0 0.25rem 0;
}
@media (min-width: 768px) { .hero-title { font-size: 2.4rem; } }
.hero-subtitle { color: rgba(255,255,255,0.5); font-size: 0.8rem; margin: 0; }
@media (min-width: 768px) { .hero-subtitle { font-size: 0.95rem; } }

/* METRIC CARDS — stacked on mobile, 3-col on tablet+ */
.metric-grid { display: grid; grid-template-columns: 1fr; gap: 0.6rem; margin-bottom: 1rem; }
@media (min-width: 480px) { .metric-grid { grid-template-columns: repeat(3, 1fr); } }
@media (min-width: 768px) { .metric-grid { gap: 1rem; margin-bottom: 2rem; } }

.metric-card {
    border-radius: 14px; padding: 0.9rem 1rem;
    border: 1px solid rgba(255,255,255,0.06);
    display: flex; align-items: center; gap: 0.9rem;
}
@media (min-width: 480px) { .metric-card { display: block; padding: 1.1rem; } }
@media (min-width: 768px) { .metric-card { border-radius: 20px; padding: 1.5rem; } }
.metric-card.balance { background: linear-gradient(135deg, #1e1b4b, #312e81); }
.metric-card.income  { background: linear-gradient(135deg, #064e3b, #065f46); }
.metric-card.expense { background: linear-gradient(135deg, #450a0a, #7f1d1d); }

.metric-card-icon {
    width: 38px; height: 38px; border-radius: 11px; flex-shrink: 0;
    display: flex; align-items: center; justify-content: center; font-size: 1.1rem;
}
@media (min-width: 480px) { .metric-card-icon { margin-bottom: 0.7rem; } }
@media (min-width: 768px) { .metric-card-icon { width: 48px; height: 48px; border-radius: 14px; font-size: 1.4rem; margin-bottom: 1rem; } }
.balance .metric-card-icon { background: rgba(99,102,241,0.25); }
.income  .metric-card-icon { background: rgba(16,185,129,0.25); }
.expense .metric-card-icon { background: rgba(239,68,68,0.25); }

.metric-info { flex: 1; min-width: 0; }
.metric-label { font-size: 0.68rem; font-weight: 600; letter-spacing: 0.07em; text-transform: uppercase; margin-bottom: 0.15rem; }
@media (min-width: 768px) { .metric-label { font-size: 0.78rem; margin-bottom: 0.4rem; } }
.balance .metric-label { color: #a5b4fc; }
.income  .metric-label { color: #6ee7b7; }
.expense .metric-label { color: #fca5a5; }
.metric-value {
    font-family: 'Space Grotesk', sans-serif !important; font-size: 1.05rem;
    font-weight: 700; color: #fff; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
@media (min-width: 768px) { .metric-value { font-size: 1.7rem; } }

.section-title {
    font-family: 'Space Grotesk', sans-serif !important; font-size: 0.92rem;
    font-weight: 700; color: #e2e8f0; margin: 1.3rem 0 0.7rem 0;
    display: flex; align-items: center; gap: 0.4rem; flex-wrap: wrap;
}
@media (min-width: 768px) { .section-title { font-size: 1.1rem; margin: 2rem 0 1rem 0; } }
.section-title span {
    background: rgba(99,102,241,0.2); border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px; padding: 2px 8px; font-size: 0.75rem; color: #a5b4fc;
}

.card {
    background: #1a1a2e; border-radius: 14px; padding: 1rem;
    border: 1px solid rgba(255,255,255,0.06); margin-bottom: 0.7rem;
}
@media (min-width: 768px) { .card { border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem; } }

div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] {
    background: #12122a !important; border: 1px solid rgba(99,102,241,0.3) !important;
    border-radius: 12px !important; color: #e2e8f0 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-size: 0.9rem !important;
}
label[data-testid="stWidgetLabel"] p {
    color: #94a3b8 !important; font-size: 0.76rem !important;
    font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 0.06em !important;
}

div[data-testid="stButton"] button {
    background: linear-gradient(135deg, #4f46e5, #7c3aed) !important; color: white !important;
    border: none !important; border-radius: 12px !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.55rem 1rem !important; width: 100% !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button:hover { box-shadow: 0 8px 20px rgba(99,102,241,0.4) !important; }

div[data-testid="stDataFrame"] {
    border-radius: 12px !important; overflow: hidden;
    border: 1px solid rgba(255,255,255,0.06) !important; font-size: 0.8rem !important;
}

div[data-testid="stExpander"] {
    background: #1a1a2e !important; border: 1px solid rgba(255,255,255,0.07) !important;
    border-radius: 14px !important; overflow: hidden;
}
div[data-testid="stExpander"] summary {
    color: #a5b4fc !important; font-weight: 600 !important;
    font-size: 0.88rem !important; padding: 0.85rem 1rem !important;
}

.progress-track { background: rgba(255,255,255,0.06); border-radius: 100px; height: 7px; overflow: hidden; margin: 0.4rem 0; }
.progress-fill-green { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #059669, #34d399); }
.progress-fill-red   { height: 100%; border-radius: 100px; background: linear-gradient(90deg, #dc2626, #f87171); }

.chat-bubble-user {
    background: linear-gradient(135deg, #312e81, #4f46e5);
    border-radius: 16px 16px 4px 16px; padding: 0.75rem 0.9rem;
    color: white; margin: 0.5rem 0 0.5rem 8%; font-size: 0.86rem; line-height: 1.6;
}
@media (min-width: 768px) { .chat-bubble-user { margin-left: 20%; font-size: 0.92rem; padding: 0.9rem 1.2rem; } }
.chat-bubble-ai {
    background: #1e1b4b; border: 1px solid rgba(99,102,241,0.25);
    border-radius: 16px 16px 16px 4px; padding: 0.75rem 0.9rem;
    color: #e2e8f0; margin: 0.5rem 8% 0.5rem 0; font-size: 0.86rem; line-height: 1.6;
}
@media (min-width: 768px) { .chat-bubble-ai { margin-right: 20%; font-size: 0.92rem; padding: 0.9rem 1.2rem; } }
.ai-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px; padding: 3px 10px; font-size: 0.72rem; font-weight: 600;
    color: #a5b4fc; margin-bottom: 0.75rem;
}

div[data-testid="stTabs"] button {
    font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 600 !important;
    color: #64748b !important; font-size: 0.78rem !important; padding: 0.45rem 0.5rem !important;
}
@media (min-width: 768px) { div[data-testid="stTabs"] button { font-size: 0.9rem !important; padding: 0.6rem 1rem !important; } }
div[data-testid="stTabs"] button[aria-selected="true"] { color: #a5b4fc !important; border-bottom-color: #6366f1 !important; }

div[data-testid="stSuccess"], div[data-testid="stAlert"],
div[data-testid="stWarning"], div[data-testid="stInfo"] {
    border-radius: 12px !important; font-size: 0.86rem !important;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 10px; }
hr { border-color: rgba(255,255,255,0.06) !important; margin: 1rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ====== SUPABASE ======
@st.cache_resource
def init_supabase() -> Client:
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_supabase()

def get_balance() -> int:
    res = supabase.table("settings").select("value").eq("key", "balance").execute()
    if res.data:
        return int(res.data[0]["value"])
    supabase.table("settings").insert({"key": "balance", "value": "0"}).execute()
    return 0

def set_balance(amount: int):
    supabase.table("settings").upsert({"key": "balance", "value": str(amount)}).execute()

def get_transactions() -> list:
    res = supabase.table("transactions").select("*").order("id", desc=True).execute()
    return res.data or []

def add_transaction(tipe, kategori, jumlah, deskripsi):
    tanggal = datetime.now().strftime("%d %b %Y, %H:%M")
    supabase.table("transactions").insert({
        "tipe": tipe, "kategori": kategori,
        "jumlah": jumlah, "deskripsi": deskripsi or "-", "tanggal": tanggal
    }).execute()
    bal = get_balance()
    set_balance(bal + jumlah if tipe == "Pemasukan" else bal - jumlah)

def delete_all_transactions():
    supabase.table("transactions").delete().neq("id", 0).execute()
    set_balance(0)

def format_rupiah(amount):
    return f"Rp {int(amount):,}".replace(",", ".")

# ====== LOAD DATA ======
balance       = get_balance()
transactions  = get_transactions()
total_income  = sum(t["jumlah"] for t in transactions if t["tipe"] == "Pemasukan")
total_expense = sum(t["jumlah"] for t in transactions if t["tipe"] == "Pengeluaran")
total_tx      = len(transactions)

# ====== HERO ======
st.markdown("""
<div class="hero-header">
    <div class="hero-title">💰 Money AI App</div>
    <div class="hero-subtitle">Kelola keuangan cerdas — analisis otomatis & saran AI real-time</div>
</div>
""", unsafe_allow_html=True)

# ====== METRIC CARDS ======
st.markdown(f"""
<div class="metric-grid">
    <div class="metric-card balance">
        <div class="metric-card-icon">🏦</div>
        <div class="metric-info">
            <div class="metric-label">Saldo</div>
            <div class="metric-value">{format_rupiah(balance)}</div>
        </div>
    </div>
    <div class="metric-card income">
        <div class="metric-card-icon">📈</div>
        <div class="metric-info">
            <div class="metric-label">Pemasukan</div>
            <div class="metric-value">{format_rupiah(total_income)}</div>
        </div>
    </div>
    <div class="metric-card expense">
        <div class="metric-card-icon">📉</div>
        <div class="metric-info">
            <div class="metric-label">Pengeluaran</div>
            <div class="metric-value">{format_rupiah(total_expense)}</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ====== TABS ======
tab1, tab2, tab3, tab4 = st.tabs(["💳 Transaksi", "📊 Analisis", "💬 AI", "⚙️ Pengaturan"])

# ======================== TAB 1 ========================
with tab1:
    st.markdown('<div class="section-title">➕ Tambah Transaksi</div>', unsafe_allow_html=True)

    tipe = st.selectbox("Tipe", ["Pemasukan", "Pengeluaran"])
    kategori_options = {
        "Pemasukan":   ["💼 Gaji", "🏪 Bisnis", "💰 Investasi", "🎁 Hadiah", "📦 Lainnya"],
        "Pengeluaran": ["🍔 Makanan", "🚗 Transportasi", "🛍️ Belanja", "💡 Tagihan",
                        "🎮 Hiburan", "🏥 Kesehatan", "📚 Pendidikan", "📦 Lainnya"]
    }
    kategori  = st.selectbox("Kategori", kategori_options[tipe])
    deskripsi = st.text_input("Deskripsi", placeholder="Contoh: Gaji Maret, Makan siang...")
    jumlah    = st.number_input("Jumlah (Rp)", min_value=0, step=1000, format="%d")

    if st.button("➕ Tambah Transaksi", use_container_width=True):
        if jumlah > 0:
            add_transaction(tipe, kategori, jumlah, deskripsi)
            st.success(f"{'✅' if tipe == 'Pemasukan' else '🔴'} {format_rupiah(jumlah)} berhasil ditambahkan!")
            st.rerun()
        else:
            st.error("⚠️ Jumlah harus lebih dari 0!")

    st.markdown(f'<div class="section-title">📋 Riwayat <span>{total_tx} transaksi</span></div>', unsafe_allow_html=True)

    if transactions:
        filter_tipe  = st.selectbox("Filter", ["Semua", "Pemasukan", "Pengeluaran"], key="ft")
        search_query = st.text_input("🔍 Cari...", placeholder="Deskripsi atau kategori")

        txs = [t for t in transactions if (filter_tipe == "Semua" or t["tipe"] == filter_tipe)]
        if search_query:
            txs = [t for t in txs if search_query.lower() in t.get("deskripsi","").lower()
                                   or search_query.lower() in t.get("kategori","").lower()]
        if txs:
            df = pd.DataFrame(txs)[["tipe","kategori","jumlah","deskripsi","tanggal"]]
            df.columns = ["Tipe","Kategori","Jumlah (Rp)","Deskripsi","Tanggal"]
            df["Jumlah (Rp)"] = df["Jumlah (Rp)"].apply(lambda x: f"{int(x):,}".replace(",","."))
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("Tidak ada transaksi yang cocok.")

        with st.expander("🗑️ Hapus Semua Data"):
            st.warning("⚠️ Tidak bisa dibatalkan!")
            if st.button("🗑️ Hapus Semua", use_container_width=True):
                delete_all_transactions()
                st.success("Data berhasil dihapus.")
                st.rerun()
    else:
        st.markdown("""
        <div style="text-align:center;padding:2rem 1rem;color:rgba(255,255,255,0.3);">
            <div style="font-size:2.5rem;margin-bottom:0.6rem;">📭</div>
            <div style="font-size:0.92rem;font-weight:500;">Belum ada transaksi</div>
            <div style="font-size:0.8rem;margin-top:0.3rem;">Tambahkan di atas!</div>
        </div>
        """, unsafe_allow_html=True)

# ======================== TAB 2 ========================
with tab2:
    st.markdown('<div class="section-title">📊 Ringkasan Keuangan</div>', unsafe_allow_html=True)

    if total_income == 0 and total_expense == 0:
        st.info("Belum ada data. Tambahkan transaksi dulu!")
    else:
        savings_rate = ((total_income - total_expense) / total_income * 100) if total_income > 0 else 0
        if savings_rate >= 30:
            hc, he, hl = "#34d399", "💚", "Sangat Sehat"
        elif savings_rate >= 10:
            hc, he, hl = "#fbbf24", "💛", "Cukup Baik"
        else:
            hc, he, hl = "#f87171", "❤️", "Perlu Perhatian"

        st.markdown(f"""
        <div class="card" style="text-align:center;padding:1.3rem;">
            <div style="font-size:1.8rem;margin-bottom:0.3rem;">{he}</div>
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.1em;color:rgba(255,255,255,0.4);margin-bottom:0.3rem;">Kondisi Keuangan</div>
            <div style="font-size:1.4rem;font-weight:800;color:{hc};">{hl}</div>
            <div style="font-size:0.82rem;color:rgba(255,255,255,0.5);margin-top:0.3rem;">Tabungan: <b style="color:{hc}">{savings_rate:.1f}%</b></div>
        </div>
        """, unsafe_allow_html=True)

        max_val = max(total_income, total_expense, 1)
        st.markdown(f"""
        <div class="card">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;color:#6ee7b7;font-weight:600;margin-bottom:0.4rem;">📈 Pemasukan</div>
            <div style="font-size:1.3rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">{format_rupiah(total_income)}</div>
            <div class="progress-track"><div class="progress-fill-green" style="width:{total_income/max_val*100}%"></div></div>
        </div>
        <div class="card">
            <div style="font-size:0.7rem;text-transform:uppercase;letter-spacing:0.07em;color:#fca5a5;font-weight:600;margin-bottom:0.4rem;">📉 Pengeluaran</div>
            <div style="font-size:1.3rem;font-weight:700;color:#fff;margin-bottom:0.5rem;">{format_rupiah(total_expense)}</div>
            <div class="progress-track"><div class="progress-fill-red" style="width:{total_expense/max_val*100}%"></div></div>
            <div style="font-size:0.76rem;color:rgba(255,255,255,0.35);margin-top:0.3rem;">Sisa: {format_rupiah(total_income-total_expense)}</div>
        </div>
        """, unsafe_allow_html=True)

        # Per kategori
        st.markdown('<div class="section-title">🗂️ Per Kategori</div>', unsafe_allow_html=True)
        exp_cat = {}
        for t in transactions:
            if t["tipe"] == "Pengeluaran":
                c = t.get("kategori","📦 Lainnya")
                exp_cat[c] = exp_cat.get(c,0) + t["jumlah"]
        if exp_cat:
            sc = sorted(exp_cat.items(), key=lambda x: x[1], reverse=True)
            tot = sum(v for _,v in sc)
            for cat, amt in sc:
                pct = (amt/tot*100) if tot>0 else 0
                st.markdown(f"""
                <div style="margin-bottom:0.8rem;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;flex-wrap:wrap;gap:3px;">
                        <span style="color:#e2e8f0;font-size:0.82rem;">{cat}</span>
                        <span style="color:#a5b4fc;font-size:0.82rem;font-weight:600;">{format_rupiah(amt)} <span style="color:rgba(255,255,255,0.3)">({pct:.0f}%)</span></span>
                    </div>
                    <div class="progress-track"><div class="progress-fill-red" style="width:{pct}%"></div></div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Belum ada pengeluaran per kategori.")

        # Tips
        st.markdown('<div class="section-title">💡 Tips</div>', unsafe_allow_html=True)
        tips = []
        if savings_rate < 20:
            tips.append(("🔴","Ikuti aturan 50/30/20","50% kebutuhan, 30% keinginan, 20% tabungan."))
        if total_expense > total_income * 0.7:
            tips.append(("🟡","Pengeluaran cukup tinggi","Kurangi 10-15% dari kategori terbesar."))
        if savings_rate >= 20:
            tips.append(("🟢","Menabung dengan baik!",f"Kamu simpan {savings_rate:.0f}%. Pertimbangkan investasi!"))
        for icon, title, desc in tips:
            st.markdown(f"""
            <div class="card" style="display:flex;gap:0.7rem;align-items:flex-start;">
                <div style="font-size:1.1rem;flex-shrink:0;margin-top:2px;">{icon}</div>
                <div>
                    <div style="font-weight:700;color:#e2e8f0;font-size:0.86rem;margin-bottom:0.2rem;">{title}</div>
                    <div style="color:rgba(255,255,255,0.5);font-size:0.8rem;line-height:1.5;">{desc}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

# ======================== TAB 3 ========================
with tab3:
    st.markdown('<div class="section-title">🤖 Tanya AI Keuangan</div>', unsafe_allow_html=True)
    st.markdown('<div class="ai-badge">🤖 AI Powered</div>', unsafe_allow_html=True)

    quick_qs = ["Kondisi keuangan saya?", "Tips hemat?", "Kapan bisa investasi?"]
    selected_quick = None
    for i, q in enumerate(quick_qs):
        if st.button(q, use_container_width=True, key=f"q{i}"):
            selected_quick = q

    pertanyaan = st.text_input("💬 Pertanyaan kamu",
                                placeholder="Contoh: Apakah pengeluaran saya terlalu besar?",
                                value=selected_quick or "")

    if st.button("🚀 Kirim", use_container_width=True):
        if pertanyaan:
            st.markdown(f'<div class="chat-bubble-user">{pertanyaan}</div>', unsafe_allow_html=True)
            p = pertanyaan.lower()
            if any(kw in p for kw in ["kondisi","bagaimana","analisis","kesehatan"]):
                if total_income == 0:
                    resp = "📊 Belum ada data. Mulai catat transaksimu!"
                elif total_expense > total_income:
                    resp = f"⚠️ Keuanganmu defisit! Pengeluaran ({format_rupiah(total_expense)}) > pemasukan ({format_rupiah(total_income)}). Kurangi pengeluaran segera."
                elif total_expense > total_income * 0.7:
                    resp = f"⚡ Keuangan cukup baik, tapi pengeluaran {(total_expense/total_income*100):.0f}% dari pemasukan. Saldo: {format_rupiah(balance)}."
                else:
                    resp = f"✅ Keuangan sehat! Kamu menyimpan {((total_income-total_expense)/total_income*100):.0f}%. Pertimbangkan investasi!"
            elif any(kw in p for kw in ["hemat","kurangi","irit","tips"]):
                resp = "💡 Tips hemat:\n1. Catat semua pengeluaran\n2. Tunggu 24 jam sebelum beli barang non-esensial\n3. Meal prep — hemat 40-60% biaya makan\n4. Batalkan langganan yang jarang dipakai\n5. Pisahkan rekening tabungan & harian"
            elif any(kw in p for kw in ["investasi","invest","saham","reksa"]):
                resp = (f"📈 Dengan saldo {format_rupiah(balance)}, kamu sudah bisa mulai! Coba Reksa Dana Pasar Uang atau ORI/SBR." 
                        if balance > 1_000_000 else "🏦 Kumpulkan dana darurat 3 bulan dulu, baru mulai investasi.")
            elif any(kw in p for kw in ["saldo","berapa","total","ringkasan"]):
                resp = f"💰 Ringkasan:\n• Saldo: {format_rupiah(balance)}\n• Pemasukan: {format_rupiah(total_income)}\n• Pengeluaran: {format_rupiah(total_expense)}\n• Transaksi: {total_tx}"
            else:
                resp = f"🤖 Saldo kamu {format_rupiah(balance)} dengan {total_tx} transaksi. Coba tanya: 'kondisi keuangan saya' atau 'tips hemat'."
            st.markdown(f'<div class="chat-bubble-ai">{resp}</div>', unsafe_allow_html=True)
        else:
            st.warning("Tulis pertanyaanmu dulu!")

# ======================== TAB 4 ========================
with tab4:
    st.markdown('<div class="section-title">⚙️ Pengaturan</div>', unsafe_allow_html=True)

    with st.expander("💳 Set / Koreksi Saldo"):
        cur = int(balance)
        saldo_baru = st.number_input("Saldo baru (Rp)", min_value=min(0,cur), step=10000, value=cur, format="%d")
        if st.button("💾 Simpan Saldo", use_container_width=True):
            set_balance(saldo_baru)
            st.success(f"✅ Saldo diperbarui ke {format_rupiah(saldo_baru)}!")
            st.rerun()

    with st.expander("📤 Export Data"):
        if transactions:
            df_exp = pd.DataFrame(transactions)[["tipe","kategori","jumlah","deskripsi","tanggal"]]
            st.download_button("⬇️ Download CSV",
                               data=df_exp.to_csv(index=False).encode("utf-8"),
                               file_name=f"money_ai_{datetime.now().strftime('%Y%m%d')}.csv",
                               mime="text/csv", use_container_width=True)
        else:
            st.info("Belum ada data untuk diexport.")

    with st.expander("ℹ️ Tentang"):
        st.markdown("""
        <div style="color:rgba(255,255,255,0.6);font-size:0.84rem;line-height:1.8;">
            <b style="color:#a5b4fc">💰 Money AI App</b> v2.2<br>
            Data tersimpan permanen di Supabase ☁️
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;padding:2rem 0 1rem;color:rgba(255,255,255,0.2);font-size:0.72rem;">
    💰 Money AI App • Powered by Supabase ☁️
</div>
""", unsafe_allow_html=True)