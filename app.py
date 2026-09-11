import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Desmatamento na Amazônia Legal",
    page_icon="🌳",
    layout="wide",
)

# =========================================================
# CARREGAMENTO DE DADOS
# =========================================================
@st.cache_data
def load_data():
    agg_ano_uf = pd.read_csv("data/agg_ano_uf.csv")
    agg_ano_uf_tipo = pd.read_csv("data/agg_ano_uf_tipo.csv")
    ranking_uf = pd.read_csv("data/ranking_uf.csv")
    return agg_ano_uf, agg_ano_uf_tipo, ranking_uf

agg_ano_uf, agg_ano_uf_tipo, ranking_uf = load_data()

UFS_AMAZONIA = sorted(agg_ano_uf["state"].unique().tolist())
ANO_MIN, ANO_MAX = int(agg_ano_uf["year"].min()), int(agg_ano_uf["year"].max())

# =========================================================
# CABEÇALHO
# =========================================================
st.title("🌳 Desmatamento na Amazônia Legal")
st.caption(
    "Painel construído a partir de dados oficiais do PRODES/INPE, "
    "disponibilizados como dados abertos do governo federal."
)

# =========================================================
# BARRA LATERAL — FILTROS
# =========================================================
st.sidebar.header("Filtros")

ufs_selecionadas = st.sidebar.multiselect(
    "Estados (UF)", options=UFS_AMAZONIA, default=UFS_AMAZONIA
)

anos_selecionados = st.sidebar.slider(
    "Período (ano)",
    min_value=ANO_MIN,
    max_value=ANO_MAX,
    value=(ANO_MIN, ANO_MAX),
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Fonte dos dados:** PRODES/INPE — Monitoramento do desmatamento "
    "da Amazônia Legal por satélite.\n\n"
    "**Reúso:** dados abertos, disponíveis no Portal Brasileiro de Dados Abertos "
    "(dados.gov.br) e no site oficial do INPE."
)

# =========================================================
# APLICAR FILTROS
# =========================================================
mask = (
    agg_ano_uf["state"].isin(ufs_selecionadas)
    & agg_ano_uf["year"].between(*anos_selecionados)
)
df_filtrado = agg_ano_uf[mask]

mask_tipo = (
    agg_ano_uf_tipo["state"].isin(ufs_selecionadas)
    & agg_ano_uf_tipo["year"].between(*anos_selecionados)
)
df_tipo_filtrado = agg_ano_uf_tipo[mask_tipo]

# =========================================================
# KPIs DE TOPO
# =========================================================
col1, col2, col3 = st.columns(3)

area_total = df_filtrado["area_km_total"].sum()
ano_mais_recente = anos_selecionados[1]
ano_anterior = ano_mais_recente - 1

area_ano_recente = df_filtrado.loc[
    df_filtrado["year"] == ano_mais_recente, "area_km_total"
].sum()
area_ano_anterior = df_filtrado.loc[
    df_filtrado["year"] == ano_anterior, "area_km_total"
].sum()

variacao = (
    ((area_ano_recente - area_ano_anterior) / area_ano_anterior * 100)
    if area_ano_anterior > 0
    else 0
)

col1.metric("Área total desmatada no período", f"{area_total:,.0f} km²")
col2.metric(f"Área desmatada em {ano_mais_recente}", f"{area_ano_recente:,.0f} km²")
col3.metric(
    f"Variação vs. {ano_anterior}",
    f"{variacao:+.1f}%",
    delta=f"{variacao:+.1f}%",
    delta_color="inverse",  # queda de desmatamento = "bom" (verde)
)

st.markdown("---")

# =========================================================
# GRÁFICO 1 — SÉRIE TEMPORAL COM ANOTAÇÕES
# =========================================================
st.subheader("Evolução do desmatamento na Amazônia Legal")

serie_total = df_filtrado.groupby("year", as_index=False)["area_km_total"].sum()

fig_linha = go.Figure()
fig_linha.add_trace(
    go.Scatter(
        x=serie_total["year"],
        y=serie_total["area_km_total"],
        mode="lines+markers",
        line=dict(color="#2E7D32", width=3),
        name="Área desmatada (km²)",
    )
)

# Anotações nos pontos de inflexão conhecidos, se estiverem no range filtrado
anotacoes = {
    2012: "Mínimo histórico",
    2019: "Forte alta",
    2023: "Início de reversão",
}
for ano, texto in anotacoes.items():
    if ano in serie_total["year"].values:
        y_valor = serie_total.loc[serie_total["year"] == ano, "area_km_total"].values[0]
        fig_linha.add_annotation(
            x=ano, y=y_valor, text=texto, showarrow=True, arrowhead=2, yshift=15
        )

fig_linha.update_layout(
    xaxis_title="Ano",
    yaxis_title="Área desmatada (km²)",
    hovermode="x unified",
    height=450,
)
st.plotly_chart(fig_linha, use_container_width=True)

# =========================================================
# GRÁFICO 2 — RANKING POR UF
# =========================================================
st.subheader("Área desmatada por estado (total no período filtrado)")

ranking_filtrado = (
    df_filtrado.groupby("state", as_index=False)["area_km_total"]
    .sum()
    .sort_values("area_km_total", ascending=True)
)

fig_barras = px.bar(
    ranking_filtrado,
    x="area_km_total",
    y="state",
    orientation="h",
    labels={"area_km_total": "Área desmatada (km²)", "state": "UF"},
    color="area_km_total",
    color_continuous_scale="Greens",
)
fig_barras.update_layout(height=400, coloraxis_showscale=False)
st.plotly_chart(fig_barras, use_container_width=True)

# =========================================================
# GRÁFICO 3 — BARRAS EMPILHADAS POR ANO E UF
# =========================================================
st.subheader("Composição anual por estado")

fig_empilhado = px.bar(
    df_filtrado,
    x="year",
    y="area_km_total",
    color="state",
    labels={"area_km_total": "Área desmatada (km²)", "year": "Ano"},
)
fig_empilhado.update_layout(height=450, legend_title="UF")
st.plotly_chart(fig_empilhado, use_container_width=True)

# =========================================================
# GRÁFICO 4 — TIPO DE DESMATAMENTO (a partir de anos com detalhe)
# =========================================================
st.subheader("Tipo de desmatamento")
st.caption(
    "O PRODES só passou a detalhar o subtipo de desmatamento a partir de "
    "determinados anos; períodos anteriores aparecem como "
    "'sem subtipo detalhado (legado)'."
)

tipo_agrupado = (
    df_tipo_filtrado.groupby(["year", "sub_class_limpo"], as_index=False)[
        "area_km_total"
    ]
    .sum()
)

fig_tipo = px.bar(
    tipo_agrupado,
    x="year",
    y="area_km_total",
    color="sub_class_limpo",
    labels={"area_km_total": "Área desmatada (km²)", "year": "Ano", "sub_class_limpo": "Tipo"},
)
fig_tipo.update_layout(height=450, legend_title="Tipo de desmatamento")
st.plotly_chart(fig_tipo, use_container_width=True)

# =========================================================
# RODAPÉ
# =========================================================
st.markdown("---")
st.caption(
    "Dados: PRODES/INPE (Instituto Nacional de Pesquisas Espaciais), "
    "disponibilizados como dados abertos. "
    "Código-fonte disponível para replicação e adaptação a outras regiões."
)
