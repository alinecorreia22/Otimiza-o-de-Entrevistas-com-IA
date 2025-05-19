from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib
import logging

logging.basicConfig(
    filename='api_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

model = joblib.load('modelo_entrevista.pkl')
le_dict = joblib.load('label_encoders.pkl')
features = joblib.load('features_utilizadas.pkl')

app = FastAPI()

class Candidato(BaseModel):
    formacao_e_idiomas_nivel_academico: str
    formacao_e_idiomas_nivel_ingles: str
    informacoes_profissionais_nivel_profissional: str
    informacoes_profissionais_remuneracao: float
    perfil_vaga_competencia_tecnicas_e_comportamentais: str
    informacoes_basicas_tipo_contratacao: str
    informacoes_basicas_cliente: str

@app.post("/predict")
def predict(candidato: Candidato):
    data = candidato.dict()
    logging.info(f"Entrada: {data}")
    df = pd.DataFrame([data])
    for col in df.columns:
        if col in le_dict:
            encoder = le_dict[col]
            try:
                df[col] = encoder.transform([df[col][0]])
            except ValueError:
                df[col] = encoder.transform([encoder.classes_[0]])
    df = df[features]
    prediction = model.predict(df)[0]
    prob = model.predict_proba(df)[0][1]
    logging.info(f"Resultado: recomendado={prediction}, probabilidade={prob}")
    return {
        "recomendado_para_entrevista": bool(prediction),
        "probabilidade_sucesso": round(prob, 2)
    }
