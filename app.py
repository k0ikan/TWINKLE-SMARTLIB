import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random
import hashlib
import re

# ========================================================
# 1. KONFIGURASI
# ========================================================
st.set_page_config(
    page_title="Archivo Smart Library",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========================================================
# 2. CSS - DARK THEME
# ========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* Base */
* {font-family: 'Poppins', sans-serif;}

/* Main Background - Dark */
.stApp {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 50%, #0d1117 100%) !important;
    background-attachment: fixed;
}

/* Text Colors - Readable on Dark */
h1, h2, h3, h4, h5, h6 {color: #f0f6fc !important; font-weight: 700;}
p, div, span, label {color: #c9d1d9 !important;}
[data-testid="stMarkdown"] p {color: #c9d1d9 !important;}

/* Input Fields - Dark Style */
.stTextInput>div>div>input {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    color: #f0f6fc !important;
}
.stTextInput>div>div>input::placeholder {color: #6e7681 !important;}
.stTextInput>div>div>input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2) !important;
}
.stTextInput>div>label {color: #f0f6fc !important;}

/* Password Input */
.stPassword>div>div>input {
    background: #21262d !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    color: #f0f6fc !important;
}
.stPassword>div>label {color: #f0f6fc !important;}

/* Buttons - Gradient Blue */
.stButton>button {
    background: linear-gradient(135deg, #1f6feb 0%, #388bfd 100%) !important;
    color: white !important;
    border-radius: 8px !important;
    border: none !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
}
.stButton>button:hover {
    background: linear-gradient(135deg, #388bfd 0%, #1f6feb 100%) !important;
    transform: translateY(-1px);
}

/* Google Button */
.google-btn {
    background: white !important;
    color: #333 !important;
    border-radius: 8px !important;
    border: 1px solid #e0e0e0 !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
}
.google-btn:hover {background: #f5f5f5 !important;}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {gap: 8px;}
.stTabs [data-baseweb="tab"] {
    background: #21262d !important;
    border-radius: 8px 8px 0 0 !important;
    color: #c9d1d9 !important;
    padding: 12px 20px !important;
}
.stTabs [aria-selected="true"] {
    background: #1f6feb !important;
    color: white !important;
}

/* Cards */
.auth-card {
    background: #161b22 !important;
    border-radius: 16px !important;
    padding: 40px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4) !important;
    border: 1px solid #30363d !important;
}

/* Logo/Title */
.logo-text {
    text-align: center;
    margin-bottom: 30px;
}
.logo-text h1 {
    font-size: 48px !important;
    margin-bottom: 10px !important;
}
.logo-text p {
    color: #8b949e !important;
    font-size: 18px !important;
}

/* Divider */
.divider {
    text-align: center;
    margin: 20px 0;
    color: #6e7681 !important;
}

/* Error/Success Messages */
.stError {background: #21262d !important; color: #f85149 !important;}
.stSuccess {background: #21262d !important; color: #3fb950 !important;}

/* Info Box */
[data-testid="stErrorMessage"] {
    background: #21262d !important;
    border-left: 4px solid #f85149 !important;
    color: #f85149 !important;
    padding: 12px 16px !important;
    border-radius: 8px !important;
}

/* Metrics */
[data-testid="stMetricValue"] {color: #f0f6fc !important;}
[data-testid="stMetricLabel"] {color: #8b949e !important;}
</style>
""", unsafe_allow_html=True)

# ========================================================
# 3. DATABASE
# ========================================================
BUKU_DATABASE = [
    {"id":1,"judul":"Atomic Habits","penulis":"James Clear","kategori":"Self-Development","rating":4.8,"cover":"📘"},
    {"id":2,"judul":"Dompet Ayah","penulis":"J.S Khairen","kategori":"Fiksi","rating":4.5,"cover":"👨‍👦"},
    {"id":3,"judul":"Sepatu Ibu","penulis":"J.S Khairen","kategori":"Fiksi","rating":4.6,"cover":"👟"},
    {"id":4,"judul":"Laut Bercerita","penulis":"Leila S. Chudori","kategori":"Fiksi","rating":4.7,"cover":"🌊"},
    {"id":5,"judul":"Kita Pergi Hari Ini","penulis":"Ziggy","kategori":"Fiksi","rating":4.4,"cover":"🚗"},
    {"id":6,"judul":"Cantik Itu Luka","penulis":"Eka Kurniawan","kategori":"Fiksi","rating":4.9,"cover":"💄"},
    {"id":7,"judul":"Manajemen Data","penulis":"Tech Author","kategori":"Teknologi","rating":4.3,"cover":"📊"},
    {"id":8,"judul":"Python Dasar","penulis":"Coder ID","kategori":"Teknologi","rating":4.5,"cover":"🐍"},
    {"id":9,"judul":"Psychology of Money","penulis":"Morgan Housel","kategori":"Keuangan","rating":4.8,"cover":"💰"},
    {"id":10,"judul":"Deep Work","penulis":"Cal Newport","kategori":"Produktivitas","rating":4.7,"cover":"🎯"},
    {"id":11,"judul":"The 5 AM Club","penulis":"Robin Sharma","kategori":"Self-Development","rating":4.6,"cover":"🌅"},
    {"id":12,"judul":"Sapiens","penulis":"Yuval Noah Harari","kategori":"Sejarah","rating":4.9,"cover":"🌍"},
]

# ========================================================
# 4. SESSION STATE
# ========================================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'user_data' not in st.session_state:
    st.session_state['user_data'] = {'nama': '', 'email': '', 'member_id': '940184', 'points': 150, 'login_method': ''}
if 'keranjang' not in st.session_state:
    st.session_state['keranjang'] = []
if 'history' not in st.session_state:
    st.session_state['history'] = []

# ========================================================
# 5. FUNGSI
# ========================================================
def cek_kuota():
    return len(st.session_state['keranjang']) >= 3

def proses_pencarian(katakunci):
    katakunci = katakunci.lower().strip()
    for buku in BUKU_DATABASE:
        if katakunci in buku['judul'].lower() or katakunci in buku['penulis'].lower():
            return buku
    return None

def pinjam_buku(buku):
    if cek_kuota():
        return False, "Limit tercapai!"
    tgl = datetime.now()
    bp = {'id': buku['id'], 'judul': buku['judul'], 'penulis': buku['penulis'], 'tgl_pinjam': tgl.strftime("%d %b %Y"), 'tgl_jatuh': (tgl + timedelta(days=7)).strftime("%d %b %Y")}
    st.session_state['keranjang'].append(bp)
    st.session_state['history'].append(bp.copy())
    return True, f"Berhasil pinjam {buku['judul']}!"

def get_rekomendasi():
    return random.sample(BUKU_DATABASE, 3)

def hash_text(text):
    return hashlib.sha256(text.encode()).hexdigest()

# ========================================================
# 6. UI - LOGIN
# ========================================================
import re

if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {}

def is_valid_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email.strip()) is not None
def render_login():
    st.write("")
    st.write("")
    
    col1, col2, col3 = st.columns([1, 1.2, 1])

    with col2:
        with st.container():
            st.markdown("""
            <div class="auth-card">
                <div class="logo-text">
                    <h1>📚</h1>
                    <h2>Archivo</h2>
                    <p>Smart Digital Library</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            tab_login, tab_daftar = st.tabs(["🔑 Login", "📝 Daftar"])
            
            # ==================== LOGIN TAB ====================
            with tab_login:
                st.markdown("### Masuk ke Archivo")
                
                # Google Login - disabled until real OAuth is configured
                if st.button("🔗 Masuk dengan Google", use_container_width=True, key="google_login_btn"):
                    st.warning("Google Login belum dikonfigurasi. Silakan gunakan email dan password.")
                
                st.markdown(
                    "<p style='text-align:center; color:#8b949e;'>atau</p>",
                    unsafe_allow_html=True
                )
                
                login_email = st.text_input(
                    "Email",
                    placeholder="email@anda.com",
                    key="login_email"
                )

                login_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="login_password"
                )
                
                col_btn, col_lupas = st.columns([1, 1])

                with col_btn:
                    if st.button("MASUK", use_container_width=True, key="login_button"):
                        email_clean = login_email.strip().lower()

                        if not email_clean or not login_password:
                            st.error("Mohon isi email dan password.")

                        elif not is_valid_email(email_clean):
                            st.error("Email tidak valid. Contoh email yang benar: nama@email.com")

                        elif email_clean not in st.session_state["registered_users"]:
                            st.error("Akun belum terdaftar. Silakan daftar terlebih dahulu.")

                        elif st.session_state["registered_users"][email_clean]["password"] != login_password:
                            st.error("Password salah.")

                        else:
                            user = st.session_state["registered_users"][email_clean]
                            st.session_state["logged_in"] = True
                           
                            st.session_state["user_data"]["nama"] = user["nama"]
                            st.session_state["user_data"]["email"] = email_clean
                            st.session_state["user_data"]["login_method"] = "email"

                            st.rerun()

                with col_lupas:
                    st.caption("Lupa do tpassword?")
                
                st.markdown("---")
                st.caption("Belum punya akun? Daftar di tab Daftar ↑")
            
            # ==================== DAFTAR TAB ====================
            with tab_daftar:
                st.markdown("### Buat Akun Baru")
                
                if st.button("🔗 Daftar dengan Google", use_container_width=True, key="google_signup_btn"):
    st.warning("Google Sign Up belum dikonfigurasi. Silakan daftar dengan email dan password.")
                
                st.markdown(
                    "<p style='text-align:center; color:#8b949e;'>atau</p>",
                    unsafe_allow_html=True
                )
                
                signup_name = st.text_input(
                    "Nama Lengkap",
                    placeholder="Nama Anda",
                    key="signup_name"
                )

                signup_email = st.text_input(
                    "Email",
                    placeholder="email@anda.com",
                    key="signup_email"
                )

                signup_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="••••••••",
                    key="signup_password"
                )

                signup_confirm_password = st.text_input(
                    "Konfirmasi Password",
                    type="password",
                    placeholder="••••••••",
                    key="signup_confirm_password"
                )
                
                signup_terms = st.checkbox(
                    "Saya setuju dengan Syarat & Ketentuan",
                    key="signup_terms"
                )
                
                if st.button("DAFTAR SEKARANG", use_container_width=True, key="signup_button"):
                    email_clean = signup_email.strip().lower()

                    if not signup_name or not email_clean or not signup_password or not signup_confirm_password:
                        st.error("Mohon isi semua kolom.")

                    elif not is_valid_email(email_clean):
                        st.error("Email tidak valid. Contoh email yang benar: nama@email.com")

                    elif signup_password != signup_confirm_password:
                        st.error("Password tidak cocok.")

                    elif not signup_terms:
                        st.error("Setujui Syarat & Ketentuan terlebih dahulu.")

                    elif email_clean in st.session_state["registered_users"]:
                        st.error("Email ini sudah terdaftar. Silakan login.")

                    else:
                        st.session_state["registered_users"][email_clean] = {
                            "nama": signup_name.strip(),
                            "email": email_clean,
                            "password": signup_password,
                            "login_method": "email"
                        }

                        st.success("Pendaftaran berhasil. Silakan login dengan akun yang baru dibuat.")
                        
# ========================================================
# 7. UI - SIDEBAR
# ========================================================
def render_sidebar():
    with st.sidebar:
        st.markdown("---")
        st.markdown("## 📚 **Archivo**")
        st.markdown("### Smart Library")
        st.markdown("---")
        
        # User Info
        st.markdown(f"""
        <div style="background: #21262d; padding: 20px; border-radius: 12px; text-align: center;">
            <div style="font-size: 40px;">👤</div>
            <p style="color: white; font-size: 18px; font-weight: 600;">{st.session_state['user_data']['nama']}</p>
            <p style="color: #6e7681; font-size: 14px;">ID: {st.session_state['user_data']['member_id']}</p>
            <p style="color: #fbbf24; font-size: 16px; font-weight: 600;">⭐ {st.session_state['user_data']['points']} Points</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Keranjang
        st.markdown("### 🛒 Keranjang")
        jml = len(st.session_state['keranjang'])
        st.progress(jml/3)
        st.markdown(f"**{jml}/3** buku", unsafe_allow_html=True)
        
        if jml >= 3:
            st.warning("Limit tercapai!")
        
        if st.session_state['keranjang']:
            st.markdown("---")
            for b in st.session_state['keranjang']:
                st.markdown(f"📚 {b['judul']}", unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Menu
        menu = st.radio("Menu", ["Beranda", "Koleksi", "Riwayat"])
        
        if st.button("🚪 Keluar", use_container_width=True):
            st.session_state['logged_in'] = False
            st.session_state['keranjang'] = []
            st.rerun()
        
        return menu

        # ========================================================
# 8. UI - BERANDA (LENGKAP)
# ========================================================
def render_beranda():
    # Stats Dashboard
    st.markdown("## 📊 Dashboard")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("📚 Koleksi", "12")
    c2.metric("⭐ Points", "150")
    c3.metric("📖 Dipinjam", len(st.session_state['keranjang']))
    c4.metric("✅ Kuota", "3")
    st.markdown("---")
    
    # Pencarian
    st.markdown("## 🔍 Cari Buku")
    q = st.text_input("Ketik judul atau penulis...", placeholder="Contoh: Atomic Habits")
    
    if q:
        if cek_kuota():
            st.error("❌ Kuota penuh!")
        else:
            hasil = proses_pencarian(q)
            if hasil:
                st.success(f"✅ Ditemukan: {hasil['judul']}")
                st.markdown(f"""
                <div style="background: #161b22; padding: 20px; border-radius: 12px; border: 1px solid #30363d;">
                    <span style="font-size: 50px;">{hasil['cover']}</span>
                    <h3 style="color: #f0f6fc;">{hasil['judul']}</h3>
                    <p style="color: #c9d1d9;"><b>Penulis:</b> {hasil['penulis']}</p>
                    <p style="color: #c9d1d9;"><b>Kategori:</b> {hasil['kategori']}</p>
                    <p style="color: #c9d1d9;"><b>Rating:</b> {hasil['rating']} ⭐</p>
                </div>
                """, unsafe_allow_html=True)
                # WRONG - missing colon
            if st.button(f"📚 Pinjam {hasil['judul']}", key=f"pinjam_{hasil['id']}"):
                    s, m = pinjam_buku(hasil)
                    if s: st.success(m); st.rerun()
            else:
                st.error(f"❌ Buku '{q}' tidak ditemukan")
    
    st.markdown("---")
    
    # Rekomendasi
    st.markdown("## ✨ Rekomendasi Untukmu")
    cols = st.columns(3)
    for i, b in enumerate(get_rekomendasi()):
        with cols[i]:
            st.info(f"**{b['cover']}**\n\n**{b['judul']}**\n{b['penulis']}\n⭐ {b['rating']}")
    
    st.markdown("---")
    
    # Semua Koleksi
    st.markdown("## 📚 Semua Koleksi")
    cols = st.columns(3)
    for i, b in enumerate(BUKU_DATABASE):
        with cols[i % 3]:
            st.info(f"**{b['cover']}**\n**{b['judul']}**\n{b['penulis']}")

# ========================================================
# 9. UI - KOLEKSI
# ========================================================
def render_koleksi():
    st.markdown("## 📖 Koleksi Saya")
    if not st.session_state['keranjang']:
        st.info("Keranjang kosong!")
    else:
        df = pd.DataFrame(st.session_state['keranjang'])
        st.dataframe(df[['judul', 'penulis', 'tgl_pinjam', 'tgl_jatuh']], use_container_width=True)

# ========================================================
# 10. UI - RIWAYAT
# ========================================================
def render_riwayat():
    st.markdown("## 📜 Riwayat Peminjaman")
    if not st.session_state['history']:
        st.info("Belum ada histori!")
    else:
        df = pd.DataFrame(st.session_state['history'])
        st.dataframe(df, use_container_width=True)

# ========================================================
# 11. MAIN APP
# ========================================================
def main():
    if not st.session_state['logged_in']:
        render_login()
    else:
        menu = render_sidebar()
        st.write("")
        if menu == "Beranda":
            render_beranda()
        elif menu == "Koleksi":
            render_koleksi()
        elif menu == "Riwayat":
            render_riwayat()

if __name__ == "__main__":
    main()