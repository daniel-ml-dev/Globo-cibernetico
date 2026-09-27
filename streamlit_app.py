import streamlit as st, pandas as pd, json, numpy as np
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="FASHIONWOMEN ULTIMATE FIXED")
st.markdown("<style>.stButton>button{background:linear-gradient(90deg,#FF00FF,#00FFFF);color:white;font-weight:900;border-radius:12px;border:none;width:100%;height:42px} div[data-testid='stMetric']{background:#111;border:1px solid #FF00FF;border-radius:10px;padding:10px}</style>", unsafe_allow_html=True)

if 'cart' not in st.session_state: st.session_state.cart=[]
if 'sel' not in st.session_state: st.session_state.sel=None

data = [
    {"id":1,"cat":"Joias","prod":"Colar Dourado Minimalista","price":19.99,"icon":"💍","lat":51.5074,"lon":-0.1278,"city":"Londres","stock":200,"viral":98,"wix":"https://fashionwomen.com.br"},
    {"id":2,"cat":"Joias","prod":"Brinco Argola Premium","price":12.99,"icon":"✨","lat":53.4808,"lon":-2.2426,"city":"Manchester","stock":300,"viral":95,"wix":"https://fashionwomen.com.br"},
    {"id":3,"cat":"Roupas","prod":"Vestido Floral Zara Inspira","price":39.99,"icon":"👗","lat":51.5074,"lon":-0.1278,"city":"Londres","stock":45,"viral":99,"wix":"https://fashionwomen.com.br"},
    {"id":4,"cat":"Roupas","prod":"Conjunto Cropped + Saia","price":45.99,"icon":"💃","lat":55.9533,"lon":-3.1883,"city":"Edinburgh","stock":25,"viral":97,"wix":"https://fashionwomen.com.br"},
    {"id":5,"cat":"Íntimas","prod":"Kit 5 Calcinhas Algodão","price":24.99,"icon":"🩷","lat":51.5074,"lon":-0.1278,"city":"Londres","stock":500,"viral":100,"wix":"https://fashionwomen.com.br"},
    {"id":6,"cat":"Íntimas","prod":"Sutiã Confort Sem Bojo","price":29.99,"icon":"👙","lat":53.8008,"lon":-1.5491,"city":"Leeds","stock":120,"viral":96,"wix":"https://fashionwomen.com.br"},
    {"id":7,"cat":"Sapatos","prod":"Bota Tratorada Cano Alto","price":69.99,"icon":"👢","lat":52.4862,"lon":-1.8904,"city":"Birmingham","stock":30,"viral":94,"wix":"https://fashionwomen.com.br"},
    {"id":8,"cat":"Sapatos","prod":"Tênis Chunky Branco","price":54.99,"icon":"👟","lat":53.4084,"lon":-2.9916,"city":"Liverpool","stock":60,"viral":93,"wix":"https://fashionwomen.com.br"},
    {"id":9,"cat":"Bolsas","prod":"Bolsa Tote Grife Inspira","price":39.99,"icon":"👜","lat":51.4545,"lon":-2.5879,"city":"Bristol","stock":80,"viral":92,"wix":"https://fashionwomen.com.br"},
    {"id":10,"cat":"Beleza","prod":"Kit Gloss + Brinco","price":18.99,"icon":"💄","lat":51.5074,"lon":-0.1278,"city":"Londres","stock":400,"viral":99,"wix":"https://fashionwomen.com.br"},
]
df=pd.DataFrame(data)
df['prev']= (df['viral']*1.5 + np.random.randint(10,30,10)).astype(int)

