#!/usr/bin/env python
# vim: set fileencoding=utf-8 :

from __future__ import absolute_import
from powerline.theme import requires_segment_info
from subprocess import Popen, PIPE
from shlex import split
import re

@requires_segment_info
def battery(pl, segment_info):
  max_hearts = 5 #How many hearts must be shown
  threshold = 100/max_hearts/2

  p1 = Popen(split("pmset -g ps"), stdout=PIPE)
  p2 = Popen(split(r'sed -n "s/.*[[:blank:]]+*\(.*%\).*/\1/p"'), stdin=p1.stdout, stdout=PIPE)

  percentage = re.search('(\d{0,3})%', p2.stdout.read()).group(1)
  nbr_full_hearts = int(min(threshold + int(percentage), 100) / int(100 / max_hearts))

  full_heart = "♥"
  empty_heart = "♡"

  s = ''.join([full_heart for num in xrange(nbr_full_hearts)])
  s += ''.join([empty_heart for num in xrange(max_hearts - nbr_full_hearts)])

  return s
