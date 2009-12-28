from django.test import TestCase
from collapser import Collapser, CollapsingFinished
from models import *
from backends import *
import datetime

class SetupHelper(object):
    def create_avatar(self):
        return Avatar.objects.create(**{
            'url':'http://www.google.com/',
        })

    def create_type(self, is_collapsible, avatar=None):
        if avatar is None:
            avatar = self.create_avatar()
        return ActivityType.objects.create(**{
            'slug':'test',
            'name':'test',
            'source_url':'http://www.google.com/',
            'avatar':avatar,
            'is_collapsible':is_collapsible,
        })

    def create_item(self, **kwargs):
        defaults = {
            'uuid':'10101010',
            'source_url':'http://www.google.com/',
            'slug':'test-slug',
            'title':'title',
            'description':'desc',
        }
        defaults.update(kwargs)
        return ActivityItem.objects.create(**defaults)

class ActivityItemTest(TestCase, SetupHelper):
    def setUp(self):
        type = self.create_type(False)
        self.item = self.create_item(**{
            'type':type,
            'published':datetime.datetime.now()
        })

    def test_collapse(self):
        class fake_collapser(object):
            def attempt_collapse(_self, item):
                self.assertTrue(isinstance(item, ActivityItem))
                self.assertEqual(item, self.item)
        self.item.collapse(fake_collapser())

class CollapserTest(TestCase):
    def test_process_backends(self):
        initialized = []
        triggers = {
            'getattr':False
        }
        class SettingsMock(object):
            COLLAPSE_BACKENDS = [
                'place.to.look'
            ]

        class TestInitialized(object):
            def __init__(_self):
                initialized.append(_self)

        class ModuleMock(object):
            def __getattr__(self, what):
                triggers['getattr'] = True
                return TestInitialized       

        def generate_mock_import_fn(should_equal):
            def mock_import_fn(module):
                self.assertEqual(should_equal, module)
                return ModuleMock() 
            return mock_import_fn

        class CollapserMock(Collapser):
            def __init__(self, import_fn, *args, **kwargs):
                self.import_fn = import_fn
                super(CollapserMock,self).__init__(*args, **kwargs)
            def process_backends(self, *args, **kwargs):
                defaults = {
                    'import_fn':self.import_fn,
                }
                defaults.update(kwargs)
                return super(CollapserMock,self).process_backends(*args, **defaults)
        cmock = CollapserMock(generate_mock_import_fn('place.to'), SettingsMock())
        self.assertTrue(isinstance(initialized[0], TestInitialized))
        self.assertTrue(triggers['getattr'])
        self.assertEqual(1, len(cmock.backends))

    def test_attempt_collapse(self):
        backends_called = []
        class BackendMock(object):
            def __init__(_self, throws=False):
                _self.throws = throws

            def collapse(_self, what):
                backends_called.append(_self)
                if _self.throws:
                    raise CollapsingFinished                
        class CollapserMock(Collapser):
            def __init__(self, backends):
                self.backends = backends

        plain_backends = [
            BackendMock(),
            BackendMock(),
            BackendMock(),
        ]

        collapser = CollapserMock(plain_backends)
        collapser.attempt_collapse('any old value')

        self.assertEqual(len(backends_called), len(plain_backends))
        backends_called = []
        stop_backends = [
            BackendMock(),
            BackendMock(True),      # should stop iterating here!
            BackendMock(),
        ]
        collapser = CollapserMock(stop_backends)
        collapser.attempt_collapse('any old value, again')
        self.assertEqual(len(backends_called), 2)


class AbstractCollapsingTest(TestCase):
    def test_collapsing(self):
        groups = {}
        class BackendMock(CollapsingBackend):
            def get_groups_for_item(_self, item):
                group = groups.get(item.__class__, None) 
                if group is None:
                    return []
                return [group]
            def add_to_group(_self, group, item):
                group.append(item)
            def create_new_group(_self, item):
                groups[item.__class__] = []
                return groups[item.__class__]

        class CollapserMock(Collapser):
            def __init__(self):
                self.backends = [BackendMock(),]

        group_these_by_type = [
            1,2,3,
            "four", object(), 1.2, 2.4, 3, object(), 'six',
            [0,1,2], (2,4), [1,2,3], (4,5),
        ]

        expected_lengths = {
            int: 4,
            str: 2,
            object: 2,
            list: 2,
            float: 2,
            tuple: 2,
        } 

        cmock = CollapserMock()
        [cmock.attempt_collapse(i) for i in group_these_by_type]

        self.assertEqual(groups.keys(), [int, str, object, list, float, tuple])
        for key, items in groups.iteritems():
            for item in items:
                self.assertEqual(key, item.__class__)
            self.assertEqual(expected_lengths[key], len(groups[key]))
