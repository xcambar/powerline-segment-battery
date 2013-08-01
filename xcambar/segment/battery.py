#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import absolute_import
from powerline.theme import requires_segment_info
from subprocess import Popen, PIPE
from shlex import split
import re


def display_symbol(value, config):
  full_symbol = config.get('full_symbol', '♥ ')
  empty_symbol = config.get('empty_symbol', "♡ ")
  count_symbols = config.get('number_of_symbols', 5) #How many symbols must be shown

  threshold = 100/count_symbols/2
  nbr_full_symbols = int(min(threshold + int(value), 100) / int(100 / count_symbols))

  s = ''.join([full_symbol for num in xrange(nbr_full_symbols)])
  s += ''.join([empty_symbol for num in xrange(count_symbols - nbr_full_symbols)])
  return s


def display_numeric(value, config):
  return ''.join([value, '%'])


@requires_segment_info
def battery(pl, segment_info, display="symbol", config={}):
  p1 = Popen(split("pmset -g ps"), stdout=PIPE)
  p2 = Popen(split(r'sed -n "s/.*[[:blank:]]+*\(.*%\).*/\1/p"'), stdin=p1.stdout, stdout=PIPE)

  value = re.search('(\d{0,3})%', p2.stdout.read()).group(1)

  try:
    output = {
      'symbol': lambda: display_symbol(value, config)
    }[display]()
  except KeyError:
    output = display_numeric(value, config)

  return [{
    'contents': output,
    'highlight_group': ['battery', 'system_load']
  }]
