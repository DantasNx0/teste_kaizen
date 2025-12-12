import os
import requests
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from dotenv import load_dotenv

# ================================
# 1. CONFIGURAÇÕES E SEGURANÇA
# ================================
# Carrega variáveis do arquivo .env (Segurança Nível Senior)
load_dotenv()

BASE_URL = os.getenv("API_BASE_URL")
USERNAME = os.getenv("API_USERNAME")
PASSWORD = os.getenv("API_PASSWORD")

# Verifica se as credenciais foram carregadas
if not all([BASE_URL, USERNAME, PASSWORD]):
    raise ValueError("❌ ERRO: Variáveis de ambiente não encontradas. Verifique o arquivo .env")

# Configuração de Pastas (Organização)
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True) # Cria a pasta se não existir

REQUEST_TIMEOUT = 15
MAX_RETRIES = 5
BACKOFF_FACTOR = 1

# ================================
# 2. SESSÃO RESILIENTE (Anti-Falha)
# ================================
def create_session():
    session = requests.Session()
    
    # Estratégia de Retentativa Inteligente (Substitui sleep fixo)
    retries = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET", "POST"]
    )
    
    adapter = HTTPAdapter(max_retries=retries)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session

http = create_session()

# ================================
# 3. FUNÇÕES DO PROCESSO
# ================================
def login():
    print("🔐 Autenticando via variáveis seguras...")
    try:
        response = http.post(
            f"{BASE_URL}/login",
            json={"username": USERNAME, "password": PASSWORD},
            timeout=REQUEST_TIMEOUT
        )
        response.raise_for_status()
        print("✅ Login realizado com sucesso")
        return response.json()["access_token"]
    except Exception as e:
        print(f"❌ Falha crítica no login: {e}")
        exit()

def fetch_all(endpoint, key, token, per_page):
    headers = {"Authorization": f"Bearer {token}"}
    page = 1
    results = []
    
    print(f"📥 Extraindo {endpoint}...")
    
    while True:
        try:
            response = http.get(
                f"{BASE_URL}{endpoint}",
                headers=headers,
                params={"page": page, "per_page": per_page},
                timeout=REQUEST_TIMEOUT
            )
            response.raise_for_status()
            data = response.json()
            
            batch = data.get(key, [])
            if not batch: break
            
            results.extend(batch)
            total = data.get("total", 0)
            
            # Feedback visual simples
            if page % 5 == 0:
                print(f"   -> Página {page} | Acumulado: {len(results)}")
            
            # Condições de parada
            if len(results) >= total or len(batch) < per_page:
                break
                
            page += 1
            
        except Exception as e:
            print(f"⚠️ Erro na página {page}: {e}")
            break
            
    print(f"✅ {endpoint} concluído. Total: {len(results)}")
    return results

def enrich_pokemons(pokemons, token):
    headers = {"Authorization": f"Bearer {token}"}
    enriched = []
    total = len(pokemons)
    
    print(f"⚡ Enriquecendo dados de {total} Pokémons...")
    
    for index, p in enumerate(pokemons):
        try:
            r = http.get(
                f"{BASE_URL}/pokemon/{p['id']}",
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            if r.status_code == 200:
                enriched.append(r.json())
            else:
                enriched.append(p)
                
        except Exception:
            enriched.append(p)
            
        if (index + 1) % 50 == 0:
            print(f"   Processados: {index + 1}/{total}")
            
    return enriched

# ================================
# 4. MAIN (EXECUÇÃO)
# ================================
def main():
    token = login()
    
    # --- COMBATES ---
    combats = fetch_all("/combats", "combats", token, per_page=100)
    if combats:
        df_battles = pd.DataFrame(combats)
        # Salva na pasta data/
        df_battles.to_csv(os.path.join(DATA_DIR, "batalhas.csv"), index=False)

    # --- POKÉMONS ---
    base_list = fetch_all("/pokemon", "pokemons", token, per_page=50)
    if base_list:
        detailed = enrich_pokemons(base_list, token)
        df_pokemons = pd.DataFrame(detailed)

        # Limpeza numérica
        num_cols = ["hp", "attack", "defense", "sp_attack", "sp_defense", "speed"]
        for col in num_cols:
            if col in df_pokemons:
                df_pokemons[col] = pd.to_numeric(df_pokemons[col], errors="coerce").fillna(0)
        
        # Salva na pasta data/
        df_pokemons.to_csv(os.path.join(DATA_DIR, "pokemons.csv"), index=False)

    # --- GERAÇÃO DE KPIS (Métricas) ---
    print("📊 Calculando KPIs e salvando tabelas auxiliares...")
    
    if combats:
        # 1. Ranking de Vitórias
        df_wins = df_battles["winner"].value_counts().reset_index()
        df_wins.columns = ["pokemon", "vitorias"]
        df_wins.to_csv(os.path.join(DATA_DIR, "ranking_vitorias.csv"), index=False)

        # 2. Total de Batalhas
        df_total = pd.concat([
            df_battles["first_pokemon"], 
            df_battles["second_pokemon"]
        ]).value_counts().reset_index()
        df_total.columns = ["pokemon", "total_batalhas"]
        df_total.to_csv(os.path.join(DATA_DIR, "total_batalhas.csv"), index=False)

        # 3. Taxa de Vitória (Join)
        df_rate = df_total.merge(df_wins, on="pokemon", how="left")
        df_rate["vitorias"] = df_rate["vitorias"].fillna(0)
        df_rate["taxa_vitoria"] = (df_rate["vitorias"] / df_rate["total_batalhas"]) * 100
        df_rate.to_csv(os.path.join(DATA_DIR, "taxa_vitoria.csv"), index=False)

    print(f"\n🚀 ETL EXECUTADO COM SUCESSO! Arquivos salvos em '{DATA_DIR}/'")

if __name__ == "__main__":
    main()