from django.db import models

class Avatar(models.Model):
    url = models.URLField()

    def __unicode__(self):
        return self.url

class ActivityType(models.Model):
    slug = models.SlugField()
    name = models.CharField(max_length = 50)
    source_url = models.URLField()
    avatar = models.ForeignKey(Avatar)
    is_collapsible = models.BooleanField(db_index=True)
    def __unicode__(self):
        return self.name

class ItemGroup(models.Model):
    items = models.ManyToManyField('ActivityItem', related_name='collapsed_into')
    started_on = models.DateTimeField()
    last_modified = models.DateTimeField()
    class Meta:
        ordering = ['-last_modified']

class ActivityItem(models.Model):
    uuid = models.CharField(max_length = 255)
    source_url = models.URLField()
    slug = models.SlugField()
    title = models.CharField(max_length = 255)
    description = models.TextField()
    type = models.ForeignKey(ActivityType)
    published = models.DateTimeField()

    class Meta(object):
        ordering = ['-published']

    def __unicode__(self):
        return "%s: %s" % (self.type, self.title)

    def collapse(self, collapser):
        collapser.attempt_collapse(self)

class LinkManager(models.Manager):
    def images(self):
        # TODO, this isn't going to perform well
        return self.filter(type__startswith="image/")

    def image(self):
        return self.images()[0]

class Link(models.Model):
    href = models.CharField(max_length=250)
    rel = models.CharField(max_length=250)
    type = models.CharField(max_length=100)

    parent = models.ForeignKey(ActivityItem, related_name="links")

    objects = LinkManager()

