from django.db import models

class Avatar(models.Model):
    url = models.URLField()

class ActivityType(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length = 50)
    source_url = models.URLField()
    avatar = models.ForeignKey(Avatar)

    def __unicode__(self):
        return self.name

class ActivityItem(models.Model):
    uuid = models.CharField(max_length = 255)
    slug = models.SlugField()
    title = models.CharField(max_length = 255)
    description = models.TextField()
    type = models.ForeignKey(ActivityType)
    published = models.DateTimeField()

    class Meta(object):
        ordering = ['-published']

    def __unicode__(self):
        return "%s: %s" % (self.type, self.title)
