#!/usr/bin/env python
import os

def DetectOS():
    """Determines the current OS so we can adapt to each OS's peculiarities."""
    # this was adapted from:
    # http://gitweb.compiz-fusion.org/?p=fusion/misc/compiz-manager;a=blob;f=compiz-manager
    # TODO: is there a better way to implement this ?
    if os.name == 'nt':
        return 'windows'
    elif os.name == 'mac':
        return 'mac'
    elif os.getenv('KDE_FULL_SESSION') == 'true':
        return 'kde'
    elif os.getenv('GNOME_DESKTOP_SESSION_ID') != '':
        return 'gnome'
    else:
        return ''

