# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Folder'
        db.create_table('spacemanager_folder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Drive', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spacemanager.Drive'])),
            ('Type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spacemanager.FolderType'])),
        ))
        db.send_create_signal('spacemanager', ['Folder'])

        # Adding model 'MediaType'
        db.create_table('spacemanager_mediatype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('spacemanager', ['MediaType'])

        # Adding model 'FolderType'
        db.create_table('spacemanager_foldertype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('MediaType', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['spacemanager.MediaType'])),
        ))
        db.send_create_signal('spacemanager', ['FolderType'])

        # Adding model 'Drive'
        db.create_table('spacemanager_drive', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Path', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('spacemanager', ['Drive'])


    def backwards(self, orm):
        
        # Deleting model 'Folder'
        db.delete_table('spacemanager_folder')

        # Deleting model 'MediaType'
        db.delete_table('spacemanager_mediatype')

        # Deleting model 'FolderType'
        db.delete_table('spacemanager_foldertype')

        # Deleting model 'Drive'
        db.delete_table('spacemanager_drive')


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
