import streamlit as st

# -----------------------------
# IMPORTAR TELAS
# -----------------------------
from dashboard import tela_dashboard
from visualizar import tela_visualizar
from adicionar_linhas import tela_adicionar_venda as tela_adicionar
from insights import tela_insights

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(
    page_title="Sistema de Vendas",
    layout="wide"
)

# -----------------------------
# ESTADOS
# -----------------------------
if "pagina" not in st.session_state:
    st.session_state.pagina = "home"

if "tema" not in st.session_state:
    st.session_state.tema = "light"

# -----------------------------
# NAVEGAÇÃO
# -----------------------------
def navegar(pagina):
    st.session_state.pagina = pagina
    st.rerun()

# -----------------------------
# TEMA DARK
# -----------------------------
if st.session_state.tema == "dark":
    st.markdown("""
        <style>
        .stApp {
            background-color: #0E1117;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# ESCONDER SIDEBAR NA HOME
# -----------------------------
if st.session_state.pagina == "home":
    st.markdown("""
        <style>
        [data-testid="stSidebar"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
if st.session_state.pagina != "home":

    st.sidebar.markdown("## 📊 Sistema de Vendas")

    menu = {
        "🏠 Home": "home",
        "📊 Dashboard": "dashboard",
        "📋 Dados": "visualizar",
        "➕ Nova Venda": "nova_venda",
        "🧠 Insights": "insights",
    }

    for nome, pagina in menu.items():
        if st.session_state.pagina == pagina:
            st.sidebar.markdown(f"▶ **{nome}**")
        else:
            if st.sidebar.button(nome, use_container_width=True, key=f"menu_{pagina}"):
                navegar(pagina)

    # -----------------------------
    # TEMA
    # -----------------------------
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🎨 Tema")

    col1, col2 = st.sidebar.columns(2)

    if col1.button("☀️", use_container_width=True, key="tema_light"):
        st.session_state.tema = "light"
        st.rerun()

    if col2.button("🌙", use_container_width=True, key="tema_dark"):
        st.session_state.tema = "dark"
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("👤 Admin")

# -----------------------------
# HOME
# -----------------------------
if st.session_state.pagina == "home":

    st.markdown("<h1 style='text-align:center;'>📊 Sistema de Vendas</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        if st.button("📊\n\nDashboard", use_container_width=True, key="home_dashboard"):
            navegar("dashboard")

    with col2:
        if st.button("📋\n\nDados", use_container_width=True, key="home_dados"):
            navegar("visualizar")

    with col3:
        if st.button("➕\n\nNova Venda", use_container_width=True, key="home_nova"):
            navegar("nova_venda")

    with col4:
        if st.button("🧠\n\nInsights", use_container_width=True, key="home_insights"):
            navegar("insights")

    # -----------------------------
    # ESTILO DOS CARDS
    # -----------------------------
    st.markdown("""
        <style>

        div.stButton > button {
            height: 180px;
            font-size: 24px;
            border-radius: 20px;
            border: none;
            font-weight: 600;
            color: white;

            background: linear-gradient(135deg, #1f2937, #111827);
            box-shadow: 0px 8px 20px rgba(0,0,0,0.25);

            transition: all 0.25s ease;
        }

        div.stButton > button:hover {
            transform: translateY(-6px) scale(1.02);
            box-shadow: 0px 12px 30px rgba(0,0,0,0.35);
        }

        </style>
    """, unsafe_allow_html=True)

# -----------------------------
# PÁGINAS
# -----------------------------
elif st.session_state.pagina == "dashboard":
    tela_dashboard()

elif st.session_state.pagina == "visualizar":
    tela_visualizar()

elif st.session_state.pagina == "nova_venda":
    tela_adicionar()

elif st.session_state.pagina == "insights":
    tela_insights()