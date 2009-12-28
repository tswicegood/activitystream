from models import ItemGroup

class CollapsingBackend(object):
    def __init__(self, *args, **kwargs):
        pass

    def get_groups_for_item(self, item):
        return ItemGroup.objects.all()

    def create_new_group(self, item):
        return ItemGroup.objects.create(started_on=item.published, last_modified=item.published)

    def add_to_group(self, group, item):
        group.items.add(item)
        if item.published > group.last_modified:
            group.last_modified = item.published
            group.save()

    def collapse(self, item):
        groups = self.get_groups_for_item(item)
        if len(groups):
            self.add_to_group(groups[0], item)
        else:
            group = self.create_new_group(item)
            self.add_to_group(group, item)

class TimeBasedBackend(CollapsingBackend):
    def get_groups_for_item(self, item):
        qs = super(TimeBasedBackend, self).get_groups_for_item(item)
        qs = qs.filter(**{
                'started_on__day':item.published.day,
                'started_on__month':item.published.month,
                'started_on__year':item.published.year,
            })
        return qs

class TypeBasedBackend(CollapsingBackend):
    def get_groups_for_item(self, item):
        qs = super(TypeBasedBackend, self).get_groups_for_item(item)
        return qs.filter(items__type=item.type, items__type__is_collapsible=True)

class TypeAndTimeBasedBackend(TypeBasedBackend, TimeBasedBackend):
    def get_groups_for_item(self, item):
        groups = super(TypeAndTimeBasedBackend, self).get_groups_for_item(item)
        return groups
