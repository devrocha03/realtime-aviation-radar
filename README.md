# ✈️ Toronto Airspace Control Tower - Real-Time Data Pipeline

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Databricks](https://img.shields.io/badge/Databricks-FF3621?style=for-the-badge&logo=databricks&logoColor=white)
![Apache Spark](https://img.shields.io/badge/PySpark-E25A1C?style=for-the-badge&logo=apachespark&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 📌 Visão Geral do Projeto
Este projeto simula uma Torre de Controle de tráfego aéreo, realizando o monitoramento contínuo de voos comerciais e privados na região de Toronto, Canadá. O objetivo principal foi construir uma pipeline de Engenharia de Dados de ponta a ponta, desde a ingestão de dados em tempo real de uma API externa até a visualização interativa em um dashboard analítico.

## 🏗️ Arquitetura de Dados (Medallion Architecture)
O processamento dos dados foi estruturado utilizando a Arquitetura Medalhão dentro do ambiente **Databricks**, garantindo qualidade e confiabilidade:

* **🥉 Camada Bronze (Ingestão):** Extração de dados brutos em formato JSON via `requests` diretamente da **OpenSky Network API**, capturando coordenadas, velocidade, país de origem e identificação (callsign) das aeronaves na bounding box de Toronto.
* **🥈 Camada Silver (Processamento e Limpeza):** Utilização de **PySpark** para transformar a estrutura complexa do JSON em um DataFrame tabular. Foram aplicadas regras de negócio cruciais, como a filtragem exclusiva de aeronaves em voo (`on_ground == false`) e a remoção de registros com coordenadas nulas.
* **🥇 Camada Gold (Disponibilização):** Os dados refinados são salvos e sobrescritos continuamente em uma tabela final (`gold_radar_toronto`), otimizada para o consumo da aplicação frontend.

## 📊 Dashboard Interativo (Frontend)
A interface de usuário foi desenvolvida em **Streamlit**, conectando-se diretamente ao Databricks SQL Warehouse. Funcionalidades incluem:
* **Mapa Geoespacial:** Plotagem em tempo real da latitude e longitude das aeronaves.
* **Filtros Dinâmicos:** Capacidade de segmentar os voos por País de Origem e Velocidade Mínima (Pandas).
* **Live Mode:** Implementação de um loop de atualização (`time.sleep` + `st.rerun()`) para atualizar a posição dos aviões no radar automaticamente.

## 📂 Estrutura do Repositório
* `radar.py`: Script principal do dashboard em Streamlit e lógica de conexão via `databricks-sql-connector`.
* `notebook_databricks.py`: Pipeline de extração e tratamento de dados em PySpark (Camadas Bronze/Silver/Gold).
* `requirements.txt`: Lista de dependências e bibliotecas Python necessárias.

## 🚀 Como Executar o Projeto
1. Clone este repositório:
   ```bash
   git clone [https://github.com/SEU_USUARIO/toronto-airspace-monitoring.git](https://github.com/SEU_USUARIO/toronto-airspace-monitoring.git)
