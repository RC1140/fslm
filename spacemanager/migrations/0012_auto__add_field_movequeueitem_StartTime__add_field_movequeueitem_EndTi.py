# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MoveQueueItem.StartTime'
        db.add_column('spacemanager_movequeueitem', 'StartTime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2011, 6, 9)), keep_default=False)

        # Adding field 'MoveQueueItem.EndTime'
        db.add_column('spacemanager_movequeueitem', 'EndTime', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.date(2011, 6, 9), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'MoveQueueItem.StartTime'
        db.delete_column('spacemanager_movequeueitem', 'StartTime')

        # Deleting field 'MoveQueueItem.EndTime'
        db.delete_column('spacemanager_movequeueitem', 'EndTime')


    models = {
        'spacemanager.drive': {
            'DriveType': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'DumpPreference': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'IdealFreeSpacePercentage': ('django.db.models.fields.IntegerField', [], {'default': '50'}),
            'MaxUsagePercentage': ('django.db.models.fields.IntegerField', [], {'default': '80'}),
            'Meta': {'object_name': 'Drive'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'Path': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.folder': {
            'Drive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spacemanager.Drive']"}),
            'MediaType': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['spacemanager.MediaType']"}),
            'Meta': {'object_name': 'Folder'},
            'Path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.mediatype': {
            'Meta': {'object_name': 'MediaType'},
            'Name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.movequeueitem': {
            'DestFolder': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'EndTime': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'Meta': {'object_name': 'MoveQueueItem'},
            'PotentialSpaceFreed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'SourceFolder': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'StartTime': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.setting': {
            'Meta': {'object_name': 'Setting'},
            'SettingKey': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            'Value': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spacemanager']
