#!/usr/bin/env python
"""\
Converts post-1970 entries from tai-utc.dat (stdin) to Python source (stdout).
"""

#                      Copyright (c) 2019
#                   Frederick H. G. Wright II
#                          fw@fwright.net
#
#        The information in this software is subject to change
#   without notice and should not be construed as a commitment  #
#   by Frederick H. G. Wright II, hereafter known as "author".
#   The author makes no representations about the suitability
#   of this software for any purpose.  It is supplied "As Is"
#   without expressed or implied  warranty.
#
#        This software may be copied or distributed for any
#   noncommercial purpose, with the inclusion of this notice,
#   and provided that any modifications are clearly identified
#   as such and are accompanied by the original unmodified
#   software.

from __future__ import absolute_import, print_function, division

import os
import sys

_BASE_YEAR = 1972

_PREFIX = '''\
"""Leap-second table, giving TAI-UTC for each starting date."""

# Autogenerated by %s, do not hand edit.

TABLE = ['''

_SUFFIX = """\
]"""

_MONTH_NAMES = (
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN',
    'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC'
    )
# Avoid dict comprehension for Python 2.6 compatibility.
# Add an empty list to avoid the pylint3 warning.
_MONTH_DICT = dict([(n, v) for v, n in enumerate(_MONTH_NAMES, 1)] + [])


def main(argv):
  """Main function."""
  out_list = []
  for line in sys.stdin:
    data = line.split()
    try:
      year = int(data[0])
      month = _MONTH_DICT[data[1].upper()]
      day = int(data[2])
      offset = int(float(data[6]))
    except ValueError:
      continue
    if not month or year < _BASE_YEAR:
      continue
    out_list.append((year, month, day, offset))
  if out_list:
    print(_PREFIX % os.path.basename(argv[0]))
    for entry in out_list:
      print('    %s,' % repr(entry))
    print(_SUFFIX)


if __name__ == '__main__':
  sys.exit(main(sys.argv))  # pragma: no cover
