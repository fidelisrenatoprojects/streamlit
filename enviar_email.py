import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def enviar_email_comprovante(pdf_path, destinatario_email):
    try:
        remetente_email = "fidelisrenatoprojects@gmail.com"
        senha = "Chatbot_procon"

        # Configuração do email
        msg = MIMEMultipart()
        msg['From'] = remetente_email
        msg['To'] = destinatario_email
        msg['Subject'] = "Resumo da sua reclamação"
        
        # Anexar o PDF
        with open(pdf_path, "rb") as pdf_file:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(pdf_file.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(pdf_path)}")
            msg.attach(part)

        # Enviar o email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(remetente_email, senha)
            server.sendmail(remetente_email, destinatario_email, msg.as_string())

        print("PDF enviado com sucesso via Email!")
        return True
    except Exception as e:
        print(f"Erro ao enviar PDF via Email: {e}")
        return False

if __name__ == "__main__":
    # Caminho do PDF e email destinatário
    pdf_path = "C:/Users/fidelisrenato/AGENTES/chatbot_streamlit/resumo_reclamacoes.pdf"
    destinatario_email = "destinatario@example.com"
    
    # Chama a função para enviar o PDF
    enviar_email_comprovante(pdf_path, destinatario_email)
