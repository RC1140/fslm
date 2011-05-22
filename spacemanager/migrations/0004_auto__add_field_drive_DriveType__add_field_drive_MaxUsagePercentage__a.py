# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Drive.DriveType'
        db.add_column('spacemanager_drive', 'DriveType', self.gf('django.db.models.fields.CharField')(max_length=1, null=True), keep_default=False)

        # Adding field 'Drive.MaxUsagePercentage'
        db.add_column('spacemanager_drive', 'MaxUsagePercentage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Adding field 'Drive.IdealFreeSpacePercentage'
        db.add_column('spacemanager_drive', 'IdealFreeSpacePercentage', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Drive.DriveType'
        db.delete_column('spacemanager_drive', 'DriveType')

        # Deleting field 'Drive.MaxUsagePercentage'
        db.delete_column('spacemanager_drive', 'MaxUsagePercentage')

        # Deleting field 'Drive.IdealFreeSpacePercentage'
        db.delete_column('spacemanager_drive', 'IdealFreeSpacePercentage')


    models = {
        'spacemanager.drive': {
            'DriveType': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'IdealFreeSpacePercentage': ('django.db.models.fields.IntegerField', [], {}),
            'MaxUsagePercentage': ('django.db.models.fields.IntegerField', [], {}),
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
