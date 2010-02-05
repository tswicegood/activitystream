from activitystream.templatetags.activitystream_extras import do_flickrify
from activitystream.management.commands.grab_activity import Command as ActivityGrabber
from activitystream.models import ActivityType, ActivityItem
from celery.decorators import task
from celery.registry import tasks
from celery.task import PeriodicTask, Task
from datetime import datetime, timedelta

@task
def update_flickrify_cache(uuid):
    logger = Task.get_logger()
    logger.info("[update_flickrify_cache] starting work on %s" % uuid)
    do_flickrify(uuid, force_refresh=True)

@task
def update_flickr_queryset(queryset):
    for item in queryset:
        update_flickrify_cache.delay(item.uuid)


class UpdateFlickrPhotos(PeriodicTask):
    run_every = timedelta(minutes=9)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Starting Flickr cache update")

        flickr = ActivityType.objects.get(name='flickr')
        queryset = ActivityItem.objects.filter(type=flickr, published__gte=datetime.now() - timedelta(days=90))

        logger.info("Updating Flickr cache for %d photos" % queryset.count())
        update_flickr_queryset.delay(queryset)

class UpdateActivityStream(PeriodicTask):
    run_every = timedelta(minutes=10)
    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("UpdateActivityStream started")

        grabber = ActivityGrabber()
        grabber.handle()

