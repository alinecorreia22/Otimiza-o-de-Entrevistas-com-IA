FROM python:3.9-slim

WORKDIR /app

# Copia tudo para dentro do container
COPY . .

# Instala scikit-learn compatível
RUN pip install --no-cache-dir scikit-learn==1.6.1     && pip install --no-cache-dir -r requirements.txt

# Gera o modelo diretamente no ambiente do Docker
RUN python treinar_modelo.py

# Expõe a porta padrão do Uvicorn
EXPOSE 8000

# Inicia a API
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
