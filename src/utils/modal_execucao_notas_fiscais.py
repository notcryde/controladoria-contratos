import pandas as pd
import streamlit as st
from src.utils.database import load_data
from src.utils.render_table import render_table
from src.utils.constants import MODAL_ACOMP_EXEC_HEADERS

@st.dialog('Acompanhamento de Itens', width='large')
def modal_execucao_notas_fiscais(autorizacoes_fornecimento_id):
    st.write(f'Detalhamento de Itens da AF: **{autorizacoes_fornecimento_id}**')
    
    itens_af = load_data('autorizacoes_itens')
    itens_nf = load_data('notas_fiscais_itens')
    df_notas_fiscais = load_data('notas_fiscais')
    
    if not itens_af.empty:
        itens_af = itens_af[itens_af['Nº AF'] == autorizacoes_fornecimento_id]
        itens_af = itens_af.rename(columns={
            'Valor Total': 'Valor Empenhado',
            'Qtde': 'Qtde Empenhado'
        })
    else:
        itens_af = pd.DataFrame(columns=['Cód. Material', 'Descrição', 'Qtde Empenhado', 'Valor Empenhado'])
        
    nf_agrupadas = pd.DataFrame(columns=['Cód. Material', 'Qtde Executado', 'Valor Executado'])
    
    if not df_notas_fiscais.empty and not itens_nf.empty:
        nfs_vinculadas = df_notas_fiscais[df_notas_fiscais['Nº AF'] == autorizacoes_fornecimento_id]['Nº NF'].tolist()
        itens_vinculados = itens_nf[itens_nf['Nº NF'].isin(nfs_vinculadas)]
        
        if not itens_vinculados.empty:
            nf_agrupadas = itens_vinculados.groupby('Cód. Material')[['Valor Executado', 'Qtde']].sum().reset_index()
            nf_agrupadas = nf_agrupadas.rename(columns={'Qtde': 'Qtde Executado'})
            
    merged = pd.merge(
        itens_af[['Cód. Material', 'Descrição', 'Qtde Empenhado', 'Valor Empenhado']], 
        nf_agrupadas, 
        on='Cód. Material', 
        how='left'
    )
    
    for col in ['Qtde Executado', 'Valor Executado', 'Qtde Empenhado', 'Valor Empenhado']:
        merged[col] = merged[col].fillna(0.0)
    
    merged['Saldo (Qtde)'] = merged['Qtde Empenhado'] - merged['Qtde Executado']
    merged['Saldo (Valor)'] = merged['Valor Empenhado'] - merged['Valor Executado']
    
    dataframe_final = merged[MODAL_ACOMP_EXEC_HEADERS]
    
    render_table(
        dataframe_final, 
        MODAL_ACOMP_EXEC_HEADERS,
        key=f"modal_exec_items_{autorizacoes_fornecimento_id}",
        export_name=f"detalhamento_itens_af_{autorizacoes_fornecimento_id.replace('/', '-')}"
    )