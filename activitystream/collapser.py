from django.conf import settings as django_settings
from django.utils.importlib import import_module

class CollapsingFinished(Exception):
    pass

class Collapser(object):
    def process_backends(self, backend_strings, import_fn=import_module):
        get_module_and_target = lambda x: x.rsplit('.', 1)
        backends_out = []
        for backend in backend_strings:
            module, target = get_module_and_target(backend)
            module = import_fn(module)
            target = getattr(module, target)
            backends_out.append(target())
        return backends_out

    def __init__(self, settings=django_settings):
        backends = getattr(settings, 'COLLAPSE_BACKENDS')
        self.backends = self.process_backends(backends)

    def attempt_collapse(self, item):
        try:
            [backend.collapse(item) for backend in self.backends]
        except CollapsingFinished:
            pass
