# 🌸 Ohana Studio

App para organizar o fluxo completo de criação de looks de moda da **Ohana Lifestyle**.

## Funcionalidades

- **Dashboard** — Calendário semanal com status visual, métricas e prioridade do dia
- **Criar Look** — Formulário com as 9 etapas do fluxo, barra de progresso, seleção de modelo
- **Biblioteca** — Acervo de prompts, links do Pinterest, Shopee e perfis de modelos
- **Histórico** — Looks finalizados organizados por semana

## Fluxo de 9 Etapas

1. 📌 Pinterest Inspo
2. 🛍️ Curadoria Shopee
3. 🤖 Gerar Modelo IA
4. 🎨 Modelo + Curadoria
5. 📸 Gerar 3-4 Poses
6. 🎠 Gerar Carrossel
7. 🎬 Gerar Vídeo
8. 📱 Gerar Reels
9. 📖 Stories (Inspo vs Ohana)

## Como rodar localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy no Streamlit Cloud

1. Suba este repositório para o GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io)
3. Conecte o repositório e aponte para `app.py`
4. Clique em **Deploy**

> Os dados são salvos em `ohana_data.json` (ignorado no `.gitignore` — apenas local).
