import os
import streamlit as st
import pandas as pd
import plotly.express as px


@st.cache_data
def carregar_dados():
    """Carrega os dados do arquivo CSV local e padroniza os nomes das colunas."""
    caminho = os.path.join(os.path.dirname(__file__), "dados-imersao-final.csv")
    df = pd.read_csv(caminho)

    df.columns = [c.replace(" ", "_").strip().lower() for c in df.columns]

    if "ano" not in df.columns and "ano_trabalho" in df.columns:
        df["ano"] = df["ano_trabalho"]

    if "contrato" not in df.columns:
        if "tipo_emprego" in df.columns:
            df["contrato"] = df["tipo_emprego"]
        elif "tipo_contrato" in df.columns:
            df["contrato"] = df["tipo_contrato"]

    if "usd" not in df.columns:
        if "salario_em_usd" in df.columns:
            df["usd"] = df["salario_em_usd"]
        elif "salario" in df.columns:
            df["usd"] = df["salario"]

    if "remoto" not in df.columns and "taxa_remoto" in df.columns:
        df["remoto"] = df["taxa_remoto"]

    return df


def configurar_pagina():
    """Define o layout, o título e o estilo da página do dashboard."""
    st.set_page_config(
        page_title="Dashboard de Salários na Área de Dados",
        page_icon="📊",
        layout="wide"
    )

    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as arquivo_css:
            st.markdown(f"<style>{arquivo_css.read()}</style>", unsafe_allow_html=True)


def construir_filtros(df):
    """Cria os filtros da barra lateral e retorna os valores selecionados."""
    st.sidebar.header("🔍 Filtros")
    st.sidebar.caption("Ajuste os filtros para explorar diferentes cenários salariais.")

    anos_disponiveis = sorted(df["ano"].unique())
    senioridades_disponiveis = sorted(df["senioridade"].unique())
    contratos_disponiveis = sorted(df["contrato"].unique())
    tamanhos_disponiveis = sorted(df["tamanho_empresa"].unique())

    # Inicializa os valores dos filtros na sessão para manter o estado entre interações.
    for key, valores in {
        "anos_selecionados": anos_disponiveis,
        "senioridades_selecionadas": senioridades_disponiveis,
        "contratos_selecionados": contratos_disponiveis,
        "tamanhos_selecionados": tamanhos_disponiveis,
    }.items():
        if key not in st.session_state:
            st.session_state[key] = valores

    # Botão para restaurar os filtros para o valor padrão rapidamente.
    if st.sidebar.button("Limpar filtros"):
        st.session_state["anos_selecionados"] = anos_disponiveis
        st.session_state["senioridades_selecionadas"] = senioridades_disponiveis
        st.session_state["contratos_selecionados"] = contratos_disponiveis
        st.session_state["tamanhos_selecionados"] = tamanhos_disponiveis

    anos_selecionados = st.sidebar.multiselect(
        "Ano",
        anos_disponiveis,
        default=st.session_state["anos_selecionados"],
        key="anos_selecionados"
    )

    senioridades_selecionadas = st.sidebar.multiselect(
        "Senioridade",
        senioridades_disponiveis,
        default=st.session_state["senioridades_selecionadas"],
        key="senioridades_selecionadas"
    )

    contratos_selecionados = st.sidebar.multiselect(
        "Tipo de Contrato",
        contratos_disponiveis,
        default=st.session_state["contratos_selecionados"],
        key="contratos_selecionados"
    )

    tamanhos_selecionados = st.sidebar.multiselect(
        "Tamanho da Empresa",
        tamanhos_disponiveis,
        default=st.session_state["tamanhos_selecionados"],
        key="tamanhos_selecionados"
    )

    return {
        "ano": anos_selecionados,
        "senioridade": senioridades_selecionadas,
        "contrato": contratos_selecionados,
        "tamanho_empresa": tamanhos_selecionados,
    }


def filtrar_dados(df, filtros):
    """Aplica os filtros selecionados ao DataFrame."""
    return df[
        (df["ano"].isin(filtros["ano"])) &
        (df["senioridade"].isin(filtros["senioridade"])) &
        (df["contrato"].isin(filtros["contrato"])) &
        (df["tamanho_empresa"].isin(filtros["tamanho_empresa"]))
    ]


def render_header(df_filtrado):
    """Exibe o título principal e a mensagem inicial do dashboard."""
    st.title("📊 Dashboard de Análise de Salários na Área de Dados")
    st.markdown("Explore os dados salariais na área de dados nos últimos anos e compare diferentes cenários profissionais.")
    st.caption("Fonte: conjunto de dados público sobre salários na área de dados.")

    if df_filtrado.empty:
        st.info("Nenhum dado corresponde aos filtros selecionados. Tente ajustar os critérios.")


