import json
import sys
import urllib
import xbmc

def handle_command():
    command = get_command()
    if 'command' not in command or not command['command']:
        xbmc.log('[script.artwork.helper] Running without a command/first argument is not supported.', xbmc.LOGWARNING)
        return
    if command['command'] == 'seriesartworkgrabber':
        watchforartwork()

def get_command():
    command = {}
    for x in range(2, len(sys.argv)):
        arg = sys.argv[x].split("=", 1)
        command[arg[0].strip().lower()] = arg[1].strip() if len(arg) > 1 else True
    if len(sys.argv) > 1:
        command['command'] = sys.argv[1].strip().lower()

    return command

# NOTE: After my pull request, this won't be needed to grab series artwork
def watchforartwork():
    fullscreenvideo = xbmc.getCondVisibility('Window.IsVisible(fullscreenvideo)')
    WatchForArtwork(fullscreenvideo).run()

class WatchForArtwork(object):
    def __init__(self, fullscreenvideo):
        self.fullscreenvideo = fullscreenvideo
        self.wait = 5 if fullscreenvideo else 0.1
        self.window = 'fullscreenvideo' if fullscreenvideo else 'videos'
        self.windowvisible = 'Window.IsVisible({0})'.format(self.window)
        self.needsartwork_conditional = 'IsEmpty({0}.Art(tvshow.fanart))'.format('Player' if fullscreenvideo else 'ListItem')
        self.seriestitle_info = '{0}.TVShowTitle'.format('VideoPlayer' if fullscreenvideo else 'ListItem')

        self.imagestoclear = []

    def run(self):
        monitor = xbmc.Monitor()
        seriestitle = None
        didneedartwork = False
        while xbmc.getCondVisibility(self.windowvisible):
            if self.fullscreenvideo or xbmc.getCondVisibility('Container.Content(episodes) | Container.Content(seasons)'):
                needsartwork = xbmc.getCondVisibility(self.needsartwork_conditional)
                if not needsartwork:
                    if self.imagestoclear:
                        self.clearproperties_seriesartwork()
                    didneedartwork = False
                    if monitor.waitForAbort(self.wait):
                        break
                    continue
                newseriestitle = xbmc.getInfoLabel(self.seriestitle_info)
                if newseriestitle != seriestitle or needsartwork != didneedartwork:
                    if newseriestitle:
                        self.grab_and_set_artwork(newseriestitle)
                    else:
                        self.clearproperties_seriesartwork()
                seriestitle = newseriestitle
                didneedartwork = needsartwork
            elif self.imagestoclear:
                self.clearproperties_seriesartwork()
                didneedartwork = False
            if monitor.waitForAbort(self.wait):
                break

        self.clearproperties_seriesartwork()

    def grab_and_set_artwork(self, seriestitle):
        json_request = get_base_json_request('VideoLibrary.GetTVShows')
        json_request['params']['filter'] = {'field': 'title', 'operator': 'is', 'value': seriestitle}
        json_request['params']['properties'] = ['art']
        json_result = execute_jsonrpc(json_request)
        images = dict((key, None) for key in self.imagestoclear)
        del self.imagestoclear[:]
        if 'result' in json_result and json_result['result']['tvshows']:
            result = json_result['result']['tvshows'][0]
            for arttype, image in result['art'].iteritems():
                arttype = 'tvshow.' + arttype
                images[arttype] = image
                self.imagestoclear.append(arttype)

        for arttype, image in images.iteritems():
            if image:
                xbmc.executebuiltin('SetProperty(%s, %s, %s)' % (arttype, unquoteimage(image), self.window))
            else:
                xbmc.executebuiltin('ClearProperty(%s, %s)' % (arttype, self.window))

    def clearproperties_seriesartwork(self):
        for arttype in self.imagestoclear:
            xbmc.executebuiltin('ClearProperty(%s, %s)' % (arttype, self.window))
        del self.imagestoclear[:]

def execute_jsonrpc(jsonrpc_command):
    if isinstance(jsonrpc_command, dict):
        jsonrpc_command = json.dumps(jsonrpc_command)

    json_result = xbmc.executeJSONRPC(jsonrpc_command)
    return json.loads(json_result, cls=UTF8JSONDecoder)

def get_base_json_request(method):
    return {'jsonrpc': '2.0', 'method': method, 'params': {}, 'id': 1}

def unquoteimage(imagestring):
    if imagestring.startswith('image://'):
        return urllib.unquote(imagestring[8:-1])
    else:
        return imagestring

class UTF8JSONDecoder(json.JSONDecoder):
    def __init__(self, *args, **kwargs):
        super(UTF8JSONDecoder, self).__init__(*args, **kwargs)

    def raw_decode(self, s, idx=0):
        result, end = super(UTF8JSONDecoder, self).raw_decode(s)
        result = self._json_unicode_to_str(result)
        return result, end

    def _json_unicode_to_str(self, jsoninput):
        if isinstance(jsoninput, dict):
            return dict((self._json_unicode_to_str(key), self._json_unicode_to_str(value)) for key, value in jsoninput.iteritems())
        elif isinstance(jsoninput, list):
            return [self._json_unicode_to_str(item) for item in jsoninput]
        elif isinstance(jsoninput, unicode):
            return jsoninput.encode('utf-8')
        else:
            return jsoninput
