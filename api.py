from fastapi import FastAPI, Request
from pydantic import BaseModel
import joblib
import pandas as pd
import logging

# CONFIGURAR LOGGING
logging.basicConfig(filename="logs_entrevistas.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Carregar modelo e encoders (substitua pelos seus arquivos reais)
model = joblib.load("modelo_entrevista.pkl")
le_dict = joblib.load("label_encoders.pkl")
features = joblib.load("features_utilizadas.pkl")

app = FastAPI(title="API Previsão de Entrevista")

class Candidato(BaseModel):
    formacao_e_idiomas_nivel_academico: str
    formacao_e_idiomas_nivel_ingles: str
    informacoes_profissionais_nivel_profissional: str
    informacoes_profissionais_remuneracao: float
    perfil_vaga_competencia_tecnicas_e_comportamentais: str
    informacoes_basicas_tipo_contratacao: str
    informacoes_basicas_cliente: str

@app.post("/prever/")
def prever_conclusao(candidato: Candidato, request: Request):
    dados = pd.DataFrame([candidato.dict()])
    dados.columns = features

    for col in dados.columns:
        if col in le_dict:
            dados[col] = le_dict[col].transform(dados[col].astype(str))

    pred = model.predict(dados)[0]
    prob = model.predict_proba(dados)[0][pred]

    resultado = {
        "previsao": int(pred),
        "probabilidade": round(prob, 2),
        "mensagem": "Entrevista provável de ser concluída" if pred == 1 else "Entrevista não deve ser concluída"
    }

    logging.info(f"IP: {request.client.host} | Entrada: {candidato.dict()} | Resultado: {resultado}")

    return resultado