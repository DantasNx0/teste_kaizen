# ⚡ Kaizen Battle Analytics

> **Teste Técnico - Analista de Dados Júnior**
>
> Uma aplicação "Premium Grade" para análise de dados de batalhas Pokémon, integrando ETL robusto, Dashboard interativo e design moderno.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458)

---

## 📋 Sobre o Projeto

Este projeto tem como objetivo demonstrar competências em **Engenharia de Dados** e **Visualização**, criando uma solução completa que consome uma API de batalhas Pokémon, processa os dados e apresenta insights estratégicos.

### 🚀 Principais Funcionalidades

1.  **ETL Resiliente (`etl_kaizen.py`)**:
    *   Extração de dados da API com paginação automática.
    *   Enriquecimento de dados (cruzamento com endpoints de detalhes).
    *   Tratamento de erros e retentativas (“Retry”) para instabilidade de rede.
    *   Cálculo automático de KPIs (Rankings, Taxas de Vitória).

2.  **Dashboard (`app.py`)**:
    *   Interface desenvolvida em **Streamlit** com CSS customizado (Glassmorphism).
    *   Visualização de métricas em tempo real.
    *   **Botão de ETL Integrado**: Permite rodar o pipeline de dados diretamente pela interface.
    *   Análise individual por Pokémon (Status, Fraquezas, Histórico).

3.  **Visualização Enterprise (`Kaizen-dashboard.pbix`)**:
    *   Dashboard complementar desenvolvido em **Microsoft Power BI**.
    *   Ideal para análise executiva e apresentações corporativas.
    *   Consome os mesmos arquivos CSV gerados pelo processo de ETL.

---

## 🛠️ Instalação e Configuração

Siga os passos abaixo para rodar o projeto em seu ambiente local.

### 1. Pré-requisitos

*   **Python 3.8** ou superior instalado.
*   **Git** instalado.

### 2. Clonar o Repositório

```bash
git clone https://github.com/seu-usuario/teste-kaizen.git
cd teste-kaizen
```

### 3. Configurar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Instalar Dependências

Instale as bibliotecas necessárias listadas no arquivo `requirements.txt`:

```bash
pip install -r requirements.txt
```

### 5. Configurar Credenciais (.env)

⚠️ **Importante**: O projeto necessita de credenciais de acesso à API. Crie um arquivo chamado `.env` na raiz do projeto e adicione as seguintes variáveis:

```env
API_BASE_URL="http://url-da-api-kaizen"
API_USERNAME="seu-usuario"
API_PASSWORD="sua-senha"
```

> **Nota**: O arquivo `.env` é ignorado pelo Git por segurança.

---

## ▶️ Como Executar

### Opção A: Via Dashboard (Recomendado)

A maneira mais visual de interagir com o projeto.

```bash
streamlit run app.py
```

*   O navegador abrirá automaticamente em `http://localhost:8501`.
*   Clique no botão **"🔄 Atualizar Dados (ETL)"** no canto superior direito para baixar os dados mais recentes.

### Opção B: Via Terminal (Apenas ETL)

Se desejar apenas processar os dados e gerar os arquivos CSV na pasta `data/`:

```bash
python etl_kaizen.py
```

---

## 📂 Estrutura do Projeto

```
Teste-Kaizen/
├── app.py              # Aplicação Dashboard (Streamlit)
├── etl_kaizen.py       # Script de Extração e Tratamento (ETL)
├── requirements.txt    # Lista de dependências
├── .env                # Arquivo de configurações (NÃO COMITAR)
├── .gitignore          # Arquivos ignorados pelo Git
├── README.md           # Documentação do projeto
├── Kaizen-dashboard.pbix # Dashboard Power BI (Enterprise)
└── data/               # Diretório onde os CSVs são salvos (gerado automaticamente)
    ├── batalhas.csv
    ├── pokemons.csv
    └── ...
```

---

## 📊 Decisões Técnicas

*   **Arquitetura**: Separação clara entre a lógica de extração (`etl_kaizen.py`) e a camada de apresentação (`app.py`), permitindo manutenção independente.
*   **Resiliência**: Implementação de `HTTPAdapter` com `Retry` no script de ETL para garantir que falhas momentâneas na API não quebrem o processo.
*   **Performance**: Uso de `st.cache_data` no Streamlit para evitar recarregamento desnecessário de arquivos CSV pesados.

---

Made with 💜 and Python. Dev Paulo Eduardo
