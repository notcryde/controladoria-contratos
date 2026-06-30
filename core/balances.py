import pandas as pd
import logging
from database.connection import get_connection

def get_authorization_summary(auth_number: str) -> dict:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute('SELECT start_date, end_date FROM authorizations WHERE authorization_number = ?', (auth_number,))
        auth_data = cursor.fetchone()
        
        cursor.execute('''
            SELECT SUM(quantity * unitary_value) 
            FROM authorization_items 
            WHERE authorization_number = ?
        ''', (auth_number,))
        initial_balance = cursor.fetchone()[0] or 0.0
        
        cursor.execute('''
            SELECT SUM(ii.quantity * ii.unitary_value) 
            FROM invoice_items ii 
            JOIN invoices i ON ii.invoice_number = i.invoice_number 
            WHERE i.authorization_number = ?
        ''', (auth_number,))
        executed_balance = cursor.fetchone()[0] or 0.0
        
        return {
            'start_date': auth_data['start_date'],
            'end_date': auth_data['end_date'],
            'initial_balance': initial_balance,
            'executed_balance': executed_balance
        }
    except Exception as e:
        logging.error(f'Erro ao buscar resumo da AF {auth_number}: {e}')
        return None
    finally:
        conn.close()

def build_items_dataframe(auth_number: str) -> pd.DataFrame:
    conn = get_connection()
    try:
        query_auth = '''
            SELECT material_code, 
                   SUM(quantity) as initial_quantity, 
                   SUM(quantity * unitary_value) as initial_value
            FROM authorization_items 
            WHERE authorization_number = ?
            GROUP BY material_code
        '''
        df_auth = pd.read_sql_query(query_auth, conn, params=(auth_number,))
        
        query_inv = '''
            SELECT i.invoice_number, 
                   ii.material_code, 
                   SUM(ii.quantity) as executed_quantity, 
                   SUM(ii.quantity * ii.unitary_value) as executed_value
            FROM invoice_items ii
            JOIN invoices i ON ii.invoice_number = i.invoice_number
            WHERE i.authorization_number = ?
            GROUP BY i.invoice_number, ii.material_code
            ORDER BY i.issue_date ASC
        '''
        df_inv = pd.read_sql_query(query_inv, conn, params=(auth_number,))
        
        rows = []
        if not df_auth.empty:
            for _, auth_row in df_auth.iterrows():
                material_code = auth_row['material_code']
                initial_quantity = auth_row['initial_quantity']
                initial_value = auth_row['initial_value']
                
                inv_matches = df_inv[df_inv['material_code'] == material_code]
                
                if inv_matches.empty:
                    rows.append({
                        'invoice_number': '-',
                        'material_code': material_code,
                        'initial_quantity': initial_quantity,
                        'initial_value': initial_value,
                        'executed_quantity': 0.0,
                        'executed_value': 0.0,
                        'balance_quantity': initial_quantity,
                        'balance_value': initial_value
                    })
                else:
                    current_qty_balance = initial_quantity
                    current_val_balance = initial_value
                    
                    for _, inv_row in inv_matches.iterrows():
                        executed_quantity = inv_row['executed_quantity']
                        executed_value = inv_row['executed_value']
                        
                        current_qty_balance -= executed_quantity
                        current_val_balance -= executed_value
                        
                        rows.append({
                            'invoice_number': inv_row['invoice_number'],
                            'material_code': material_code,
                            'initial_quantity': initial_quantity,
                            'initial_value': initial_value,
                            'executed_quantity': executed_quantity,
                            'executed_value': executed_value,
                            'balance_quantity': current_qty_balance,
                            'balance_value': current_val_balance
                        })
                        
        return pd.DataFrame(rows)
    except Exception as e:
        logging.error(f'Erro ao construir dataframe de itens: {e}')
        return pd.DataFrame()
    finally:
        conn.close()
