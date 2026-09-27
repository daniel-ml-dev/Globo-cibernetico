import streamlit as st, json
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="FASHIONWOMEN LIBRA GLOBAL")
st.markdown("<style>.stButton>button{background:linear-gradient(90deg,#FF00FF,#00FFFF);color:white;font-weight:900;border-radius:12px;border:none;width:100%}</style>", unsafe_allow_html=True)

if "cart" not in st.session_state:
    st.session_state.cart=[]
if "sel" not in st.session_state:
    st.session_state.sel=None

# TODAS AS CIDADES E PAISES QUE PAGAM EM LIBRA £ - MERCADO TOTAL
cidades_libra = [
    # INGLATERRA - TOP VENDAS
    {"city":"Londres","lat":51.5074,"lon":-0.1278,"pais":"UK","pop":9500000,"potencial":100},
    {"city":"Birmingham","lat":52.4862,"lon":-1.8904,"pais":"UK","pop":1140000,"potencial":85},
    {"city":"Manchester","lat":53.4808,"lon":-2.2426,"pais":"UK","pop":547000,"potencial":90},
    {"city":"Leeds","lat":53.8008,"lon":-1.5491,"pais":"UK","pop":789000,"potencial":80},
    {"city":"Liverpool","lat":53.4084,"lon":-2.9916,"pais":"UK","pop":498000,"potencial":82},
    {"city":"Bristol","lat":51.4545,"lon":-2.5879,"pais":"UK","pop":467000,"potencial":78},
    {"city":"Sheffield","lat":53.3811,"lon":-1.4701,"pais":"UK","pop":584000,"potencial":75},
    {"city":"Newcastle","lat":54.9783,"lon":-1.6178,"pais":"UK","pop":300000,"potencial":77},
    {"city":"Nottingham","lat":52.9548,"lon":-1.1581,"pais":"UK","pop":321000,"potencial":74},
    {"city":"Southampton","lat":50.9097,"lon":-1.4044,"pais":"UK","pop":271000,"potencial":72},
    {"city":"Leicester","lat":52.6369,"lon":-1.1398,"pais":"UK","pop":355000,"potencial":73},
    {"city":"Coventry","lat":52.4068,"lon":-1.5197,"pais":"UK","pop":371000,"potencial":70},
    # ESCOCIA - LIBRA ESCOCESA MAS PAGA EM £
    {"city":"Glasgow","lat":55.8642,"lon":-4.2518,"pais":"Scotland","pop":635000,"potencial":88},
    {"city":"Edinburgh","lat":55.9533,"lon":-3.1883,"pais":"Scotland","pop":524000,"potencial":85},
    {"city":"Aberdeen","lat":57.1497,"lon":-2.0943,"pais":"Scotland","pop":200000,"potencial":68},
    {"city":"Dundee","lat":56.4620,"lon":-2.9707,"pais":"Scotland","pop":148000,"potencial":65},
    # PAIS DE GALES
    {"city":"Cardiff","lat":51.4816,"lon":-3.1791,"pais":"Wales","pop":362000,"potencial":76},
    {"city":"Swansea","lat":51.6214,"lon":-3.9436,"pais":"Wales","pop":246000,"potencial":70},
    # IRLANDA DO NORTE
    {"city":"Belfast","lat":54.5973,"lon":-5.9301,"pais":"N.Ireland","pop":343000,"potencial":79},
    {"city":"Derry","lat":54.9970,"lon":-7.3092,"pais":"N.Ireland","pop":85000,"potencial":60},
    # TERRITORIOS BRITANICOS QUE USAM LIBRA
    {"city":"St Helier - Jersey","lat":49.1867,"lon":-2.1058,"pais":"Jersey","pop":107000,"potencial":65},
    {"city":"St Peter Port - Guernsey","lat":49.4656,"lon":-2.5853,"pais":"Guernsey","pop":63000,"potencial":60},
    {"city":"Douglas - Isle of Man","lat":54.1523,"lon":-4.4861,"pais":"Isle of Man","pop":83000,"potencial":62},
    {"city":"Gibraltar","lat":36.1408,"lon":-5.3536,"pais":"Gibraltar","pop":34000,"potencial":70},
    {"city":"Hamilton - Bermuda","lat":32.2948,"lon":-64.7839,"pais":"Bermuda","pop":64000,"potencial":75},
    {"city":"Stanley - Falkland","lat":-51.6977,"lon":-57.8517,"pais":"Falkland","pop":3500,"potencial":40},
    {"city":"George Town - Cayman","lat":19.3133,"lon":-81.2546,"pais":"Cayman","pop":65000,"potencial":80},
]

produtos_base=[
    {"nome":"Kit 5 Calcinhas","preco":24.99,"cat":"Intimas","viral":100},
    {"nome":"Colar Dourado","preco":19.99,"cat":"Joias","viral":98},
    {"nome":"Vestido Floral","preco":39.99,"cat":"Roupas","viral":99},
    {"nome":"Bota Tratorada","preco":69.99,"cat":"Sapatos","viral":94},
    {"nome":"Bolsa Tote","preco":39.99,"cat":"Bolsas","viral":92},
    {"nome":"Brinco Argola","preco":12.99,"cat":"Joias","viral":95},
]

