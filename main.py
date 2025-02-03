import streamlit as st
import re
import datetime
from database import salvar_reclamacao  # Importa a função para salvar no banco
from gerar_pdf import gerar_resumo_pdf  # Importa a função para gerar o PDF
from enviar_email import enviar_email_comprovante  # Importa a função para enviar o PDF por email
import streamlit.components.v1 as components

# Função para validar CPF
def validar_cpf(cpf):
    return re.fullmatch(r"\d{3}\.\d{3}\.\d{3}-\d{2}", cpf) is not None

# Função para validar telefone
def validar_telefone(telefone):
    return re.fullmatch(r"\(\d{2}\) \d{5}-\d{4}", telefone) is not None

# Função para validar email
def validar_email(email):
    return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email) is not None

# Função para validar nota fiscal
def validar_nota_fiscal(nota):
    return re.fullmatch(r"\d+", nota) is not None

# Função para validar nome
def validar_nome(nome):
    return re.fullmatch(r"[A-Za-zÀ-ÿ ]+", nome) is not None

# Título da aplicação Streamlit
st.title("Registro de Reclamações - PROCON")

# Definir intervalo de datas
ano_atual = datetime.datetime.now().year

# Sessão para armazenar reclamações enviadas
if "reclamacoes_enviadas" not in st.session_state:
    st.session_state.reclamacoes_enviadas = []

# Formulário para entrada de dados
with st.form("reclamacao_form"):
    nome = st.text_input("Nome", value="")
    cpf = st.text_input("CPF (Formato: 000.000.000-00)", value="")
    email = st.text_input("Email", value="")
    data_nascimento = st.date_input("Data de Nascimento", min_value=datetime.date(1900, 1, 1), max_value=datetime.date(ano_atual, 12, 31), format="DD/MM/YYYY")
    telefone = st.text_input("Telefone (Formato: (00) 00000-0000)", value="")
    endereco = st.text_area("Endereço", value="")
    produto = st.text_input("Produto", value="")
    nota_fiscal = st.text_input("Número da Nota Fiscal", value="")
    documento = st.file_uploader("Comprovante ou Documentação. (Formatos aceitos: PDF, JPG, PNG)", type=["pdf", "jpg", "png"])
    descricao = st.text_area("Descrição do Problema", value="")
    confirmar = st.form_submit_button("Enviar Reclamação")

    if confirmar:
        erros = []
        if not validar_nome(nome):
            erros.append("Nome inválido. Use apenas letras e espaços.")
        if not validar_cpf(cpf):
            erros.append("CPF inválido. Use o formato 000.000.000-00.")
        if not validar_email(email):
            erros.append("Email inválido.")
        if not validar_telefone(telefone):
            erros.append("Telefone inválido. Use o formato (00) 00000-0000.")
        if nota_fiscal and not validar_nota_fiscal(nota_fiscal):
            erros.append("Número da Nota Fiscal inválido. Use apenas números.")
        if nota_fiscal and not documento:
            erros.append("É necessário anexar um documento quando há uma nota fiscal.")
        if documento and documento.size > 2 * 1024 * 1024:
            erros.append("O documento deve ter no máximo 2MB.")
        if not descricao.strip():
            erros.append("A descrição do problema não pode estar vazia.")

        if erros:
            for erro in erros:
                st.error(erro)
        else:
            documento_bytes = documento.read() if documento else None
            dados = (nome, cpf, email, str(data_nascimento), telefone, endereco, produto, nota_fiscal, documento_bytes, descricao)
            salvar_reclamacao(dados)
            st.session_state.reclamacoes_enviadas.append(dados)
            st.success("Reclamação registrada com sucesso! Você pode enviar outra reclamação se desejar.")
            st.rerun()

# Exibir reclamações enviadas
if st.session_state.reclamacoes_enviadas:
    st.subheader("Reclamações enviadas:")
    for idx, rec in enumerate(st.session_state.reclamacoes_enviadas, start=1):
        st.text(f"{idx}. {rec[6]} - {rec[9]}")
    
    # Botão para gerar PDF e enviar por email
    if st.button("Enviar resumo por Email"):
        pdf_path = gerar_resumo_pdf(st.session_state.reclamacoes_enviadas)
        enviar_email_comprovante(pdf_path, email)
        st.success("Resumo enviado por Email!")
