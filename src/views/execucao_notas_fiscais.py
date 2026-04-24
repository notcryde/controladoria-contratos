import streamlit as st
import pandas as pd

from src.utils.modal_execucao_notas_fiscais import modal_execucao_notas_fiscais
from src.utils.database import load_data
from src.utils.render_table import render_table
from src.utils.constants import EXEC_NF_HEADERS
from src.utils.calcular_prazo import calcular_prazo

st.subheader('Execução de Notas Fiscais')

if 'modal_id_autorizacao_fornecimento' not in st.session_state:
    st.session_state.modal_id_autorizacao_fornecimento = None
if 'execucao_aggrid_key' not in st.session_state:
    st.session_state.execucao_aggrid_key = 0

st.markdown('''
    <style>
    div[data-testid='stDialog'] div[role='dialog'] {
        max-width: 75vw !important;
    }
    </style>
    ''', unsafe_allow_html=True)

if st.session_state.modal_id_autorizacao_fornecimento:
    modal_execucao_notas_fiscais(st.session_state.modal_id_autorizacao_fornecimento)
    st.session_state.modal_id_autorizacao_fornecimento = None

autorizacoes_fornecimento_dataframe = load_data('autorizacoes')
notas_fiscais_dataframe = load_data('notas_fiscais')

execucao_notas_fiscais_data = []
if not autorizacoes_fornecimento_dataframe.empty:
    for _, autorizacao_fornecimento in autorizacoes_fornecimento_dataframe.iterrows():
        numero_autorizacao_fornecimento = autorizacao_fornecimento.get('Nº AF', '')
        total_empenho = autorizacao_fornecimento.get('Valor Empenhado', 0.0)
        if pd.isna(total_empenho): total_empenho = 0.0
        
        total_execucao = 0.0
        if not notas_fiscais_dataframe.empty and 'Nº AF' in notas_fiscais_dataframe.columns:
            linked_notas_fiscais = notas_fiscais_dataframe[notas_fiscais_dataframe['Nº AF'] == numero_autorizacao_fornecimento]
            total_execucao = linked_notas_fiscais['Valor Executado'].sum()
            
        saldo = total_empenho - total_execucao
        
        prazo = calcular_prazo(
            autorizacao_fornecimento.get('Vigência Inicial', ''), 
            autorizacao_fornecimento.get('Vigência Final', ''))
        
        execucao_notas_fiscais_data.append({
            'Nº AF': numero_autorizacao_fornecimento,
            'Total Empenhado': total_empenho,
            'Total Executado': total_execucao,
            'Saldo Atual': saldo,
            'Prazo': prazo
        })

dataframe_execucao_notas_fiscais = pd.DataFrame(
    execucao_notas_fiscais_data, 
    columns=EXEC_NF_HEADERS[:-1] if execucao_notas_fiscais_data else EXEC_NF_HEADERS
)

_, selected_rows = render_table(
    dataframe_execucao_notas_fiscais, 
    EXEC_NF_HEADERS, 
    enable_selection=True, 
    key=f'exec_grid_{st.session_state.execucao_aggrid_key}'
)

if selected_rows is not None and len(selected_rows) > 0:
    if isinstance(selected_rows, pd.DataFrame):
        autorizacoes_fornecimento_id = selected_rows.iloc[0]['Nº AF']
    else:
        autorizacoes_fornecimento_id = selected_rows[0]['Nº AF']
        
    st.session_state.modal_id_autorizacao_fornecimento = autorizacoes_fornecimento_id
    st.session_state.execucao_aggrid_key += 1
    st.rerun()