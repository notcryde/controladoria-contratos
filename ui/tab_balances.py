import streamlit as st

from datetime import datetime


from utils.formatters import format_currency
from utils.headers import BALANCES_HEADERS

import core.authorizations as auth
import core.balances as bal

def render():
    st.header('Acompanhamento de Saldos')
    
    authorizations = auth.get_all()
    
    if authorizations.empty:
        st.info('Não há Autorizações de Fornecimento cadastradas no sistema.')
        return
        
    auth_number = st.selectbox(
        'Selecione o Nº da AF', 
        authorizations,
        key='slb_balance_auth_number'
    )
    
    if auth_number:
        summary = bal.get_authorization_summary(auth_number)
        
        if summary:
            current_balance = summary['initial_balance'] - summary['executed_balance']
            
            today = datetime.now().date()
            start_date = datetime.strptime(summary['start_date'], '%Y-%m-%d').date()
            end_date = datetime.strptime(summary['end_date'], '%Y-%m-%d').date()
            remaining_days = (end_date - today).days
            
            st.markdown('### Resumo Financeiro')

            col1, col2, col3 = st.columns(3)

            col1.metric('Saldo Inicial', format_currency(summary['initial_balance']))
            col2.metric('Saldo Executado', format_currency(summary['executed_balance']))
            col3.metric('Saldo Atual', format_currency(current_balance))
            
            st.markdown('### Prazos e Vigência')

            col4, col5, col6 = st.columns(3)
            
            col4.metric('Data Inicial', start_date.strftime('%d/%m/%Y'))
            col5.metric('Data Final', end_date.strftime('%d/%m/%Y'))
            col6.metric('Prazo Restante', f'{remaining_days} dias')
            
            st.markdown('### Totalidade Unitária de Itens')
            df_items = bal.build_items_dataframe(auth_number)
            
            if not df_items.empty:
                df_display = df_items.copy()
                
                currency_cols = ['initial_value', 'executed_value', 'balance_value']
                for col in currency_cols:
                    df_display[col] = df_display[col].apply(format_currency)
                
                df_display = df_display.rename(columns=BALANCES_HEADERS)
                st.dataframe(df_display, width='stretch', hide_index=True)
            else:
                st.warning('Não foi possível carregar os itens desta Autorização.')