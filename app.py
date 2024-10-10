import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Carregar os dados
@st.cache_data
def load_data():
    # Substitua isso pelo caminho real do seu arquivo Excel
    df = pd.read_excel("caminho_para_seu_arquivo.xlsx")
    return df

df = load_data()

st.title("Dashboard do Plano de Logística Sustentável - UFMS")

# Sidebar para seleção de categoria
categoria = st.sidebar.selectbox(
    "Escolha uma categoria",
    ["Educação Socioambiental", "Governança e Transparência", "Otimização de Recursos",
     "Material de Consumo", "Compras, Obras e Parcerias Sustentáveis", "Gestão de Resíduos",
     "Mobilidade e Acessibilidade"]
)

# Filtrar dados para a categoria selecionada
df_categoria = df[df['Categoria'] == categoria]

# Gráfico de pizza para distribuição de respostas
fig_pie = px.pie(df_categoria, names='Avaliação', values='Contagem', title=f'Distribuição de Respostas: {categoria}')
st.plotly_chart(fig_pie)

# Resumo das avaliações
st.subheader("Resumo das Avaliações")
resumo = df_categoria.groupby('Avaliação')['Contagem'].sum().reset_index()
st.table(resumo)

# Gráfico de barras para comparação entre categorias
df_comparacao = df.groupby(['Categoria', 'Avaliação'])['Contagem'].sum().unstack()
fig_bar = px.bar(df_comparacao, x=df_comparacao.index, y=['Positiva', 'Negativa', 'Neutra'],
                 title="Comparação entre Categorias",
                 labels={'value': 'Contagem', 'variable': 'Avaliação'})
st.plotly_chart(fig_bar)

# Nuvem de palavras para sugestões (assumindo que você tenha uma coluna 'Sugestões')
if 'Sugestões' in df.columns:
    st.subheader("Sugestões mais comuns")
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt

    texto_sugestoes = " ".join(df['Sugestões'].dropna())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(texto_sugestoes)

    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# Campo de texto para sugestões adicionais
st.subheader("Deixe sua sugestão")
sugestao = st.text_area("Sua sugestão para melhorias na sustentabilidade da UFMS:")
if st.button("Enviar Sugestão"):
    # Aqui você implementaria a lógica para salvar a sugestão
    st.success("Sugestão enviada com sucesso!")
