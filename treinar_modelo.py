import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

features = [
    'formacao_e_idiomas.nivel_academico',
    'formacao_e_idiomas.nivel_ingles',
    'informacoes_profissionais.nivel_profissional',
    'informacoes_profissionais.remuneracao',
    'perfil_vaga.competencia_tecnicas_e_comportamentais',
    'informacoes_basicas.tipo_contratacao',
    'informacoes_basicas.cliente'
]

X_dummy = pd.DataFrame({col: [1]*10 for col in features})
y_dummy = [0, 1]*5

model = RandomForestClassifier()
model.fit(X_dummy, y_dummy)

joblib.dump(model, "modelo_entrevista.pkl")
