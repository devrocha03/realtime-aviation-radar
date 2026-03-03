import streamlit as st
import pandas as pd
from databricks import sql
import time

# --- 1. Configurações da Página ---
st.set_page_config(page_title="Radar Toronto AO VIVO", page_icon="✈️", layout="wide")

st.title("✈️ Torre de Controle - Espaço Aéreo de Toronto")
st.markdown("Monitoramento em tempo real de voos comerciais e privados na região.")

# --- 2. Credenciais do Databricks ---
# Use o mesmo Hostname e HTTP Path do seu Cluster de Compute do projeto anterior!
DATABRICKS_SERVER_HOSTNAME =  "dbc-38fc862a-bf7b.cloud.databricks.com"
DATABRICKS_HTTP_PATH = "/sql/1.0/warehouses/a3efbc0f7c7f3d0c"

# --- 3. Conexão OAuth ---
# Tiramos o cache_data para o mapa atualizar com dados frescos toda vez que recarregarmos!
def puxar_radar():
  try:
    connection = sql.connect(
      server_hostname=DATABRICKS_SERVER_HOSTNAME,
            http_path=DATABRICKS_HTTP_PATH,
            auth_type="databricks-oauth"
    )
    
    # Trazendo as coordenadas, identificação e velocidade
    query ="""
            SELECT latitude, longitude, callsign, origin_country, velocity 
            FROM default.gold_radar_toronto
        """
    df = pd.read_sql(query, connection)
    connection.close()
    return df
  except Exception as e:
    st.error(f'Erro de Conexão: {e}')
    return pd.DataFrame()
  
# --- 4. Construindo o Mapa ---
df_radar = puxar_radar()

if not df_radar.empty:
    
    # --- 4. 🎛️ Criando os Filtros (Barra Lateral) ---
    st.sidebar.header("🎛️ Ajustes do Radar")
    
    # Descobre todos os países únicos que estão voando agora
    paises_unicos = df_radar['origin_country'].dropna().unique().tolist()
    
    # Filtro 1: Múltipla escolha de países
    paises_selecionados = st.sidebar.multiselect(
        "Filtrar por País de Origem:", 
        options=paises_unicos, 
        default=paises_unicos # Já vem com todos selecionados por padrão
    )
    
    # Filtro 2: Slider de velocidade
    vel_max = float(df_radar['velocity'].max())
    vel_minima = st.sidebar.slider(
        "Velocidade Mínima (m/s):", 
        min_value=0.0, 
        max_value=vel_max, 
        value=0.0
    )
    
    # Aplicando os filtros na nossa tabela usando a lógica do Pandas
    df_filtrado = df_radar[
        (df_radar['origin_country'].isin(paises_selecionados)) & 
        (df_radar['velocity'] >= vel_minima)
    ]

    # --- 5. 🟢 O Modo "Ao Vivo" ---
    st.sidebar.divider()
    modo_live = st.sidebar.toggle("🟢 Ligar Radar Contínuo (Atualiza a cada 15s)")

    # --- 6. Construindo o Mapa com os Dados Filtrados ---
    st.success(f"Radar Ativo: {len(df_filtrado)} aeronaves atendem aos seus filtros.")
    
    col_mapa, col_dados = st.columns([2, 1]) 
    
    with col_mapa:
        st.map(df_filtrado, size=200, color="#00ff00") 
        
    with col_dados:
        st.dataframe(df_filtrado[['callsign', 'origin_country', 'velocity']], use_container_width=True)

    # A mágica do Loop: Se a chavinha estiver ligada, ele espera 15s e recarrega a página sozinho
    if modo_live:
        time.sleep(60)
        st.rerun()

else:
    st.warning("Nenhum voo detectado ou erro na conexão.")
  
  
  
  
  