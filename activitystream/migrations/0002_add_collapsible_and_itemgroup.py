
from south.db import db
from django.db import models
from activitystream.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ItemGroup'
        db.create_table('activitystream_itemgroup', (
            ('id', models.AutoField(primary_key=True)),
            ('started_on', models.DateTimeField()),
            ('last_modified', models.DateTimeField()),
        ))
        db.send_create_signal('activitystream', ['ItemGroup'])
        
        # Adding field 'ActivityType.is_collapsible'
        db.add_column('activitystream_activitytype', 'is_collapsible', models.BooleanField(db_index=True))
        
        # Adding ManyToManyField 'ItemGroup.items'
        db.create_table('activitystream_itemgroup_items', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('itemgroup', models.ForeignKey(orm.ItemGroup, null=False)),
            ('activityitem', models.ForeignKey(orm.ActivityItem, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ItemGroup'
        db.delete_table('activitystream_itemgroup')
        
        # Deleting field 'ActivityType.is_collapsible'
        db.delete_column('activitystream_activitytype', 'is_collapsible')
        
        # Dropping ManyToManyField 'ItemGroup.items'
        db.delete_table('activitystream_itemgroup_items')
        
    
    
    models = {
        'activitystream.activitytype': {
            'avatar': ('models.ForeignKey', ["orm['activitystream.Avatar']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_collapsible': ('models.BooleanField', [], {'db_index': 'True'}),
            'name': ('models.CharField', [], {'max_length': '50'}),
            'slug': ('models.SlugField', [], {}),
            'source_url': ('models.URLField', [], {})
        },
        'activitystream.link': {
            'href': ('models.CharField', [], {'max_length': '250'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'parent': ('models.ForeignKey', ["orm['activitystream.ActivityItem']"], {'related_name': '"links"'}),
            'rel': ('models.CharField', [], {'max_length': '250'}),
            'type': ('models.CharField', [], {'max_length': '100'})
        },
        'activitystream.avatar': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'url': ('models.URLField', [], {})
        },
        'activitystream.activityitem': {
            'Meta': {'ordering': "['-published']"},
            'description': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'published': ('models.DateTimeField', [], {}),
            'slug': ('models.SlugField', [], {}),
            'source_url': ('models.URLField', [], {}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'type': ('models.ForeignKey', ["orm['activitystream.ActivityType']"], {}),
            'uuid': ('models.CharField', [], {'max_length': '255'})
        },
        'activitystream.itemgroup': {
            'Meta': {'ordering': "['-last_modified']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'items': ('models.ManyToManyField', ["orm['activitystream.ActivityItem']"], {'related_name': "'collapsed_into'"}),
            'last_modified': ('models.DateTimeField', [], {}),
            'started_on': ('models.DateTimeField', [], {})
        }
    }
    
    complete_apps = ['activitystream']
