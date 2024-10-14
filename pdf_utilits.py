import os
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

def generate_document(db_helper, order_id):
    documents_dir = "documents"
    if not os.path.exists(documents_dir):
        os.makedirs(documents_dir) 

    db_helper.cursor.execute("SELECT last_name, first_name, middle_name, phone, emailFROM orders WHERE id = ?", (order_id,))
    order = db_helper.cursor.fetchone()
    last_name, first_name, middle_name, phone, email = order

    item_query = """
    SELECT component_name, price, quantity
    FROM order_items
    WHERE order_id = ?
    """
    db_helper.cursor.execute(item_query, (order_id,))
    items = db_helper.cursor.fetchall()

    total_price = sum(item[1] * item[2] for item in items)

    pdf_file_path = os.path.join(documents_dir,  f"Заказ_{last_name}_{first_name}.pdf")
    doc = SimpleDocTemplate(pdf_file_path, page_size=letter)
    elements = []

    pdfmetrics.registerFont(TTFont('Arial', 'Arial.ttf'))

    styles = getSampleStyleSheet()
    header_style = ParagraphStyle(name="HeaderStyle", fontSize=16, fontName="Arial", alignment=1)
    title_style = ParagraphStyle(name="TitleStyle", fontSize=14, fontName="Arial", alignment=1)
    normal_style = styles['Normal']
    normal_style.fontName = "Arial"
    normal_style.fontSize = 12

    header = Paragraph("Технический центр <<ТехноПрогресс>>", header_style)
    elements.append(header)
    elements.append(Paragraph("<br/><br/>", normal_style))

    elements.append(Paragraph(f"Адрес: ул. Молдавских партизан, 13, Электросинегорск, республика Украина(в составе России)", normal_style))
    elements.append(Paragraph(f"Телефон: +7 (123) 456_7890", normal_style))
    elements.append(Paragraph(f"Email: pasha@techno-raper.ru", normal_style))
    elements.append(Paragraph("<br/>Дата: {}". format(datetime.today().strftime('%d-%m-%Y')), normal_style))
    elements.append(Paragraph("<br/><br/>", normal_style))

    title = Paragraph(f"Заказ №{order_id}", title_style)
    elements.append(title)
    elements.append(Paragraph(f"Клиент: {last_name} {first_name} {middle_name}", normal_style))
    elements.append(Paragraph(f"Телефон: {phone}", normal_style))
    elements.append(Paragraph(f"Email: {email}", normal_style))
    elements.append(Paragraph("<br/><br/><br/>", normal_style))

    data = [["№", "Компонент", "Цена", "Кол-во"]]
    for index, item in enumerate(items, start=1):
        component_name, price, quantity = item
        data.append([str(index), component_name, f"{price} руб.", str(quantity)])

    data.append(["", "", "Итоговая цена:", f"{total_price} руб."])

    table = Table(data, colWidth=[30, 200, 80, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), '#d3d3d3'),
        ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ('FONT', (0, 0), (-1, -1), 'Arial', 10),
        ('backgound', (-1, -1), (-1, -1), '#f2f2f2'),
    ]))

    elements.append(table)
    elements.append(Paragraph("<br/><br/>", normal_style))

    elements.append(Paragraph("Место печати", normal_style))
    elements.append(Paragraph("______________________________", normal_style))

    elements.append(Paragraph("<br/><br/>", normal_style))
    signature_table = Table([
        ["Подпись менеджера:", "Подпись клиента:"],
        ["______________________________", "______________________________"],
        ["Менеджер по продажам:", "Клиент:"],
    ], colWidth=[250, 250])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONT', (0, 0), (-1, -1), 'Arial', 12)
    ]))
    elements.append(signature_table)

    elements.append(Paragraph("<br/><br/><br/>", normal_style))
    elements.append(Paragraph(f"Юридическая информация:", normal_style))
    elements.append(Paragraph(f"Общество с ограниченной ответсвенностью <<ТехноПрогресс>>", normal_style))
    elements.append(Paragraph(f"ИНН: 1234567890", normal_style))
    elements.append(Paragraph(f"КПП: 1234567456", normal_style))
    elements.append(Paragraph(f"Юридический адрес: ул. Молдавских партизан, 13, Электросинегорск, республика Украина(в составе России)", normal_style))

    doc.build(elements)

    print(f"Документ для заказа {order_id} создан: {pdf_file_path}")


        