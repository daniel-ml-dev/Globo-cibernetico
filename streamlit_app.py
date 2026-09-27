import streamlit as st, json

st.set_page_config(layout="wide", page_title="FASHIONWOMEN FIX")
st.markdown("<style>.stButton>button{background:linear-gradient(90deg,#FF00FF,#00FFFF);color:white;font-weight:900;border-radius:12px;border:none;width:100%}</style>", unsafe_allow_html=True)

if 'cart' not in st.session_state: st.session_state.cart=[]
if 'sel' not in st.session_state: st.session_state.sel=None

produtos = [
    {"id":1,"cat":"Joias","prod":"Colar Dourado","price":19.99,"icon":"💍","lat":51.5074,"lon":-0.1278,"city":"Londres","viral":98},
    {"id":2,"cat":"Joias","prod":"Brinco Argola","price":12.99,"icon":"✨","lat":53.4808,"lon":-2.2426,"city":"Manchester","viral":95},
    {"id":3,"cat":"Roupas","prod":"Vestido Floral","price":39.99,"icon":"👗","lat":51.5074,"lon":-0.1278,"city":"Londres","viral":99},
    {"id":4,"cat":"Roupas","prod":"Conjunto Cropped","price":45.99,"icon":"💃","lat":55.95,"lon":-3.18,"city":"Edinburgh","viral":97},
    {"id":5,"cat":"Intimas","prod":"Kit 5 Calcinhas","price":24.99,"icon":"🩷","lat":51.5074,"lon":-0.1278,"city":"Londres","viral":100},
    {"id":6,"cat":"Intimas","prod":"Sutia Confort","price":29.99,"icon":"👙","lat":53.80,"lon":-1.54,"city":"Leeds","viral":96},
    {"id":7,"cat":"Sapatos","prod":"Bota Tratorada","price":69.99,"icon":"👢","lat":52.48,"lon":-1.89,"city":"Birmingham","viral":94},
    {"id":8,"cat":"Sapatos","prod":"Tenis Chunky","price":54.99,"icon":"👟","lat":53.40,"lon":-2.99,"city":"Liverpool","viral":93},
    {"id":9,"cat":"Bolsas","prod":"Bolsa Tote","price":39.99,"icon":"👜","lat":51.45,"lon":-2.58,"city":"Bristol","viral":92},
    {"id":10,"cat":"Beleza","prod":"Kit Gloss + Brinco","price":18.99,"icon":"💄","lat":51.5074,"lon":-0.1278,"city":"Londres","viral":99},
]

with st.sidebar:
    st.title("LOJA GLOBO")
    if st.session_state.cart:
        total = sum(p["price"] for p in st.session_state.cart)
        st.metric("Carrinho", f"{len(st.session_state.cart)} itens - £{total:.2f}")
        for p in st.session_state.cart:
            st.write(f"{p['icon']} {p['prod']} £{p['price']}")
        st.link_button("FINALIZAR NA WIX", "https://fashionwomen.com.br/cart", use_container_width=True)
        if st.button("Limpar Carrinho"):
            st.session_state.cart=[]; st.rerun()
        st.divider()
    categoria = st.selectbox("Categoria", ["Todas","Joias","Roupas","Intimas","Sapatos","Bolsas"])
    lista = produtos if categoria=="Todas" else [p for p in produtos if p["cat"]==categoria]
    for p in lista:
        with st.container(border=True):
            st.write(f"**{p['icon']} {p['prod']}**")
            st.caption(f"£{p['price']} | {p['city']} | {p['viral']}% VIRAL")
            c1,c2 = st.columns(2)
            with c1:
                if st.button("GLOBO", key=f"g{p['id']}"):
                    st.session_state.sel=p["id"]; st.rerun()
            with c2:
                if st.button("ESCOLHER", key=f"b{p['id']}"):
                    st.session_state.cart.append(p)
                    st.session_state.sel=p["id"]
                    st.rerun()

c1,c2,c3=st.columns(3)
c1.metric("Vendas UK Hoje","£0,00","INICIANDO")
c2.metric("Previsao 7 dias","£56,280","IA")
c3.metric("Cidade Ouro","Londres","60% vendas")

if st.session_state.sel:
    globo_lista = [p for p in produtos if p["id"]==st.session_state.sel]
    sel_prod = globo_lista[0]
    st.success(f"SELECIONADO: {sel_prod['icon']} {sel_prod['prod']} em {sel_prod['city']}")
else:
    globo_lista = lista
    st.info("Clique em GLOBO ou ESCOLHER na barra lateral")

cores = {"Joias":"#FFD700","Roupas":"#FF00FF","Intimas":"#FF1493","Sapatos":"#00FFFF","Bolsas":"#FFA500","Beleza":"#FF69B4"}
pontos = []
for p in globo_lista:
    pontos.append({
        "lat": p["lat"],
        "lng": p["lon"],
        "prod": p["prod"],
        "city": p["city"],
        "price": p["price"],
        "icon": p["icon"],
        "size": 2.5 if st.session_state.sel==p["id"] else 0.6,
        "color": "#FFFFFF" if st.session_state.sel==p["id"] else cores.get(p["cat"],"#FF00FF")
    })

pontos_json = json.dumps(pontos)
lat0 = globo_lista[0]["lat"] if globo_lista else 51.5
lon0 = globo_lista[0]["lon"] if globo_lista else -2.0

import streamlit.components.v1 as components
html = f"""
<div id="globe" style="width:100%;height:620px;background:#000;border-radius:20px;border:2px solid #FF00FF"></div>
<script src="//unpkg.com/globe.gl"></script>
<script>
const data = {pontos_json};
const g = Globe()(document.getElementById('globe'))
.globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg')
.backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
.pointsData(data).pointLat('lat').pointLng('lng')
.pointAltitude(d=>d.size*0.2).pointRadius(d=>d.size*0.25).pointColor('color')
.pointLabel(d=>`<b>${{d.icon}} ${{d.prod}} £${{d.price}}<br>${{d.city}} UK</b>`)
.atmosphereColor('#FF00FF').atmosphereAltitude(0.25);
g.controls().autoRotate=true; g.controls().autoRotateSpeed=0.7;
g.pointOfView({{lat:{lat0},lng:{lon0},altitude:0.8}},1500);
</script>
"""
components.html(html, height=640)

st.divider()
st.subheader("VITRINE CIBERNETICA")
cols=st.columns(5)
for i,p in enumerate(lista):
    with cols[i%5]:
        with st.container(border=True):
            icon = p["icon"]
            prod_name = p["prod"]
            price = p["price"]
            st.markdown(f"<center style='font-size:40px'>{icon}</center>", unsafe_allow_html=True)
            st.write(f"**{prod_name}**")
            st.write(f"£{price}")
            if st.button("ESCOLHER PRODUTO", key=f"v{p['id']}", use_container_width=True):
                st.session_state.cart.append(p); st.session_state.sel=p["id"]; st.rerun()
