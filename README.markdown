Activity Stream
===============
This is a simple project for bringing together RSS feeds from a bunch
of different sources and displaying them in a single stream of activity.


Usage
-----

### Vimeo
Vimeo's default item rendering (located in
activitystream/fragments/vimeo_item.html) adds a the `embeddable` CSS class to
the link for Vimeo objects.  You can use this to hook up inline viewing, as is
done in the default project.

Make sure you have [jquery-oembed][jquery-oembed] code loaded, then add
something along the lines of the following to your `base.html` file:

    $(document).ready(function() {
        $('.oembeddable').click(function() {
            console.log("sup?");
            $(this).oembed();
            return false;
        });
    });


[jquery-oembed]: http://code.google.com/p/jquery-oembed/
