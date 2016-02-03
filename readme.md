# Artwork Helper

Artwork Helper currently provides a couple of tools to skins and other add-ons for working with artwork.

## ListItem multi image plugin path

The simplest form grabs multiple images for the currently focused ListItem, suitable to populate a `multiimage` or list control.  
`plugin://script.artwork.helper/multiimage/listitem/?refresh=$INFO[ListItem.DBID]`

Mostly for fanart (fanart#), but works for any art type that has one or more images. Additional query params are available to modify its behavior, separate them with `&amp;&amp;`.
- `refresh` is required to get Kodi to fire off the plugin when the focused item changes. Set it to something that will change when the fanart should change (ListItem.DBID, or ListItem.TVShowTitle for series fanart when listing episodes/seasons)
- `containerid` points to an alternate container
- `arttype` lets you select different artwork. 'tvshow.fanart' is a useful alternative for a list of seasons/episodes.
- `shuffle` shuffles the list, maybe useful if you aren't using a multiimage control that can randomize it

With the full complement of options:  
`plugin://script.artwork.helper/multiimage/listitem/?refresh=$INFO[ListItem.DBID]&amp;&amp;containerid=4250&amp;&amp;arttype=tvshow.fanart&amp;&amp;shuffle=true`

## Arbitrary images plugin path

This format lets you stitch any images together into a list, by specifying their path.  
`plugin://script.artwork.helper/multiimage/?image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>`

When the ListItem option above doesn't work for you, this is your very wordy friend. Repeat the image block for as many images as you like, and it will ignore empty ones. The double ampersand `&amp;&amp;` separator between images is required.

## Series artwork grabber

This is just a temporary workaround for a bug in Kodi that leaves `ListItem.Art(tvshow.*)` empty when the selected season or episode has its own fanart. The real fix is scheduled for Kodi Krypton, with PR [#8645](https://github.com/xbmc/xbmc/pull/8645).

To use it, stick `<onload>RunScript(script.artwork.helper, SeriesArtworkGrabber)</onload>` on MyVideoNav.xml and VideoFullscreen.xml if you need series artwork on these windows.

When items that are affected (`IsEmpty(ListItem.Art(tvshow.fanart)` or `Player.Art`) are selected or played, `Window.Property(tvshow.*)` is set.
