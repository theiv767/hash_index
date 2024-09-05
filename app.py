import streamlit as st
import pandas as pd
from scripts.structures import *


def process_file(file):
    df = pd.read_csv(file)
    return df

st.title("Configuração de buffer e páginas")

#----------------------------------------------------------------


tab1, tab2 = st.tabs(["Upload e Configuração", "Visualização de Dados"])

with tab1:
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

    if uploaded_file is not None:

        primary_key = st.text_input("Nome da Primary key")

        numero_buckets = st.number_input("Número de Buckets", min_value=1, value=1)
        tamanho_buckets = st.number_input("Tamanho dos Buckets", min_value=1, value=1)
        tamanho_paginas = st.number_input("Tamanho das Páginas", min_value=1, value=1)

        df = process_file(uploaded_file)

        st.write("Aqui estão as primeiras linhas do arquivo carregado:")
        st.write(df.head())

        # Mostrar os valores das variáveis
        st.write(f"Número de Buckets: {numero_buckets}")
        st.write(f"Tamanho dos Buckets: {tamanho_buckets}")
        st.write(f"Tamanho das Páginas: {tamanho_paginas}")

        # Adicionar dadoos Bucketsdo
        st.session_state.df = df
        st.session_state.numero_buckets = numero_buckets
        st.session_state.tamanho_buckets = tamanho_buckets
        st.session_state.tamanho_paginas = tamanho_paginas

        # Botão "Aplicar"
        if st.button("Aplicar"):
            fields = df.columns.tolist()
            print(fields)
            primary_key = primary_key
            bucket_size = tamanho_buckets
            page_size = tamanho_paginas

            table = Table(fields, primary_key, page_size)
            bucket = Bucket(numero_buckets, bucket_size, table)


            for _, row in df.iterrows():
                row_dict = row.to_dict()
                print(row_dict)
                bucket.add_value(row_dict)

            st.session_state.table = table
            st.session_state.bucket = bucket

            st.write("Configuração aplicada com sucesso!")

# Aba 2: Visualização de Dados
with tab2:
    if 'df' in st.session_state:
        df = st.session_state.df
        
        st.write("Selecione as colunas que deseja visualizar:")
        selected_columns = st.multiselect("Colunas", options=df.columns.tolist(), default=df.columns.tolist())

        if selected_columns:
            st.write(df[selected_columns])
        else:
            st.write("Nenhuma coluna selecionada.")
    else:
        st.write("Por favor, carregue um arquivo na aba 'Upload e Configuração' primeiro.")

    if st.button("Buscar"):
        pass
