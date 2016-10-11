import os
import sys
import xbmc
from xbmcaddon import Addon

addonpath = xbmc.translatePath(Addon().getAddonInfo('path')).decode('utf-8')
sys.path.append(os.path.join(addonpath, u'resources', u'lib'))

import listbuilder

# Keep the initial script simple as possible to reduce the "compile" delay;
#  for multi fanart nearly every millisecond can count.
if __name__ == '__main__':
    if sys.argv[0].startswith('plugin://'):
        listbuilder.handle_pluginlist()
    else:
        xbmc.log("[script.artwork.helper]: SeriesArtworkGrabber no longer supported", xbmc.LOGWARNING)
