# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MoveQueueItem'
        db.create_table('spacemanager_movequeueitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('SourceFolder', self.gf('django.db.models.fields.CharField')(max_length=1024)),
        ))
        db.send_create_signal('spacemanager', ['MoveQueueItem'])

        # Adding field 'Drive.DumpPreference'
        db.add_column('spacemanager_drive', 'DumpPreference', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'MoveQueueItem'
        db.delete_table('spacemanager_movequeueitem')

        # Deleting field 'Drive.DumpPreference'
        db.delete_column('spacemanager_drive', 'DumpPreference')


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
            'Meta': {'object_name': 'Folder'},
            'Path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '1024'}),
            'Type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spacemanager.FolderType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.foldertype': {
            'MediaType': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['spacemanager.MediaType']"}),
            'Meta': {'object_name': 'FolderType'},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.mediatype': {
            'Meta': {'object_name': 'MediaType'},
            'Name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.movequeueitem': {
            'Meta': {'object_name': 'MoveQueueItem'},
            'SourceFolder': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spacemanager']
