#!/usr/bin/env python
# encoding: utf-8
#
# Copyright (c) 2017 Dean Jackson <deanishe@deanishe.net>
#
# MIT Licence. See http://opensource.org/licenses/MIT
#
# Created on 2017-12-10
#

"""searchio toggle <setting>

Toggle a workflow setting on/off.

Usage:
    searchio toggle <setting>
    searchio toggle -h

Options:
    -h, --help   Display this help message

"""

from __future__ import print_function, absolute_import

from plistlib import readPlist, writePlist

from docopt import docopt
from workflow import Variables

from searchio.core import Context
from searchio import util

log = util.logger(__name__)


def usage(wf):
    """CLI usage instructions."""
    return __doc__


def set_variable(wf, key, value):
    """Set a variable in ``info.plist``."""
    p = wf.workflowfile('info.plist')
    d = readPlist(p)
    d['variables'][key] = value
    writePlist(d, p)


def do_toggle_show_query(wf):
    """Toggle "show query in results" setting."""
    ctx = Context(wf)
    v = ctx.getbool('SHOW_QUERY_IN_RESULTS')
    if v:
        new = '0'
        status = 'off'
    else:
        new = '1'
        status = 'on'

    log.debug('turning "SHOW_QUERY_IN_RESULTS" %s ...', status)
    set_variable(wf, 'SHOW_QUERY_IN_RESULTS', new)

    print(Variables(title='Show query in results', text='Turned ' + status))


def run(wf, argv):
    """Run ``searchio web`` sub-command."""
    args = docopt(usage(wf), argv)
    key = args.get('<setting>')
    if key == 'show-query':
        return do_toggle_show_query(wf)
    raise ValueError('Unknown Setting: ' + key)