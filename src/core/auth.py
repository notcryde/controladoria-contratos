import streamlit as st

def render_login():
    st.title('Login - SEDIS Controladoria')
    
    with st.form('login_form'):
        username = st.text_input('Usuário')
        password = st.text_input('Senha', type='password')
        submit_button = st.form_submit_button('Entrar')
        
        if submit_button:
            if username == 'admin' and password == 'admin':
                st.session_state.is_user_logged_in = True
                st.success('Login realizado com sucesso!')
                st.rerun()
            else:
                st.error('Usuário ou senha incorretos')

def handle_logout():
    st.session_state.is_user_logged_in = False
    st.rerun()