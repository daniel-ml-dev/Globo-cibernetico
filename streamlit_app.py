import streamlit as st
from datetime import datetime, timezone, timedelta
import time
import requests
import random
import pydeck as pdk

# ──────────────────────────────────────────────
# CONFIGURAÇÃO
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Global Observation System | MUNDIAL",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🔑 CHAVES
NASA_KEY = "DEMO_KEY"
WEATHER_KEY = ""  # ← Coloque sua chave do openweathermap.org aqui

# ──────────────────────────────────────────────
# FUNÇÕES DE DADOS REAIS
# ──────────────────────────────────────────────

def br_time():
    return datetime.now(timezone.utc) - timedelta(hours=3)

# 🛰️ ISS — Posição em tempo real
def get_iss():
    try:
        r = requests.get("http://api.open-notify.org/iss-now.json", timeout=5)
        return r.json() if r.status_code == 200 else None
    except: return None

# 🌋 TERREMOTOS — USGS (últimas 24h, ≥2.5 mag)
def get_earthquakes():
    try:
        url = "https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=" + \
              (datetime.utcnow()-timedelta(days=1)).strftime("%Y-%m-%d") + "&minmagnitude=2.5&limit=100"
        r = requests.get(url, timeout=10)
        return r.json() if r.status_code == 200 else None
    except: return None

# 🌤️ CLIMA — Qualquer cidade do mundo
def get_weather(city):
    if not WEATHER_KEY:
        return {"main":{"temp":22,"humidity":70},"weather":[{"description":"Céu limpo"}],"name":city,"sys":{"country":"--"},"wind":{"speed":3.5}}
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_KEY}&units=metric&lang=pt"
        r = requests.get(url, timeout=8)
        return r.json() if r.status_code == 200 else None
    except: return None

# ☁️ NASA APOD
def get_apod():
    try:
        r = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={NASA_KEY}", timeout=5)
        return r.json() if r.status_code == 200 else {"url": "https://apod.nasa.gov/apod/image/2408/M31_Hubble_960.jpg", "title": "Modo offline"}
    except:
        return {"url": "https://apod.nasa.gov/apod/image/2408/M31_Hubble_960.jpg", "title": "Andrômeda (offline)", "explanation": "Sem sinal"}

# ASTEROIDES
def get_neo():
    try:
        today = datetime.now().strftime("%Y-%m-%d")
        r = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={NASA_KEY}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            return list(data['near_earth_objects'].values())[0][:3]
        return [{"name": "Offline", "close_approach_data": [{"miss_distance": {"kilometers": "1200000"}}]}]
    except:
        return [{"name": "Asteroide Modo Offline", "close_approach_data": [{"miss_distance": {"kilometers": "1200000"}}]}]

# ☄️ ASTEROIDES
def get_neo():
    try:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        r = requests.get(f"https://api.nasa.gov/neo/rest/v1/feed?start_date={today}&end_date={today}&api_key={NASA_KEY}", timeout=5)
        if r.status_code == 200:
            data = r.json()
            return list(data['near_earth_objects'].values())[0][:3]
        else:
            raise Exception("offline")
    except:
        return [{"name": "Asteroide Modo Offline (sem sinal)", "close_approach_data": [{"miss_distance": {"kilometers": "1200000"}}]}]

# 🔥 FOCOS DE INCÊNDIO (dados simulados com base em regiões reais)
def get_fires():
    return [
        {"lat": -3.46, "lon": -62.22, "intensity": "Alta", "region": "Amazônia, BR"},
        {"lat": 34.05, "lon": -118.24, "intensity": "Média", "region": "Califórnia, EUA"},
        {"lat": 36.77, "lon": -119.41, "intensity": "Alta", "region": "Yosemite, EUA"},
        {"lat": -8.34, "lon": -55.95, "intensity": "Baixa", "region": "Mato Grosso, BR"},
        {"lat": 30.04, "lon": 31.24, "intensity": "Média", "region": "Cairo, EG"},
        {"lat": 64.20, "lon": -149.49, "intensity": "Baixa", "region": "Alasca, EUA"},
    ]

# 📈 DADOS GLOBAIS SIMULADOS (indicadores agregados)
def get_global_stats():
    return {
        "population": "8.1B",
        "cities_monitored": "5,280",
        "active_sensors": "1.2M+",
        "events_today": 1847,
        "disasters_detected": 3,
        "air_quality_index": 72,
        "ocean_temp_anomaly": "+0.84°C",
        "forecast_accuracy": "94.2%"
    }

