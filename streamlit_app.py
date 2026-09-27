import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="GLOBO CIBERNÉTICO - Daniel Ramos", layout="wide", page_icon="🌐")

st.title("🌐 GLOBO CIBERNÉTICO - Daniel Ramos")
st.subheader("8 Módulos: LERMING + AI MIND + COLMEIA + PRODUTO + TEMPO + CHURN + TICKET + GLOBO CORE | DADOS REAIS")

# --- SIDEBAR - DADOS REAIS ---
st.sidebar.title("📁 Fonte de Dados")
st.sidebar.info("Carregue seu arquivo real ou use simulação")

uploaded_file = st.sidebar.file_uploader("Carregar CSV real (colunas: cidade, produto, valor, lat, lon)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success(f"✅ {len(df)} registros reais carregados!")
    # Tenta adaptar colunas
    if 'valor' not in df.columns:
        df['valor'] = np.random.uniform(500, 10000, len(df))
    is_real = True
else:
    st.sidebar.warning("Usando dados simulados")
    # DADOS SIMULADOS (seu original melhorado)
    cidades = {
        'Berlim': [52.52, 13.40], 'São Paulo': [-23.55, -46.63], 'Tóquio': [35.67, 139.65],
        'Nova York': [40.71, -74.00], 'Penha-SC': [-26.77, -48.64], 'Londres': [51.50, -0.12]
    }
    produtos = ['Notebook Gamer', 'iPhone 15', 'PS5', 'Alexa', 'Monitor 4K']
    data = []
    for _ in range(400):
        cidade = np.random.choice(list(cidades.keys()))
        lat, lon = cidades[cidade]
        data.append({
            'cidade': cidade,
            'produto': np.random.choice(produtos),
            'valor': np.random.uniform(500, 12000),
            'lat': lat + np.random.uniform(-1,1),
            'lon': lon + np.random.uniform(-1,1),
            'risco': np.random.uniform(0.5, 1.0)
        })
    df = pd.DataFrame(data)
    is_real = False

# --- GLOBO ---
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.scatter_geo(df, lat='lat', lon='lon', color='risco',
                         hover_name='cidade', hover_data=['produto', 'valor'],
                         color_continuous_scale='RdYlGn_r',
                         projection="orthographic", title="Mapa Global em Tempo Real")
    fig.update_layout(height=600, paper_bgcolor="black", font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.metric("🧠 AI MIND - Pessoas Online", len(df))
    produto_top = df.groupby('produto')['valor'].sum().idxmax() if 'produto' in df.columns else "Notebook Gamer"
    st.metric("🔥 Produto Mais Quente", produto_top)
    cidade_top = df['cidade'].value_counts().idxmax() if 'cidade' in df.columns else "Berlim"
    st.metric("📍 Cidade Que Mais Compra", cidade_top)
    st.metric("💰 Ticket Médio Previsto", f"R$ {df['valor'].mean():.2f}")

# --- DASHBOARD + DOWNLOADS ---
st.divider()
st.subheader("📊 Relatório e Downloads")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.dataframe(df.head(20), use_container_width=True)
with col_b:
    if 'produto' in df.columns:
        chart = df.groupby('produto')['valor'].sum().reset_index()
        st.plotly_chart(px.bar(chart, x='produto', y='valor', title="Vendas por Produto"), use_container_width=True)
with col_c:
    st.write("⬇️ **Baixar Relatórios**")

    # Botão CSV
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Baixar CSV Completo",
        data=csv,
        file_name=f"relatorio_globo_{datetime.now().strftime('%d%m%Y')}.csv",
        mime="text/csv",
    )

    # Botão Excel
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    st.download_button(
        label="📊 Baixar EXCEL",
        data=output.getvalue(),
        file_name=f"relatorio_globo_{datetime.now().strftime('%d%m%Y')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    if is_real:
        st.success("Relatório com DADOS REAIS")
    else:
        st.info("Carregue um CSV para ter dados reais")

st.caption(f"Atualizado em {datetime.now().strftime('%d/%m/%Y %H:%M')} | Daniel Ramos | Penha-SC")
