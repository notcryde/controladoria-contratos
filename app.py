import streamlit as st
from database.connection import init_db

@st.cache_resource
def setup_environment():
    init_db()

setup_environment()

st.set_page_config(
    page_title='Controladoria de Contratos - PMT',
    page_icon=':material/bar_chart:',
    layout='wide'
)

st.title('Sistema de Controladoria de Contratos')

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    'Solicitações', 
    'Empenhos', 
    'Autorizações', 
    'Notas Fiscais',
    'Acompanhamento de Saldos'
])

with tab1:
    import ui.tab_requests
    ui.tab_requests.render()

with tab2:
    import ui.tab_commitments
    ui.tab_commitments.render()

with tab3:
    import ui.tab_authorizations
    ui.tab_authorizations.render()

with tab4:
    import ui.tab_invoices
    ui.tab_invoices.render()
    
with tab5:
    import ui.tab_balances
    ui.tab_balances.render()
    
