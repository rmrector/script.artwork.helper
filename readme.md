# Artwork Skin Helper

Artwork Skin Helper provides useful tools to skins and other add-ons for working with artwork.

## ListItem multi image plugin path
The simplest form grabs multiple images for the currently focused ListItem, suitable to populate a `multiimage` or list control.

`plugin://script.artwork.skinhelper/multiimage/listitem/?refresh=$INFO[ListItem.DBID]`

 Mostly for fanart (fanart#), but works for any art type that has one or more images. Additional query params are available to modify its behavior, separate them with `&amp;&amp;`.
- `refresh` is required to get Kodi to fire off the plugin when the focused item changes. Set it to something that will change when the fanart should change (ListItem.DBID, or ListItem.TVShowTitle for series fanart when listing episodes/seasons)
- `containerid` points to an alternate container
- `arttype` lets you select different artwork. 'tvshow.fanart' is a useful alternative for a list of seasons/episodes.
- `shuffle` shuffles the list, if you aren't using a multiimage control that can randomize it

## Arbitrary images plugin path
This format lets you stitch any images together into a list.

`plugin://script.artwork.skinhelper/multiimage/?image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>&amp;&amp;image=<image_path>`

 When the ListItem option above doesn't work for you, this is your very wordy friend. Repeat the image block for as many images as you like, and it will ignore empty ones. The double `&amp;&amp;` separator between images is required.
