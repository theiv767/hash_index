import streamlit as st
import pandas as pd
import math
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
        df = process_file(uploaded_file)
        

        primary_key = st.text_input("Nome da Primary key", placeholder="O valor padrão é a primeira coluna...")


        bucket_size = st.number_input("Tamanho dos Buckets", min_value=1, value=1)
        page_size = st.number_input("Tamanho das Páginas", min_value=1, value=1)
        num_buckets = math.ceil( len(df)/bucket_size )
        num_pages = math.ceil( len(df)/page_size )
        
        st.write("Preview - primeiras linhas do arquivo carregado:")
        st.write(df.head())
    

        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Configurações:")
            st.write(f"Número de Buckets: {num_buckets}")
            st.write(f"Tamanho dos Buckets: {bucket_size}")
            st.write(f"Tamanho das Páginas: {page_size}")


        st.session_state.df             = df
        st.session_state.num_buckets    = num_buckets
        st.session_state.num_pages      = num_pages
        st.session_state.bucket_size    = bucket_size
        st.session_state.page_size      = page_size

        if st.button("Aplicar"):

            if primary_key == '':
                primary_key = df.columns[0]

            fields = df.columns.tolist()
            #bucket_size = bucket_size
            #page_size = page_size

            table = Table(fields, primary_key, num_pages, page_size)
            bucket = Bucket(num_buckets, bucket_size, table)

            for _, row in df.iterrows():
                row_dict = {k: v.strip() if isinstance(v, str) else v for k, v in row.to_dict().items()}
                bucket.add_tuple(row_dict)

            st.session_state.table  = table
            st.session_state.bucket = bucket

            with col2:
                num_colisions = bucket.get_num_colisions()
                num_overflows = bucket.get_num_overflows()
                print(num_colisions)
                print(num_overflows)

                st.markdown("<p style='color:MediumSeaGreen;'>Estatísticas:</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:MediumSeaGreen;'>Número de Colisões: {num_colisions}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='color:MediumSeaGreen;'>Número de overflows: {num_overflows}</p>", unsafe_allow_html=True)


            st.markdown("<p style='color:MediumSeaGreen;'>Configuração aplicada com sucesso!</p>", unsafe_allow_html=True)

#---------------------------------------------------------------

with tab2:
    st.title("Visualização de Dados")

    if 'bucket' in st.session_state:
        valor_chave = st.text_input("Digite o valor da chave primária:")

        if st.button("Buscar Tupla"):
            bucket  = st.session_state.bucket

            resultado, page_index, num_accessed_pages   = bucket.get_tuple(valor_chave)
            _, _, num_accessed_pages_seq_search         = bucket.get_tuple_seq_search(valor_chave)

            if resultado:
                st.write("Tupla encontrada:", resultado)
                st.write("ID da página em memória:", page_index)
                st.write("Número de páginas acessadas usando busca hash:", num_accessed_pages, "    |    ", "Número páginas acessadas usando busca sequencial:", num_accessed_pages_seq_search)
            else:
                st.write("Tupla não encontrada.")
    else:
        st.write("Por favor, faça o upload do arquivo e configure os buckets na aba 'Upload e Configuração'.")