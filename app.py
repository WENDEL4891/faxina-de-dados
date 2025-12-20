# app.py
import streamlit as st
import pandas as pd
import io

# 1. Configuração da Página (Título, Ícone)
st.set_page_config(page_title="Faxina de Dados", page_icon="🧹")

# 2. Interface Visual (Frontend)
st.title("🧹 Faxina de Dados Automática")
st.markdown("""
Sua planilha está bagunçada? 
Suba seu arquivo Excel ou CSV abaixo e nossa IA (na verdade, Python puro) vai:
- ✅ Padronizar Nomes (Maiúsculas/Minúsculas)
- ✅ Limpar CPFs (Apenas números)
- ✅ Padronizar E-mails (Minúsculas)
""")

# 3. Botão de Upload
arquivo = st.file_uploader("Carregue seu arquivo aqui", type=["xlsx", "csv"])

# 4. A Lógica (Só roda se tiver arquivo)
if arquivo is not None:
    try:
        # Lê o arquivo (detecta se é Excel ou CSV)
        if arquivo.name.endswith('.csv'):
            df = pd.read_csv(arquivo)
        else:
            df = pd.read_excel(arquivo)

        st.subheader("🔍 Visualizando os Dados Sujos (Amostra)")
        st.dataframe(df.head())

        # Botão para processar
        if st.button("Iniciar Faxina"):
            
            # --- SUA LÓGICA AQUI (Versão Pandas) ---
            # Tratamento de erro caso a coluna não exista
            colunas = df.columns.str.lower() # facilita a busca
            
            # Limpeza de Nomes (se achar coluna parecida com 'nome')
            cols_nome = [c for c in colunas if 'nome' in c]
            if cols_nome:
                col = cols_nome[0] # pega a primeira que achou
                # Remove espaços extras e coloca em Title Case
                df[col] = df[col].astype(str).str.strip().str.replace(r'\s+', ' ', regex=True).str.title()
                st.success(f"Coluna '{col}' padronizada!")

            # Limpeza de CPF (se achar coluna parecida com 'cpf')
            cols_cpf = [c for c in colunas if 'cpf' in c]
            if cols_cpf:
                col = cols_cpf[0]
                # Remove tudo que não é dígito
                df[col] = df[col].astype(str).str.replace(r'\D', '', regex=True)
                st.success(f"Coluna '{col}' limpa (apenas números)!")

            # Limpeza de Email (se achar coluna parecida com 'email')
            cols_email = [c for c in colunas if 'email' in c or 'e-mail' in c]
            if cols_email:
                col = cols_email[0]
                df[col] = df[col].astype(str).str.lower().str.replace(' ', '')
                st.success(f"Coluna '{col}' normalizada!")

            st.markdown("---")
            st.subheader("✨ Dados Limpos e Prontos")
            st.dataframe(df.head())

            # 5. Botão de Download
            # Converte o DataFrame de volta para CSV na memória
            csv_convertido = df.to_csv(index=False).encode('utf-8')
            
            st.download_button(
                label="📥 Baixar Planilha Limpa",
                data=csv_convertido,
                file_name="dados_limpos.csv",
                mime="text/csv",
            )
            
    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

# Rodapé
st.markdown("---")
st.caption("Desenvolvido com Python e Streamlit")
