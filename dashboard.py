import streamlit as st
import pandas as pd
from pathlib import Path

def tela_dashboard():

    st.title("📊 Dashboard de Vendas")

    # -----------------------------
    # CAMINHOS
    # -----------------------------
    base_path = Path(__file__).parent / "datasets"
    caminho_compras = base_path / "compras.csv"

    # -----------------------------
    # CARREGAR DADOS
    # -----------------------------
    if not caminho_compras.exists():
        st.error("Arquivo de vendas não encontrado.")
        return

    df = pd.read_csv(caminho_compras)

    if df.empty:
        st.warning("Nenhuma venda registrada.")
        return

    # Converter data com segurança
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Remover linhas inválidas de data
    df = df.dropna(subset=["data"])

    if df.empty:
        st.warning("Não há dados válidos após tratamento.")
        return

    # -----------------------------
    # FILTROS
    # -----------------------------
    st.sidebar.subheader("🔎 Filtros")

    data_min = df["data"].min().date()
    data_max = df["data"].max().date()

    data_inicio, data_fim = st.sidebar.date_input(
        "Período",
        [data_min, data_max]
    )

    # Garantir formato datetime
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)

    estados = st.sidebar.multiselect(
        "Estado",
        options=df["estado"].dropna().unique(),
        default=df["estado"].dropna().unique()
    )

    vendedores = st.sidebar.multiselect(
        "Vendedor",
        options=df["vendedor"].dropna().unique(),
        default=df["vendedor"].dropna().unique()
    )

    # -----------------------------
    # APLICAR FILTROS
    # -----------------------------
    df_filtrado = df[
        (df["data"] >= data_inicio) &
        (df["data"] <= data_fim) &
        (df["estado"].isin(estados)) &
        (df["vendedor"].isin(vendedores))
    ]

    if df_filtrado.empty:
        st.warning("Nenhum dado encontrado com os filtros selecionados.")
        return

    # -----------------------------
    # KPIs
    # -----------------------------
    faturamento = df_filtrado["valor_total"].sum()
    lucro = df_filtrado["lucro_total"].sum()
    vendas = len(df_filtrado)
    ticket_medio = faturamento / vendas if vendas > 0 else 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Faturamento", f"R$ {faturamento:,.2f}")
    col2.metric("📈 Lucro", f"R$ {lucro:,.2f}")
    col3.metric("🛒 Vendas", vendas)
    col4.metric("🎯 Ticket Médio", f"R$ {ticket_medio:,.2f}")

    st.markdown("---")

    # -----------------------------
    # GRÁFICOS
    # -----------------------------

    # 📍 Vendas por estado
    st.subheader("📍 Vendas por Estado")
    vendas_estado = df_filtrado.groupby("estado")["valor_total"].sum().sort_values()
    st.bar_chart(vendas_estado)

    st.markdown("---")

    # 🏆 Produtos mais vendidos
    st.subheader("🏆 Produtos mais vendidos")
    produtos = df_filtrado.groupby("produto")["quantidade"].sum().sort_values()
    st.bar_chart(produtos)

    st.markdown("---")

    # 📅 Vendas por dia
    st.subheader("📅 Vendas por dia")

    vendas_dia = df_filtrado.groupby(df_filtrado["data"].dt.date)["valor_total"].sum()
    st.line_chart(vendas_dia)

    st.markdown("---")

    # 💳 Forma de pagamento
    st.subheader("💳 Forma de pagamento")

    pagamento = df_filtrado["forma_pagamento"].value_counts()
    st.bar_chart(pagamento)

    st.markdown("---")

    # 🧾 Tabela detalhada
    st.subheader("🧾 Dados detalhados")

    st.dataframe(df_filtrado, use_container_width=True)