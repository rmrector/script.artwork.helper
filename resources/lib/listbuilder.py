import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin
import xbmcvfs
from xbmcaddon import Addon

def handle_pluginlist():
    path = _get_pluginpath(True)
    uselist = None
    if path['path'][0] == 'multiimage':
        if len(path['path']) == 1:
            uselist = stitch_multiimage(path['query'])
        elif path['path'][1] == 'listitem':
            uselist = get_listitem_multiimage(path['query'])
        elif path['path'][1] == 'container':
            uselist = get_container_multiimage(path['query'])
        elif path['path'][1] == 'smartseries':
            uselist = get_smartseries_multiimage(path['query'])
    _build_list(uselist, path['handle'])

def _get_pluginpath(doublequerysplit=False):
    path = sys.argv[0].split('://')[1].rstrip('/').split('/')[1:] # cuts out addon id
    query_list = sys.argv[2].lstrip('?').split('&&' if doublequerysplit else '&')
    query = {}
    if query_list and query_list[0]:
        for item in query_list:
            key, value = item.split("=", 1)
            if key in query:
                if isinstance(query[key], list):
                    query[key].append(value)
                else:
                    query[key] = [query[key], value]
            else:
                query[key] = value

    return {'handle': int(sys.argv[1]), 'path': path, 'query': query}

def _build_list(items, handle):
    xbmcplugin.setContent(handle, 'files')
    if items:
        xbmcplugin.addDirectoryItems(handle, [_build_item(item) for item in items])
    xbmcplugin.endOfDirectory(handle)

def _build_item(item):
    if item.startswith('image://'):
        item = urllib.unquote(item[8:-1])
    return (item, xbmcgui.ListItem(item))

def stitch_multiimage(query):
    if 'image' not in query or not query['image']:
        return []
    elif isinstance(query['image'], list):
        return [image for image in query['image'] if image]
    else:
        return [query['image']]

def get_listitem_multiimage(query):
    if not query.get('refresh'):
        return []
    arttype = query.get('arttype', 'fanart')
    infolabel = 'Container.ListItem.' if not query.get('containerid') \
        else 'Container({0}).ListItem.'.format(query['containerid'])
    artlabel = infolabel + 'Art({0}{1})'.format(arttype, '{0}')
    count = 0
    inforesult = xbmc.getInfoLabel(artlabel.format(''))
    while not inforesult and count < 10:
        xbmc.sleep(200)
        inforesult = xbmc.getInfoLabel(artlabel.format(''))
        count += 1

    if inforesult:
        result = [inforesult]
    else:
        return []
    lastempty = False
    for i in range(1, query.get('limit', 100)):
        inforesult = xbmc.getInfoLabel(artlabel.format(i))
        if inforesult:
            result.append(inforesult)
            lastempty = False
        else:
            if lastempty:
                break
            lastempty = True
    if len(result) == 1 and Addon().getSetting('classicmulti') == 'true' and arttype in ('fanart', 'thumb', 'tvshow.fanart'):
        infopath = xbmc.getInfoLabel(infolabel + 'Path')
        if not infopath.startswith('plugin://'):
            episodefanart = arttype == 'fanart' and xbmc.getInfoLabel(infolabel + 'DBTYPE') == 'episode' and \
                xbmc.getCondVisibility('!String.IsEqual({0}Art(tvshow.fanart), {0}Art(fanart))'.format(infolabel))
            if not episodefanart:
                infopath += 'extrafanart' if arttype.endswith('fanart') else 'extrathumbs'
                infopath += '\\' if '\\' in infopath else '/'
                if xbmcvfs.exists(infopath):
                    _, files = xbmcvfs.listdir(infopath)
                    for filename in files:
                        result.append(infopath + filename)

    return result

def get_container_multiimage(query):
    if not query.get('refresh'):
        return []
    arttype = query.get('arttype', 'tvshow.fanart')
    infolabel = 'Container.Art({0}{1})'.format(arttype, '{0}')

    inforesult = xbmc.getInfoLabel(infolabel.format(''))
    count = 0
    while not inforesult and count < 10:
        xbmc.sleep(200)
        inforesult = xbmc.getInfoLabel(infolabel.format(''))
        count += 1

    if inforesult:
        result = [inforesult]
    else:
        return []
    lastempty = False
    for i in range(1, query.get('limit', 100)):
        inforesult = xbmc.getInfoLabel(infolabel.format(i))
        if inforesult:
            result.append(inforesult)
            lastempty = False
        else:
            if lastempty:
                break
            lastempty = True

    return result

def get_smartseries_multiimage(query):
    if not query.get('title') and not query.get('refresh'):
        return []
    elif not query.get('refresh'):
        query['refresh'] = query['title']

    if not query.get('arttype'):
        query['arttype'] = 'fanart'
    elif '.'  in query['arttype']:
        query['arttype'] = query['arttype'].rsplit('.', 1)[1]

    count = 0 # Wait for InfoLabel availability
    while not xbmc.getInfoLabel('ListItem.Label') and count < 10:
        xbmc.sleep(200)
        count += 1

    arttype = 'tvshow.' + query['arttype']
    if not xbmc.getCondVisibility('String.IsEmpty(ListItem.Art({0}))'.format(arttype)):
        query['arttype'] = arttype
        return get_listitem_multiimage(query)
    if not xbmc.getCondVisibility('String.IsEmpty(Container.Art({0}))'.format(arttype)):
        query['arttype'] = arttype
        return get_container_multiimage(query)

    return get_listitem_multiimage(query)
