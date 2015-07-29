#-*- coding: utf-8 -*-
from reportlab import rl_config as _rl_config
from reportlab.lib.units import cm as _cm
from reportlab.lib.pagesizes import (LETTER as _LETTER, landscape as _landscape, portrait as _portrait)
#from reportlab.lib.styles import (getSampleStyleSheet as _getSampleStyleSheet,)
from reportlab.lib.styles import ParagraphStyle as _ParagraphStyle
from reportlab.lib.enums import (TA_LEFT as _TA_LEFT, TA_CENTER as _TA_CENTER, TA_RIGHT as _TA_RIGHT, TA_JUSTIFY as _TA_JUSTIFY)
from reportlab.lib import (colors as _colors,)
from reportlab.platypus import (SimpleDocTemplate as _SimpleDocTemplate, Paragraph as _Paragraph, Spacer as _Spacer, PageBreak as _PageBreak)
from reportlab.platypus.tables import (Table as _Table, TableStyle as _TableStyle)
from . import getLocals as _getLocals
from . import cdict
from cStringIO import StringIO as _StringIO

_rl_config.defaultImageCaching = 1
#_style = _getSampleStyleSheet()
# portrait vars
_ppagesize = _portrait(_LETTER)
_ppw, _pph = _ppagesize
_p_vars = cdict(
	imgxy = dict(x=.5*_cm, y=4*_cm, anchor="c"),
	hline = dict(x1=2.5*_cm, y1=_pph-(1.94*_cm), x2=_ppw-(2*_cm), y2=_pph-(1.94*_cm)),
	vline = dict(x1=2*_cm, y1=1.5*_cm, x2=2*_cm, y2=_pph-(1.94*_cm)),
	ctitle = dict(x=_ppw/2.0, y=_pph-(1.94*_cm)),
	date_time = dict(x=_ppw/2.0, y=1.5*_cm),
	page_count = dict(x=_ppw-(2*_cm), y=1.5*_cm),
	name_year = dict(x=_pph-(7.94*_cm), y=-1.15*_cm),
)
# end portrait
# landscape vars
_lpagesize = _landscape(_LETTER)
_lpw, _lph = _lpagesize
_l_vars = cdict(
	imgxy = dict(x=5*_cm, y=2*_cm, width=18*_cm, height=18*_cm, anchor="c"),
	hline = dict(x1=2.5*_cm, y1=_lph-(1.94*_cm), x2=_lpw-(2*_cm), y2=_lph-(1.94*_cm)),
	vline = dict(x1=2*_cm, y1=1.5*_cm, x2=2*_cm, y2=_lph-(1.94*_cm)),
	ctitle = dict(x=_lpw/2.0, y=_lph-(1.94*_cm)),
	date_time = dict(x=_lpw/2.0, y=1.5*_cm),
	page_count = dict(x=_lpw-(2*_cm), y=1.5*_cm),
	name_year = dict(x=_lph-(7.94*_cm), y=-1.15*_cm),
)
# end landscape
_choice_page = lambda flag: _p_vars if flag else _l_vars
_tbstyle = _TableStyle([
	('GRID', (0,0), (-1,-1), .01*_cm, _colors.Color(.8,.8,.8)),
	('ALIGN', (0,0), (-1,-1), 'CENTER'),
	('VALIGN', (0,0), (-1,-1), 'TOP'),
	('LEFTPADDING', (0,0), (-1,-1), 5),
	('RIGHTPADDING', (0,0), (-1,-1), 5),
	('FONTSIZE', (0,1), (-1,-1), 8),
	('BOTTOMPADDING', (0,0), (-1,0), 10),
	('BACKGROUND', (0,0), (-1,0), _colors.Color(0,.352,.612)),
	('TEXTCOLOR', (0,0), (-1,0), _colors.Color(1,1,1)),
	('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
	('FONTSIZE', (0,0), (-1,0), 14),
	('VALIGN', (0,0), (-1,-0), 'MIDDLE'),
])
"""
_tbstyle = _TableStyle([
	('ALIGN',(1,1),(-2,-2),'RIGHT'),
	('TEXTCOLOR',(1,1),(-2,-2),_colors.red),
	('VALIGN',(0,0),(0,-1),'TOP'),
	('TEXTCOLOR',(0,0),(0,-1),_colors.blue),
	('ALIGN',(0,-1),(-1,-1),'CENTER'),
	('VALIGN',(0,-1),(-1,-1),'MIDDLE'),
	('TEXTCOLOR',(0,-1),(-1,-1),_colors.green),
	('INNERGRID', (0,0), (-1,-1), 0.25, _colors.black),
	('BOX', (0,0), (-1,-1), 0.25, _colors.black),
])
"""
def _base_pagemaker(canvas, doc, **kwargs):
	kwargs = cdict(kwargs)
	psize = _choice_page(kwargs.portrait)
	canvas.drawImage(image=kwargs.img_path, **psize.imgxy)
	#horizontal line
	canvas.setStrokeColorRGB(.8,.8,.8)
	canvas.setLineWidth(.01*_cm)
	canvas.line(**psize.hline)#x1 y1 x2 y2
	#vertical line
	canvas.setStrokeColorRGB(0,.352,.612)
	canvas.setLineWidth(.6*_cm)
	canvas.line(**psize.vline)#x1 y1 x2 y2
	canvas.setFont("Helvetica-Bold", 18)
	canvas.drawCentredString(text=kwargs.title, **psize.ctitle)
	canvas.setFont("Courier", 7)
	canvas.drawString(2.5*_cm, 1.5*_cm, kwargs.user or "--")
	canvas.drawCentredString(text="{}, {}".format(kwargs.odate or "", kwargs.otime or ""), **psize.date_time)
	canvas.drawRightString(text=u"Página {}".format(doc.page), **psize.page_count)
	canvas.translate(_cm, _cm)
	canvas.rotate(90)
	canvas.setFillColorRGB(1,1,1)
	canvas.setFont("Helvetica-Bold", 12)
	canvas.drawString(text="Enlaces - {}".format(kwargs.odate.split("/")[-1]), **psize.name_year)

class ReportMaker(object):
	def __init__(self, title="Reporte", author="Enlaces", subject="Reporte", keywords="Python", creator="Reportlab", img_path=None, user=None, odate=None, otime=None, portrait=True):
		self.config = _getLocals(locals())
		self.config.update(dict(leftMargin=2.5*_cm, rightMargin=2*_cm, topMargin=2*_cm, bottomMargin=1.8*_cm, pagesize = _portrait(_LETTER) if portrait else _landscape(_LETTER), pageCompression=1))
		self.elements = list()
	def FirtPage(self, canvas, doc):
		canvas.saveState()
		_base_pagemaker(canvas, doc, **self.config)
		canvas.restoreState()
	def LaterPages(self, canvas, doc):
		canvas.saveState()
		_base_pagemaker(canvas, doc, **self.config)
		canvas.restoreState()
	def parse_content(self, list_content, default_style="body", align="justify", before_pg=False, after_pg=False):
		style = _ParagraphStyle(default_style)
		style.alignment = _TA_LEFT if align=="left" else _TA_CENTER if align=="center" else _TA_RIGHT if align=="right" else _TA_JUSTIFY
		self.elements += [_PageBreak()] if before_pg else list()
		for dt in list_content:
			self.elements += [_Paragraph(dt, style)]
		self.elements += [_PageBreak()] if after_pg else list()
	def parse_datatable(self, matrix_content, fix_content = True, before_pg=False, after_pg=False, cellsW=dict()):
		tb = _Table(self.__parse_datatable(matrix_content) if fix_content else matrix_content, repeatRows=1, **(dict(colWidths=1.5*_cm) if cellsW else dict()))
		for idx, val in cellsW.iteritems():
			tb._argW[idx] = float(val)*_cm
		tb.setStyle(_tbstyle)
		self.elements += [_PageBreak()] if before_pg else list()
		self.elements += [tb, _Spacer(1, .3*_cm)]
		self.elements += [_PageBreak()] if after_pg else list()
	def __parse_datatable(self, matrix_content):
		thead = _ParagraphStyle("body")
		thead.alignment = _TA_CENTER
		thead.fontName = "Helvetica-Bold"
		thead.fontSize = 14
		thead.textColor = "white"
		thead.splitLongWords = 1
		tbody = _ParagraphStyle("body")
		tbody.fontName = "Helvetica"
		tbody.fontSize = 8
		#body.wordWrap = 'CJK'
		tbody.alignment = _TA_JUSTIFY
		tbody.splitLongWords = 1
		parse_head = lambda text: _Paragraph('{}'.format(text), thead)
		parse_body = lambda text, i=-1, j=-1: _Paragraph('{}'.format(i), tbody) if j==0 and i>=1 else _Paragraph(text, tbody)
		parse_cell = lambda ctx, idx, jdx=-1: parse_head(ctx) if idx==0 else parse_body(ctx, idx, jdx)
		return [[parse_cell("{}".format(cell), i, j) for j,cell in enumerate(row)] for i,row in enumerate(matrix_content)]
	def build_pdf(self):
		pdf = _StringIO()
		sdoc = _SimpleDocTemplate(filename=pdf, **self.config)
		sdoc.build(self.elements, onFirstPage=self.FirtPage, onLaterPages=self.LaterPages)
		return pdf.getvalue()