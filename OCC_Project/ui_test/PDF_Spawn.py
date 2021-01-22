from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('pingbold', 'PingBold.ttf'))
pdfmetrics.registerFont(TTFont('ping', 'ping.ttf'))
pdfmetrics.registerFont(TTFont('hv', 'Helvetica.ttf'))

# 生成PDF文件
class PDFGenerator:
    def __init__(self, filename):
        self.filename = filename
        self.file_path = '/'
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
                                       ('ALIGN', (0, 13), (3, 13), 'CENTER'),
                                       ('ALIGN', (0, 20), (3, 20), 'CENTER'),
                                       ('ALIGN', (0, 28), (3, 28), 'CENTER'),
                                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                       ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                       # 'SPAN' (列,行)坐标
                                       ('SPAN', (2, 0), (3, 0)),
                                       ('SPAN', (0, 1), (1, 1)),
                                       ('SPAN', (2, 1), (3, 1)),
                                       ('SPAN', (0, 2), (1, 2)),
                                       ('SPAN', (2, 2), (3, 2)),
                                       ('SPAN', (3, 3), (3, 12)),
                                       ('SPAN', (1, 7), (2, 7)),
                                       ('SPAN', (1, 12), (2, 12)),
                                       ('SPAN', (0, 13), (3, 13)),
                                       ('SPAN', (1, 14), (3, 14)),
                                       ('SPAN', (2, 15), (3, 15)),
                                       ('SPAN', (2, 16), (3, 16)),
                                       ('SPAN', (2, 17), (3, 17)),
                                       ('SPAN', (1, 18), (3, 18)),
                                       ('SPAN', (1, 19), (3, 19)),
                                       ('SPAN', (0, 20), (3, 20)),
                                       ('SPAN', (1, 21), (3, 21)),
                                       ('SPAN', (2, 22), (3, 22)),
                                       ('SPAN', (2, 23), (3, 23)),
                                       ('SPAN', (2, 24), (3, 24)),
                                       ('SPAN', (2, 25), (3, 25)),
                                       ('SPAN', (1, 26), (3, 26)),
                                       ('SPAN', (2, 27), (3, 27)),
                                       ('SPAN', (0, 28), (3, 28)),
                                       ('SPAN', (2, 29), (3, 29)),
                                       ('SPAN', (1, 30), (3, 30)),
                                       ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                       ])
        self.common_style = TableStyle([('FONTNAME', (0, 0), (-1, -1), 'ping'),
                                      ('FONTSIZE', (0, 0), (-1, -1), 12),
                                      ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                      ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                      ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                      ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                     ])

    def genTaskPDF(self, home_data, task_data, basic_data, case_set_data, fail_case_data, p0_case_data):
        story = []

        # 首页内容
        story.append(Spacer(1, 20 * mm))
        '''img = Image('./icons/3/newicon.png')
        img.drawHeight = 20 * mm
        img.drawWidth = 40 * mm
        img.hAlign = TA_LEFT
        story.append(img)
        story.append(Spacer(1, 10 * mm))
        story.append(Paragraph("测试报告", self.title_style))
        story.append(Spacer(1, 20 * mm))
        story.append(Paragraph("Test Report of XXX", self.sub_title_style))
        story.append(Spacer(1, 45 * mm))
        story.append(Paragraph("报告编号：" + home_data['report_code'], self.content_style))
        story.append(Paragraph("计划名称：" + home_data['task_name'], self.content_style))
        story.append(Paragraph("报告日期：" + home_data['report_date'], self.content_style))
        story.append(Paragraph(" 负责人：" + home_data['report_creator'], self.content_style))
        story.append(Spacer(1, 55 * mm))
        story.append(Paragraph("内部文档，请勿外传", self.foot_style))
        story.append(PageBreak())'''

        # 表格允许单元格内容自动换行格式设置
        stylesheet = getSampleStyleSheet()
        body_style = stylesheet["BodyText"]
        body_style.wordWrap = 'CJK'
        body_style.fontName = 'ping'
        body_style.fontSize = 12

        '''# 测试计划
        story.append(Paragraph("测试计划", self.table_title_style))
        story.append(Spacer(1, 3 * mm))
        task_table = Table(task_data, colWidths=[25 * mm, 141 * mm], rowHeights=12 * mm, style=self.common_style)
        story.append(task_table)

        story.append(Spacer(1, 10 * mm))'''

        # 基础参数
        #story.append(Paragraph("基础参数", self.sub_table_style))
        basic_table = Table(basic_data, colWidths=[45*mm, 61*mm, 40*mm, 55*mm], rowHeights=12 * mm, style=self.basic_style)
        story.append(basic_table)
        story.append(Spacer(1, 10 * mm))

        '''# 测试用例集
        story.append(Paragraph("用例集参数", self.sub_table_style))
        case_set_table = Table(case_set_data, colWidths=[25 * mm, 141 * mm], rowHeights=12 * mm, style=self.common_style)
        story.append(case_set_table)

        # story.append(PageBreak())
        story.append(Spacer(1, 15 * mm))

        # 失败用例--使用可以自动换行的方式需要data里都是str类型的才OK
        story.append(Paragraph("失败用例", self.table_title_style))
        story.append(Spacer(1, 3 * mm))
        para_fail_case_data = [[Paragraph(cell, body_style) for cell in row] for row in fail_case_data]
        fail_case_table = Table(para_fail_case_data, colWidths=[20 * mm, 35 * mm, 91 * mm, 20 * mm])
        fail_case_table.setStyle(self.common_style)
        story.append(fail_case_table)

        story.append(Spacer(1, 15 * mm))

        # 基础用例（P0）
        story.append(Paragraph("基础用例（P0）", self.table_title_style))
        story.append(Spacer(1, 3 * mm))
        para_p0_case_data = [[Paragraph(cell, body_style) for cell in row] for row in p0_case_data]
        p0_case_table = Table(para_p0_case_data, colWidths=[20 * mm, 35 * mm, 91 * mm, 20 * mm])
        p0_case_table.setStyle(self.common_style)
        story.append(p0_case_table)'''

        doc = SimpleDocTemplate(self.file_path + self.filename + ".pdf",
                                leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm)


        doc.build(story)

