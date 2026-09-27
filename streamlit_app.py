import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide", page_title="Globo Cibernético REAL")
st.title("🌍 GLOBO CIBERNÉTICO - REALISTA 3D")
st.caption("Arraste para girar | Scroll para zoom | Passe o mouse nos pontos")

# --- Dados base com coordenadas REAIS ---
dados_base = {
    'cidade': ['Penha', 'Londres', 'Manchester', 'Birmingham', 'Edinburgh', 'Liverpool', 'Londrina', 'São Paulo'],
    'regiao': ['Santa Catarina', 'England', 'England', 'England', 'Scotland', 'England', 'Paraná', 'São Paulo'],
    'pais': ['BR', 'UK', 'UK', 'UK', 'UK', 'UK', 'BR', 'BR'],
    'lat': [-26.7760, 51.5074, 53.4808, 52.4862, 55.9533, 53.4084, -23.3044, -23.5505],
    'lon': [-48.6525, -0.1278, -2.2426, -1.8904, -3.1883, -2.9916, -51.1696, -46.6333],
    'produto': ['PS5', 'PS5', 'iPhone 15', 'PS5', 'iPhone 15', 'Xbox', 'PS5', 'iPhone 15'],
    'vendas': [12, 53, 21, 35, 18, 27, 8, 42],
    'valor': [4299, 429.99, 899.99, 429.99, 899.99, 449.99, 4299, 7999],
    'risco': [1, 2, 1, 3, 1, 2, 1, 1]
}

@st.cache_data
def load_data(uploaded):
    if uploaded:
        df = pd.read_csv(uploaded)
        # garante colunas
        return df
    return pd.DataFrame(dados_base)

with st.sidebar:
    st.header("Fonte de Dados")
    up = st.file_uploader("Upload seu CSV (com lat,lon)", type="csv")
    df = load_data(up)
    if up:
        st.success(f"{len(df)} registros reais carregados!")
    else:
        st.info("Usando dados de exemplo REALISTAS")

    produto_filtro = st.multiselect("Filtrar Produto", df['produto'].unique(), default=df['produto'].unique())

df_f = df[df['produto'].isin(produto_filtro)]

# --- GLOBO REALISTA ---
fig = go.Figure()

# 1. Globo base (oceano + terra)
fig.add_trace(go.Scattergeo(
    lat=[0], lon=[0], mode='markers', marker=dict(size=1, color='rgba(0,0,0,0)'), showlegend=False
))

# 2. Pontos de venda
for _, row in df_f.iterrows():
    color = '#00FFFF' if row['pais']=='UK' else '#FF00FF' if row['cidade']=='Penha' else '#00FF88'
    size = max(8, row['vendas'] * 0.8)

    fig.add_trace(go.Scattergeo(
        lat=[row['lat']],
        lon=[row['lon']],
        text=f"<b>{row['cidade']}</b><br>{row['regiao']}, {row['pais']}<br>📦 {row['produto']}<br>📈 {row['vendas']} vendas<br>💰 R$ {row['valor']}<br>Lat: {row['lat']}, Lon: {row['lon']}",
        hoverinfo='text',
        mode='markers',
        marker=dict(
            size=size,
            color=color,
            line=dict(width=1, color='white'),
            sizemode='diameter'
        ),
        name=f"{row['cidade']} - {row['produto']}"
    ))

# 3. Linhas Penha -> UK (conexão cibernética)
penha = df_f[df_f['cidade']=='Penha']
uk = df_f[df_f['pais']=='UK']
if not penha.empty:
    for _, u in uk.iterrows():
        fig.add_trace(go.Scattergeo(
            lat=[penha.iloc[0]['lat'], u['lat']],
            lon=[penha.iloc[0]['lon'], u['lon']],
            mode='lines',
            line=dict(width=1, color='rgba(0,255,255,0.4)'),
            hoverinfo='skip',
            showlegend=False
        ))

fig.update_layout(
    height=700,
    margin={"r":0,"t":0,"l":0,"b":0},
    paper_bgcolor='black',
    geo=dict(
        projection_type='orthographic',
        showland=True,
        landcolor='rgb(20,20,20)',
        showocean=True,
        oceancolor='rgb(5,10,20)',
        showcountries=True,
        countrycolor='rgb(60,60,60)',
        showcoastlines=True,
        coastlinecolor='rgb(80,80,80)',
        showlakes=False,
        bgcolor='rgba(0,0,0,0)',
        projection=dict(
            rotation=dict(lon=-30, lat=15)
        )
    ),
    legend=dict(font=dict(color='white'))
)

st.plotly_chart(fig, use_container_width=True)

# Relatorio
st.divider()
col1, col2 = st.columns(2)
with col1:
    st.subheader("Relatório e Downloads")
    st.dataframe(df_f[['cidade','regiao','pais','produto','vendas','valor','lat','lon']], use_container_width=True)
    st.download_button("📥 Baixar relatório", df_f.to_csv(index=False), "relatorio_globo_realista.csv")
with col2:
    st.subheader("Vendas por Produto")
    st.bar_chart(df_f.groupby('produto')['vendas'].sum())