with st.sidebar:
    st.title("🛒 LOJA GLOBO")
    if st.session_state.cart:
        total=sum([float(x['price']) for x in st.session_state.cart])
        st.subheader(f"Carrinho: {len(st.session_state.cart)} itens")
        for i in st.session_state.cart: st.write(f"{i['icon']} {i['prod']} £{i['price']}")
        st.metric("TOTAL", f"£{total:.2f}")
        st.link_button("💳 FINALIZAR NA WIX", "https://fashionwomen.com.br/cart", use_container_width=True)
        if st.button("Limpar Carrinho"): st.session_state.cart=[]; st.rerun()
        st.divider()
    cat=st.selectbox("Filtrar Categoria", ["Todas","Joias","Roupas","Íntimas","Sapatos","Bolsas","Beleza"])
    dff=df if cat=="Todas" else df[df['cat']==cat]
    st.caption(f"{len(dff)} produtos | Globo + Loja")
    for _,p in dff.iterrows():
        sel = st.session_state.sel==p['id']
        with st.container(border=True):
            st.markdown(f"**{p['icon']} {p['prod']}** {'⭐' if sel else ''}")
            st.write(f"£{p['price']} | {p['city']} | 🔥{p['viral']}% VIRAL")
            c1,c2=st.columns(2)
            with c1:
                if st.button("📍 GLOBO", key=f"g{p['id']}"): st.session_state.sel=p['id']; st.rerun()
            with c2:
                if st.button("🛒 ESCOLHER", key=f"a{p['id']}"): st.session_state.cart.append(p.to_dict()); st.session_state.sel=p['id']; st.toast("Adicionado!"); st.rerun()

c1,c2,c3,c4=st.columns(4)
c1.metric("Vendas Hoje UK","£0,00","INICIANDO")
c2.metric("Previsão 7d",f"£{int(dff['prev'].sum()*35)}","IA")
c3.metric("Produto Top",dff.sort_values('viral',ascending=False).iloc[0]['prod'][:15])
c4.metric("Cidade Ouro","Londres","60% vendas")

if st.session_state.sel:
    prod=df[df['id']==st.session_state.sel].iloc[0]
    st.success(f"🎯 SELECIONADO: {prod['icon']} {prod['prod']} - £{prod['price']} | Previsão {prod['prev']} vendas/7d em {prod['city']}")
    dg=df[df['id']==st.session_state.sel]
else:
    st.info("👈 Clique em 📍 GLOBO ou 🛒 ESCOLHER na barra lateral pra integrar loja no globo cibernético")
    dg=dff

# --- LINHA CORRIGIDA AQUI: r['city'] em vez de r.city ---
colors={"Joias":"#FFD700","Roupas":"#FF00FF","Íntimas":"#FF1493","Sapatos":"#00FFFF","Bolsas":"#FFA500","Beleza":"#FF69B4"}
pts=[]
for _, r in dg.iterrows():
    pts.append({
        "lat": float(r['lat']), "lng": float(r['lon']), "prod": r['prod'], "cat": r['cat'],
        "price": float(r['price']), "city": r['city'],
        "size": 2.2 if st.session_state.sel==r['id'] else float(r['viral'])/50,
        "color": "#FFFFFF" if st.session_state.sel==r['id'] else colors.get(r['cat'],"#FF00FF"),
        "icon": r['icon']
    })

j=json.dumps(pts)
flat, flng = (float(dg.iloc[0]['lat']), float(dg.iloc[0]['lon'])) if len(dg)>0 else (51.5, -2.0)

html=f"""
<div id="g" style="width:100%;height:620px;background:#000;border-radius:20px;border:2px solid #FF00FF"></div>
<script src="//unpkg.com/globe.gl"></script>
<script>
const d={j};
const w=Globe()(document.getElementById('g')).globeImageUrl('//unpkg.com/three-globe/example/img/earth-night.jpg').bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png').backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png').pointsData(d).pointLat('lat').pointLng('lng').pointAltitude(p=>p.size*0.12).pointRadius(p=>p.size*0.2).pointColor('color').pointLabel(p=>`<b>${{p.icon}} ${{p.prod}}</b><br>${{p.cat}} £${{p.price}}<br>${{p.city}} UK`).atmosphereColor('#FF00FF').atmosphereAltitude(0.25);
w.controls().autoRotate=true; w.controls().autoRotateSpeed=0.7; w.pointOfView({{lat:{flat},lng:{flng},altitude:0.7}},1200);
</script>
"""
components.html(html, height=640)

st.divider()
st.subheader("💎 VITRINE CIBERNÉTICA - LOJA INTEGRADA NO GLOBO")
cols=st.columns(5)
for i,(_,p) in enumerate(dff.iterrows()):
    with cols[i%5]:
        with st.container(border=True):
            st.markdown(f"<center style='font-size:40px'>{p['icon