def render_kpis(df_filtrado):
    """Mostra métricas resumidas com base nos dados filtrados."""
    st.subheader("Métricas Gerais (Salário anual em USD)")

    if not df_filtrado.empty:
        salario_medio = df_filtrado["usd"].mean()
        salario_maximo = df_filtrado["usd"].max()
        total_registros = df_filtrado.shape[0]
        cargo_mais_frequente = df_filtrado["cargo"].mode()[0]
    else:
        salario_medio = 0
        salario_maximo = 0
        total_registros = 0
        cargo_mais_frequente = ""

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Salário médio", f"${salario_medio:,.0f}")
    col2.metric("Salário máximo", f"${salario_maximo:,.0f}")
    col3.metric("Total de registros", f"{total_registros:,}")
    col4.metric("Cargo mais frequente", cargo_mais_frequente)

    st.markdown("---")


def render_graficos(df_filtrado):
    """Renderiza os gráficos principais do dashboard."""
    st.subheader("Gráficos")

    col_graf1, col_graf2 = st.columns(2)

    # Gráfico 1: Top cargos por salário
    with col_graf1:
        if not df_filtrado.empty:
            top_cargos = (
                df_filtrado.groupby("cargo")["usd"]
                .mean()
                .nlargest(10)
                .sort_values(ascending=True)
                .reset_index()
            )

            grafico_cargos = px.bar(
                top_cargos,
                x="usd",
                y="cargo",
                orientation="h",
                title="Top 10 cargos por salário médio",
                labels={"usd": "Média salarial anual (USD)", "cargo": "Cargo"}
            )
            grafico_cargos.update_layout(title_x=0.1)
            st.plotly_chart(grafico_cargos, width='stretch')
        else:
            st.warning("Nenhum dado para exibir no gráfico de cargos.")

    # Gráfico 2: Distribuição de salários
    with col_graf2:
        if not df_filtrado.empty:
            grafico_hist = px.histogram(
                df_filtrado,
                x="usd",
                nbins=30,
                title="Distribuição de salários anuais",
                labels={"usd": "Faixa salarial (USD)"}
            )
            grafico_hist.update_layout(title_x=0.1)
            st.plotly_chart(grafico_hist, width='stretch')
        else:
            st.warning("Nenhum dado para exibir no gráfico de distribuição.")

    col_graf3, col_graf4 = st.columns(2)

    # Gráfico 3: Proporção dos tipos de trabalho
    with col_graf3:
        if not df_filtrado.empty:
            remoto_contagem = df_filtrado["remoto"].value_counts().reset_index()
            remoto_contagem.columns = ["tipo_trabalho", "quantidade"]

            grafico_remoto = px.pie(
                remoto_contagem,
                names="tipo_trabalho",
                values="quantidade",
                title="Proporção dos tipos de trabalho",
                hole=0.5
            )
            grafico_remoto.update_traces(textinfo="percent+label")
            grafico_remoto.update_layout(title_x=0.1)
            st.plotly_chart(grafico_remoto, width='stretch')
        else:
            st.warning("Nenhum dado para exibir no gráfico dos tipos de trabalho.")

    # Gráfico 4: Mapa salarial por país
    with col_graf4:
        if not df_filtrado.empty:
            df_ds = df_filtrado[df_filtrado["cargo"] == "Data Scientist"]

            if not df_ds.empty:
                media_ds_pais = df_ds.groupby("residencia_iso3")["usd"].mean().reset_index()

                grafico_paises = px.choropleth(
                    media_ds_pais,
                    locations="residencia_iso3",
                    color="usd",
                    color_continuous_scale="rdylgn",
                    title="Salário médio de Cientista de Dados por país",
                    labels={"usd": "Salário médio (USD)", "residencia_iso3": "País"}
                )
                grafico_paises.update_layout(title_x=0.1)
                st.plotly_chart(grafico_paises, width='stretch')
            else:
                st.info("Não há registros de 'Data Scientist' nos dados filtrados.")
        else:
            st.warning("Nenhum dado para exibir no gráfico de países.")


def render_tabela(df_filtrado):
    """Exibe a tabela com os dados filtrados."""
    st.subheader("Dados Detalhados")
    st.dataframe(df_filtrado)


def main():
    """Função principal que organiza a execução do dashboard."""
    configurar_pagina()
    df = carregar_dados()
    filtros = construir_filtros(df)
    df_filtrado = filtrar_dados(df, filtros)

    render_header(df_filtrado)
    render_kpis(df_filtrado)
    render_graficos(df_filtrado)
    render_tabela(df_filtrado)


if __name__ == "__main__":
    main()
