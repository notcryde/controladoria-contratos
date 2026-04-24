import streamlit as st
import sqlite3
from src.utils.constants import (
    LABEL_TIPO_DOC, TIPOS_DOCS,
    LABEL_NUM_PROC,
    LABEL_UPLOAD_SECTION,
    LABEL_SOLIC_VINC,
    LABEL_TIPO_SOLIC,
    LABEL_SELEC_SOLIC,
    LABEL_VIG_INICIAL,
    LABEL_VIG_FINAL,
    TIPOS_SOLIC,
    LABEL_BTN_UPLOAD
)
from src.utils.regex_patterns import (
    REGEX_SOLIC_CONS, REGEX_SOLIC_COMPR, EMP_PATTERNS, AF_PATTERNS, NF_PATTERNS
)
from src.core.database import save_document, get_solicitacoes_por_tipo
from src.utils.pdf_parser import process_files

DOCUMENT_MAPPING = {
    'Solicitação de Consumo': ('solicitacoes_consumo', REGEX_SOLIC_CONS),
    'Solicitação de Compras': ('solicitacoes_compras', REGEX_SOLIC_COMPR),
    'Empenho': ('empenhos', EMP_PATTERNS),
    'Autorização de Fornecimento': ('autorizacoes', AF_PATTERNS),
    'Nota Fiscal': ('notas_fiscais', NF_PATTERNS)
}

st.header('Upload de Documentos')

current_document_type = st.session_state.get("document_type_selection", TIPOS_DOCS[0])
is_request_type = current_document_type in ['Solicitação de Consumo', 'Solicitação de Compras']

input_numero_processo = ""
input_vigencia_inicial = ""
input_vigencia_final = ""
input_numero_solicitacao = ""

if is_request_type:
    col_type, col_proc = st.columns(2)
    with col_type:
        st.selectbox(LABEL_TIPO_DOC, TIPOS_DOCS, key="document_type_selection")
    with col_proc:
        input_numero_processo = st.text_input(LABEL_NUM_PROC)
else:
    st.selectbox(LABEL_TIPO_DOC, TIPOS_DOCS, key="document_type_selection")

    if current_document_type == 'Empenho':
        has_linked_request = st.session_state.get("linked_request_state", 'Sim')
        
        if has_linked_request == 'Sim':
            col_toggle, col_req_type = st.columns(2)
            with col_toggle:
                st.selectbox(LABEL_SOLIC_VINC, ['Sim', 'Não'], key="linked_request_state")
            with col_req_type:
                tipo_solicitacao = st.selectbox(LABEL_TIPO_SOLIC, TIPOS_SOLIC, key="request_type_selection")
            
            lista_solicitacoes = get_solicitacoes_por_tipo(tipo_solicitacao)
            if not lista_solicitacoes:
                lista_solicitacoes = ["Nenhuma solicitação encontrada"]
                
            input_numero_solicitacao = st.selectbox(LABEL_SELEC_SOLIC, lista_solicitacoes)
        else:
            st.selectbox(LABEL_SOLIC_VINC, ['Sim', 'Não'], key="linked_request_state")

    elif current_document_type == 'Autorização de Fornecimento':
        col_start, col_end = st.columns(2)
        with col_start:
            input_vigencia_inicial = st.text_input(LABEL_VIG_INICIAL)
        with col_end:
            input_vigencia_final = st.text_input(LABEL_VIG_FINAL)

files_buffer = st.file_uploader(
    LABEL_UPLOAD_SECTION,
    type=['pdf'],
    accept_multiple_files=True
)

if files_buffer:
    if st.button(LABEL_BTN_UPLOAD):
        table_name, regex_patterns = DOCUMENT_MAPPING[current_document_type]
        extra_data = {}

        if is_request_type and input_numero_processo:
            extra_data['Nº Processo'] = input_numero_processo
            
        elif current_document_type == 'Empenho' and input_numero_solicitacao and input_numero_solicitacao != "Nenhuma solicitação encontrada":
            extra_data['Nº Solicitação'] = input_numero_solicitacao
            
        elif current_document_type == 'Autorização de Fornecimento':
            extra_data['Vigência Inicial'] = input_vigencia_inicial
            extra_data['Vigência Final'] = input_vigencia_final

        try:
            process_files(files_buffer, regex_patterns, save_document, table_name, extra_data)
            st.success("Arquivos processados e salvos com sucesso!")
        except sqlite3.IntegrityError:
            st.error("Erro de vínculo: O documento base mencionado neste arquivo ainda não foi cadastrado. Faça o upload do documento anterior (Empenho ou Autorização) primeiro.")
        except Exception as e:
            st.error(f"Erro inesperado ao processar o arquivo: {e}")