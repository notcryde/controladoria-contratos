import pandas as pd
import streamlit as st

from src.utils.database import load_data
from src.utils.render_table import render_table
from src.utils.constants import EXEC_NF_HEADERS, MODAL_ACOMP_EXEC_HEADERS


@st.dialog('Acompanhamento de Itens', width='large')
def modal_execucao_notas_fiscais(autorizacoes_fornecimento_id):
    st.write(f'Detalhamento de Itens da AF: **{autorizacoes_fornecimento_id}**')
    
    itens_autorizacoes_fornecimento = load_data('autorizacoes_itens')
    itens_notas_fiscais = load_data('notas_fiscais_itens')
    dataframe_notas_fiscais = load_data('notas_fiscais')
    
    if not itens_autorizacoes_fornecimento.empty:
        itens_autorizacoes_fornecimento = itens_autorizacoes_fornecimento[
            itens_autorizacoes_fornecimento['Nº AF'] == autorizacoes_fornecimento_id
        ]

        itens_autorizacoes_fornecimento.rename(columns={'Valor Total': 'Total Empenhado'}, inplace=True)
    else:
        itens_autorizacoes_fornecimento = pd.DataFrame(
            columns=[
                'Cód. Material', 
                'Descrição', 
                'Total Empenhado'
            ]
        )
        
    notas_fiscais_grouped = pd.DataFrame(columns=['Cód. Material', 'Total Executado'])
    
    if not dataframe_notas_fiscais.empty and not itens_notas_fiscais.empty:
        linked_notas_fiscais = dataframe_notas_fiscais[dataframe_notas_fiscais['Nº AF'] == autorizacoes_fornecimento_id]['Nº NF'].tolist()
        linked_itens_notas_fiscais = itens_notas_fiscais[itens_notas_fiscais['Nº NF'].isin(linked_notas_fiscais)]
        
        if not linked_itens_notas_fiscais.empty:
            notas_fiscais_grouped = linked_itens_notas_fiscais.groupby('Cód. Material')['Valor Executado'].sum().reset_index()
            notas_fiscais_grouped.rename(columns={'Valor Executado': 'Total Executado'}, inplace=True)
            
    merged = pd.merge(
        itens_autorizacoes_fornecimento[
            ['Cód. Material', 'Descrição', 'Total Empenhado']
        ], notas_fiscais_grouped, on='Cód. Material', how='left')
    
    merged['Total Executado'] = merged['Total Executado'].fillna(0.0)
    merged['Total Empenhado'] = merged['Total Empenhado'].fillna(0.0)
    merged['Saldo Atual'] = merged['Total Empenhado'] - merged['Total Executado']
    
    dataframe_final = merged[MODAL_ACOMP_EXEC_HEADERS]
    render_table(dataframe_final, MODAL_ACOMP_EXEC_HEADERS)