if __name__ == '__main__':
    pdf_generator = PDFGenerator('3DViewer')
    basic_data = [['封头校核', '计算单位', '压力容器计算软件', ''],
                ['计算标准', '', 'GB 150', ''],
                ['计算条件', '', '封头简图', ''],
                ['计算压力P', '3.10', 'MPa', ''],
                ['设计温度T', '100.00', '℃', ''],
                ['内径', '500', 'mm', ''],
                ['曲面深度 H', '150.00', 'mm', ''],
                ['材料', 'Q345R', '', ''],
                ['设计温度许用应力', '189.00', 'MPa', ''],
                ['试验温度许用应力', '189.00', 'MPa', ''],
                ['负偏差C1', '0.30', 'mm', ''],
                ['腐蚀裕量C2', '0.50', 'mm', ''],
                ['焊接接头系数', '1.00', '', ''],
                ['压力试验时应力校核', '', '', ''],
                ['压力试验类型', '液压试验', '', ''],
                ['试验压力值', '3.2000', 'MPa', ''],
                ['压力试验允许通过应力', '310.5', 'MPa', ''],
                ['试验压力下封头应力', '89.28', 'MPa', ''],
                ['校核条件', 'Q1<Q2', '', ''],
                ['校核结果', '合格', '', ''],
                ['厚度及重量计算', '', '', ''],
                ['形状系数', '0.7963', '', ''],
                ['计算厚度', '3.28', 'mm', ''],
                ['有效厚度', '7.20', 'mm', ''],
                ['最小厚度', '3.00', 'mm', ''],
                ['名义厚度', '8.00', 'mm', ''],
                ['结论', '满足最小厚度要求', '', ''],
                ['重量', '23.79', 'Kg', ''],
                ['压力计算', '', '', ''],
                ['最大允许工作压力', '6.7749', 'MPa', ''],
                ['结论', '合格', '', '']]
    pdf_generator.genTaskPDF([], [], basic_data, [], [], [])