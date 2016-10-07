# Artwork Helper

Artwork Helper provides skins a few options for building a list of images for a `multiimage`
or list control from images available via InfoLabels. This is a helper for a general replacement of
extrafanart/extrathumbs, see [this forum post] for a rambling explanation on why we might want that.
This is a small add-on that skins can use as a dependency, only doing what a skin asks it to do.

[this forum post]: http://forum.kodi.tv/showthread.php?tid=236649

## Add-on setting

There is an add-on setting to pull extrafanart and extrathumbs from the filesystem, if there is
only a single image in the library. It is off by default, but can be turned on by the end user/viewer.
It can be found by navigating to Kodi settings -> Add-ons -> System -> Dependencies -> Artwork Helper.

## ListItem multi image plugin path

The simplest form grabs multiple images for the currently focused ListItem.  
`plugin://script.artwork.helper/multiimage/listitem/?refresh=$INFO[ListItem.DBID]`

Mostly for fanart (fanart#), but works for any art type that has one or more images.
Additional query params are available to modify its behavior, separate them with `&amp;&amp;`.
- `refresh` is required to get Kodi to fire off the plugin when the focused item changes. Set it
  to something that will change when the fanart should change, like ListItem.DBID
- `containerid` points to an alternate container
- `arttype` lets you select different artwork. Defaults to 'fanart'.
- `shuffle` shuffles the list, maybe useful if you aren't using a multiimage control that can randomize it

With the full complement of options:  
`plugin://script.artwork.helper/multiimage/listitem/?refresh=$INFO[ListItem.DBID]&amp;&amp;containerid=4250&amp;&amp;arttype=tvshow.fanart&amp;&amp;shuffle=true`

## Container multi image plugin path

This grabs multiple images for the current Container.  
`plugin://script.artwork.helper/multiimage/container/?refresh=$INFO[Container.FolderName]`

Additional query params are available to modify its behavior, separate them with `&amp;&amp;`.
- `refresh` is required to get Kodi to fire off the plugin when the focused item changes. Set it
  to something that will change when the fanart should change, like Container.FolderName
- `arttype` lets you select different artwork. Defaults to 'tvshow.fanart'.
- `shuffle` shuffles the list, maybe useful if you aren't using a multiimage control that can randomize it

With the full complement of options:  
`plugin://script.artwork.helper/multiimage/container/?refresh=$INFO[ListItem.DBID]&amp;&amp;arttype=set.fanart&amp;&amp;shuffle=true`

## Smart series multi image plugin path

This grabs multiple images for the current series, keeping the path the same through
series-season-episode lists so that the fanart display stays smooth.  
`plugin://script.artwork.helper/multiimage/smartseries/?title=$INFO[ListItem.Title]`

Additional query params are available to modify its behavior, separate them with `&amp;&amp;`.
- `title` is required to get Kodi to fire off the plugin when the focused item changes, like
  'refresh' in ListItem/Container paths. Set it to ListItem.Title if Container.Content is tvshows
  and Container.TVShowTitle if seasons/episodes.
- `arttype` lets you select different artwork. Defaults to 'fanart'. Use only the base
  art type like 'fanart', the plugin will decide if tvshow.* is needed.
- `shuffle` shuffles the list, maybe useful if you aren't using a multiimage control that can randomize it

With the full complement of options:  
`plugin://script.artwork.helper/multiimage/smartseries/?title=$INFO[ListItem.Title]&amp;&amp;arttype=fanart&amp;&amp;shuffle=true`

## Arbitrary images plugin path

This format lets you stitch any images together into a list, by specifying their path.  
`plugin://script.artwork.helper/multiimage/?image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>`

When the ListItem option above doesn't work for you, this is your very wordy friend. Repeat the
image block for as many images as you like, and it will ignore empty ones. The
double ampersand `&amp;&amp;` separator between images is required.

