import streamlit as st
import pandas as pd
import io

# Configuração da Página (Título e Ícone da Aba)
st.set_page_config(page_title="Limpador de Dados Pro", page_icon="🧹", layout="centered")

# --- FUNÇÃO 1: A FERRAMENTA (Sua lógica de limpeza fica aqui) ---
def mostrar_ferramenta():
    st.title("🧰 Sua Área de Trabalho")
    st.info(f"Logado com a chave: {st.session_state['chave_acesso']}")
    
    # Botão de Sair
    if st.button("Sair / Logout"):
        st.session_state['logado'] = False
        st.rerun()
        
    st.markdown("---")
    
    # --- SEU CÓDIGO DE LIMPEZA ORIGINAL COMEÇA AQUI ---
    arquivo = st.file_uploader("Carregue seu arquivo Excel ou CSV", type=["xlsx", "csv"])

    if arquivo is not None:
        try:
            if arquivo.name.endswith('.csv'):
                df = pd.read_csv(arquivo)
            else:
                df = pd.read_excel(arquivo)

            st.subheader("Prévia dos Dados")
            st.dataframe(df.head())

            if st.button("Processar Arquivo"):
                # Simulação da limpeza (Insira sua lógica completa aqui)
                # Exemplo rápido para teste:
                colunas_texto = df.select_dtypes(include=['object']).columns
                for col in colunas_texto:
                    df[col] = df[col].astype(str).str.upper().str.strip()
                
                st.success("Limpeza Concluída!")
                
                # Conversão para download
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    df.to_excel(writer, index=False)
                    
                st.download_button(
                    label="📥 Baixar Excel Limpo",
                    data=buffer,
                    file_name="dados_limpos.xlsx",
                    mime="application/vnd.ms-excel"
                )

        except Exception as e:
            st.error(f"Erro ao processar: {e}")
    # --- FIM DO CÓDIGO DE LIMPEZA ---

# --- FUNÇÃO 2: A PÁGINA DE VENDAS (Vitrine) ---
def mostrar_pagina_vendas():
    st.title("🚀 Pare de perder tempo no Excel")
    st.markdown("### A solução definitiva para higienização de dados corporativos.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **O que nosso robô faz por você:**
        * ✅ **Padroniza Nomes:** Remove espaços e ajusta maiúsculas.
        * ✅ **Valida CPFs:** Remove pontos e traços automaticamente.
        * ✅ **Sanitiza E-mails:** Prepara listas para marketing.
        
        Tudo isso sem armazenar seus dados. **Privacidade Total.**
        """)
        st.markdown("---")
        st.metric(label="Linhas Processadas", value="150.000+")
        
    with col2:
        # Aqui você pode colocar uma imagem ou vídeo depois
        st.info("💡 Ideal para Escritórios de Advocacia, Clínicas e RH.")
        
        st.markdown("### Apenas R$ 49,90 / ano")
        st.link_button("👉 Comprar Acesso Agora", "https://link.mercadopago.com.br/SEU_LINK_AQUI")

# --- CONTROLE PRINCIPAL (O Maestro) ---
def main():
    # Inicializa a variável de sessão se não existir
    if 'logado' not in st.session_state:
        st.session_state['logado'] = False

    # BARRA LATERAL (Sidebar) para Login
    with st.sidebar:
        if not st.session_state['logado']:
            st.header("Área do Cliente")
            chave_digitada = st.text_input("Insira sua Chave de Acesso", type="password")
            
            if st.button("Entrar"):
                # --- VALIDAÇÃO DA SENHA ---
                # Por enquanto está fixo. Depois conectaremos ao Google Sheets aqui.
                if chave_digitada == "CLIENTE-VIP": 
                    st.session_state['logado'] = True
                    st.session_state['chave_acesso'] = chave_digitada
                    st.rerun() # Recarrega a página para mostrar a ferramenta
                else:
                    st.error("Chave inválida!")
        else:
            st.write("✅ Status: Conectado")

    # DECISÃO DO QUE MOSTRAR NA TELA
    if st.session_state['logado']:
        mostrar_ferramenta()
    else:
        mostrar_pagina_vendas()

if __name__ == "__main__":
    main()
