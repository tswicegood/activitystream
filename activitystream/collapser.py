from django.conf import settings
from django.utils.importlib import import_module
from models import ItemGroup

class CollapsingFinished(Exception):
    pass

class Collapser(object):
    def process_backends(self, backend_strings):
        get_module_and_target = lambda x: x.rsplit('.', 1)
        backends_out = []
        for backend in backend_strings:
            module, target = get_module_and_target(backend)
            module = import_module(module)
            target = getattr(module, target)
            backends_out.append(target())
        return backends_out

    def __init__(self, backends=None):
        if backends is None:
            backends = getattr(settings, 'COLLAPSE_BACKENDS')
        self.backends = self.process_backends(backends)

    def attempt_collapse(self, item):
        try:
            for backend in self.backends:
                backend.collapse(item)
        except CollapsingFinished as e:
            pass

class CollapsingStrategy(object):
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

class TimeBasedStrategy(CollapsingStrategy):
    def get_groups_for_item(self, item):
        return super(TimeBasedStrategy, self).get_groups_for_item(item).filter(started_on__day=item.published.day, started_on__month=item.published.month, started_on__year=item.published.year)

class TypeBasedStrategy(CollapsingStrategy):
    def get_groups_for_item(self, item):
        qs = super(TypeBasedStrategy, self).get_groups_for_item(item)
        return qs.filter(items__type=item.type, items__type__is_collapsible=True)

class TypeAndTimeBasedStrategy(TypeBasedStrategy, TimeBasedStrategy):
    def get_groups_for_item(self, item):
        groups = super(TypeAndTimeBasedStrategy, self).get_groups_for_item(item)
        return groups

