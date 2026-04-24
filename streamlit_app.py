import streamlit as st

st.set_page_config(layout="wide", page_title="SEDIS Controladoria")

from src.utils.auth import render_login, handle_logout
from src.utils.database import initialize_database

initialize_database()

if 'is_user_logged_in' not in st.session_state:
    st.session_state.is_user_logged_in = False

login = st.Page(render_login, title='Log in', icon=':material/login:')
logout = st.Page(handle_logout, title='Log out', icon=':material/logout:')

gestao_documental = st.Page('src/views/gestao_documental.py', title='Gestão Documental', icon=':material/dashboard:', default=True)
execucao_notas_fiscais = st.Page('src/views/execucao_notas_fiscais.py', title='Execução de Notas Fiscais', icon=':material/description:')
uploads = st.Page('src/views/uploads.py', title='Uploads', icon=':material/receipt_long:')

if st.session_state.is_user_logged_in:
    navigation_router = st.navigation(
        [
            uploads,
            gestao_documental, 
            execucao_notas_fiscais, 
            logout,
        ]
    )
else:
    navigation_router = st.navigation([login])

navigation_router.run()