import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from database.connection import get_connection

def get_af_numbers() -> list:
    """Busca a lista de todas as Autorizações de Fornecimento cadastradas."""
    conn = get_connection()
    try:
        query = "SELECT authorization_number FROM authorizations ORDER BY authorization_number DESC"
        df = pd.read_sql_query(query, conn)
        return df['authorization_number'].tolist()
    except Exception as e:
        logging.error(f"Erro ao buscar AFs: {e}")
        return []
    finally:
        conn.close()

def get_af_summary(auth_number: str) -> dict:
    """Calcula os saldos totais e recupera as datas da AF informada."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT start_date, end_date FROM authorizations WHERE authorization_number = ?", (auth_number,))
        auth_data = cursor.fetchone()
        
        cursor.execute("""
            SELECT SUM(quantity * unitary_value) 
            FROM authorization_items 
            WHERE authorization_number = ?
        """, (auth_number,))
        init_val = cursor.fetchone()[0] or 0.0
        
        cursor.execute("""
            SELECT SUM(ii.quantity * ii.unitary_value) 
            FROM invoice_items ii 
            JOIN invoices i ON ii.invoice_number = i.invoice_number 
            WHERE i.authorization_number = ?
        """, (auth_number,))
        exec_val = cursor.fetchone()[0] or 0.0
        
        return {
            'start_date': auth_data['start_date'],
            'end_date': auth_data['end_date'],
            'initial_balance': init_val,
            'executed_balance': exec_val
        }
    except Exception as e:
        logging.error(f"Erro ao buscar resumo da AF {auth_number}: {e}")
        return None
    finally:
        conn.close()

def build_items_dataframe(auth_number: str) -> pd.DataFrame:
    """Constrói o dataframe detalhado cruzando os itens da AF com as NFs vinculadas."""
    conn = get_connection()
    try:
        query_af = """
            SELECT material_code, 
                   SUM(quantity) as qtde_inicial, 
                   SUM(quantity * unitary_value) as valor_inicial
            FROM authorization_items 
            WHERE authorization_number = ?
            GROUP BY material_code
        """
        df_af = pd.read_sql_query(query_af, conn, params=(auth_number,))
        
        query_nf = """
            SELECT i.invoice_number, 
                   ii.material_code, 
                   SUM(ii.quantity) as qtde_executada, 
                   SUM(ii.quantity * ii.unitary_value) as valor_executado
            FROM invoice_items ii
            JOIN invoices i ON ii.invoice_number = i.invoice_number
            WHERE i.authorization_number = ?
            GROUP BY i.invoice_number, ii.material_code
            ORDER BY i.issue_date ASC
        """
        df_nf = pd.read_sql_query(query_nf, conn, params=(auth_number,))
        
        rows = []
        if not df_af.empty:
            for _, af_row in df_af.iterrows():
                mat_code = af_row['material_code']
                q_init = af_row['qtde_inicial']
                v_init = af_row['valor_inicial']
                
                nf_matches = df_nf[df_nf['material_code'] == mat_code]
                
                if nf_matches.empty:
                    rows.append({
                        'Nº NF': '-',
                        'Cód. Material': mat_code,
                        'Qtde Inicial': q_init,
                        'Valor Inicial': v_init,
                        'Qtde Executada': 0.0,
                        'Valor Executado': 0.0,
                        'Saldo (Qtde)': q_init,
                        'Saldo (Valor)': v_init
                    })
                else:
                    current_q_saldo = q_init
                    current_v_saldo = v_init
                    
                    for _, nf_row in nf_matches.iterrows():
                        q_exec = nf_row['qtde_executada']
                        v_exec = nf_row['valor_executado']
                        
                        current_q_saldo -= q_exec
                        current_v_saldo -= v_exec
                        
                        rows.append({
                            'Nº NF': nf_row['invoice_number'],
                            'Cód. Material': mat_code,
                            'Qtde Inicial': q_init,
                            'Valor Inicial': v_init,
                            'Qtde Executada': q_exec,
                            'Valor Executado': v_exec,
                            'Saldo (Qtde)': current_q_saldo,
                            'Saldo (Valor)': current_v_saldo
                        })
                        
        return pd.DataFrame(rows)
    except Exception as e:
        logging.error(f"Erro ao construir dataframe de itens: {e}")
        return pd.DataFrame()
    finally:
        conn.close()

def format_currency(value: float) -> str:
    """Formata valor flutuante para o padrão monetário brasileiro."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def render():
    st.header("Acompanhamento de Saldos")
    
    af_list = get_af_numbers()
    
    if not af_list:
        st.info("Não há Autorizações de Fornecimento cadastradas no sistema.")
        return
        
    selected_af = st.selectbox(
        "Selecione o Nº da AF", 
        af_list,
        key="select_balance_af"
    )
    
    if selected_af:
        summary = get_af_summary(selected_af)
        
        if summary:
            saldo_atual = summary['initial_balance'] - summary['executed_balance']
            
            hoje = datetime.now().date()
            data_inicial_dt = datetime.strptime(summary['start_date'], "%Y-%m-%d").date()
            data_final_dt = datetime.strptime(summary['end_date'], "%Y-%m-%d").date()
            prazo_restante = (data_final_dt - hoje).days
            
            st.markdown("### Resumo Financeiro")
            col1, col2, col3 = st.columns(3)
            col1.metric("Saldo Inicial", format_currency(summary['initial_balance']))
            col2.metric("Saldo Executado", format_currency(summary['executed_balance']))
            col3.metric("Saldo Atual", format_currency(saldo_atual))
            
            st.markdown("### Prazos e Vigência")
            col4, col5, col6 = st.columns(3)
            col4.metric("Data Inicial", data_inicial_dt.strftime("%d/%m/%Y"))
            col5.metric("Data Final", data_final_dt.strftime("%d/%m/%Y"))
            col6.metric("Prazo Restante", f"{prazo_restante} dias")
            
            st.markdown("### Totalidade Unitária de Itens")
            df_items = build_items_dataframe(selected_af)
            
            if not df_items.empty:
                df_display = df_items.copy()
                currency_cols = ['Valor Inicial', 'Valor Executado', 'Saldo (Valor)']
                for col in currency_cols:
                    df_display[col] = df_display[col].apply(format_currency)
                
                st.dataframe(df_display, use_container_width=True, hide_index=True)
            else:
                st.warning("Não foi possível carregar os itens desta Autorização.")