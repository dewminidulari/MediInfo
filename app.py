import streamlit as st
from drug_lookup import get_drug_info
from explain import explain

st.set_page_config(page_title="MediInfo", page_icon=":material/medication:", layout="centered")

# ---------- Icons (inline SVG, no downloads needed) ----------
ICONS = {
    "pill": '<path d="m10.5 20.5 10-10a4.95 4.95 0 1 0-7-7l-10 10a4.95 4.95 0 1 0 7 7Z"/><path d="m8.5 8.5 7 7"/>',
    "landmark": '<line x1="3" x2="21" y1="22" y2="22"/><line x1="6" x2="6" y1="18" y2="11"/><line x1="10" x2="10" y1="18" y2="11"/><line x1="14" x2="14" y1="18" y2="11"/><line x1="18" x2="18" y1="18" y2="11"/><polygon points="12 2 20 7 4 7"/>',
    "message": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "shield": '<path d="M20 13c0 5-3.5 7.5-7.66 8.95a1 1 0 0 1-.67-.01C7.5 20.5 4 18 4 13V6a1 1 0 0 1 1-1c2 0 4.5-1.2 6.24-2.72a1.17 1.17 0 0 1 1.52 0C14.51 3.81 17 5 19 5a1 1 0 0 1 1 1z"/><path d="m9 12 2 2 4-4"/>',
    "sparkles": '<path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z"/>',
    "alert": '<path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
}

def icon(name, size=20):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="vertical-align:-3px;flex-shrink:0">{ICONS[name]}</svg>'
    )

# ---------- Styling (dark mode) ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }

.stApp {
    background:
        radial-gradient(circle at 8% 0%, rgba(37, 99, 235, 0.16) 0%, transparent 40%),
        radial-gradient(circle at 92% 8%, rgba(20, 184, 166, 0.12) 0%, transparent 38%),
        radial-gradient(circle at 50% 100%, rgba(109, 40, 217, 0.14) 0%, transparent 42%),
        #0b1220;
}
[data-testid="stHeader"] { background: transparent; }
#MainMenu, footer { visibility: hidden; }
.block-container { max-width: 760px; padding-top: 2rem; }

