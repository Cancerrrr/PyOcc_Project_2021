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
pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttc'))
# pdfmetrics.registerFont(TTFont('simsun', 'simsun.ttf'))
# pdfmetrics.registerFont(TTFont('simsun', 'Helvetica.ttf'))

# 生成PDF文件
class PDFGenerator:
    def __init__(self, cylinder_parameter={}):
        root = tk.Tk()
        root.withdraw()
        Folderpath = filedialog.asksaveasfilename()  # 获得选择好的文件夹
        self.cylinder_parameter = cylinder_parameter
        self.file_path = Folderpath
        self.title_style = ParagraphStyle(name="TitleStyle", fontName="simsun", fontSize=48, alignment=TA_LEFT,)
        self.sub_title_style = ParagraphStyle(name="SubTitleStyle", fontName="simsun", fontSize=32,
                                              textColor=colors.HexColor(0x666666), alignment=TA_LEFT, )
        self.content_style = ParagraphStyle(name="ContentStyle", fontName="simsun", fontSize=18, leading=25, spaceAfter=20,
                                            underlineWidth=1, alignment=TA_LEFT, )
        self.foot_style = ParagraphStyle(name="FootStyle", fontName="simsun", fontSize=14, textColor=colors.HexColor(0xB4B4B4),
                                         leading=25, spaceAfter=20, alignment=TA_CENTER, )
        self.table_title_style = ParagraphStyle(name="TableTitleStyle", fontName="simsun", fontSize=20, leading=25,
                                                spaceAfter=10, alignment=TA_LEFT, )
        self.sub_table_style = ParagraphStyle(name="SubTableTitleStyle", fontName="simsun", fontSize=16, leading=25,
                                                spaceAfter=10, alignment=TA_LEFT, )
        self.basic_style = TableStyle([('FONTNAME', (0, 0), (-1, -1), 'simsun'),
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
                                       ('SPAN', (3, 3), (3, 12)),
                                       ('SPAN', (1, 7), (2, 7)),
                                       ('SPAN', (1, 12), (2, 12)),
                                       ('SPAN', (1, 14), (3, 14)),
                                       ('SPAN', (2, 15), (3, 15)),
                                       ('SPAN', (2, 16), (3, 16)),
                                       ('SPAN', (2, 17), (3, 17)),
                                       ('SPAN', (1, 18), (3, 18)),
                                       ('SPAN', (1, 19), (3, 19)),
                                       ('SPAN', (0, 20), (3, 20)),
                                       ('SPAN', (1, 21), (2, 21)),
                                       ('SPAN', (2, 22), (3, 22)),
                                       ('SPAN', (2, 23), (3, 23)),
                                       ('SPAN', (2, 24), (3, 24)),
                                       ('SPAN', (1, 25), (3, 25)),
                                       ('SPAN', (2, 26), (3, 26)),
                                       ('SPAN', (0, 27), (3, 27)),
                                       ('SPAN', (2, 28), (3, 28)),
                                       ('SPAN', (1, 29), (3, 29)),
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
        # R = float(self.cylinder_parameter['internal_diameter'])  # 壳体内径
        # t = float(self.cylinder_parameter['thickness'])  # 设计厚度
        # L = float(self.cylinder_parameter['Length'])  # 筒体长度
        # cylinder_pressure = float(self.cylinder_parameter['pressure'])  # 设计压力
        # cylinder_temperature = float(self.cylinder_parameter['temperature'])  # 设计温度
        # cylinder_corrosion = float(self.cylinder_parameter['corrosion'])  # 腐蚀系数
        # cylinder_welding = float(self.cylinder_parameter['welding'])  # 焊接系数
        #
        # t_min1 = (cylinder_pressure*R)/(147.6*cylinder_welding-0.6*cylinder_pressure) # 最小厚度t
        # t_e = t - cylinder_corrosion # 有效厚度
        # P_MAWP1 = 147.6*cylinder_welding*t_e/(R+0.6*t_e) # 最大许用工作压力1
        #
        # t_min2 = cylinder_pressure*R/(2*148*cylinder_welding+0.4*cylinder_pressure) # 计算厚度
        # P_MAWP2 = 2*147.6*cylinder_welding*t_e/(R-0.4*t_e) # 最大许用工作压力2
        #
        # t_min = max(t_min1, t_min2) # 最终-最小厚度
        # P_MAWP = min(P_MAWP1, P_MAWP2) # 最终-许用工作压力
        #
        # P_MAPNC = 147.6*cylinder_welding*t/(R+0.6*t) # 最大许用工作压力
        # P_Sact = (cylinder_pressure*(R+0.6*t_e))/(cylinder_welding*t_e) # 最大许用应力计算
        # check1 = ''
        # check2 = ''
        # if t >= t_min and t_min > 0:
        #     check1 = '合格'
        # else:
        #     check1 = '不合格'
        #
        # if P_MAWP >= cylinder_pressure and 147.6 >= P_Sact:
        #     check2 = '合格'
        # else:
        #     check2 = '不合格'

        # 表格格式生成
        self.basic_data = [['内压圆筒校核', '计算单位', '压力容器专用计算软件', ''],
                           ['计算所依据的标准', 'GB 150.3-2011', '', ''],
                           ['计算条件', '', '椭圆封头简图', ''],
                           ['计算压力P', '3.10', 'MPa', img],
                           ['设计温度t', '100.00', '℃', ''],
                           ['内径Di', '500.00', 'mm', ''],
                           ['曲面深度hi', '150.00', 'mm', ''],
                           ['材料', 'Q345R(板材)', '', ''],
                           ['设计温度许用应力St', '189.00', 'MPa', ''],
                           ['试验温度许用应力St', '189.00', 'MPa', ''],
                           ['钢板负偏差C1', '0.30', 'mm', ''],
                           ['腐蚀裕量C2', '0.50', 'mm', ''],
                           ['焊接接头系数', '1.00', '', ''],
                           ['压力试验时应力校核', '', '', ''],
                           ['压力试验类型', '液压试验', '', ''],
                           ['试验压力值', '3.2000', 'MPa', ''],
                           ['压力试验允许通过的应力', '310.50', 'MPa', ''],
                           ['试验压力下封头的应力', '89.28', 'MPa', ''],
                           ['校核条件', 'tn>t', '', ''],
                           ['结论', '合格', '', ''],
                           ['厚度及重量计算', '', '', ''],
                           ['形状系数', '0.7963', '', ''],
                           ['计算厚度', '3.28', 'mm', ''],
                           ['最小厚度', '3.00', 'mm', ''],
                           ['名义厚度', '8.00', 'mm', ''],
                           ['结论', '满足最小厚度需求', '', ''],
                           ['重量', '23.79', 'Kg', ''],
                           ['压力计算', '', '', ''],
                           ['最大允许工作压力 ', 'StE>=P_Sact P_MAWP>= P 6.77439', 'MPa', ''],
                           ['结论', '合格', '', ''], ]

    def genTaskPDF(self):
        story = []
        # 表格允许单元格内容自动换行格式设置
        stylesheet = getSampleStyleSheet()
        body_style = stylesheet["BodyText"]
        body_style.wordWrap = 'CJK'
        body_style.fontName = 'simsun'
        body_style.fontSize = 12
        # 基础参数
        basic_table = Table(self.basic_data, colWidths=None , rowHeights=None, style=self.basic_style)
        story.append(basic_table)
        doc = SimpleDocTemplate(self.file_path + ".pdf", leftSpace=37 * mm, rightMargin=15 * mm, pagesize = A4)
        doc.build(story)

if __name__ == '__main__':
    # cylinder_parameter = {'pressure': '3.1',
    #             'temperature': '232',
    #             'corrosion': '0',
    #             'welding': '0.8',
    #             'internal_diameter': '95',
    #             'thickness': '3',
    #             'Length': '800'}

    cylinder_parameter = {}
    pdf_generator = PDFGenerator(cylinder_parameter)
    pdf_generator.genTaskPDF()