import math
from math import sqrt

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
import tkinter as tk
from tkinter import  filedialog

# 生成PDF文件
class PDFGenerator:
    def __init__(self, TTKT_Parameter={}):
        root = tk.Tk() # 通过对话框选择保存路径
        root.withdraw()
        Folderpath = filedialog.asksaveasfilename()  # 获得选择好的文件夹
        self.TTKT_Parameter = TTKT_Parameter
        self.file_path = Folderpath
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
        #参数计算
        D_i = float(self.TTKT_Parameter['shell_internal_radius'])  # 壳内半径
        t = float(self.TTKT_Parameter['shell_thickness'])  # 壳厚度
        l = float(self.TTKT_Parameter['cylinder_length'])  # 筒体长度
        R_n = float(self.TTKT_Parameter['pipe_internal_radius'])  # 接管内半径
        L_pr1 = float(self.TTKT_Parameter['pipe_out_length'])  # 容器壁外侧接管伸出长度
        t_n = float(self.TTKT_Parameter['pipe_thickness'])  # 接管壁厚度
        t_n2 = float(self.TTKT_Parameter['nominal_thickness'])  # 变厚度接管较薄部分公称厚度
        t_e = float(self.TTKT_Parameter['plate_thickness'])  # 补强板厚度
        L_pr2 = float(self.TTKT_Parameter['pipe_in_length'])  # 容器壁内侧接管伸出长度
        L_pr3 = float(self.TTKT_Parameter['out_thickness_length'])  # 外侧变厚度t的长度
        P = float(self.TTKT_Parameter['pressure']) # 设计压力
        T = float(self.TTKT_Parameter['temperature']) # 设计温度
        C_2 = float(self.TTKT_Parameter['shell_corrosion']) # 壳体腐蚀裕量
        C_2t = float(self.TTKT_Parameter['pipe_corrosion']) # 接管腐蚀裕量
        W = float(self.TTKT_Parameter['plate_width'])  # 补强板宽度
        L_42 = float(self.TTKT_Parameter['L_42'])
        L_43 = float(self.TTKT_Parameter['L_43'])
        R_nc = float(self.TTKT_Parameter['R_nc']) # 容器上沿接管开口方向接管半径
        E = float(self.TTKT_Parameter['E']) # 焊接接头系数
        thita = float(self.TTKT_Parameter['thita']) # 接管轴线与筒体表面法线夹角

        # Step 1
        L_R = 0 # 容器壁补强范围
        if t_e == 0:
            L_R = 8*t
        elif t_e < 0.5*t or W < 2*t:
            L_R = 8*t
        elif t_e >= 0.5*t or W < 8*(t+t_e):
            L_R = 10*t
        elif t_e >= 0.5*t or W >= 8*(t+t_e):
            L_R = 8*(t+t_e)
        # Step 2
        L_H = min(t+(0.78*sqrt(R_n*t_n)), min(L_pr1+t, 8*t))  # 容器外表面沿接管壁补强范围
        L_I = 0  # 容器内表面沿接管壁补强范围

        if L_pr2>0:
            L_T1 = 0.75*sqrt(R_n*t_n2)
            L_T2 = L_pr2
            L_T3 = 8*(t+t_e)
            L_I = min(L_T3, min(L_T1, L_T2))

        # Step 3
        A_y = min((2*R_n+t_n)/(sqrt(D_i+t)*t), 10)
        A_1 = t*L_R*max(A_y/4, 1)
        A_2 = 0
        if L_H <= L_pr3+t:
            A_2 = t_n*L_H
        else:
            A_2 = t_n*(L_pr3+t)+0.78*(t_n2*t_n2/t_n)*sqrt(R_n*t_n2)
        A_3 = t_n*L_I
        A_42 = 0.5*L_42*L_42
        A_43 = 0.5*L_43*L_43
        A_5 = min(W*t_e, L_R*t_e)
        A_T = A_1+A_2+A_3+A_42+A_43+A_5 # 靠近接管开孔处的有效总面积

        # Step 4
        R_eff = D_i/2  # 壳体有效半径

        # Step 5
        f_N = P*R_n*(L_H-t)  # 内压在容器外侧接管上引起的力
        f_S = P*R_eff*(L_R+t_n)  # 内压在壳体上引起的力
        f_Y = P*R_eff*R_nc  # 内压引起的不连续力

        # Step 6
        t_eff = 0 # 壳体有效厚度
        if t_e > 0.5*t and W >= 8*(t+t_e):
            t_eff = t+t_e
        else:
            t_eff = t

        # Step 7
        sigma_avg = (f_N+f_S+f_Y)/A_T # 平均局部一次薄膜应力
        sigma_eire = P*R_eff/t_eff # 总体一次薄膜应力

        # Step 8
        P_L = max(2*sigma_avg-sigma_eire, sigma_eire) # 接管相交处最大局部一次薄膜应力
        R_ne = R_n/math.sin(thita)
        A_P = R_n*(L_H-t)+R_eff*(L_R+t_n+R_ne)
        P_MAX = min(1.5*140*E/(2*A_P/A_T-R_eff/t_eff), 140*t/R_eff) # 接管最大许用工作压力

        # 校核
        check_P_L = ''
        if P_L < 1.5*140*E:
            check_P_L = '合格'
        else:
            check_P_L = '不合格'

        img = Image('../icons/TTKT.png')
        img.drawWidth = 4 * inch
        img.drawHeight = 2.5 * inch
        self.basic_data = [['开孔补强计算', '', '计算单位', '压力容器计算软件', '', ''],
                      ['接管:N1', '', '', '计算方法:ASME VIII-1', '', ''],
                      ['设计条件', '', '', '简图', '', ''],
                      ['计算压力P', '%.2f' % P, 'MPa', img, '', ''],
                      ['设计温度T', '%.2f' % T, '℃', '', '', ''],
                      ['壳体型式', '圆形筒体', '', '', '', ''],
                      ['壳体材料名称及类型', 'Q245R板材', '', '', '', ''],
                      ['焊接接头系数E', '%.2f' % E, '', '', '', ''],
                      ['壳体内直径Di', '%.2f' % D_i, 'mm', '', '', ''],
                      ['壳体开孔处公称厚度t', '%.2f' % t, 'mm', '', '', ''],
                      ['壳体厚度负偏差C1', '0.00', 'mm', '', '', ''],
                      ['壳体腐蚀裕量C2', '%.2f' % C_2, 'mm', '', '', ''],
                      ['壳体材料许用应力', '140', 'MPa', '', '', ''],
                      ['接管轴线与筒体表面法线夹角', '', thita, '', '', ''],
                      ['接管实际外伸长度', '%.2f' % L_pr1, 'mm', '接管连接型式', '插入式接管壁安放在容器壁上', ''],
                      ['接管实际内伸长度', '%.2f' % L_pr2, 'mm', '接管材料', 'Q245R', ''],
                      ['接管壁公称厚度', '%.2f' % t_n, 'mm', '名称及类型', '板材', ''],
                      ['接管内半径', '%.2f' % R_n, 'mm', '补强圈材料名称', '', ''],
                      ['接管腐蚀裕量C2t', '%.2f' % C_2t, 'mm', '补强圈宽度', '%.2f' % W, 'mm'],
                      ['', '', '', '补强圈厚度', '%.2f' % t_e, 'mm'],
                      ['接管厚度负偏差C1t', '0', 'mm', '补强圈厚度负偏差C1r', '', 'mm'],
                      ['接管材料许用应力', '140', 'MPa', '补强圈许用应力', '', 'mm'],
                      ['开孔补强计算', '', '', '', '', ''],
                      ['沿容器壁补强范围', '%.2f' % L_R, 'mm', '最大局部一次薄膜应力', '%.2f' % P_L, 'MPa'],
                      ['伸出在容器外表面沿接管壁补强范围', '%.2f' % L_H, 'mm', '平均一次薄膜应力', '%.2f' % sigma_avg, 'MPa'],
                      ['伸入在容器内表面沿接管壁补强范围', '%.2f' % L_I, 'mm', '总体一次薄膜应力', '%.2f' % sigma_eire, 'MPa'],
                      ['壳体有效半径', '%.2f' % R_eff, 'mm', '壳体有效厚度', '%.2f' % t_eff, 'mm'],
                      ['接管有效外伸长度', '%.2f' % L_pr1, 'mm', '接管有效内伸长度', '%.2f' % L_pr2, 'mm'],
                      ['接管开口处有效总面积', '%.2f' % A_T, 'mm^2', '内压在壳体上引起的力', '%.2f' % f_S, 'mm'],
                      ['内压在容器外侧接管上引起的力', '%.2f' % f_N, 'N', '内压引起的不连续的力', '%.2f' % f_Y, 'mm^2'],
                      ['许用应力', '', 'MPa', '接管最大许用应力', '%.2f' % P_MAX, 'mm^2'],
                      ['结论:'+check_P_L, '', '', '']]

    def genTaskPDF(self):
        story = []
        # 表格允许单元格内容自动换行格式设置
        stylesheet = getSampleStyleSheet()
        body_style = stylesheet["BodyText"]
        body_style.wordWrap = 'CJK'
        body_style.fontName = 'ping'
        body_style.fontSize = 12
        # 基础参数
        basic_table = Table(self.basic_data, colWidths=None, rowHeights=None, style=self.basic_style)
        story.append(basic_table)
        doc = SimpleDocTemplate(self.file_path + ".pdf", leftSpace=37 * mm, rightMargin=15 * mm, pagesize = A4)
        doc.build(story)

'''if __name__ == '__main__':
    parameter = {'shell_internal_radius': 1000,
                                   'shell_thickness': 35,
                                   'cylinder_length': 2000,
                                   'pipe_internal_radius': 35,
                                   'pipe_out_length': 300,
                                   'pipe_thickness': 35,
                                   'nominal_thickness': 30,
                                   'plate_thickness':30,
                                   'pipe_in_length': 100,
                                   'out_thickness_length': 30,
                                   'pressure': 5.8,
                                   'temperature': 100,
                                   'shell_corrosion': 1.5,
                                   'pipe_corrosion': 1.5,
                                   'plate_width': 300,
                                   'L_42': 15,
                                   'L_43': 15,
                                   'R_nc': 20,
                                   'E': 1,
                                   'thita': 30}
    pdf_generator = PDFGenerator(parameter)
    pdf_generator.genTaskPDF()'''