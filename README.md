# 🌳 Amazônia Legal — Painel de Desmatamento

Painel interativo em Streamlit com dados abertos do PRODES/INPE sobre desmatamento na Amazônia Legal (2008–2025). Mostra evolução anual, ranking por estado e tipos de desmatamento, com pontos de inflexão associados a mudanças de política pública.

Desenvolvido para o **2º Concurso de Reúso de Dados Abertos da Controladoria-Geral da União (CGU)**.

🔗 **Acesse o painel online:** _[https://desmatamento-amazonia.streamlit.app/]_

---

## 📊 O que o painel mostra

- **KPIs de topo**: área total desmatada no período, área do ano mais recente e variação percentual em relação ao ano anterior
- **Série temporal anotada**: evolução do desmatamento ano a ano, com marcações nos principais pontos de inflexão (mínimo histórico em 2012, forte alta em 2019, início de reversão em 2023)
- **Ranking por estado (UF)**: quais estados da Amazônia Legal concentram a maior parte do desmatamento
- **Composição anual por UF**: barras empilhadas mostrando a contribuição de cada estado ano a ano
- **Tipo de desmatamento**: quebra por subtipo (corte raso, degradação progressiva, mineração) nos anos em que o PRODES detalha essa informação
- **Filtros interativos**: seleção de estados e intervalo de anos na barra lateral

## 🗂️ Fonte dos dados

Os dados utilizados são provenientes do **PRODES** (Programa de Monitoramento do Desmatamento da Amazônia Legal por Satélite), do **INPE** (Instituto Nacional de Pesquisas Espaciais), disponibilizados em formato aberto.

O conjunto original é um shapefile com um registro por polígono/mancha de desmatamento detectada (mais de 835 mil registros), contendo estado, ano, área em km², tipo de desmatamento, satélite/sensor utilizado na detecção, entre outros atributos. Os dados foram agregados para uso neste painel — os arquivos processados estão na pasta `data/`.

**Nota de qualidade dos dados:** o detalhamento por subtipo de desmatamento (`sub_class`) só está disponível de forma consistente a partir de determinados anos; períodos anteriores aparecem categorizados como "sem subtipo detalhado (legado)".

## 🛠️ Tecnologias

- [Streamlit](https://streamlit.io/) — interface e servidor do painel
- [Pandas](https://pandas.pydata.org/) — manipulação dos dados agregados
- [Plotly](https://plotly.com/python/) — visualizações interativas

## 🚀 Rodando localmente

```bash
git clone https://github.com/<seu-usuario>/amazonia-legal-desmatamento-painel.git
cd amazonia-legal-desmatamento-painel
pip install -r requirements.txt
streamlit run app.py
```

O app abre automaticamente em `http://localhost:8501`.

## ☁️ Deploy

Este projeto está hospedado gratuitamente no [Streamlit Community Cloud](https://share.streamlit.io/). Para publicar sua própria versão:

1. Faça um fork ou suba este repositório na sua conta do GitHub
2. Acesse [share.streamlit.io](https://share.streamlit.io/) e conecte sua conta GitHub
3. Selecione o repositório e aponte `app.py` como arquivo principal
4. Clique em "Deploy"

## 📁 Estrutura do projeto

```
.
├── app.py                      # aplicação Streamlit
├── requirements.txt            # dependências Python
├── README.md
└── data/
    ├── agg_ano_uf.csv           # área desmatada agregada por ano e UF
    ├── agg_ano_uf_tipo.csv      # área desmatada agregada por ano, UF e tipo
    └── ranking_uf.csv           # ranking total de área desmatada por UF
```

## 🔁 Replicabilidade

O código é aberto e pode ser adaptado para:
- Outras regiões ou biomas monitorados pelo INPE
- Outras fontes de dados PRODES (ex.: séries históricas mais longas, quando disponíveis)
- Cruzamento com outras bases públicas (ex.: unidades de conservação, terras indígenas, dados de fiscalização do IBAMA)

## 📄 Licença

Este projeto utiliza dados públicos e é disponibilizado para fins de reúso e reprodução, em linha com os objetivos do Concurso de Reúso de Dados Abertos da CGU.
