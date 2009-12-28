
from south.db import db
from django.db import models
from activitystream.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'ActivityType'
        db.create_table('activitystream_activitytype', (
            ('id', models.AutoField(primary_key=True)),
            ('slug', models.SlugField()),
            ('name', models.CharField(max_length=50)),
            ('source_url', models.URLField()),
            ('avatar', models.ForeignKey(orm.Avatar)),
        ))
        db.send_create_signal('activitystream', ['ActivityType'])
        
        # Adding model 'Link'
        db.create_table('activitystream_link', (
            ('id', models.AutoField(primary_key=True)),
            ('href', models.CharField(max_length=250)),
            ('rel', models.CharField(max_length=250)),
            ('type', models.CharField(max_length=100)),
            ('parent', models.ForeignKey(orm.ActivityItem, related_name="links")),
        ))
        db.send_create_signal('activitystream', ['Link'])
        
        # Adding model 'Avatar'
        db.create_table('activitystream_avatar', (
            ('id', models.AutoField(primary_key=True)),
            ('url', models.URLField()),
        ))
        db.send_create_signal('activitystream', ['Avatar'])
        
        # Adding model 'ActivityItem'
        db.create_table('activitystream_activityitem', (
            ('id', models.AutoField(primary_key=True)),
            ('uuid', models.CharField(max_length=255)),
            ('source_url', models.URLField()),
            ('slug', models.SlugField()),
            ('title', models.CharField(max_length=255)),
            ('description', models.TextField()),
            ('type', models.ForeignKey(orm.ActivityType)),
            ('published', models.DateTimeField()),
        ))
        db.send_create_signal('activitystream', ['ActivityItem'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ActivityType'
        db.delete_table('activitystream_activitytype')
        
        # Deleting model 'Link'
        db.delete_table('activitystream_link')
        
        # Deleting model 'Avatar'
        db.delete_table('activitystream_avatar')
        
        # Deleting model 'ActivityItem'
        db.delete_table('activitystream_activityitem')
        
    
    
    models = {
        'activitystream.activitytype': {
            'avatar': ('models.ForeignKey', ["orm['activitystream.Avatar']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
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
        }
    }
    
    complete_apps = ['activitystream']
