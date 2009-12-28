from activitystream.models import ItemGroup, ActivityItem 
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^list/?$', 'django.views.generic.list_detail.object_list', {
        'queryset': ActivityItem.objects.all(),
    }, name='activitystream_list'),
    url(r'^collapsed/?$', 'django.views.generic.list_detail.object_list', {
        'queryset': ItemGroup.objects.all(),
    }, name='activitystream_list_collapsed')
)