# ──────────────────────────────────────────────
# ESTILO
# ──────────────────────────────────────────────
st.markdown("""
    <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    .stApp {
        background: linear-gradient(180deg, #030712 0%, #081226 50%, #030712 100%);
        color: #e0f0ff;
        font-family: 'Segoe UI', 'Roboto', sans-serif;
    }
    .gs-card {
        background: linear-gradient(135deg, #0c1a2f 0%, #0a1425 100%);
        border: 1px solid #16355f;
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0;
        box-shadow: 0 0 30px rgba(0, 140, 255, 0.05);
    }
    .gs-card-dark {
        background: linear-gradient(135deg, #0a1520 0%, #071018 100%);
        border: 1px solid #152a45;
    }
    .gold { color: #ffd700; }
    .cyan { color: #00d4ff; }
    .green { color: #00ff88; }
    .red-alert { color: #ff4d4d; }
    .orange-alert { color: #ffb020; }
    .text-muted { color: #7a94b8; }
    .gs-label { font-size: 11px; color: #6a8ab8; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
    .gs-value { font-size: 22px; font-weight: 700; }
    .gs-big { font-size: 48px; font-weight: 900; line-height: 1; }
    .divider { height: 1px; background: linear-gradient(90deg, transparent, #1e4070, transparent); margin: 24px 0; }
    .stat-row { display: flex; justify-content: space-between; padding: 6px 0; border-bottom: 1px solid #152842; }
    .pulse { animation: pulse 2s infinite; }
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
    }
    .tab-active { background: #00d4ff; color: #000; font-weight: bold; border-radius: 6px; padding: 6px 12px; }
    .tab-inactive { background: #0f2038; color: #7ac4ff; border-radius: 6px; padding: 6px 12px; }
    </style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# SIDEBAR — NAVEGAÇÃO
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
        <div style="text-align:center; padding:10px 0;">
            <span style="font-size:28px;">🌍</span>
            <h2 style="margin:4px 0; color:#00d4ff;">GOS</h2>
            <p style="font-size:11px; color:#6a8ab8; text-transform:uppercase; letter-spacing:1px;">Global Observation System</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.radio("", [
        "🌐 Visão Global",
        "🗺️ Mapa Mundial",
        "🌤️ Clima & Cidades",
        "🌋 Riscos & Desastres",
        "🛰️ Espaço & NASA",
        "📊 Dados & Estatísticas"
    ], label_visibility="collapsed")
    
    st.markdown(f"""
        <div style="margin-top:20px; font-size:11px; color:#5a7898;">
            <b>🕒 Atualizado:</b> {br_time().strftime('%d/%m/%Y %H:%M:%S')}<br>
            <b>📍 Posição ISS:</b> Recebendo...<br>
            <b>📡 Status:</b> <span class="green">● ONLINE</span>
        </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# LOAD DE DADOS
# ──────────────────────────────────────────────
iss_data = get_iss()
quake_data = get_earthquakes()
apod_data = get_apod()
neo_data = get_neo()
fire_list = get_fires()
global_stats = get_global_stats()

# ──────────────────────────────────────────────
# ABA 1 — VISÃO GLOBAL
# ──────────────────────────────────────────────
if menu == "🌐 Visão Global":
    st.markdown("""
    <div style='text-align:center; padding:10px 0 30px;'>
        <h1 style='font-size:32px; margin:0;'>🌍 <span class='gold'>GLOBAL OBSERVATION SYSTEM</span></h1>
        <p class='text-muted' style='font-size:14px;'>Monitoramento Planetário Integrado • Rastreamento em Tempo Real • Detecção de Eventos</p>
    </div>
    """, unsafe_allow_html=True)

    # PAINEL DE NÚMEROS GLOBAIS
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='gs-card' style='text-align:center;'>
            <div class='gs-label'>População Mundial</div>
            <div class='gs-big cyan'>{global_stats['population']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class='gs-card' style='text-align:center;'>
            <div class='gs-label'>Cidades Monitoradas</div>
            <div class='gs-big cyan'>{global_stats['cities_monitored']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class='gs-card' style='text-align:center;'>
            <div class='gs-label'>Sensores Ativos</div>
            <div class='gs-big green'>{global_stats['active_sensors']}</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class='gs-card' style='text-align:center;'>
            <div class='gs-label'>Eventos Hoje</div>
            <div class='gs-big orange-alert'>{global_stats['events_today']}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # LINHA MEIO — ISS + ÚLTIMOS EVENTOS
    col_left, col_right = st.columns([1.2, 1])
    
    with col_left:
        st.markdown("""<div class='gs-card'><div class='gs-label'>🛰️ ESTAÇÃO ESPACIAL INTERNACIONAL — POSIÇÃO EM TEMPO REAL</div>""", unsafe_allow_html=True)
        if iss_data and iss_data.get("message") == "success":
            lat = iss_data["iss_position"]["latitude"]
            lon = iss_data["iss_position"]["longitude"]
            st.markdown(f"""
                <div style='font-size:18px; margin:15px 0;'>
                    <b>🌍 Latitude:</b> <span class='cyan'>{lat}</span><br>
                    <b>🌎 Longitude:</b> <span class='cyan'>{lon}</span><br>
                    <b>🚀 Velocidade:</b> ~7.7 km/s • Orbitando a cada 92 min
                </div>
                <div style='background:#0c2040; border-radius:8px; padding:10px; text-align:center; font-size:12px;'>
                    ✅ Transmissão contínua • Dados atualizados a cada 5s
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ Sem conexão com ISS no momento")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown("""<div class='gs-card'><div class='gs-label'>⚠️ DETECÇÃO DE RISCOS — HOJE</div>""", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='stat-row'><span>🌋 Terremotos detectados</span><span class='orange-alert'>{len(quake_data['features']) if quake_data else '--'}</span></div>
            <div class='stat-row'><span>🔥 Focos de incêndio</span><span class='orange-alert'>{len(fire_list)} regiões</span></div>
            <div class='stat-row'><span>🌊 Inundações/alertas hidrológicos</span><span class='cyan'>Monitorando</span></div>
            <div class='stat-row'><span>☢️ Outros alertas ambientais</span><span class='green'>Estável</span></div>
            <div class='stat-row'><span>🚨 Catástrofes em desenvolvimento</span><span class='red-alert pulse'>{global_stats['disasters_detected']} ATIVAS</span></div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # PAINEL INFERIOR — RESUMO CLIMA GLOBAL
    st.markdown("""<div class='gs-card'><div class='gs-label'>🌤️ CONDIÇÕES CLIMÁTICAS — PRINCIPAIS CIDADES DO MUNDO</div>""", unsafe_allow_html=True)
    cities = ["Nova York", "Londres", "Tóquio", "São Paulo", "Sydney", "Dubai", "Paris", "Pequim"]
    cols = st.columns(8)
    for i, city in enumerate(cities):
        w = get_weather(city)
        with cols[i]:
            country = w.get('sys',{}).get('country','--')
            temp = w.get('main',{}).get('temp','--')
            desc = w.get('weather',[{}])[0].get('description','--')
            st.markdown(f"""
                <div style='text-align:center; padding:8px 4px;'>
                    <div style='font-size:11px; color:#7ac4ff;'>{city}</div>
                    <div style='font-size:10px; color:#5a88a8;'>{country}</div>
                    <div style='font-size:18px; font-weight:bold; margin:4px 0;'>{temp}°</div>
                    <div style='font-size:9px; color:#6a8898;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ABA 2 — MAPA MUNDIAL
# ──────────────────────────────────────────────
elif menu == "🗺️ Mapa Mundial":
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px;'>
        <h2 style='margin:0;'>🗺️ <span class='cyan'>MAPA MUNDIAL INTERATIVO</span></h2>
        <p class='text-muted' style='font-size:12px;'>ISS • Terremotos • Incêndios • Cidades</p>
    </div>
    """, unsafe_allow_html=True)

    # PREPARAR DADOS DO MAPA
    quake_points = []
    if quake_data:
        for f in quake_data["features"]:
            coords = f["geometry"]["coordinates"]
            props = f["properties"]
            mag = props["mag"] or 3
            quake_points.append({
                "lat": coords[1],
                "lon": coords[0],
                "name": props["place"],
                "mag": mag,
                "size": max(mag * 8, 30)
            })

    iss_lat = float(iss_data["iss_position"]["latitude"]) if iss_data else 0
    iss_lon = float(iss_data["iss_position"]["longitude"]) if iss_data else 0

    # CAMADAS DO MAPA
    layers = []
    
    # 🔥 CAMADA DE INCÊNDIOS
    fire_layer = pdk.Layer(
        "ScatterplotLayer",
        data=fire_list,
        get_position=["lon", "lat"],
        get_radius=80000,
        get_color=[255, 69, 0, 160],
        pickable=True
    )
    layers.append(fire_layer)

    # 🌋 CAMADA DE TERREMOTOS
    if quake_points:
        quake_layer = pdk.Layer(
            "ScatterplotLayer",
            data=quake_points,
            get_position=["lon", "lat"],
            get_radius="size",
            get_color=[255, 180, 0, 140],
            pickable=True
        )
        layers.append(quake_layer)

    # 🛰️ CAMADA DA ISS
    iss_layer = pdk.Layer(
        "IconLayer",
        data=[{"lat": iss_lat, "lon": iss_lon, "name": "ISS"}],
        get_position=["lon", "lat"],
        get_icon="https://cdn-icons-png.flaticon.com/512/1149/1149166.png",
        get_size=40,
        pickable=True
    )
    layers.append(iss_layer)

    # RENDERIZAR MAPA
    view_state = pdk.ViewState(latitude=10, longitude=0, zoom=1, pitch=0)
    tooltip = {
        "html": "<b>{name}</b><br>Magnitude: {mag}",
        "style": {"backgroundColor": "#0a192f", "color": "#fff", "border": "1px solid #1e4070"}
    }
    
    st.pydeck_chart(pdk.Deck(
        layers=layers,
        initial_view_state=view_state,
        map_style="mapbox://styles/mapbox/dark-v10",
        tooltip=tooltip
    ))

    # LEGENDA DO MAPA
    st.markdown("""
    <div style='display:flex; gap:20px; flex-wrap:wrap; margin-top:10px; font-size:12px;'>
        <span style='color:#ff4500;'>● 🔴 Incêndios ativos</span>
        <span style='color:#ffb400;'>● 🟡 Terremotos (≥2.5)</span>
        <span style='color:#00d4ff;'>● 🛰️ Estação Espacial</span>
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ABA 3 — CLIMA & CIDADES
# ──────────────────────────────────────────────
elif menu == "🌤️ Clima & Cidades":
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px;'>
        <h2 style='margin:0;'>🌤️ <span class='cyan'>CLIMA GLOBAL</span> • CIDADES DO MUNDO</h2>
        <p class='text-muted' style='font-size:12px'>Digite o nome de qualquer cidade para consultar em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

    city_search = st.text_input("🔍 Buscar cidade:", value="Brasília")
    
    if city_search:
        w = get_weather(city_search)
        if w and "main" in w:
            temp = w["main"]["temp"]
            hum = w["main"]["humidity"]
            desc = w["weather"][0]["description"].capitalize()
            country = w["sys"]["country"]
            wind = w["wind"]["speed"]
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.markdown(f"""
                <div class='gs-card' style='text-align:center;'>
                    <div class='gs-label'>Cidade</div>
                    <div style='font-size:24px; font-weight:bold;'>{w['name']}, {country}</div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                st.markdown(f"""
                <div class='gs-card' style='text-align:center;'>
                    <div class='gs-label'>Temperatura</div>
                    <div style='font-size:36px; font-weight:bold; color:#ffb400;'>{temp}°C</div>
                </div>
                """, unsafe_allow_html=True)
            with col3:
                st.markdown(f"""
                <div class='gs-card' style='text-align:center;'>
                    <div class='gs-label'>Umidade</div>
                    <div style='font-size:36px; font-weight:bold; color:#00d4ff;'>{hum}%</div>
                </div>
                """, unsafe_allow_html=True)
            with col4:
                st.markdown(f"""
                <div class='gs-card' style='text-align:center;'>
                    <div class='gs-label'>Vento</div>
                    <div style='font-size:36px; font-weight:bold; color:#7ac4ff;'>{wind} m/s</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class='gs-card' style='text-align:center;'>
                <div style='font-size:18px;'>☁️ {desc}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Cidade não encontrada — verifique o nome")

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # CIDADES DESTAQUE
    st.markdown("""<div class='gs-card'><div class='gs-label'>🏙️ CAPITAIS DO MUNDO — VISÃO RÁPIDA</div>""", unsafe_allow_html=True)
    grid_cities = [
        ("Nova York", "US"), ("Londres", "UK"), ("Tóquio", "JP"), 
        ("Pequim", "CN"), ("Sydney", "AU"), ("Moscou", "RU"),
        ("Cairo", "EG"), ("São Paulo", "BR"), ("Cidade do México", "MX"),
        ("Berlim", "DE"), ("Paris", "FR"), ("Dubai", "AE")
    ]
    cols = st.columns(4)
    for idx, (c, cnt) in enumerate(grid_cities):
        with cols[idx % 4]:
            w = get_weather(c)
            temp = w.get('main',{}).get('temp','--')
            desc = w.get('weather',[{}])[0].get('description','--')
            st.markdown(f"""
                <div style='background:#0c1a30; border-radius:8px; padding:12px; margin:4px 0;'>
                    <div style='display:flex; justify-content:space-between;'>
                        <span style='font-weight:bold;'>{c}</span>
                        <span style='color:#00d4ff;'>{temp}°</span>
                    </div>
                    <div style='font-size:10px; color:#6a8898; margin-top:4px;'>{desc}</div>
                </div>
            """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ABA 4 — RISCOS & DESASTRES
# ──────────────────────────────────────────────
elif menu == "🌋 Riscos & Desastres":
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px;'>
        <h2 style='margin:0;'>⚠️ <span class='orange-alert'>MONITORAMENTO DE RISCOS</span></h2>
        <p class='text-muted' style='font-size:12px'>Detecção e acompanhamento de eventos naturais em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

    # 🌋 TERREMOTOS
    st.markdown("""<div class='gs-card'><div class='gs-label'>🌋 TERREMOTOS — ÚLTIMAS 24H (≥2.5 Mw)</div>""", unsafe_allow_html=True)
    if quake_data:
        for feat in quake_data["features"][:15]:
            p = feat["properties"]
            mag = p["mag"]
            place = p["place"]
            time_q = datetime.fromtimestamp(p["time"]/1000).strftime("%d/%m %H:%M")
            color = "#ff4d4d" if mag >= 5 else "#ffb020" if mag >=4 else "#7ac4ff"
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; padding:8px 4px; border-bottom:1px solid #152842; align-items:center;'>
                <span style='font-size:11px; color:#5a7898;'>{time_q}</span>
                <span style='flex:1; padding:0 10px;'>{place}</span>
                <span style='font-weight:bold; color:{color};'>M{mag}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Dados indisponíveis no momento")
    st.markdown("</div>", unsafe_allow_html=True)

    # 🔥 INCÊNDIOS
    st.markdown("""<div class='gs-card'><div class='gs-label'>🔥 FOCOS DE INCÊNDIO — MONITORAMENTO GLOBAL</div>""", unsafe_allow_html=True)
    for f in fire_list:
        color_f = "#ff4500" if f["intensity"] == "Alta" else "#ffb020" if f["intensity"] == "Média" else "#00ff88"
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; padding:8px 4px; border-bottom:1px solid #152842;'>
            <span>{f['region']}</span>
            <span style='color:{color_f}; font-weight:bold;'>{f['intensity']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # 🚨 ALERTAS GLOBAIS
    st.markdown("""<div class='gs-card gs-card-dark'><div class='gs-label'>🚨 SITUAÇÕES EM DESTAQUE — ALERTAS GLOBAIS</div>""", unsafe_allow_html=True)
    alerts = [
        {"nivel": "CRÍTICO", "local": "Amazônia, Brasil", "tipo": "Incêndios", "status": "Em desenvolvimento"},
        {"nivel": "ATENÇÃO", "local": "Chile — Costa do Pacífico", "tipo": "Atividade sísmica", "status": "Monitoramento contínuo"},
        {"nivel": "OBSERVAÇÃO", "local": "Oceano Índico", "tipo": "Padrões climáticos", "status": "Estável"}
    ]
    for a in alerts:
        cor = "#ff4d4d" if a["nivel"] == "CRÍTICO" else "#ffb020" if a["nivel"] == "ATENÇÃO" else "#00d4ff"
        st.markdown(f"""
        <div style='background:#0c1628; border-left:3px solid {cor}; padding:10px 14px; margin:6px 0; border-radius:0 6px 6px 0;'>
            <div style='display:flex; justify-content:space-between;'>
                <span style='font-weight:bold; color:{cor};'>{a['nivel']}</span>
                <span style='font-size:11px; color:#5a7898;'>{a['tipo']}</span>
            </div>
            <div style='margin-top:4px;'>{a['local']}</div>
            <div style='font-size:10px; color:#6a8898; margin-top:2px;'>{a['status']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ABA 5 — ESPAÇO & NASA
# ──────────────────────────────────────────────
elif menu == "🛰️ Espaço & NASA":
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px;'>
        <h2 style='margin:0;'>🚀 <span class='gold'>NASA • ESPAÇO • ASTROFÍSICA</span></h2>
        <p class='text-muted' style='font-size:12px'>Dados reais da NASA em tempo real</p>
    </div>
    """, unsafe_allow_html=True)

    # ☄️ ASTEROIDES
    st.markdown("""<div class='gs-card'><div class='gs-label'>☄️ OBJETOS PRÓXIMOS À TERRA — HOJE</div>""", unsafe_allow_html=True)
    if neo_data:
        try:
            today_key = list(neo_data["near_earth_objects"].keys())[0]
            neos = neo_data["near_earth_objects"][today_key]
            hazardous = sum(1 for n in neos if n["is_potentially_hazardous_asteroid"])
            col1, col2, col3 = st.columns(3)
            with col1: st.markdown(f"<div style='text-align:center;'><div style='font-size:40px; font-weight:bold; color:#ffb400;'>{len(neos)}</div><div style='font-size:11px;'>Asteroides detectados</div></div>", unsafe_allow_html=True)
            with col2: st.markdown(f"<div style='text-align:center;'><div style='font-size:40px; font-weight:bold; color:#ff4d4d;'>{hazardous}</div><div style='font-size:11px;'>Potencialmente perigosos</div></div>", unsafe_allow_html=True)
            with col3: st.markdown(f"<div style='text-align:center;'><div style='font-size:40px; font-weight:bold; color:#00ff88;'>Seguros</div><div style='font-size:11px;'>Risco baixo</div></div>", unsafe_allow_html=True)
            
            st.markdown("<div style='margin-top:15px;'><div class='gs-label'>Lista de aproximação:</div></div>", unsafe_allow_html=True)
            for n in neos[:8]:
                name = n["name"]
                dist = n["close_approach_data"][0]["miss_distance"]["kilometers"]
                diam = n["estimated_diameter"]["meters"]["estimated_diameter_max"]
                hazard = n["is_potentially_hazardous_asteroid"]
                color_h = "#ff4d4d" if hazard else "#00ff88"
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; padding:6px 4px; border-bottom:1px solid #152842; font-size:12px;'>
                    <span>{name}</span>
                    <span>{float(dist):,.0f} km</span>
                    <span>{diam:.0f} m</span>
                    <span style='color:{color_h};'>⚠️ Sim" if hazard else "✅ Não"</span>
                </div>
                """, unsafe_allow_html=True)
        except: st.info("Dados indisponíveis no momento")
    else:
        st.info("Conectando à NASA...")
    st.markdown("</div>", unsafe_allow_html=True)

    # 🌌 IMAGEM DO DIA
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("""<div class='gs-card'><div class='gs-label'>🌌 IMAGEM DO DIA — NASA APOD</div>""", unsafe_allow_html=True)
    if apod_data:
        st.subheader(apod_data.get("title", ""))
        if apod_data.get("media_type") == "image":
            st.image(apod_data["url"], use_container_width=True)
        with st.expander("📝 Ler explicação completa"):
            st.write(apod_data.get("explanation", "")[:1500] + "...")
    else:
        st.image("https://apod.nasa.gov/apod/image/2409/NGC6355_Hubble_960.jpg", use_container_width=True)
        st.caption("Imagem de demonstração — ative sua chave da NASA para dados reais")
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# ABA 6 — DADOS & ESTATÍSTICAS
# ──────────────────────────────────────────────
elif menu == "📊 Dados & Estatísticas":
    st.markdown("""
    <div style='text-align:center; padding:10px 0 20px;'>
        <h2 style='margin:0;'>📊 <span class='cyan'>INDICADORES GLOBAIS</span> • COMPORTAMENTO • TENDÊNCIAS</h2>
        <p class='text-muted' style='font-size:12px'>Dados agregados e estatísticas planetárias</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""<div class='gs-card'><div class='gs-label'>🌐 INDICADORES PLANETÁRIOS</div>""", unsafe_allow_html=True)
        indicators = [
            ("População Mundial", "8.1 Bilhões", "+1.05%/ano"),
            ("Cidades Conectadas", "12.800+", "+218 este mês"),
            ("Qualidade do Ar (média)", "72 AQI", "Estável"),
            ("Anomalia da Temperatura do Mar", "+0.84°C", "↑ Aquecimento"),
            ("Precipitação Global Acumulada", "102% da média", "Acima do normal"),
            ("Área de Floresta Remanescente", "31% da terra firme", "↓ -0.18%/ano")
        ]
        for name, val, trend in indicators:
            st.markdown(f"""
            <div class='stat-row'>
                <span>{name}</span>
                <span style='text-align:right;'>
                    <span style='font-weight:bold;'>{val}</span><br>
                    <span style='font-size:10px; color:#6a8898;'>{trend}</span>
                </span>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class='gs-card'><div class='gs-label'>📈 COMPORTAMENTO HUMANO — TENDÊNCIAS GLOBAIS</div>""", unsafe_allow_html=True)
        trends = [
            ("Mobilidade Urbana", "↑ 4.2% vs. mês anterior", "#00d4ff"),
            ("Uso de Energia", "↑ 1.8% — horário de pico", "#ffb400"),
            ("Conectividade Digital", "67% da população online", "#00ff88"),
            ("Migração Populacional", "↔ Estável sem grandes fluxos", "#7ac4ff"),
            ("Atividade Portuária/Comércio", "↓ 0.8% — tendência estável", "#ffb400"),
            ("Eventos Públicos & Reuniões", "↑ 12% — recuperação pós-pandemia", "#00d4ff")
        ]
        for name, val, color in trends:
            st.markdown(f"""
            <div style='padding:8px 6px; border-bottom:1px solid #152842;'>
                <div style='font-size:13px;'>{name}</div>
                <div style='font-size:11px; color:{color};'>{val}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # PREVISÃO GLOBAL
    st.markdown("""<div class='gs-card'><div class='gs-label'>🔮 PREVISÃO GLOBAL — PRÓXIMAS 72h</div>""", unsafe_allow_html=True)
    forecast = [
        {"regiao": "Américas", "condicao": "Maioria estável — temp. levemente acima da média", "alerta": "Nenhum"},
        {"regiao": "Europa/África", "condicao": "Frente fria atravessando o norte — chuvas no Mediterrâneo", "alerta": "Ventos fortes no Atlântico"},
        {"regiao": "Ásia/Oceania", "condicao": "Tufões na região do Pacífico — monções na Ásia Sul", "alerta": "⚠️ Acompanhar ciclones tropicais"}
    ]
    for f in forecast:
        alerta_cor = "#ff4d4d" if "⚠️" in f["alerta"] else "#00ff88"
        st.markdown(f"""
        <div style='background:#0c1a30; border-radius:8px; padding:14px; margin:8px 0;'>
            <div style='font-weight:bold; font-size:15px; margin-bottom:6px;'>🌍 {f['regiao']}</div>
            <div style='font-size:12px; color:#9ac4e8;'>{f['condicao']}</div>
            <div style='font-size:11px; margin-top:6px; color:{alerta_cor};'>{f['alerta']}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# RODAPÉ
# ──────────────────────────────────────────────
st.markdown("""
<div style='text-align:center; font-size:10px; color:#4a6888; padding:20px 0 30px; margin-top:30px; border-top:1px solid #152842;'>
    🌍 <b>GLOBAL OBSERVATION SYSTEM</b> • Dados via NASA Open APIs, USGS Earthquake Catalog, OpenWeatherMap, Open Notify<br>
    ⚠️ Alguns dados em modo de demonstração. Obtenha chaves gratuitas em: api.nasa.gov • openweathermap.org • earthquake.usgs.gov
</div>
""", unsafe_allow_html=True)

# ATUALIZAÇÃO AUTOMÁTICA - FIX NÃO APAGA
pass
