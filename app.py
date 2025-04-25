import streamlit as st
import pandas as pd


st.sidebar.header("📤 Enviar Planilha")
arquivo_excel = st.sidebar.file_uploader("Selecione o arquivo Excel", type=["xlsx"])

if arquivo_excel:
    df = pd.read_excel(arquivo_excel)

    st.sidebar.header("🔍 Filtros")

    colaboradores = ["Todos"] + sorted(df["Nome"].unique().tolist())
    produtos = ["Todos"] + sorted(df["Produto"].unique().tolist())

    filtro_nome = st.sidebar.selectbox("Filtrar por colaborador", colaboradores)
    filtro_produto = st.sidebar.selectbox("Filtrar por produto", produtos)

    if filtro_nome != "Todos":
        df = df[df["Nome"] == filtro_nome]

    if filtro_produto != "Todos":
        df = df[df["Produto"] == filtro_produto]

    pagina = st.sidebar.radio("📂 Navegar", ["📈 Progresso de Vendas", "🛒 Sell-Out por Produto"])

    def barra_progresso(valor, cor="#00BFFF"):
        valor_percentual = int(valor * 100)
        valor_limitado = min(valor_percentual, 100)
        st.markdown(f"""
            <div style="background-color: #e0e0e0; border-radius: 10px; height: 25px; position: relative;">
                <div style="width: {valor_limitado}%; background-color: {cor}; height: 100%; border-radius: 10px;"></div>
                <div style="position: absolute; width: 100%; text-align: center; top: 0; line-height: 25px;">
                    <strong>{valor_percentual}%</strong>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if pagina == "📈 Progresso de Vendas":
        st.title("📊 Painel de Vendas da Equipe")

        meta_total = df["Meta"].sum()
        vendas_total = df["Vendas"].sum()
        progresso_total = vendas_total / meta_total if meta_total > 0 else 0

        st.subheader("Progresso Geral da Equipe")
        barra_progresso(progresso_total, cor="#228B22")  

        st.subheader("Progresso Individual")
        for _, row in df.iterrows():
            progresso_individual = row["Vendas"] / row["Meta"] if row["Meta"] > 0 else 0
            st.write(f"👤 {row['Nome']}")
            barra_progresso(progresso_individual, cor="#1E90FF") 

    elif pagina == "🛒 Sell-Out por Produto":
        st.title("📦 Acompanhamento de Sell-Out")

        sellout = df.groupby("Produto")["SellOut"].sum().reset_index()

        for _, row in sellout.iterrows():
            st.write(f"🧴 {row['Produto']}: {row['SellOut']} unidades vendidas")

else:
    st.warning("🔁 Por favor, envie um arquivo Excel para começar.")

