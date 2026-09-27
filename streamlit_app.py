import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="GLOBO CIBERNÉTICO | Daniel Ramos", layout="wide", page_icon="🌐")

st.markdown("# 🌐 GLOBO CIBERNÉTICO - Daniel Ramos")
st.markdown("### 8 Módulos: LERMING + AI MIND + COLMEIA + PRODUTO + TEMPO + CHURN + TICKET + GLOBO CORE")
st.markdown("---")

# --- SIMULAÇÃO DA COLMEIA GLOBAL ---
np.random.seed(7)
n = 400
df = pd.DataFrame({
    'lat': np.random.uniform(-60, 75, n),
    'lon': np.random.uniform(-180, 180, n),
    'comportamento': np.random.choice(['Navegando','Comprando','Abandonando','Comparando Preço'], n, p=[0.4,0.3,0.2,0.1]),
    'produto': np.random.choice(['iPhone 15','Tênis Nike','Notebook Gamer','Camisa','Perfume Importado','Curso IA'], n),
    'valor': np.random.uniform(80, 12000, n),
    'cidade': np.random.choice(['Penha-SC','Balneário Camboriú','São Paulo','New York','Tokyo','Berlim','Dubai','Londres'], n),
    'churn_risk': np.random.uniform(0,1,n)
})

col1, col2 = st.columns([3,1])

with col1:
    fig = go.Figure(go.Scattergeo(
        lat=df['lat'], lon=df['lon'],
        mode='markers',
        marker=dict(size=df['valor']/400, color=df['churn_risk'], colorscale='Jet', showscale=True, colorbar_title="Risco"),
        text=df['produto'] + " | " + df['cidade'] + " | R$" + df['valor'].astype(int).astype(str) + " | " + df['comportamento'],
        hoverinfo='text'
    ))
    fig.update_geos(projection_type="orthographic", showland=True, showocean=True)
    fig.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("🧠 AI MIND - Pessoas Online", f"{n}")
    st.metric("🔥 Produto Mais Quente", df['produto'].mode()[0])
    st.metric("📍 Cidade Que Mais Compra", df['cidade'].mode()[0])
    st.metric("💰 Ticket Médio Previsto", f"R$ {df['valor'].mean():.2f}")
    
    st.divider()
    st.subheader("🎯 COLMEIA - Filtros")
    filtro = st.selectbox("Comportamento:", ['Todos','Comprando','Navegando','Abandonando'])
    if filtro != 'Todos':
        st.dataframe(df[df['comportamento']==filtro][['cidade','produto','valor','comportamento']].head(10), use_container_width=True)
    else:
        st.dataframe(df[['cidade','produto','comportamento','valor']].head(15), use_container_width=True)

st.success(f"GLOBO CORE ATIVO - LERMING RODANDO - {datetime.now().strftime('%d/%m %H:%M:%S')} - Penha-SC")
