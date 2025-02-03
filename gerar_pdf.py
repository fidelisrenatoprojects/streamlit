from fpdf import FPDF

def gerar_resumo_pdf(reclamacoes):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for idx, rec in enumerate(reclamacoes, start=1):
        pdf.cell(200, 10, txt=f"Reclamação {idx}", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Nome: {rec[0]}", ln=True)
        pdf.cell(200, 10, txt=f"CPF: {rec[1]}", ln=True)
        pdf.cell(200, 10, txt=f"email: {rec[2]}", ln=True)
        pdf.cell(200, 10, txt=f"Data de Nascimento: {rec[3]}", ln=True)
        pdf.cell(200, 10, txt=f"Telefone: {rec[4]}", ln=True)
        pdf.cell(200, 10, txt=f"Endereço: {rec[5]}", ln=True)
        pdf.cell(200, 10, txt=f"Produto: {rec[6]}", ln=True)
        pdf.cell(200, 10, txt=f"Nota Fiscal: {rec[7]}", ln=True)
        pdf.cell(200, 10, txt=f"Descrição do Problema: {rec[9]}", ln=True)
        pdf.cell(200, 10, txt="-" * 50, ln=True)

    pdf_path = "resumo_reclamacoes.pdf"
    pdf.output(pdf_path)
    return pdf_path