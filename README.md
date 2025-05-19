# 🤖 Otimizador de Entrevistas com IA

Este projeto é um MVP de uma solução inteligente para recomendar candidatos com maior potencial para entrevistas, usando machine learning e dados históricos de recrutamento.

---

## 🔍 Funcionalidades

- API com FastAPI para predições em tempo real
- Modelo de machine learning (Random Forest)
- Empacotamento com Docker
- Deploy na nuvem com Render
- Logging contínuo de entradas e previsões
- Testes unitários com pytest
- Monitoramento de uso e preparo para detecção de drift

---

## 🚀 Como rodar localmente (com Docker)

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/otimizador-entrevistas-ia.git
cd otimizador-entrevistas-ia

# Construa a imagem Docker
docker build -t otimizador-ia .

# Rode o container
docker run -p 8000:8000 otimizador-ia
