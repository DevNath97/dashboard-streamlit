import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

def tela_insights():

    st.title("🧠 Insights Inteligentes")

    caminho = Path(__file__).parent / "datasets" / "compras.csv"

    # -----------------------------
    # CACHE
    # -----------------------------
    @st.cache_data
    def carregar():
        df = pd.read_csv(caminho)

        if "data" in df.columns:
            df["data"] = pd.to_datetime(df["data"], errors="coerce")

        return df

    # -----------------------------
    # CARREGAR DADOS
    # -----------------------------
    if not caminho.exists():
        st.error("Arquivo de dados não encontrado.")
        return

    df = carregar()

    if df.empty:
        st.warning("Sem dados disponíveis.")
        return

    # Remover datas inválidas
    df = df.dropna(subset=["data"])

    if df.empty:
        st.warning("Sem dados válidos após tratamento.")
        return

    # -----------------------------
    # SEGURANÇA PARA GRUPOS
    # -----------------------------
    def top_valor(col, valor):
        if col in df.columns and not df[col].dropna().empty:
            return df.groupby(col)[valor].sum().idxmax()
        return "N/A"

    def top_count(col):
        if col in df.columns and not df[col].dropna().empty:
            return df[col].value_counts().idxmax()
        return "N/A"

    # -----------------------------
    # 📊 CÁLCULOS
    # -----------------------------
    produto_top = top_valor("produto", "quantidade")
    cidade_top = top_valor("cidade", "valor_total")
    pagamento_top = top_count("forma_pagamento")
    vendedor_top = top_valor("vendedor", "valor_total")

    hoje = datetime.now()

    ultimos_7 = df[df["data"] >= hoje - pd.Timedelta(days=7)]
    anterior = df[
        (df["data"] < hoje - pd.Timedelta(days=7)) &
        (df["data"] >= hoje - pd.Timedelta(days=14))
    ]

    vendas_7 = ultimos_7["valor_total"].sum() if not ultimos_7.empty else 0
    vendas_ant = anterior["valor_total"].sum() if not anterior.empty else 0

    crescimento = (
        ((vendas_7 - vendas_ant) / vendas_ant * 100)
        if vendas_ant > 0 else 0
    )

    # -----------------------------
    # 🎴 CARDS
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🏆 Produto Top", produto_top)
    col2.metric("🏙️ Cidade Destaque", cidade_top)
    col3.metric("💳 Pagamento Top", pagamento_top)
    col4.metric("🧑‍💼 Melhor Vendedor", vendedor_top)

    st.markdown("---")

    # -----------------------------
    # 📈 ALERTA
    # -----------------------------
    if crescimento > 0:
        st.success(f"📈 Crescimento de {crescimento:.1f}% na última semana")
    elif crescimento < 0:
        st.error(f"📉 Queda de {abs(crescimento):.1f}% na última semana")
    else:
        st.info("📊 Sem variação na última semana")

    # -----------------------------
    # 🤖 INSIGHT AUTOMÁTICO
    # -----------------------------
    st.markdown("---")
    st.subheader("🤖 Insight Automático")

    st.info(f"""
    📊 O produto **{produto_top}** está liderando as vendas.

    📍 A cidade com maior faturamento é **{cidade_top}**.

    💳 Clientes preferem pagar via **{pagamento_top}**.

    🧑‍💼 O vendedor destaque é **{vendedor_top}**.

    📈 O desempenho recente indica {'crescimento' if crescimento > 0 else 'queda'}.
    """)

    # -----------------------------
    # 🔥 IA SIMULADA
    # -----------------------------
    st.markdown("---")
    st.subheader("🧠 Insight com IA")

    usar_ia = st.toggle("Gerar análise avançada")

    if usar_ia:

        st.success("""
        📌 Análise Inteligente:

        O sistema identificou um padrão consistente de vendas concentrado no produto líder,
        sugerindo forte aceitação no mercado.

        A cidade destaque indica possível concentração de demanda regional.

        O método de pagamento predominante pode ser explorado em campanhas futuras.

        Recomenda-se:
        - Aumentar estoque do produto líder
        - Replicar estratégias da cidade destaque
        - Incentivar o vendedor top como benchmark
        """)