from django import template
from django.conf import settings
from django.core.cache import cache
from django.template.defaultfilters import stringfilter
from django.template.loader import render_to_string
from dolt import Dolt

register = template.Library()

class Flickr(Dolt):
    # TODO: Move this to where it belongs... definitely doesn't belong here.
    def __init__(self, api_key, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self._api_key = api_key
        self._api_url = "http://api.flickr.com"
        self._url_template = "%(domain)s/services/rest/?format=json&method=%(generated_url)s"
        self._stack_collapser = self._collapse_stack
        self._params_template = "&%s"

    def _collapse_stack(self, *args, **kwargs):
        self._attribute_stack[0:0] = "flickr",
        return ".".join(self._attribute_stack)

    def get_url(self):
        url = super(self.__class__, self).get_url()
        return url + "&api_key=%s" % self._api_key

    def _handle_response(self, response, data):
        return super(self.__class__, self)._handle_response(response, data[14:-1])


@register.filter("flickrify")
@stringfilter
def do_flickrify(uuid, force_refresh=False):
    cache_key = "do_flickrify:%s" % uuid
    result = cache.get(cache_key)
    if not result or force_refresh:
        result = do_uncached_flickrify(uuid)
        cache.set(cache_key, result, 600)
    return result

@register.filter('uncached_flickrify')
@stringfilter
def do_uncached_flickrify(uuid):
    photo_id = uuid.split("/")[-1]
    flickr = Flickr(settings.ACTIVITYSTREAM['FLICKR_API_KEY'])
    response = flickr.photos.getSizes(photo_id=photo_id)
    return response['sizes']['size'][0]['source']

@register.filter("inline_vimeo_player")
def do_inline_vimeo_player(item):
    return item.description.replace('<a href', '<a class="oembeddable" href', 1)

class ActivityStreamItemNode(template.Node):
    def __init__(self, item_to_be_rendered):
        self.item_to_be_rendered = template.Variable(item_to_be_rendered)

    def render(self, context):
        item = self.item_to_be_rendered.resolve(context)
        try:
            t = template.loader.get_template("activitystream/fragments/%s_item.html" % item.type.name)
        except template.TemplateDoesNotExist:
            t = template.loader.get_template("activitystream/fragments/default_item.html")
        return t.render(template.Context({"item": item,}))

@register.tag('display_activity')
def do_display_activity(parser, token):
    _tag_name, item_name = token.split_contents()
    return ActivityStreamItemNode(item_name)