.hero {
    background: linear-gradient(135deg, #115e59 0%, #1e40af 55%, #5b21b6 100%);
    padding: 2.6rem 1.5rem;
    border-radius: 24px;
    text-align: center;
    margin-bottom: 1.2rem;
    border: 1px solid rgba(148, 163, 184, 0.18);
    box-shadow: 0 14px 34px rgba(0, 0, 0, 0.45);
}
.hero-logo {
    width: 64px; height: 64px;
    margin: 0 auto 0.8rem auto;
    border-radius: 18px;
    background: rgba(255, 255, 255, 0.12);
    border: 1px solid rgba(255, 255, 255, 0.2);
    display: flex; align-items: center; justify-content: center;
    color: #f1f5f9;
}
.hero h1 { color: #f1f5f9; margin: 0; font-size: 2.6rem; font-weight: 700; letter-spacing: -0.5px; }
.hero p  { color: #cbd5e1; margin: 0.5rem 0 0 0; font-size: 1.05rem; }

.features { display: flex; gap: 0.8rem; margin-bottom: 1.4rem; flex-wrap: wrap; }
.feature {
    flex: 1 1 150px;
    background: #111a2e;
    border: 1px solid #1f2a44;
    border-radius: 16px;
    padding: 0.9rem 1rem;
    text-align: center;
    font-size: 0.9rem;
    font-weight: 500;
    color: #cbd5e1;
}
.feature .ficon {
    width: 40px; height: 40px;
    margin: 0 auto 0.5rem auto;
    border-radius: 12px;
    background: rgba(59, 130, 246, 0.14);
    color: #60a5fa;
    display: flex; align-items: center; justify-content: center;
}

.stTextInput input {
    border-radius: 14px;
    padding: 0.75rem 1rem;
    border: 1.5px solid #334155;
    background: #0f172a;
    color: #e2e8f0;
}
.stTextInput input::placeholder { color: #64748b; }
.stTextInput input:focus { border-color: #3b82f6; box-shadow: 0 0 0 3px rgba(59,130,246,0.25); }

div.stButton > button {
    border-radius: 14px;
    font-weight: 600;
    padding: 0.6rem 1rem;
    background: #111a2e;
    color: #cbd5e1;
    border: 1.5px solid #334155;
    transition: all 0.15s ease;
}
div.stButton > button:hover { border-color: #60a5fa; color: #93c5fd; transform: translateY(-1px); }
div.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #2563eb, #5b21b6);
    color: #f8fafc;
    border: none;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.25);
}
div.stButton > button[kind="primary"]:hover { color: #ffffff; transform: translateY(-1px); }

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #111a2e;
    border: 1px solid #1f2a44;
    border-radius: 18px;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35);
}

.badge {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(45, 212, 191, 0.14);
    color: #5eead4;
    padding: 0.28rem 0.85rem;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    margin: 0.2rem 0.4rem 0.8rem 0;
}
.badge.purple { background: rgba(167, 139, 250, 0.16); color: #c4b5fd; }

.notice {
    display: flex; gap: 0.7rem; align-items: flex-start;
    background: rgba(245, 158, 11, 0.09);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-left: 5px solid #f59e0b;
    padding: 0.9rem 1.1rem;
    border-radius: 12px;
    margin-top: 1.5rem;
    font-size: 0.9rem;
    color: #fcd34d;
}
.notice svg { margin-top: 2px; }
.footer { text-align: center; color: #64748b; font-size: 0.82rem; margin: 1.8rem 0 0.5rem 0; }
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown(f"""
<div class="hero">
<div class="hero-logo">{icon("pill", 32)}</div>
<h1>MediInfo</h1>
<p>Understand your medicine in simple words, with facts from official sources</p>
</div>
<div class="features">
<div class="feature"><div class="ficon">{icon("landmark", 22)}</div>Official FDA data</div>
<div class="feature"><div class="ficon">{icon("message", 22)}</div>Simple language</div>
<div class="feature"><div class="ficon">{icon("link", 22)}</div>Source shown</div>
</div>
""", unsafe_allow_html=True)

# ---------- Input ----------
def use_example(name):
    st.session_state.query = name
    st.session_state.go = True

st.text_input(":material/search: Medicine name", key="query",
              placeholder="Type a medicine name, e.g. ibuprofen")

st.caption("Try an example:")
examples = ["acetaminophen", "cetirizine", "metformin", "albuterol"]
cols = st.columns(len(examples))
for col, ex in zip(cols, examples):
    col.button(ex.title(), key="ex_" + ex, on_click=use_example, args=(ex,),
               use_container_width=True)

search = st.button("Search", type="primary", icon=":material/search:", use_container_width=True)
run = search or st.session_state.pop("go", False)

# ---------- Result ----------
name = st.session_state.get("query", "").strip()

if run and name:
    try:
        with st.spinner("Looking up official FDA data..."):
            info = get_drug_info(name)
        if info is None:
            st.error("Medicine not found. Try the generic name (for example, acetaminophen instead of paracetamol).")
        else:
            st.success("Found: " + info["generic_name"].title(), icon=":material/check_circle:")
            st.markdown(
                f'<span class="badge">{icon("shield", 15)} Official FDA data</span>'
                f'<span class="badge purple">{icon("sparkles", 15)} AI-simplified</span>',
                unsafe_allow_html=True,
            )
            with st.spinner("Writing a simple explanation..."):
                text = explain(info)
            with st.container(border=True):
                st.markdown(text)
            st.caption("Source: " + info["source"])
    except Exception as e:
        st.error("Something went wrong. Please try again in a minute.")
        st.caption(str(e))
elif run:
    st.warning("Please type a medicine name first.")

# ---------- Safety notice and footer ----------
st.markdown(f"""
<div class="notice">
{icon("alert", 20)}
<div><b>Information only.</b> This tool does not give medical advice or doses.
Always ask a doctor or pharmacist before using any medicine.</div>
</div>
<div class="footer">
<div style="display:inline-flex;align-items:center;gap:0.4rem;color:#94a3b8;font-weight:500;">
Developed
<svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" viewBox="0 0 24 24" fill="#f472b6" stroke="#f472b6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/></svg>
by Devmini Dulari
</div>
<div style="margin-top:0.4rem;">© 2026 MediInfo. Designed and developed by Devmini Dulari. All rights reserved.</div>
<div style="margin-top:0.3rem;opacity:0.8;">Built with Python, openFDA and Gemini</div>
</div>
""", unsafe_allow_html=True)