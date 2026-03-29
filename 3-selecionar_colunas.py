import streamlit as st
import pandas as pd
from pathlib import Path

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Dashboard", layout="wide")
st.title("📊 Dashboard de Vendas")

# -----------------------------
# DADOS
# -----------------------------
caminho = Path(__file__).parent / "datasets" / "compras.csv"

@st.cache_data
def carregar():
    df = pd.read_csv(caminho)
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df

df = carregar()

if df.empty:
    st.stop()

# -----------------------------
# FILTRO SIMPLES (ESSENCIAL)
# -----------------------------
st.sidebar.header("Filtros")

# Filtro de período (único filtro global)
if "data" in df.columns:
    intervalo = st.sidebar.date_input(
        "Período",
        [df["data"].min(), df["data"].max()]
    )

    if len(intervalo) == 2:
        df = df[
            (df["data"] >= pd.to_datetime(intervalo[0])) &
            (df["data"] <= pd.to_datetime(intervalo[1]))
        ]

# -----------------------------
# KPIs PRINCIPAIS
# -----------------------------
st.subheader("📈 Visão Geral")

col1, col2, col3 = st.columns(3)

col1.metric("Vendas", len(df))
col2.metric("Faturamento", f"R$ {df['valor_total'].sum():,.0f}")
col3.metric("Lucro", f"R$ {df['lucro_total'].sum():,.0f}")

# -----------------------------
# INSIGHTS PRINCIPAIS
# -----------------------------
st.subheader("🏆 Destaques")

col1, col2, col3 = st.columns(3)

# Quem vende mais
top_vendedor = (
    df.groupby("vendedor")["valor_total"]
    .sum()
    .idxmax()
)

col1.write("👤 Vendedor destaque")
col1.success(top_vendedor)

# Produto campeão
top_produto = (
    df.groupby("produto")["quantidade"]
    .sum()
    .idxmax()
)

col2.write("👟 Produto mais vendido")
col2.success(top_produto)

# Maior lucro
top_lucro = (
    df.groupby("produto")["lucro_total"]
    .sum()
    .idxmax()
)

col3.write("💰 Produto mais lucrativo")
col3.success(top_lucro)

# -----------------------------
# COMPORTAMENTO
# -----------------------------
st.subheader("🧠 Comportamento de Compra")

comportamento = (
    df.groupby("comportamento")["valor_total"]
    .mean()
    .sort_values(ascending=False)
)

st.dataframe(comportamento.rename("ticket_medio"))

# -----------------------------
# TABELA FINAL
# -----------------------------
with st.expander("📋 Ver dados detalhados"):
    st.dataframe(df, use_container_width=True)