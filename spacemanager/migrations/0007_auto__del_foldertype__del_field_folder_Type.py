# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'FolderType'
        db.delete_table('spacemanager_foldertype')

        # Deleting field 'Folder.Type'
        db.delete_column('spacemanager_folder', 'Type_id')


    def backwards(self, orm):
        
        # Adding model 'FolderType'
        db.create_table('spacemanager_foldertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('MediaType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spacemanager.MediaType'])),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('spacemanager', ['FolderType'])

        # User chose to not deal with backwards NULL issues for 'Folder.Type'
        raise RuntimeError("Cannot reverse this migration. 'Folder.Type' and its values cannot be restored.")


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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.mediatype': {
            'Meta': {'object_name': 'MediaType'},
            'Name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'spacemanager.movequeueitem': {
            'DestFolder': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'Meta': {'object_name': 'MoveQueueItem'},
            'PotentialSpaceFreed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'SourceFolder': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spacemanager']
