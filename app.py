import streamlit as st
import google.generativeai as genai
import mercadopago
import time

# Configurações de Segurança da Página
st.set_page_config(page_title="Axé - Portal de Alta Magia", layout="centered")

# --- BLOQUEIO DE SCREENSHOT/COMPARTILHAMENTO (CSS INJETADO) ---
st.markdown("""
    <style>
    @media print {
        body { display: none !important; }
    }
    body {
        -webkit-user-select: none;
        -moz-user-select: none;
        -ms-user-select: none;
        user-select: none;
    }
    </style>
    <script>
    document.addEventListener('keyup', (e) => {
        if (e.key == 'PrintScreen') {
            navigator.clipboard.writeText('');
            alert('Capturas de tela são proibidas neste portal sagrado.');
        }
    });
    </script>
    """, unsafe_allow_globals=True)

# --- INICIALIZAÇÃO DE APIs ---
try:
    genai.configure(api_key=st.secrets["api_key"])
    sdk = mercadopago.SDK(st.secrets["MP_TOKEN"])
except Exception as e:
    st.error("Erro na configuração das chaves. Verifique os Secrets.")

# --- SISTEMA DE LOGIN E VERIFICAÇÃO ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def login():
    st.title("🛡️ Acesso Restrito - Portal Axé")
    st.subheader("Verificação de Identidade")
    
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    captcha = st.checkbox("Eu sou humano (Verificação Anti-Bot)")

    if st.button("Entrar"):
        if captcha and usuario == "admin" and senha == "axe2026": # Você pode mudar a senha aqui
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Credenciais inválidas ou falha na verificação humana.")

# --- CONTEÚDO PRINCIPAL (SÓ APARECE APÓS LOGIN) ---
if not st.session_state.autenticado:
    login()
else:
    st.title("✨ Oráculo Axé")
    st.write("Bem-vindo ao ambiente seguro. Suas consultas são privadas.")
    
    pergunta = st.text_input("Faça sua pergunta ao Oráculo:")
    
    if st.button("Consultar"):
        if pergunta:
            with st.spinner("Consultando as energias..."):
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(pergunta)
                st.write("---")
                st.markdown(f"### Resposta do Oráculo:")
                st.write(response.text)
                st.info("Este conteúdo é privado. Proibido compartilhar com terceiros.")
        else:
            st.warning("Por favor, digite uma pergunta.")

    if st.sidebar.button("Sair"):
        st.session_state.autenticado = False
        st.rerun()
