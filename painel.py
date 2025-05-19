import streamlit as st
import pandas as pd
import os
import json
import re

st.set_page_config(page_title="Painel IA de Entrevistas", layout="wide")

st.title("📊 Painel de Monitoramento - IA Otimização de Entrevistas")
st.markdown("---")

LOG_FILE = "logs_entrevistas.log"

def parse_log(file_path):
    entradas = []
    if not os.path.exists(file_path):
        return pd.DataFrame()

    with open(file_path, "r") as f:
        for linha in f:
            try:
                match = re.search(r"IP: (.*?) \| Entrada: (.*?) \| Resultado: (.*)", linha)
                if match:
                    ip = match.group(1)
                    entrada = json.loads(match.group(2).replace("'", '"'))
                    resultado = json.loads(match.group(3).replace("'", '"'))
                    entrada.update(resultado)
                    entrada["IP"] = ip
                    entrada["timestamp"] = linha[:19]
                    entradas.append(entrada)
            except Exception as e:
                print(f"Erro ao processar linha: {e}")
    return pd.DataFrame(entradas)

df = parse_log(LOG_FILE)

if df.empty:
    st.warning("Nenhum log encontrado.")
else:
    col1, col2 = st.columns(2)

    with col1:
        filtro_pred = st.selectbox("🔍 Filtrar por previsão", options=["Todos", "Concluída", "Não concluída"])
        if filtro_pred != "Todos":
            df = df[df["previsao"] == (1 if filtro_pred == "Concluída" else 0)]

    with col2:
        qtd = st.slider("🔢 Quantidade de registros exibidos", min_value=5, max_value=100, value=20)

    st.markdown("### 📄 Registros Recentes")
    st.dataframe(df.sort_values("timestamp", ascending=False).head(qtd), use_container_width=True)