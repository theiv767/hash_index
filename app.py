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

        # Armazenar as configurações no estado da sessão
        st.session_state.df = df
        st.session_state.numero_buckets = numero_buckets
        st.session_state.tamanho_buckets = tamanho_buckets
        st.session_state.tamanho_paginas = tamanho_paginas

        # Botão "Aplicar"
        if st.button("Aplicar"):
            fields = df.columns.tolist()
            bucket_size = tamanho_buckets
            page_size = tamanho_paginas

            # Cria a instância da tabela e do bucket
            table = Table(fields, primary_key, page_size)
            bucket = Bucket(numero_buckets, bucket_size, table)

            # Itera sobre as linhas do DataFrame e adiciona os valores
            for _, row in df.iterrows():
                # Converte a linha para dicionário e remove espaços em branco
                row_dict = {k: v.strip() if isinstance(v, str) else v for k, v in row.to_dict().items()}

                # Adiciona a tupla ao bucket
                bucket.add_value(row_dict)

            # Salvar a tabela e o bucket no estado da sessão
            st.session_state.table = table
            st.session_state.bucket = bucket

            st.write("Configuração aplicada com sucesso!")

#---------------------------------------------------------------

with tab2:
    st.title("Visualização de Dados")

    if 'bucket' in st.session_state:
        valor_chave = st.text_input("Digite o valor da chave primária:")

        if st.button("Buscar Tupla"):
            bucket = st.session_state.bucket
            resultado = bucket.get_record(valor_chave)

            if resultado:
                st.write("Tupla encontrada:", resultado)
            else:
                st.write("Tupla não encontrada.")
    else:
        st.write("Por favor, faça o upload do arquivo e configure os buckets na aba 'Upload e Configuração'.")