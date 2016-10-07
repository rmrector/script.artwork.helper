import os
import sys
import xbmc
import xbmcaddon

addon = xbmcaddon.Addon()
resourcelibs = xbmc.translatePath(addon.getAddonInfo('path')).decode('utf-8')
resourcelibs = os.path.join(resourcelibs, u'resources', u'lib')
sys.path.append(resourcelibs)

import listbuilder

# Keep the initial script simple as possible to reduce the start delay; for multi fanart nearly every millisecond can count.
if __name__ == '__main__':
    if sys.argv[0].startswith('plugin://'):
        listbuilder.handle_pluginlist()
    else:
        xbmc.log("[script.artwork.helper]: SeriesArtworkGrabber no longer supported", xbmc.LOGWARNING)
