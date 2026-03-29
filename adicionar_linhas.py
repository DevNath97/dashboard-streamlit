import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import ast

def tela_adicionar_venda():

    st.title("🛒 Registrar Nova Venda")

    # -----------------------------
    # SESSION STATE
    # -----------------------------
    if "mensagem" not in st.session_state:
        st.session_state.mensagem = ""

    if st.session_state.mensagem:
        st.success(st.session_state.mensagem)
        st.session_state.mensagem = ""

    # -----------------------------
    # CAMINHOS
    # -----------------------------
    base_path = Path(__file__).parent / "datasets"

    caminho_compras = base_path / "compras.csv"
    caminho_lojas = base_path / "lojas.csv"
    caminho_produtos = base_path / "produtos.csv"

    # -----------------------------
    # CARREGAR DADOS
    # -----------------------------
    def carregar_dados():
        df_compras = pd.read_csv(caminho_compras) if caminho_compras.exists() else pd.DataFrame()
        df_lojas = pd.read_csv(caminho_lojas) if caminho_lojas.exists() else pd.DataFrame()
        df_produtos = pd.read_csv(caminho_produtos) if caminho_produtos.exists() else pd.DataFrame()

        if not df_compras.empty:
            df_compras["data"] = pd.to_datetime(df_compras["data"], errors="coerce")

        return df_compras, df_lojas, df_produtos

    df_compras, df_lojas, df_produtos = carregar_dados()

    # -----------------------------
    # VALIDAÇÃO
    # -----------------------------
    if df_lojas.empty or df_produtos.empty:
        st.error("⚠️ Dados de lojas ou produtos não encontrados.")
        return

    # -----------------------------
    # LOJA
    # -----------------------------
    st.subheader("🏬 Loja")

    col1, col2 = st.columns(2)

    loja = col1.selectbox("Cidade", df_lojas["cidade"].astype(str))
    loja_info = df_lojas[df_lojas["cidade"] == loja].iloc[0]

    vendedores = loja_info["vendedores"]
    if isinstance(vendedores, str):
        vendedores = ast.literal_eval(vendedores)

    vendedor = col2.selectbox("Vendedor", vendedores)

    # -----------------------------
    # FORMULÁRIO
    # -----------------------------
    st.subheader("📦 Dados da venda")

    with st.form("form_venda"):

        col1, col2 = st.columns(2)

        produto_nome = col1.selectbox("Produto", df_produtos["produto"].unique())
        produto = df_produtos[df_produtos["produto"] == produto_nome].iloc[0]

        quantidade = col2.number_input("Quantidade", min_value=1, value=1)

        forma_pagamento = st.selectbox(
            "Forma de pagamento",
            ["Cartão de Crédito", "Pix", "Boleto"]
        )

        submit = st.form_submit_button("💾 Registrar Venda")

    # -----------------------------
    # SALVAR
    # -----------------------------
    if submit:

        novo_id = int(df_compras["id_compra"].max()) + 1 if not df_compras.empty else 1

        nova_venda = {
            "id_compra": novo_id,
            "data": datetime.now(),
            "estado": loja_info["estado"],
            "cidade": loja_info["cidade"],
            "vendedor": vendedor,
            "produto": produto["produto"],
            "sku": produto["sku"],
            "cor": produto["cor"],
            "quantidade": quantidade,
            "valor_total": produto["preco"] * quantidade,
            "lucro_total": produto["lucro_unitario"] * quantidade,
            "forma_pagamento": forma_pagamento,
            "cliente_nome": "Cliente Novo",
            "cpf": "000.000.000-00",
            "idade": 30,
            "comportamento": "não informado"
        }

        df_compras = pd.concat([df_compras, pd.DataFrame([nova_venda])], ignore_index=True)
        df_compras.to_csv(caminho_compras, index=False)

        st.session_state.mensagem = f"🟢 Venda registrada: {produto['produto']} (x{quantidade})"
        st.rerun()

    # -----------------------------
    # ÚLTIMAS VENDAS
    # -----------------------------
    st.markdown("---")
    st.subheader("⏱️ Últimas vendas")

    if not df_compras.empty:

        horas = st.selectbox("Período (horas)", [1, 3, 6, 12, 24], index=2)

        limite = datetime.now() - pd.Timedelta(hours=horas)

        ultimas = df_compras[df_compras["data"] >= limite]
        ultimas = ultimas.sort_values("data", ascending=False)

        if ultimas.empty:
            st.info("Nenhuma venda recente.")
        else:
            st.dataframe(
                ultimas[["data", "produto", "quantidade", "valor_total", "vendedor", "cidade"]],
                use_container_width=True
            )