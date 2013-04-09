# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ActiveBoard'
        db.create_table('game_activeboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('game', ['ActiveBoard'])


    def backwards(self, orm):
        # Deleting model 'ActiveBoard'
        db.delete_table('game_activeboard')


    models = {
        'game.activeboard': {
            'Meta': {'object_name': 'ActiveBoard'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'game.hexicprofile': {
            'Meta': {'object_name': 'HexicProfile'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['security.Account']"}),
            'color': ('django.db.models.fields.CharField', [], {'default': "'#ffffff'", 'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'security.account': {
            'Meta': {'object_name': 'Account'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {}),
            'pin_code': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['game']