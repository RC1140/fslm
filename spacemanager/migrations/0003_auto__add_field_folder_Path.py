# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Folder.Path'
        db.add_column('spacemanager_folder', 'Path', self.gf('django.db.models.fields.CharField')(default='', max_length=1024), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Folder.Path'
        db.delete_column('spacemanager_folder', 'Path')


    models = {
        'spacemanager.drive': {
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
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['spacemanager']
