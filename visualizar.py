import streamlit as st
import pandas as pd
from pathlib import Path
from io import BytesIO

def tela_visualizar():

    st.title("📋 Exploração de Dados")

    # -----------------------------
    # CAMINHO
    # -----------------------------
    caminho = Path(__file__).parent / "datasets" / "compras.csv"

    # -----------------------------
    # CARREGAR DADOS
    # -----------------------------
    if not caminho.exists():
        st.error("Arquivo de vendas não encontrado.")
        return

    df = pd.read_csv(caminho)

    if df.empty:
        st.warning("Nenhum dado disponível.")
        return

    # -----------------------------
    # TRATAMENTO DE DATA
    # -----------------------------
    if "data" in df.columns:
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data"])

    if df.empty:
        st.warning("Sem dados válidos após tratamento.")
        return

    df_filtrado = df.copy()

    # -----------------------------
    # FILTROS
    # -----------------------------
    st.subheader("🎯 Filtros")

    col1, col2, col3 = st.columns(3)

    # 📅 PERÍODO
    if "data" in df.columns:
        data_min = df["data"].min().date()
        data_max = df["data"].max().date()

        intervalo = col1.date_input(
            "Período",
            [data_min, data_max]
        )

        if len(intervalo) == 2:
            inicio = pd.to_datetime(intervalo[0])
            fim = pd.to_datetime(intervalo[1])

            df_filtrado = df_filtrado[
                (df_filtrado["data"] >= inicio) &
                (df_filtrado["data"] <= fim)
            ]

    # 📍 ESTADO
    if "estado" in df.columns:
        estados = df["estado"].dropna().unique()

        estados_sel = col2.multiselect(
            "Estado",
            options=estados,
            default=estados
        )

        df_filtrado = df_filtrado[df_filtrado["estado"].isin(estados_sel)]

    # 👤 VENDEDOR
    if "vendedor" in df.columns:
        vendedores = df["vendedor"].dropna().unique()

        vendedores_sel = col3.multiselect(
            "Vendedor",
            options=vendedores,
            default=vendedores
        )

        df_filtrado = df_filtrado[df_filtrado["vendedor"].isin(vendedores_sel)]

    # -----------------------------
    # FILTROS ADICIONAIS
    # -----------------------------
    col4, col5 = st.columns(2)

    # 📦 PRODUTO
    if "produto" in df.columns:
        produtos = df["produto"].dropna().unique()

        produtos_sel = col4.multiselect(
            "Produto",
            options=produtos,
            default=produtos
        )

        df_filtrado = df_filtrado[df_filtrado["produto"].isin(produtos_sel)]

    # 💳 PAGAMENTO
    if "forma_pagamento" in df.columns:
        pagamentos = df["forma_pagamento"].dropna().unique()

        pagamentos_sel = col5.multiselect(
            "Forma de pagamento",
            options=pagamentos,
            default=pagamentos
        )

        df_filtrado = df_filtrado[df_filtrado["forma_pagamento"].isin(pagamentos_sel)]

    # -----------------------------
    # RESUMO
    # -----------------------------
    st.markdown("---")
    st.subheader("📈 Resumo")

    col1, col2, col3 = st.columns(3)

    col1.metric("📊 Registros", len(df_filtrado))
    col2.metric("📂 Colunas", df_filtrado.shape[1])

    if "valor_total" in df_filtrado.columns:
        total = df_filtrado["valor_total"].sum()
        col3.metric("💰 Faturamento", f"R$ {total:,.2f}")

    # -----------------------------
    # TABELA
    # -----------------------------
    st.markdown("---")
    st.subheader("📋 Dados")

    st.dataframe(df_filtrado, use_container_width=True)

    # -----------------------------
    # EXPORTAÇÃO
    # -----------------------------
    st.markdown("---")
    st.subheader("📥 Exportar Dados")

    col1, col2 = st.columns(2)

    # CSV
    col1.download_button(
        label="⬇️ Baixar CSV",
        data=df_filtrado.to_csv(index=False),
        file_name="dados_filtrados.csv",
        mime="text/csv"
    )

    # Excel correto
    def to_excel(df):
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Dados")
        return output.getvalue()

    excel_data = to_excel(df_filtrado)

    col2.download_button(
        label="⬇️ Baixar Excel",
        data=excel_data,
        file_name="dados_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )