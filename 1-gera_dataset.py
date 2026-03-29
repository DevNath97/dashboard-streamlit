import random
from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd

# -----------------------------
# PASTA DATASETS
# -----------------------------
pasta_datasets = Path(__file__).parent / "datasets"
pasta_datasets.mkdir(exist_ok=True)

# -----------------------------
# LOJAS
# -----------------------------
LOJAS = [
    {"estado": "SP", "cidade": "São Paulo", "vendedores": ["Thales", "Amanda"]},
    {"estado": "RJ", "cidade": "Rio de Janeiro", "vendedores": ["Carlos", "Fernanda"]},
    {"estado": "MG", "cidade": "Belo Horizonte", "vendedores": ["João", "Mariana"]},
    {"estado": "RS", "cidade": "Porto Alegre", "vendedores": ["Lucas", "Patrícia"]},
    {"estado": "PR", "cidade": "Curitiba", "vendedores": ["Bruno", "Juliana"]},
    {"estado": "BA", "cidade": "Salvador", "vendedores": ["Rafael", "Camila"]},
    {"estado": "PE", "cidade": "Recife", "vendedores": ["Diego", "Larissa"]}
]

# -----------------------------
# PRODUTOS
# -----------------------------
PRODUTOS_BASE = [
    {"produto": "Tenis Zallur Casual A1", "id": 0, "preco": 150, "categoria": "Casual"},
    {"produto": "Tenis Zallur Esportivo A2", "id": 1, "preco": 200, "categoria": "Esportivo"},
    {"produto": "Tenis Zallur Running A3", "id": 2, "preco": 250, "categoria": "Running"},
    {"produto": "Tenis Zallur Street A4", "id": 3, "preco": 180, "categoria": "Street"},
    {"produto": "Tenis Zallur Classic A5", "id": 4, "preco": 220, "categoria": "Casual"},
    {"produto": "Tenis Zallur Comfort A6", "id": 5, "preco": 170, "categoria": "Conforto"},
    {"produto": "Tenis Zallur Performance A7", "id": 6, "preco": 300, "categoria": "Performance"},
    {"produto": "Tenis Zallur Lifestyle A8", "id": 7, "preco": 190, "categoria": "Lifestyle"},
    {"produto": "Tenis Zallur Flex A9", "id": 8, "preco": 210, "categoria": "Esportivo"},
    {"produto": "Tenis Zallur Pro A10", "id": 9, "preco": 280, "categoria": "Performance"},
    {"produto": "Tenis Zallur Elite A11", "id": 10, "preco": 350, "categoria": "Premium"},
    {"produto": "Tenis Zallur Max A12", "id": 11, "preco": 320, "categoria": "Premium"},
    {"produto": "Tenis Zallur Ultra A13", "id": 12, "preco": 400, "categoria": "Premium"},
    {"produto": "Tenis Zallur Air A14", "id": 13, "preco": 270, "categoria": "Running"},
    {"produto": "Tenis Zallur Zoom A15", "id": 14, "preco": 230, "categoria": "Esportivo"}
]

CORES = ["Preto", "Branco", "Cinza", "Azul", "Vermelho"]
FORMA_PAGAMENTO = ["Cartão de Crédito", "Boleto", "Pix"]

# -----------------------------
# GERAR CPF
# -----------------------------
def gerar_cpf():
    return f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}"

# -----------------------------
# GERAR NOMES
# -----------------------------
NOMES = ["Lucas", "Mariana", "Pedro", "Ana", "João", "Julia", "Carlos", "Fernanda"]
SOBRENOMES = ["Silva", "Souza", "Oliveira", "Santos", "Costa", "Pereira"]

def gerar_nome():
    return f"{random.choice(NOMES)} {random.choice(SOBRENOMES)}"

# -----------------------------
# GERAR SKUs
# -----------------------------
produtos_sku = []

for produto in PRODUTOS_BASE:
    for cor in CORES:
        sku = f"A{produto['id']}-{cor[:3].upper()}"

        custo = int(produto["preco"] * random.uniform(0.5, 0.7))

        produtos_sku.append({
            "sku": sku,
            "produto": produto["produto"],
            "categoria": produto["categoria"],
            "cor": cor,
            "preco": produto["preco"],
            "custo": custo,
            "lucro_unitario": produto["preco"] - custo
        })

# -----------------------------
# PERFIL CLIENTE
# -----------------------------
def perfil_cliente():
    idade = random.randint(18, 65)

    if idade < 25:
        comportamento = "impulsivo"
        qtd = random.randint(1, 3)
    elif idade < 40:
        comportamento = "equilibrado"
        qtd = random.randint(1, 2)
    else:
        comportamento = "conservador"
        qtd = 1

    return idade, comportamento, qtd

# -----------------------------
# GERAR VENDAS
# -----------------------------
compras = []

for i in range(3000):
    loja = random.choice(LOJAS)
    vendedor = random.choice(loja["vendedores"])
    produto = random.choice(produtos_sku)

    idade, comportamento, quantidade = perfil_cliente()

    data = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23)
    )

    valor_total = produto["preco"] * quantidade
    lucro_total = produto["lucro_unitario"] * quantidade

    compras.append({
        "id_compra": i,
        "data": data,
        "estado": loja["estado"],
        "cidade": loja["cidade"],
        "vendedor": vendedor,
        "produto": produto["produto"],
        "sku": produto["sku"],
        "cor": produto["cor"],
        "quantidade": quantidade,
        "valor_total": valor_total,
        "lucro_total": lucro_total,
        "forma_pagamento": random.choice(FORMA_PAGAMENTO),
        "cliente_nome": gerar_nome(),
        "cpf": gerar_cpf(),
        "idade": idade,
        "comportamento": comportamento
    })

# -----------------------------
# DATAFRAMES
# -----------------------------
df_produtos = pd.DataFrame(produtos_sku)

# 🔥 CORREÇÃO AQUI (ordem decrescente)
df_compras = pd.DataFrame(compras).sort_values("data", ascending=False)

df_lojas = pd.DataFrame(LOJAS)

# -----------------------------
# EXPORTAR CSV
# -----------------------------
df_produtos.to_csv(pasta_datasets / "produtos.csv", index=False)
df_compras.to_csv(pasta_datasets / "compras.csv", index=False)
df_lojas.to_csv(pasta_datasets / "lojas.csv", index=False)

# -----------------------------
# EXPORTAR EXCEL
# -----------------------------
df_produtos.to_excel(pasta_datasets / "produtos.xlsx", index=False)
df_compras.to_excel(pasta_datasets / "compras.xlsx", index=False)
df_lojas.to_excel(pasta_datasets / "lojas.xlsx", index=False)