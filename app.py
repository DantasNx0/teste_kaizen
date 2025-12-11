import streamlit as st
import pandas as pd
import requests

# =====================
# CONFIGURAÇÃO DA PÁGINA
# =====================
st.set_page_config(
    page_title="Kaizen Battle Analytics",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================
# CSS PREMIUM (DARK GLASS)
# =====================
st.markdown("""
<style>
    /* Reset e Fonte */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
    }

    /* Cards Gerais (Clean Light) */
    .glass-card {
        background: #ffffff;
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    /* Topo (HUD) */
    .hud-metric {
        text-align: center;
        background: white;
    }
    .hud-value {
        font-size: 28px;
        font-weight: 800;
        color: #2c3e50;
    }
    .hud-label {
        font-size: 12px;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    /* Badges de Tipo */
    .type-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-transform: uppercase;
        margin-right: 5px;
        color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Cores dos Tipos */
    .bg-normal { background-color: #A8A878; }
    .bg-fire { background-color: #F08030; }
    .bg-water { background-color: #6890F0; }
    .bg-grass { background-color: #78C850; }
    .bg-electric { background-color: #F8D030; color: #333;}
    .bg-ice { background-color: #98D8D8; color: #333; }
    .bg-fighting { background-color: #C03028; }
    .bg-poison { background-color: #A040A0; }
    .bg-ground { background-color: #E0C068; }
    .bg-flying { background-color: #A890F0; }
    .bg-psychic { background-color: #F85888; }
    .bg-bug { background-color: #A8B820; }
    .bg-rock { background-color: #B8A038; }
    .bg-ghost { background-color: #705898; }
    .bg-dragon { background-color: #7038F8; }
    .bg-steel { background-color: #B8B8D0; }
    .bg-fairy { background-color: #EE99AC; }

    /* Inputs e Tabs */
    .stSelectbox > div > div {
        background-color: white;
        color: #2c3e50;
        border: 1px solid #dcdcdc;
        border-radius: 10px;
    }
    div[data-baseweb="select"] span {
        color: #2c3e50;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: transparent;
        border-radius: 10px;
        color: #7f8c8d;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        background-color: #eecda3;
        background: linear-gradient(to right, #eecda3, #ef629f); /* Sunset gradient para destaque */
        color: white;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    /* Métricas e Textos Gerais */
    div[data-testid="stMetricLabel"] {
        color: #7f8c8d;
    }
    div[data-testid="stMetricValue"] {
        color: #2c3e50;
    }
    h1, h2, h3, h4, h5, h6, p, div {
        color: #2c3e50;
    }

</style>
""", unsafe_allow_html=True)

# =====================
# LÓGICA & DADOS
# =====================

# Mapeamento de Fraquezas (Simples)
WEAKNESS_MAP = {
    'normal': ['fighting'],
    'fire': ['water', 'ground', 'rock'],
    'water': ['electric', 'grass'],
    'grass': ['fire', 'ice', 'poison', 'flying', 'bug'],
    'electric': ['ground'],
    'ice': ['fire', 'fighting', 'rock', 'steel'],
    'fighting': ['flying', 'psychic', 'fairly'],
    'poison': ['ground', 'psychic'],
    'ground': ['water', 'grass', 'ice'],
    'flying': ['electric', 'ice', 'rock'],
    'psychic': ['bug', 'ghost', 'dark'],
    'bug': ['fire', 'flying', 'rock'],
    'rock': ['water', 'grass', 'fighting', 'ground', 'steel'],
    'ghost': ['ghost', 'dark'],
    'dragon': ['ice', 'dragon', 'fairy'],
    'steel': ['fire', 'fighting', 'ground'],
    'fairy': ['poison', 'steel']
}

@st.cache_data
def load_data():
    try:
        pokemons = pd.read_csv("data/pokemons.csv")
        battles = pd.read_csv("data/batalhas.csv")
        wins = pd.read_csv("data/ranking_vitorias.csv")
        return pokemons, battles, wins
    except:
        return None, None, None

def get_image(name, poke_id):
    try:
        fmt_name = name.lower().replace(" ", "-").replace(".", "").replace("'", "").replace("♀", "-f").replace("♂", "-m")
        url = f"https://pokeapi.co/api/v2/pokemon/{fmt_name}"
        r = requests.get(url, timeout=1)
        if r.status_code == 200:
            return r.json()['sprites']['other']['official-artwork']['front_default']
    except:
        pass
    return f"https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/{poke_id}.png"

pokemons, battles, wins = load_data()

# --- HEADER (TITULO + ETL) ---
c_head1, c_head2 = st.columns([3, 1])
with c_head1:
    st.subheader("Teste Técnico Pokémon - Kaizen (Analista de Dados Júnior)")
with c_head2:
    if st.button("🔄 Atualizar Dados (ETL)", type="primary"):
        with st.spinner("Processando dados (isso pode levar alguns instantes)..."):
            import os
            os.system("python etl_kaizen.py")
            st.cache_data.clear()
        st.success("Dados atualizados com sucesso!")
        st.rerun()

st.divider()

if pokemons is None:
    st.warning("⚠️ Base de dados vazia ou não encontrada. Clique no botão acima para gerar os arquivos.")
    st.stop()

# =====================
# DASHBOARD LAYOUT
# =====================

# --- 1. HUD GLOBAL (STATUS DO SERVIDOR/ARENA) ---
st.markdown("### 🌐 ARENA GLOBAL STATUS")
col_h1, col_h2, col_h3, col_h4 = st.columns(4)

total_pokes = len(pokemons)
top_winner_id = wins.iloc[0]['pokemon']
top_winner_name = pokemons[pokemons['id'] == top_winner_id]['name'].values[0]
top_wins_val = wins.iloc[0]['vitorias']

with col_h1:
    st.markdown(f'<div class="glass-card hud-metric"><div class="hud-value">{total_pokes}</div><div class="hud-label">Pokémons</div></div>', unsafe_allow_html=True)
with col_h2:
    st.markdown(f'<div class="glass-card hud-metric"><div class="hud-value">{top_winner_name}</div><div class="hud-label">Campeão Atual</div></div>', unsafe_allow_html=True)
with col_h3:
    st.markdown(f'<div class="glass-card hud-metric"><div class="hud-value">{top_wins_val}</div><div class="hud-label">Vitórias (Campeão)</div></div>', unsafe_allow_html=True)
with col_h4:
    st.markdown(f'<div class="glass-card hud-metric"><div class="hud-value">LIVE</div><div class="hud-label">Arena Status</div></div>', unsafe_allow_html=True)


col_left, col_right = st.columns([1, 2])

# --- 2. COLUNA ESQUERDA: PERFIL DO POKÉMON ---
with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    # Seletor
    selected_name = st.selectbox("🎯 SELECIONAR AGENTE", pokemons['name'].unique())
    
    # Dados da Seleção
    poke_data = pokemons[pokemons['name'] == selected_name].iloc[0]
    pid = poke_data['id']
    img = get_image(selected_name, pid)
    
    # Imagem
    st.image(img, use_container_width=True)
    
    # Nome e Tipo
    st.markdown(f"<h2 style='text-align: center; margin: 0;'>{selected_name}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #aaa;'>ID: #{pid:03d}</p>", unsafe_allow_html=True)
    
    # Badges de Tipo
    ptype = str(poke_data['types']).split('/')[0].lower().strip()
    types_html = f"<div style='text-align: center; margin-top: 10px;'><span class='type-badge bg-{ptype}'>{poke_data['types']}</span></div>"
    st.markdown(types_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# --- 3. COLUNA DIREITA: DETALHES (ABAS) ---
with col_right:
    tab1, tab2, tab3 = st.tabs(["📊 METRICAS", "⚔️ COMBATES", "⚠️ INTELIGÊNCIA"])
    
    # === ABA 1: STATUS ===
    with tab1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.caption("ATRIBUTOS DE BATALHA")
        
        # Grid de Stats
        c1, c2 = st.columns(2)
        def stat_item(label, val):
            return f"**{label}**: {val} <progress value='{val}' max='200' style='width: 100%'></progress>"
            
        with c1:
            st.markdown(stat_item("HP", poke_data['hp']), unsafe_allow_html=True)
            st.markdown(stat_item("Ataque", poke_data['attack']), unsafe_allow_html=True)
            st.markdown(stat_item("Defesa", poke_data['defense']), unsafe_allow_html=True)
        with c2:
            st.markdown(stat_item("Velocidade", poke_data['speed']), unsafe_allow_html=True)
            st.markdown(stat_item("Sp. Atk", poke_data['sp_attack']), unsafe_allow_html=True)
            st.markdown(stat_item("Sp. Def", poke_data['sp_defense']), unsafe_allow_html=True)
            
        st.divider()
        st.caption("INFO GERAL")
        col_i1, col_i2 = st.columns(2)
        
        # Tratamento seguro de dados
        gen = poke_data.get('generation', 'N/A')
        leg_val = poke_data.get('legendary', 'False')
        is_legendary = str(leg_val).strip().lower() == 'true'
        
        col_i1.metric("Geração", gen)
        col_i2.metric("Lendário", "Sim" if is_legendary else "Não")
        st.markdown('</div>', unsafe_allow_html=True)

    # === ABA 2: COMBATES ===
    with tab2:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        # Filtra histórico
        my_battles = battles[
            (battles['first_pokemon'] == pid) | 
            (battles['second_pokemon'] == pid)
        ].copy()
        
        if not my_battles.empty:
            # Stats Rápido da Aba
            wins_count = len(my_battles[my_battles['winner'] == pid])
            total_b = len(my_battles)
            wr = (wins_count / total_b) * 100
            
            sc1, sc2, sc3 = st.columns(3)
            sc1.metric("Total Batalhas", total_b)
            sc2.metric("Vitórias", wins_count)
            sc3.metric("Taxa de Vitória", f"{wr:.1f}%")
            
            st.markdown("### 📜 Log Recente")
            # Log Logic
            id_map = pokemons.set_index('id')['name'].to_dict()
            
            def fmt_log(row):
                opp_id = row['second_pokemon'] if row['first_pokemon'] == pid else row['first_pokemon']
                opp_name = id_map.get(opp_id, f"#{opp_id}")
                result = "WIN 🟢" if row['winner'] == pid else "LOSS 🔴"
                return {"Oponente": opp_name, "Resultado": result}
                
            logs = my_battles.apply(fmt_log, axis=1, result_type='expand')
            st.dataframe(logs, use_container_width=True, height=300)
        else:
            st.warning("Sem registro de combate para este agente.")
        st.markdown('</div>', unsafe_allow_html=True)

    # === ABA 3: FRAQUEZAS ===
    with tab3:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown(f"### Análise Tática: {selected_name}")
        
        # Lógica de Fraqueza
        my_type_prim = ptype
        weaknesses = WEAKNESS_MAP.get(my_type_prim, [])
        
        if weaknesses:
            st.error(f"⚠️ CUIDADO! {selected_name} (Tipo {ptype.upper()}) é vulnerável contra:")
            
            cols = st.columns(len(weaknesses))
            for i, weak in enumerate(weaknesses):
                with cols[i]:
                    st.markdown(f"<div style='text-align:center'><span class='type-badge bg-{weak}'>{weak}</span></div>", unsafe_allow_html=True)
            
            st.markdown("---")
            st.info("💡 Dica Tática: Evite confrontos diretos contra estes tipos em arenas neutras.")
        else:
            st.success("🛡️ Este tipo não possui fraquezas elementares registradas no banco de dados padrão.")
            
        st.markdown('</div>', unsafe_allow_html=True)
