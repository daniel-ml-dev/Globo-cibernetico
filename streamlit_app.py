import streamlit as st, json
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="LIBRA GLOBAL V7")
st.markdown("<style>.stButton>button{background:linear-gradient(90deg,#FF00FF,#00FFFF);color:white;font-weight:900;border-radius:12px;width:100%}</style>", unsafe_allow_html=True)

if "cart" not in st.session_state: st.session_state.cart=[]
if "sel" not in st.session_state: st.session_state.sel=None

cidades_libra = [
    {"city":"Londres","lat":51.5074,"lon":-0.1278,"pais":"UK","pot":100},
    {"city":"Birmingham","lat":52.4862,"lon":-1.8904,"pais":"UK","pot":85},
    {"city":"Manchester","lat":53.4808,"lon":-2.2426,"pais":"UK","pot":90},
    {"city":"Leeds","lat":53.8008,"lon":-1.5491,"pais":"UK","pot":80},
    {"city":"Liverpool","lat":53.4084,"lon":-2.9916,"pais":"UK","pot":82},
    {"city":"Bristol","lat":51.4545,"lon":-2.5879,"pais":"UK","pot":78},
    {"city":"Sheffield","lat":53.3811,"lon":-1.4701,"pais":"UK","pot":75},
    {"city":"Glasgow","lat":55.8642,"lon":-4.2518,"pais":"Scotland","pot":88},
    {"city":"Edinburgh","lat":55.9533,"lon":-3.1883,"pais":"Scotland","pot":85},
    {"city":"Cardiff","lat":51.4816,"lon":-3.1791,"pais":"Wales","pot":76},
    {"city":"Belfast","lat":54.5973,"lon":-5.9301,"pais":"N.Ireland","pot":79},
    {"city":"Jersey","lat":49.2144,"lon":-2.1318,"pais":"Jersey","pot":65},
    {"city":"Guernsey","lat":49.4656,"lon":-2.5853,"pais":"Guernsey","pot":60},
    {"city":"Isle of Man","lat":54.1523,"lon":-4.4861,"pais":"Isle of Man","pot":62},
    {"city":"Gibraltar","lat":36.1408,"lon":-5.3536,"pais":"Gibraltar","pot":70},
    {"city":"Bermuda","lat":32.2948,"lon":-64.7839,"pais":"Bermuda","pot":75},
    {"city":"Cayman","lat":19.3133,"lon":-81.2546,"pais":"Cayman","pot":80},
    {"city":"Newcastle","lat":54.9783,"lon":-1.6178,"pais":"UK","pot":77},
    {"city":"Nottingham","lat":52.9548,"lon":-1.1581,"pais":"UK","pot":74},
    {"city":"Southampton","lat":50.9097,"lon":-1.4044,"pais":"UK","pot":72},
    {"city":"Aberdeen","lat":57.1497,"lon":-2.0943,"pais":"Scotland","pot":68},
    {"city":"Swansea","lat":51.6214,"lon":-3.9436,"pais":"Wales","pot":70},
    {"city":"Derry","lat":54.9970,"lon":-7.3092,"pais":"N.Ireland","pot":60},
    {"city":"Leicester","lat":52.6369,"lon":-1.1398,"pais":"UK","pot":73},
    {"city":"Coventry","lat":52.4068,"lon":-1.5197,"pais":"UK","pot":70},
    {"city":"Falkland","lat":-51.6977,"lon":-57.8517,"pais":"Falkland","pot":40},
    {"city":"York","lat":53.9590,"lon":-1.0815,"pais":"UK","pot":71},
]

produtos_base=[
    {"nome":"Kit Calcinhas","preco":24.99,"viral":100},
    {"nome":"Colar Dourado","preco":19.99,"viral":98},
    {"nome":"Vestido Floral","preco":39.99,"viral":99},
]

# GERA TODAS COMBINACOES PRA CALCULO
lista=[]
for c in cidades_libra:
    for p in produtos_base:
        lista.append({"id":len(lista)+1,"city":c["city"],"pais":c["pais"],"lat":c["lat"],"lon":c["lon"],"nome":p["nome"],"preco":p["preco"],"prev":int(c["pot"]*p["viral"]/2),"pot":c["pot"]})

with st.sidebar:
    st.metric("CIDADES £", len(cidades_libra))
    st.metric("TOTAL NO GLOBO", f"{len(cidades_libra)} PONTOS")
    filtro=st.selectbox("Ver", ["TODAS 27 CIDADES","So UK","So Territorios £"])
    if filtro=="So UK": mostra=[c for c in cidades_libra if c["pais"] in ["UK","Scotland","Wales","N.Ireland"]]
    elif filtro=="So Territorios £": mostra=[c for c in cidades_libra if c["pais"] not in ["UK","Scotland","Wales","N.Ireland"]]
    else: mostra=cidades_libra

# --- AQUI ESTAVA O ERRO: AGORA MOSTRA TODAS ---
pontos=[]
for p in mostra:
    pontos.append({
        "lat":p["lat"],"lng":p["lon"],
        "city":p["city"],"pais":p["pais"],
        "size": p["pot"]/15,  # PONTO 3x MAIOR AGORA
        "color": "#FF00FF" if p["pais"] in ["UK","Scotland","Wales","N.Ireland"] else "#00FFFF",
        "label": f"{p['city']} - {p['pais']} - POT {p['pot']}%"
    })

pontos_json=json.dumps(pontos)

html_code="""
<div id="globe" style="width:100%;height:700px;background:#000;border-radius:20px;border:3px solid #FF00FF"></div>
<script src="//unpkg.com/globe.gl"></script>
<script>
const data = """ + pontos_json + """;
const g = Globe()(document.getElementById('globe'))
.globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
.backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
.pointsData(data)
.pointLat('lat').pointLng('lng')
.pointAltitude(d=>d.size*0.3)
.pointRadius(d=>d.size)
.pointColor('color')
.pointLabel(d=>d.label)
.atmosphereColor('#FF00FF').atmosphereAltitude(0.3);
g.controls().autoRotate=true; g.controls().autoRotateSpeed=0.8;
g.pointOfView({lat:51.5, lng:-20, altitude:1.5},1000);
</script>
"""
components.html(html_code, height=720)

st.divider()
st.write("### TODAS AS CIDADES QUE PAGAM EM LIBRA NO GLOBO:")
cols=st.columns(5)
for i,c in enumerate(mostra):
    with cols[i%5]:
        st.success(f"{c['city']} - {c['pais']} - {c['pot']}%")