# GERAR TODAS COMBINACOES CIDADE x PRODUTO = PREVISAO MAXIMA
lista_completa=[]
for cid in cidades_libra:
    for prod in produtos_base:
        prev = int(cid["potencial"] * prod["viral"] / 10 + cid["pop"]/100000)
        lista_completa.append({
            "id": len(lista_completa)+1,
            "city": cid["city"], "pais": cid["pais"],
            "lat": cid["lat"], "lon": cid["lon"],
            "nome": prod["nome"], "preco": prod["preco"], "cat": prod["cat"],
            "viral": prod["viral"], "potencial": cid["potencial"], "prev_venda": prev,
            "pop": cid["pop"]
        })

with st.sidebar:
    st.header("LIBRA GLOBAL MAP")
    st.metric("Cidades £", len(cidades_libra))
    st.metric("Mercado Total", f"{sum(c['pop'] for c in cidades_libra)/1000000:.1f}M pessoas")
    st.metric("Previsao Total", f"{sum(x['prev_venda'] for x in lista_completa)} vendas/7d")

    pais_filtro=st.selectbox("Filtrar Pais £", ["Todos","UK","Scotland","Wales","N.Ireland","Jersey","Guernsey","Isle of Man","Gibraltar","Bermuda"])
    if pais_filtro=="Todos":
        filtrada=lista_completa
    else:
        filtrada=[x for x in lista_completa if x["pais"]==pais_filtro]

    cat_filtro=st.selectbox("Categoria", ["Todas","Intimas","Joias","Roupas","Sapatos","Bolsas"])
    if cat_filtro!="Todas":
        filtrada=[x for x in filtrada if x["cat"]==cat_filtro]

    st.write(f"{len(filtrada)} oportunidades")
    for p in sorted(filtrada, key=lambda x: x["prev_venda"], reverse=True)[:10]:
        if st.button(f"{p['city'][:12]} - {p['nome'][:12]} {p['prev_venda']}vd", key=str(p["id"])):
            st.session_state.sel=p["id"]
            st.session_state.cart.append(p)

# METRICAS TOPO
c1,c2,c3,c4=st.columns(4)
c1.metric("Faturamento Previsto 7d", f"£{sum(x['prev_venda']*x['preco'] for x in filtrada):,.0f}", "LIBRA")
c2.metric("Cidade Ouro", sorted(cidades_libra, key=lambda x: x["potencial"], reverse=True)[0]["city"])
c3.metric("Produto Ouro", "Kit Calcinhas", "100% viral")
c4.metric("Paises £", "15 territorios")

if st.session_state.sel:
    sel_item=[x for x in lista_completa if x["id"]==st.session_state.sel][0]
    st.success(f"FOCO: {sel_item['nome']} em {sel_item['city']} ({sel_item['pais']}) - Prev: {sel_item['prev_venda']} vendas - £{sel_item['prev_venda']*sel_item['preco']:.0f}")
    globo_dados=[sel_item]
    lat0=sel_item["lat"]; lon0=sel_item["lon"]
else:
    # Top 30 cidades por potencial pro globo nao pesar
    top_cidades=sorted(filtrada, key=lambda x: x["prev_venda"], reverse=True)[:30]
    globo_dados=top_cidades
    lat0=51.5; lon0=-2.0

pontos=[]
for p in globo_dados:
    pontos.append({"lat":p["lat"],"lng":p["lon"],"name":p["nome"],"city":p["city"],"pais":p["pais"],"prev":p["prev_venda"],"size":p["potencial"]/20})

pontos_json=json.dumps(pontos)
html_code="""
<div id="globe" style="width:100%;height:650px;background:#000;border-radius:20px;border:2px solid #FF00FF"></div>
<script src="//unpkg.com/globe.gl"></script>
<script>
const data = """ + pontos_json + """;
const g = Globe()(document.getElementById('globe'))
.globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
.backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
.pointsData(data).pointLat('lat').pointLng('lng').pointAltitude(d=>d.size*0.05).pointRadius(d=>d.size*0.15).pointColor(d=> d.pais=='UK'? '#FF00FF' : '#00FFFF')
.pointLabel(d=> d.city + ' - ' + d.pais + '<br>' + d.name + '<br>Prev: ' + d.prev + ' vendas')
.atmosphereColor('#FF00FF').atmosphereAltitude(0.25);
g.controls().autoRotate=true; g.controls().autoRotateSpeed=0.5;
g.pointOfView({lat:""" + str(lat0) + """, lng:""" + str(lon0) + """, altitude:0.9},1200);
</script>
"""
components.html(html_code, height=670)

st.divider()
st.subheader("TOP 20 CIDADES QUE PAGAM EM LIBRA - ONDE VENDER MAIS")
cols=st.columns(4)
top20=sorted(filtrada, key=lambda x: x["prev_venda"], reverse=True)[:20]
for i,p in enumerate(top20):
    with cols[i%4]:
        st.container(border=True)
        st.write(f"**{p['city']}** - {p['pais']}")
        st.caption(f"{p['nome']} | £{p['preco']}")
        st.metric("Prev 7d", f"{p['prev_venda']} un", f"£{p['prev_venda']*p['preco']:.0f}")
        if st.button("VENDER AQUI", key="sell"+str(p["id"])):
            st.session_state.sel=p["id"]
            st.rerun()
