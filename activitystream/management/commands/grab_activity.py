from django.core.management.base import BaseCommand
from activitystream.models import ActivityType, ActivityItem
import datetime
import feedparser
import re

class Command(BaseCommand):
    def handle(self, *args, **kwags):
        # TODO: handle this so it doesn't try to grab everything sequentially
        # TODO: do this via a conditional GET
        types = ActivityType.objects.all()
        regex = re.compile('&[^;]+;|\(.*\)')
        for activity_type in types:
            d = feedparser.parse(activity_type.source_url)
            for entry in d['entries']:
                try:
                    ActivityItem.objects.get(uuid=entry.id)
                except ActivityItem.DoesNotExist:
                    item = ActivityItem.objects.create(
                        uuid=entry.id,
                        source_url=entry.link,
                        type=activity_type,
                        title=entry.title,
                        description=getattr(entry, "summary", ''),
                        slug=regex.sub('', entry.title).strip().replace(' ', '-'),
                        published=datetime.datetime(*entry.published_parsed[:7])
                    )

