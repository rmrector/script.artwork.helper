import random
import sys
import urllib
import xbmc
import xbmcgui
import xbmcplugin

def handle_pluginlist():
    path = get_pluginpath(True)
    if path['path'][0] == 'multiimage':
        if len(path['path']) == 1:
            build_list(stitch_multiimage(path), path['handle'])
        elif path['path'][1] == 'listitem':
            build_list(get_listitem_multiimage(path), path['handle'])

def stitch_multiimage(path):
    """Stitch together a bunch of images for a 'multiimage' control. Feed it as many images as you want, any empty values are safely ignored. Use when listitem doesn't quite work, like so:
    plugin://script.artwork.skinhelper/multiimage/?image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>
    """

    if 'image' not in path['query'] or not path['query']['image']:
        return []
    elif isinstance(path['query']['image'], list):
        return [unquoteimage(image) for image in path['query']['image'] if image]
    else:
        return [unquoteimage(path['query']['image'])]

def get_listitem_multiimage(path):
    """Stitch together all fanart for the selected ListItem:
    plugin://script.artwork.helper/multiimage/listitem/?refresh=$INFO[ListItem.DBID]&amp;&amp;containerid=4250&amp;&amp;arttype=tvshow.fanart&amp;&amp;shuffle=true

    'refresh' is just to get Kodi to fire off the plugin again, just set it to something that will change when the fanart should change
    'containerid' is optional, and points to an alternate container
    'arttype' is optional, and lets you select different artwork
    'shuffle' is optional and shuffles the list, useful if you aren't using a multiimage control that can randomize it
    """

    if 'containerid' in path['query']:
        infolabel = 'Container(%s).ListItem.Art(%s%s)' % (path['query']['containerid'], path['query'].get('arttype', 'fanart'), '%s')
    else:
        infolabel = 'ListItem.Art(%s%s)' % (path['query'].get('arttype', 'fanart'), '%s')

    inforesult = xbmc.getInfoLabel(infolabel % '')
    if inforesult:
        result = [unquoteimage(inforesult)]
    else:
        return []
    lastempty = False
    for i in range(1, path['query'].get('limit', 100)):
        inforesult = xbmc.getInfoLabel(infolabel % i)
        if inforesult:
            result.append(unquoteimage(inforesult))
            lastempty = False
        else:
            if lastempty:
                break
            lastempty = True

    if 'shuffle' in path['query']:
        resultcopy = list(result)
        random.shuffle(resultcopy)
        random.shuffle(result)
        result.extend(resultcopy)
    return result

def get_pluginpath(doublequerysplit=False):
    """Split path into a handy dict.
    Parameter 'doublequerysplit' requires '&&' to separate query bits, so skins can pass in paths that contain a querysplit.

    Returns dict keys:
    'handle' is plugin handle as int
    'path' is a list of folder/filename components
    'query' is another dict of the query. Duplicated keys are returned as a list of values"""
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

def build_list(items, handle):
    """Pack up a list of image URLs into the plugin list"""
    xbmcplugin.setContent(handle, 'files')
    xbmcplugin.addDirectoryItems(handle, [(item, xbmcgui.ListItem(item)) for item in items])
    xbmcplugin.endOfDirectory(handle)

def unquoteimage(imagestring):
    if imagestring.startswith('image://'):
        return urllib.unquote(imagestring[8:-1])
    else:
        return imagestring
