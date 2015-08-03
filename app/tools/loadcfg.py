#-*- coding: utf-8 -*-
import re as _re
from os.path import (dirname as _dirname, sep as _sep)
from . import cdict as _cdict

_sections = "(?:\[(?P<section>[a-z]+)\](?:\r\n)?)(?P<body>(?:(?:\r\n)?[\s0-9A-Za-z._+\-=\\/?]+)(?:\r\n)?)+"
_tags = r"(?:(?P<key>(?:[a-z]+))(?:(?: +)?=(?: +)?))(?P<value>(?:[\-+]?[^\s]+))"

projdir = '{}'.format(_sep).join(_dirname(__file__).split(_sep)[:-2])

def _load_file(cfgfile='app.ini'):
	filedir = '{}{}{}'.format(projdir, _sep, cfgfile)
	return open(filedir, 'rb').read()

_ofile = _load_file()
#print _ofile
_checktype = lambda val: eval(val) if val.isdigit() else val

_paramsDict = lambda match: _cdict((k.group('key'),_checktype(k.group('value'))) for k in _re.finditer(_tags, match.group('body')))

conf = _cdict((mt.group('section'),_paramsDict(mt)) for mt in _re.finditer(_sections, _ofile))