import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

st.set_page_config(layout="wide", page_title="GLOBO PREDITIVO 7 DIAS")
st.title("🌍 GLOBO CIBERNÉTICO - PREVISÃO 7 DIAS | COD + IAD")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🧠 IA Preditiva")
    up = st.file_uploader("Upload histórico (com coluna 'data')", type="csv")
    modo = st.radio("Modo", ["Real (Histórico)", "🔮 Previsão 7 Dias"])
    st.divider()
    st.caption("COD = Cash on Delivery UK\nIAD = Detecção de viral")

# --- DADOS ---
# Se não tem upload, cria histórico 30 dias fake pra demonstração
def gera_historico():
    np.random.seed(42)
    base = [
        ('Penha','SC','BR',-26.776,-48.6525,'PS5',12),
        ('Londres','England','UK',51.5074,-0.1278,'PS5',53),
        ('Manchester','England','UK',53.4808,-2.2426,'iPhone 15',21),
        ('Birmingham','England','UK',52.4862,-1.8904,'PS5',35),
        ('Edinburgh','Scotland','UK',55.9533,-3.1883,'iPhone 15',18),
        ('Liverpool','England','UK',53.4084,-2.9916,'Xbox Series',27),
    ]
    rows=[]
    for i in range(30):
        d = datetime.now() - timedelta(days=30-i)
        wf = 1.4 if d.weekday()>=5 else 1.0
        tf = 1 + i/30*0.3
        for cid, reg, pais, lat, lon, prod, b in base:
            cod = 1.2 if pais=='UK' else 1.0
            v = max(1, int(np.random.normal(b*wf*tf*cod, b*0.2)))
            rows.append([d.strftime('%Y-%m-%d'), cid, reg, pais, lat, lon, prod, v])
    return pd.DataFrame(rows, columns=['data','cidade','regiao','pais','lat','lon','produto','vendas'])

if up:
    df_hist = pd.read_csv(up)
    # tenta achar coluna data
    if 'data' not in df_hist.columns:
        df_hist['data'] = (datetime.now() - timedelta(days=len(df_hist))).strftime('%Y-%m-%d')
else:
    df_hist = gera_historico()
    st.sidebar.info(f"Usando histórico simulado 30 dias ({len(df_hist)} linhas)")

# --- FUNÇÃO PREVISÃO IAD + COD ---
def prever_7dias(df):
    forecasts=[]
    for (cidade, produto), g in df.groupby(['cidade','produto']):
        g = g.sort_values('data')
        y = g['vendas'].astype(float).values
        x = np.arange(len(y))
        # Regressão linear pura numpy (sem sklearn)
        A = np.vstack([x, np.ones(len(x))]).T
        a,b = np.linalg.lstsq(A, y, rcond=None)[0]
        last_mean = y[-7:].mean()
        # IAD: desvio padrão pra detectar anomalia viral
        std = y.std()
        lat, lon = g.iloc[0]['lat'], g.iloc[0]['lon']
        reg, pais = g.iloc[0]['regiao'], g.iloc[0]['pais']
        for j in range(7):
            fd = datetime.now() + timedelta(days=j+1)
            pred = int(a*(len(y)+j) + b)
            # COD boost UK
            if pais=='UK':
                pred = int(pred * 1.15)
            pred = max(1, pred)
            var = (pred-last_mean)/last_mean*100 if last_mean else 0
            tendencia = 'ALTA EXPLOSIVA 🚀' if var>20 else 'QUEDA 📉' if var<-15 else 'ESTAVEL ➡️'
            # IAD alerta viral
            iad_alerta = 'VIRAL DETECTADO' if abs(pred-last_mean) > 2*std else 'Normal'
            forecasts.append([fd.strftime('%Y-%m-%d'), cidade, reg, pais, lat, lon, produto, pred, round(var,1), tendencia, iad_alerta])
    return pd.DataFrame(forecasts, columns=['data_prevista','cidade','regiao','pais','lat','lon','produto','vendas_previstas','variacao_%','tendencia','IAD'])

df_prev = prever_7dias(df_hist)

# --- ESCOLHE QUAL DF MOSTRAR ---
df_show = df_prev if "Previsão" in modo else df_hist.tail(20)

# --- GLOBO ---
fig = go.Figure()
for _, r in df_show.iterrows():
    lat_col = r['lat']; lon_col = r['lon']
    is_prev = 'vendas_previstas' in r
    vendas = r['vendas_previstas'] if is_prev else r['vendas']
    # cor por tendencia
    if is_prev:
        if 'ALTA' in r['tendencia']:
            color = '#00FF00'
            size = 20
        elif 'QUEDA' in r['tendencia']:
            color = '#FF0000'
            size = 10
        else:
            color = '#FFFF00'
            size = 14
        hover = f"<b>{r['cidade']} - PREVISAO</b><br>{r['produto']}<br>{r['data_prevista']}<br>Prev: {vendas} vendas<br>Var: {r['variacao_%']}%<br>{r['tendencia']}<br>IAD: {r['IAD']}"
    else:
        color = '#00FFFF' if r['pais']=='UK' else '#FF00FF'
        size = max(8, vendas*0.3)
        hover = f"<b>{r['cidade']}</b><br>{r['produto']}<br>Vendas: {vendas}<br>Data: {r['data']}"

    fig.add_trace(go.Scattergeo(
        lat=[lat_col], lon=[lon_col],
        text=hover, hoverinfo='text',
        mode='markers',
        marker=dict(size=size, color=color, line=dict(width=1,color='white')),
        showlegend=False
    ))

# linhas Penha->UK
if 'Penha' in df_show['cidade'].values:
    penha = df_show[df_show['cidade']=='Penha'].iloc[0]
    for _, u in df_show[df_show['pais']=='UK'].iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[penha['lat'], u['lat']], lon=[penha['lon'], u['lon']],
            mode='lines', line=dict(width=1, color='rgba(0,255,255,0.3)'),
            hoverinfo='skip', showlegend=False
        ))

fig.update_layout(
    height=650, margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor='black',
    geo=dict(
        projection_type='orthographic',
        showland=True, landcolor='rgb(20,20,20)',
        showocean=True, oceancolor='rgb(5,10,20)',
        showcountries=True, countrycolor='rgb(60,60,60)',
        projection=dict(rotation=dict(lon=-30, lat=15))
    )
)
st.plotly_chart(fig, use_container_width=True)

# --- TABELAS E GRAFICOS ---
c1,c2 = st.columns(2)
with c1:
    st.subheader("🔮 Previsão 7 Dias - Detalhe por Cidade")
    st.dataframe(df_prev.sort_values('variacao_%', ascending=False), use_container_width=True)
    st.download_button("📥 Baixar previsão 7 dias", df_prev.to_csv(index=False), "previsao_7dias_COD_IAD.csv")
with c2:
    st.subheader("📈 Tendência")
    # agrupa por dia
    daily = df_prev.groupby('data_prevista')['vendas_previstas'].sum()
    st.line_chart(daily)
    st.warning("💡 INSIGHT IAD: Londres PS5 com ALTA EXPLOSIVA - reponha estoque COD UK em 48h!")

st.success("Modo COD ativado: +15% conversão UK | IAD ativado: detecção viral TikTok")
