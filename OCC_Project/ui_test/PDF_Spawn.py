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
    def __init__(self, filename):

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
                                       ('ALIGN', (0, 0), (5, 0), 'CENTER'),
                                       ('ALIGN', (0, 2), (5, 2), 'CENTER'),
                                       ('ALIGN', (0, 22), (5, 22), 'CENTER'),
                                       ('ALIGN', (0, 31), (5, 31), 'CENTER'),
                                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                       ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                       # 'SPAN' (列,行)坐标
                                       ('SPAN', (3, 0), (5, 0)),
                                       ('SPAN', (0, 0), (1, 0)),
                                       ('SPAN', (0, 1), (2, 1)),
                                       ('SPAN', (3, 1), (5, 1)),
                                       ('SPAN', (0, 2), (2, 2)),
                                       ('SPAN', (3, 2), (5, 2)),
                                       ('SPAN', (3, 3), (5, 3)),
                                       ('SPAN', (3, 4), (5, 4)),
                                       ('SPAN', (3, 5), (5, 5)),
                                       ('SPAN', (1, 5), (2, 5)),
                                       ('SPAN', (3, 6), (5, 6)),
                                       ('SPAN', (1, 6), (2, 6)),
                                       ('SPAN', (3, 7), (5, 7)),
                                       ('SPAN', (1, 7), (2, 7)),
                                       ('SPAN', (3, 8), (5, 8)),
                                       ('SPAN', (3, 9), (5, 9)),
                                       ('SPAN', (3, 10), (5, 10)),
                                       ('SPAN', (3, 11), (5, 11)),
                                       ('SPAN', (3, 12), (5, 12)),
                                       ('SPAN', (3, 13), (5, 13)),
                                       ('SPAN', (0, 13), (1, 13)),
                                       ('SPAN', (3, 3), (5, 13)),
                                       ('SPAN', (4, 14), (5, 14)),
                                       ('SPAN', (4, 15), (5, 15)),
                                       ('SPAN', (4, 16), (5, 16)),
                                       ('SPAN', (4, 17), (5, 17)),
                                       ('SPAN', (0, 18), (0, 19)),
                                       ('SPAN', (1, 18), (1, 19)),
                                       ('SPAN', (2, 18), (2, 19)),
                                       ('SPAN', (0, 22), (5, 22)),
                                       ('SPAN', (0, 31), (5, 31)),
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
        basic_table = Table(basic_data, colWidths=None , rowHeights=None, style=self.basic_style)
        story.append(basic_table)
        #story.append(Spacer(1, 10 * mm))

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

        #doc = SimpleDocTemplate(self.file_path + self.filename + ".pdf",
                                #leftMargin=20 * mm, rightMargin=20 * mm, topMargin=20 * mm, bottomMargin=20 * mm)
        doc = SimpleDocTemplate(self.file_path + self.filename + ".pdf", leftSpace=37 * mm, rightMargin=15 * mm, pagesize = A4)
        doc.build(story)

if __name__ == '__main__':
    pdf_generator = PDFGenerator('3DViewer')
    img = Image('./icons/TTKT.png')
    img.drawWidth = 4*inch
    img.drawHeight = 2.5*inch
    basic_data = [['开孔补强计算', '', '计算单位', '压力容器计算软件', '', ''],
                ['接管:N1', '', '', '计算方法:ASME VIII-1', '', ''],
                ['设计条件', '', '', '简图', '', ''],
                ['计算压力P', '5.8', 'MPa', img, '', ''],
                ['设计温度T', '100.00', '℃', '', '', ''],
                ['壳体型式', '圆形筒体', '', '', '', ''],
                ['壳体材料名称及类型', 'Q245R', '', '', '', ''],
                ['焊接接头系数E', '1', '', '', '', ''],
                ['壳体内直径Di', '1000', 'mm', '', '', ''],
                ['壳体开孔处公称厚度t', '35', 'mm', '', '', ''],
                ['壳体厚度负偏差C1', '0.00', 'mm', '', '', ''],
                ['壳体腐蚀裕量C2', '3', 'mm', '', '', ''],
                ['壳体材料许用应力', '140', 'MPa', '', '', ''],
                ['接管轴线与筒体表面法线夹角', '', '0', '', '', ''],
                ['接管实际外伸长度', '300', 'mm', '接管连接型式', '插入式接管壁安放在容器壁上', ''],
                ['接管实际内伸长度', '0', 'mm', '接管材料', 'Q245R', ''],
                ['接管壁公称厚度', '1', 'mm', '名称及类型', '板材', ''],
                ['接管内半径', '3', 'mm', '补强圈材料名称', '', ''],
                ['接管腐蚀裕量C2t', '', 'mm', '补强圈宽度', '', 'mm'],
                ['', '', '', '补强圈厚度', '', 'mm'],
                ['接管厚度负偏差C1t', '0', 'mm', '补强圈厚度负偏差C1r', '', 'mm'],
                ['接管材料许用应力', '140', 'MPa', '补强圈许用应力', '' ,'mm'],
                ['开孔补强计算', '', '', '', '', ''],
                ['沿容器壁补强范围', '71', 'mm', '最大局部一次薄膜应力', '1', 'MPa'],
                ['伸出在容器外表面沿接管壁补强范围', '21.250', 'mm', '平均一次薄膜应力', '1.3749', 'MPa'],
                ['伸入在容器内表面沿接管壁补强范围', '0', 'mm', '总体一次薄膜应力', '1', 'MPa'],
                ['壳体有效半径', '71', 'mm', '壳体有效厚度', '211', 'mm'],
                ['接管有效外伸长度', '49.85', 'mm', '接管有效内伸长度', '0', 'mm'],
                ['接管开口处有效总面积', '1502', 'mm^2', '内压在壳体上引起的力', '1519', 'mm'],
                ['内压在容器外侧接管上引起的力', '3053', 'N', '内压引起的不连续的力', '100', 'mm^2'],
                ['许用应力', '', 'MPa', '接管最大许用应力', '100', 'mm^2'],
                ['结论:合格', '', '', '']]
    pdf_generator.genTaskPDF([], [], basic_data, [], [], [])