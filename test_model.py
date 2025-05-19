import joblib
import pandas as pd

def test_model_carrega():
    model = joblib.load('modelo_entrevista.pkl')
    assert model is not None

def test_previsao_simples():
    model = joblib.load('modelo_entrevista.pkl')
    features = joblib.load('features_utilizadas.pkl')
    le_dict = joblib.load('label_encoders.pkl')

    dados = {
        'formacao_e_idiomas.nivel_academico': 'Ensino Médio',
        'formacao_e_idiomas.nivel_ingles': 'Intermediário',
        'informacoes_profissionais.nivel_profissional': 'Júnior',
        'informacoes_profissionais.remuneracao': 3500,
        'perfil_vaga.competencia_tecnicas_e_comportamentais': 'HTML, CSS',
        'informacoes_basicas.tipo_contratacao': 'CLT',
        'informacoes_basicas.cliente': 'Empresa XP'
    }

    df = pd.DataFrame([dados])
    for col in df.columns:
        if col in le_dict:
            encoder = le_dict[col]
            try:
                df[col] = encoder.transform([df[col][0]])
            except ValueError:
                df[col] = encoder.transform([encoder.classes_[0]])

    df = df[features]
    pred = model.predict(df)[0]
    assert pred in [0, 1]
