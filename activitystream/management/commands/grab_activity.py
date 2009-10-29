from django.core.management.base import BaseCommand
from activitystream.models import ActivityType, ActivityItem, Link
import datetime
import feedparser
import re

def add_extra(parent, data):
    return Link.objects.create(
        parent=parent,
        href=data["href"],
        rel="rel" in data and data["rel"] or "",
        type=data["type"]
    )

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
                    published = getattr(entry, "published_parsed", entry.updated_parsed)
                    item = ActivityItem.objects.create(
                        uuid=entry.id,
                        source_url=entry.link,
                        type=activity_type,
                        title=entry.title,
                        description=getattr(entry, "summary", ''),
                        slug=regex.sub('', entry.title).strip().replace(' ', '-'),
                        published=datetime.datetime(*published)[:7]
                    )
                    if "links" in entry:
                        [add_extra(item, a) for a in entry["links"]]
                    if "enclosures" in entry:
                        [add_extra(item, a) for a in entry["enclosures"]]

