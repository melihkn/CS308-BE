import os

from fpdf import FPDF


pdf = FPDF()

with open("../invoices/INV-f88a4f5b-5463-449a-98f8-da0fc06c9b10.pdf", "r") as f:
    pdf.set_font("Arial", size=12)
    pdf.add_page()
    for line in f:
        pdf.cell(200, 10, txt=line, ln=True)