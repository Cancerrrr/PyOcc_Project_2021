import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, LongTable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('pingbold', 'PingBold.ttf'))
pdfmetrics.registerFont(TTFont('ping', 'ping.ttf'))
pdfmetrics.registerFont(TTFont('hv', 'Helvetica.ttf'))

# 生成PDF文件
class PDFGenerator:
    def __init__(self, filename, cylinder_parameter={}):
        self.cylinder_parameter = cylinder_parameter
        self.filename = filename
        self.file_path = 'F:/pycharm_project/PyOcc_Project_2021/OCC_Project/pdf_spawn/'
        self.title_style = ParagraphStyle(name="TitleStyle", fontName="pingbold", fontSize=48, alignment=TA_LEFT,)
        self.sub_title_style = ParagraphStyle(name="SubTitleStyle", fontName="hv", fontSize=32,
                                              textColor=colors.HexColor(0x666666), alignment=TA_LEFT, )
        self.content_style = ParagraphStyle(name="ContentStyle", fontName="ping", fontSize=18, leading=25, spaceAfter=20,
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.foot_style = ParagraphStyle(name="FootStyle", fontName="ping", fontSize=14, textColor=colors.HexColor(0xB4B4B4),
                                         leading=25, spaceAfter=20, alignment=TA_CENTER, )
        self.table_title_style = ParagraphStyle(name="TableTitleStyle", fontName="pingbold", fontSize=20, leading=25,
                                                spaceAfter=10, alignment=TA_LEFT, )
        self.sub_table_style = ParagraphStyle(name="SubTableTitleStyle", fontName="ping", fontSize=16, leading=25,
                                                spaceAfter=10, alignment=TA_LEFT, )
        self.basic_style = TableStyle([('FONTNAME', (0, 0), (-1, -1), 'ping'),
                                       ('FONTSIZE', (0, 0), (-1, -1), 12),
                                       ('ALIGN', (0, 0), (3, 2), 'CENTER'),
                                       ('ALIGN', (0, 12), (3, 12), 'CENTER'),
                                       ('ALIGN', (0, 18), (3, 18), 'CENTER'),
                                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                       ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                       # 'SPAN' (列,行)坐标
                                       ('SPAN', (2, 0), (3, 0)),
                                       ('SPAN', (1, 1), (3, 1)),
                                       ('SPAN', (0, 2), (1, 2)),
                                       ('SPAN', (2, 2), (3, 2)),
                                       ('SPAN', (3, 3), (3, 11)),
                                       ('SPAN', (1, 7), (2, 7)),
                                       ('SPAN', (1, 11), (2, 11)),
                                       ('SPAN', (0, 12), (3, 12)),
                                       ('SPAN', (1, 13), (2, 13)),
                                       ('SPAN', (1, 14), (2, 14)),
                                       ('SPAN', (1, 15), (2, 15)),
                                       ('SPAN', (1, 16), (3, 16)),
                                       ('SPAN', (1, 17), (3, 17)),
                                       ('SPAN', (0, 18), (3, 18)),
                                       ('SPAN', (1, 19), (2, 19)),
                                       ('SPAN', (1, 20), (2, 20)),
                                       ('SPAN', (1, 21), (2, 21)),
                                       ('SPAN', (1, 22), (3, 22)),
                                       ('SPAN', (1, 23), (3, 23)),
                                       ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                       ])
        self.common_style = TableStyle([('FONTNAME', (0, 0), (-1, -1), 'ping'),
                                      ('FONTSIZE', (0, 0), (-1, -1), 12),
                                      ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                      ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ])
        img = Image('./icons/TT.png')
        img.drawWidth = 2 * inch
        img.drawHeight = 1.5 * inch
        R = float(self.cylinder_parameter['internal_diameter'])  # 壳体内径
        t = float(self.cylinder_parameter['thickness']) # 设计厚度
        L = float(self.cylinder_parameter['Length'])  # 筒体长度
        cylinder_pressure = float(self.cylinder_parameter['pressure'])  # 设计压力
        cylinder_temperature = float(self.cylinder_parameter['temperature'])  # 设计温度
        cylinder_corrosion = float(self.cylinder_parameter['corrosion'])  # 腐蚀系数
        cylinder_welding = float(self.cylinder_parameter['welding'])  # 焊接系数

        t_min1 = (cylinder_pressure*R)/(148*cylinder_welding-0.6*cylinder_pressure) # 最小厚度t
        t_e = t - cylinder_corrosion # 有效厚度
        P_MAWP1 = 148*cylinder_welding*t_e/(R+0.6*t_e) # 最大许用工作压力1

        t_min2 = cylinder_pressure*R/(2*148*cylinder_welding+0.4*cylinder_pressure) # 计算厚度
        P_MAWP2 = 2*148*cylinder_welding*t_e/(R-0.4*t_e) # 最大许用工作压力2

        t_min = max(t_min1, t_min2) # 最终-最小厚度
        P_MAWP = min(P_MAWP1, P_MAWP2) # 最终-许用工作压力

        P_MAPNC = 148*cylinder_welding*t/(R+0.6*t) # 最大许用工作压力
        P_Sact = (cylinder_pressure*(R+0.6*t_e))/(cylinder_welding*t_e) # 最大许用应力计算




        check1 = ''
        check2 = ''

        if t >= t_min and t_min > 0:
            check1 = '合格'
        else:
            check1 = '不合格'


        if P_MAWP >= cylinder_pressure and 140*cylinder_welding >= P_Sact:
            check2 = '合格'
        else:
            check2 = '不合格'


        self.basic_data = [['内压圆筒校核', '计算单位', '压力容器专用计算软件', ''],
                      ['计算标准', 'ASME VIII-1', '', ''],
                      ['计算条件', '', '简图', ''],
                      ['计算压力P', cylinder_pressure, 'MPa', img],
                      ['设计温度T', cylinder_temperature, '℃', ''],
                      ['设计厚度tn', t, 'mm', ''],
                      ['内半径', R, 'mm', ''],
                      ['材料', 'Q245R(板材)', '', ''],
                      ['最大许用应力S', '148.00', 'MPa', ''],
                      ['设计温度许用应力St', '140.00', 'MPa', ''],
                      ['腐蚀裕量C', cylinder_corrosion, 'mm', ''],
                      ['焊接接头系数E', cylinder_welding, '', ''],
                      ['厚度计算', '', '', ''],
                      ['计算厚度t', str(t_min), '', 'mm'],
                      ['有效厚度te', str(t_e), '', 'mm'],
                      ['设计厚度tn', str(t), '', 'mm'],
                      ['校核条件', 'tn>t', '', ''],
                      ['结论', check1, '', ''],
                      ['压力及应力计算', '', '', ''],
                      ['最大允许工作压力', str(P_MAWP), '', 'MPa'],
                      ['最大许用压力', str(P_MAPNC), '', 'MPa'],
                      ['最大许用应力', str(P_Sact), '', 'MPa'],
                      ['校核条件', 'StE>=P_Sact P_MAWP>= P', '', ''],
                      ['结论', check2, '', ''], ]





    def genTaskPDF(self):
        story = []


        # 表格允许单元格内容自动换行格式设置
        stylesheet = getSampleStyleSheet()
        body_style = stylesheet["BodyText"]
        body_style.wordWrap = 'CJK'
        body_style.fontName = 'ping'
        body_style.fontSize = 12



        # 基础参数
        #story.append(Paragraph("基础参数", self.sub_table_style))
        basic_table = Table(self.basic_data, colWidths=None , rowHeights=None, style=self.basic_style)
        story.append(basic_table)
        #story.append(Spacer(1, 10 * mm))



        #doc = SimpleDocTemplate(self.file_path + self.filename + ".pdf",
                                #leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm)
        doc = SimpleDocTemplate(self.file_path + self.filename + ".pdf", leftSpace=37 * mm, rightMargin=15 * mm, pagesize = A4)
        doc.build(story)

'''if __name__ == '__main__':
    cylinder_parameter = {'pressure': '5.8',
                'temperature': '100',
                'corrosion': '3.00',
                'welding': '1.00',
                'internal_diameter': '1000.00',
                'thickness': '55',
                'Length': '500'}

    pdf_generator = PDFGenerator('Cylinder_Report', cylinder_parameter)
    pdf_generator.genTaskPDF()'''