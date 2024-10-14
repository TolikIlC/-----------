import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

def generate_report(order):
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir)

        client_name = f"{order['surname']}_{order['first_name']}"
        pdf_filename = f"{documents_dir}/{client_name}_order_{order['id']}.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

        styles = getSampleStyleSheet()
        normal_style = styles['Normal']
        normal_style.fontName = 'Arial'
        normal_style.fontSize = 12

        elements = []

        header = Paragraph("Технический центр <<ТехноПрогресс>>", ParagraphStyle(name='HeaderStyle', fontSize=16, fontName='Arial', alignment=1))
        elements.append(header)
        elements.append(Paragraph("<br/><br/>", normal_style))

        elements.append(Paragraph(f"Адрес: ул. Молдавских партизан, 13, Электросинегорск, республика Украина(в составе России)", normal_style))
        elements.append(Paragraph(f"Телефон: +7 (123) 456_7890", normal_style))
        elements.append(Paragraph(f"Email: pasha@techno-raper.ru", normal_style))
        elements.append(Paragraph("<br/>Дата: {}". format(datetime.today().strftime('%d-%m-%Y')), normal_style))
        elements.append(Paragraph("<br/><br/>", normal_style))

        elements.append(Paragraph(f"Заявка №: {order['id']}", normal_style))
        elements.append(Paragraph(f"Фамилия: {order['surname']}", normal_style))
        elements.append(Paragraph(f"Имя: {order['first_name']}", normal_style))
        elements.append(Paragraph(f"Отчество: {order['patronymic']}", normal_style))
        elements.append(Paragraph(f"Комплектующие: {order['components']}", normal_style))

        elements.append(Paragraph(f"Заявка №{order['id']}", normal_style))
        elements.append(Paragraph(f"Фамилия: {order['surname']}", normal_style))
        elements.append(Paragraph(f"Имя: {order['first_name']}", normal_style))
        elements.append(Paragraph(f"Отчество: {order['patronymic']}", normal_style))
        elements.append(Paragraph(f"Комплектующие: {order['components']}", normal_style))
        elements.append(Paragraph(f"Описание проблемы: {order['problem_description']}", normal_style))
        elements.append(Paragraph(f"Телефон: {order['phone']}", normal_style))
        elements.append(Paragraph(f"Email: {order['email']}", normal_style))
        elements.append(Paragraph(f"Ожидаемая дата завершения:{order['expected_completion_date']}", normal_style))
        elements.append(Paragraph(f"Статус:{order['status']}", normal_style))



        elements.append(Paragraph("<br/><br/>", normal_style))
        
        signature_table = Table([["Подпись менеджера:", "Подпись клиента:" ],
                                ["_________________________", "______________________"],
                                ["Менеджер по продажам", "Клиент"]],
                                colWidths=[250, 250])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1, -1), 'CENTER')
            ('VALIGN', (0,0), (-1, -1), 'MIDDLE')
            ('FONT', (0,0), (-1, -1), 'Arial', 12)
        ]))
        elements.append(signature_table)

        elements.append(Paragraph("<br/><br/>", normal_style))
        elements.append(Paragraph("Юридическая информация", normal_style))
        elements.append(Paragraph("ООО ТехноПргоресс", normal_style))
        elements.append(Paragraph("ИНН: 123456789", normal_style))
        elements.append(Paragraph("КПП: 987654321", normal_style))
        elements.append(Paragraph("ОГРН: 1234567893645", normal_style))
        elements.append(Paragraph("Юридический адрес: ул. Примерная, 1, Москва, Россия", normal_style))

        doc.build(elements)

        print(f"Документ для заказа {order['id']} создан: {pdf_filename}")
        
