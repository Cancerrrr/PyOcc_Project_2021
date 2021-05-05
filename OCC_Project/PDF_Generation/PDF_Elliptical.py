import math
import latexify
import reportlab
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, LongTable
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm, inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import tkinter as tk
from tkinter import filedialog

#需要宋体字体
pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttc'))


# 生成PDF文件
class PDFGenerator:
    def __init__(self, elliptical_parameter={}):
        root = tk.Tk()
        root.withdraw()
        Folderpath = filedialog.asksaveasfilename()  # 获得选择好的文件夹
        self.elliptical_parameter = elliptical_parameter
        self.file_path = Folderpath
        self.title_style = ParagraphStyle(name="TitleStyle", fontName="simsun", fontSize=48, alignment=TA_LEFT, )
        self.sub_title_style = ParagraphStyle(name="SubTitleStyle", fontName="simsun", fontSize=32,
                                              textColor=colors.HexColor(0x666666), alignment=TA_LEFT, )
        self.content_style = ParagraphStyle(name="ContentStyle", fontName="simsun", fontSize=18, leading=25,
                                            spaceAfter=20,
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.foot_style = ParagraphStyle(name="FootStyle", fontName="simsun", fontSize=14,
                                         textColor=colors.HexColor(0xB4B4B4),
                                         leading=25, spaceAfter=20, alignment=TA_CENTER, )
        self.table_title_style = ParagraphStyle(name="TableTitleStyle", fontName="simsun", fontSize=20, leading=25,
                                                spaceAfter=10, alignment=TA_LEFT, )
        self.sub_table_style = ParagraphStyle(name="SubTableTitleStyle", fontName="simsun", fontSize=16, leading=25,
                                              spaceAfter=10, alignment=TA_LEFT, )
        self.basic_style = TableStyle([('FONTNAME', (0, 0), (-1, -1), 'simsun'),
                                       ('FONTSIZE', (0, 0), (-1, -1), 12),
                                       ('ALIGN', (0, 0), (3, 2), 'CENTER'),
                                       ('ALIGN', (0, 13), (3, 13), 'CENTER'),
                                       ('ALIGN', (0, 20), (3, 20), 'CENTER'),
                                       ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                       ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                       # 'SPAN' (列,行)坐标
                                       ('SPAN', (0, 0), (1, 0)),
                                       ('SPAN', (0, 1), (2, 1)),
                                       ('SPAN', (0, 2), (2, 2)),
                                       ('SPAN', (3, 3), (3, 12)),
                                       ('SPAN', (1, 7), (2, 7)),
                                       ('SPAN', (1, 12), (2, 12)),
                                       ('SPAN', (0, 13), (3, 13)),
                                       ('SPAN', (1, 14), (3, 14)),
                                       ('SPAN', (2, 15), (3, 15)),
                                       ('SPAN', (2, 16), (3, 16)),
                                       ('SPAN', (2, 17), (3, 17)),
                                       ('SPAN', (2, 18), (3, 18)),
                                       ('SPAN', (1, 19), (3, 19)),
                                       ('SPAN', (0, 20), (3, 20)),
                                       ('SPAN', (2, 21), (3, 21)),
                                       ('SPAN', (1, 22), (3, 22)),
                                       ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                       ])
        self.common_style = TableStyle([('FONTNAME', (0, 0), (-1, -1), 'simsun'),
                                        ('FONTSIZE', (0, 0), (-1, -1), 12),
                                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                                        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                                        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
                                        ])
        img = Image('../icons/Elliptical.png')
        img.drawWidth = 2 * inch
        img.drawHeight = 1.5 * inch
        # 参数计算
        pressure = float(self.elliptical_parameter['Pressure'])  # 计算压力 MPa
        temperature = float(self.elliptical_parameter['temperature'])  # 设计温度 摄氏度
        Di = float(self.elliptical_parameter['Equipment_inner_diameter'])  # 封头内径
        hi = float(self.elliptical_parameter['Depth'])  # 曲面内深度
        allowable_stress = float(self.elliptical_parameter['allowable_stress'])  # 设计温度下的材料的许用应力
        C1 = float(self.elliptical_parameter['deviation'])  # 钢板负偏差
        C2 = float(self.elliptical_parameter['Corrosion_allowance'])  # 腐蚀裕量
        C3 = float(self.elliptical_parameter['Processing_thinning'])  # 加工减薄量
        E = float(self.elliptical_parameter['Welding_factor'])  # 焊接系数

        # 封头计算厚度
        K = (2 + math.pow((0.5 * Di / hi), 2)) / 6  # 椭圆封头形状系数
        calculate_thickness = round((K * pressure * Di) / (2 * allowable_stress * E - 0.5 * pressure), 2)

        # 封头设计厚度
        design_thickness = round((calculate_thickness + C1 + C2 + C3), 2)

        # 封头名义厚度
        titular_thickness = math.ceil(design_thickness)
        if titular_thickness == 13:
            titular_thickness =14

        # 封头有效厚度
        effective_thickness = round((titular_thickness - C1 - C2 - C3), 2)

        # 应力计算
        # 最大允许工作压力计算
        max_work_press = round(((2 * allowable_stress * E * effective_thickness) / (K * Di + 0.5 * effective_thickness)), 2)

        # 校核
        # 厚度校核
        check_thickness = ''
        if calculate_thickness < effective_thickness:
            check_thickness = '满足最小厚度要求'
        else:
            check_thickness = '不满足最小厚度要求'

        # 压力校验
        check_pressure = ''
        if pressure < max_work_press:
            check_pressure = '合格'
        else:
            check_pressure = '不合格'


        # 表格格式生成
        self.basic_data = [['内压圆筒校核',  '', '计算单位', '压力容器专用计算软件'],
                           ['计算所依据的标准', '', '', 'GB 150.3-2011'],
                           ['计算条件', '', '', '椭圆封头简图'],
                           ['计算压力P', pressure, 'MPa', img],
                           ['设计温度t', temperature, '℃', ''],
                           ['内径Di', Di, 'mm', ''],
                           ['曲面深度hi', hi, 'mm', ''],
                           ['材料', 'Q345R(板材)', '', ''],
                           ['设计温度许用应力St', allowable_stress, 'MPa', ''],
                           ['钢板负偏差C1', C1, 'mm', ''],
                           ['腐蚀裕量C2', C2, 'mm', ''],
                           ['加工减薄量', C3, 'mm', ''],
                           ['焊接接头系数'+chr(934), E, '', ''],
                           ['厚度计算', '', '', ''],
                           ['形状系数', K, '', ''],
                           ['计算厚度', calculate_thickness, 'mm', ''],
                           ['有效厚度', effective_thickness, 'mm', ''],
                           ['设计厚度', design_thickness, 'mm', ''],
                           ['名义厚度', titular_thickness, 'mm', ''],
                           ['结论', check_thickness, '', ''],
                           ['压力计算', '', '', ''],
                           ['最大允许工作压力 ', max_work_press, 'MPa', ''],
                           ['结论', check_pressure, '', ''], ]

    def genTaskPDF(self):
        story = []
        # 表格允许单元格内容自动换行格式设置
        stylesheet = getSampleStyleSheet()
        body_style = stylesheet["BodyText"]
        body_style.wordWrap = 'CJK'
        body_style.fontName = 'simsun'
        body_style.fontSize = 12
        # 基础参数
        basic_table = Table(self.basic_data, colWidths=None, rowHeights=None, style=self.basic_style)
        story.append(basic_table)
        doc = SimpleDocTemplate(self.file_path + ".pdf", leftSpace=37 * mm, rightMargin=15 * mm, pagesize=A4)
        doc.build(story)


# if __name__ == '__main__':
#
#     elliptical_parameter = {'Pressure': '1.2',
#                             'temperature': '200.00',
#                             'Equipment_inner_diameter': '2000.00',
#                             'Depth': '500.00',
#                             'allowable_stress': '183',
#                             'deviation': '0.30',
#                             'Corrosion_allowance': '3.0',
#                             'Processing_thinning': '1.96',
#                             'Welding_factor': '0.85'}
#
#     pdf_generator = PDFGenerator(elliptical_parameter)
#     pdf_generator.genTaskPDF()
