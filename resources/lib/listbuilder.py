import random
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
    infolabel = 'Container({0}).'.format(query['containerid']) if 'containerid' in query else ''
    infolabel += 'ListItem.Art({0}{1})'.format(arttype, '{0}')
    count = 0
    while count < 10:
        inforesult = xbmc.getInfoLabel(infolabel.format(''))
        if not inforesult:
            # WARN: This is only needed until my PR is merged into Krypton
            inforesult = xbmc.getInfoLabel('Window.Property({0})'.format(arttype))
            if inforesult:
                infolabel = 'Window.Property({0}{1})'.format(arttype, '{0}')
        if inforesult:
            break
        count += 1
        xbmc.sleep(200)

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
    if len(result) == 1 and Addon().getSetting('classicmulti') == 'true' and arttype in ('fanart', 'thumb', 'tvshow.fanart'):
        infolabel = 'Container({0}).ListItem.'.format(query['containerid']) if 'containerid' in query else 'ListItem.'
        episodefanart = arttype == 'fanart' and xbmc.getInfoLabel(infolabel + 'DBTYPE') == 'episode' and \
            xbmc.getCondVisibility('!StringCompare(ListItem.Art(tvshow.fanart), ListItem.Art(fanart))')
        if not episodefanart:
            infopath = xbmc.getInfoLabel(infolabel + 'Path') + ('extrafanart' if arttype.endswith('fanart') else 'extrathumbs')
            infopath += '\\' if '\\' in infopath else '/'
            if xbmcvfs.exists(infopath):
                _, files = xbmcvfs.listdir(infopath)
                for filename in files:
                    result.append(infopath + filename)

    if 'shuffle' in query:
        resultcopy = list(result)
        random.shuffle(resultcopy)
        random.shuffle(result)
        result.extend(resultcopy)
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

    if 'shuffle' in query:
        resultcopy = list(result)
        random.shuffle(resultcopy)
        random.shuffle(result)
        result.extend(resultcopy)
    return result

def get_smartseries_multiimage(query):
    if not query.get('title') and not query.get('refresh'):
        return []
    elif not query.get('refresh'):
        query['refresh'] = query['title']
    content = xbmc.getInfoLabel('Container.Content')
    if not content:
        content = xbmc.getInfoLabel('ListItem.DBTYPE')
    count = 0
    while not content and count < 10:
        xbmc.sleep(200)
        content = xbmc.getInfoLabel('Container.Content')
        if not content:
            content = xbmc.getInfoLabel('ListItem.DBTYPE')
        count += 1

    if content in ('tvshows', 'tvshow'):
        return get_listitem_multiimage(query)
    elif content in ('seasons', 'episodes', 'season', 'episode'):
        if query.get('arttype') and '.' not in query['arttype']:
            query['arttype'] = 'tvshow.' + query['arttype']
        else:
            query['arttype'] = 'tvshow.fanart'
        if xbmc.getCondVisibility('!IsEmpty(ListItem.Art({0}))'.format(query['arttype'])) \
                or xbmc.getCondVisibility('IsEmpty(Container.Art({0}))'.format(query['arttype'])):
            # Prefer ListItem to grab extrafanart
            return get_listitem_multiimage(query)
        else:
            return get_container_multiimage(query)
    else:
        if query.get('arttype') and '.' not in query['arttype']:
            query['arttype'] = 'tvshow.' + query['arttype']
        else:
            query['arttype'] = 'tvshow.fanart'
        return get_listitem_multiimage(query)
