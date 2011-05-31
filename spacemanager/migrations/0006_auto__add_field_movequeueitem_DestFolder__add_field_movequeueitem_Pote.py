# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'MoveQueueItem.DestFolder'
        db.add_column('spacemanager_movequeueitem', 'DestFolder', self.gf('django.db.models.fields.CharField')(default='', max_length=1024), keep_default=False)

        # Adding field 'MoveQueueItem.PotentialSpaceFreed'
        db.add_column('spacemanager_movequeueitem', 'PotentialSpaceFreed', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'MoveQueueItem.SourceFolder'
        db.alter_column('spacemanager_movequeueitem', 'SourceFolder', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255))

        # Adding unique constraint on 'MoveQueueItem', fields ['SourceFolder']
        db.create_unique('spacemanager_movequeueitem', ['SourceFolder'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'MoveQueueItem', fields ['SourceFolder']
        db.delete_unique('spacemanager_movequeueitem', ['SourceFolder'])

        # Deleting field 'MoveQueueItem.DestFolder'
        db.delete_column('spacemanager_movequeueitem', 'DestFolder')

        # Deleting field 'MoveQueueItem.PotentialSpaceFreed'
        db.delete_column('spacemanager_movequeueitem', 'PotentialSpaceFreed')

        # Changing field 'MoveQueueItem.SourceFolder'
        db.alter_column('spacemanager_movequeueitem', 'SourceFolder', self.gf('django.db.models.fields.CharField')(max_length=1024))


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
            'DestFolder': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'Meta': {'object_name': 'MoveQueueItem'},
            'PotentialSpaceFreed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'SourceFolder': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spacemanager']
