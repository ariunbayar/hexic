# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Board.players'
        db.add_column('game_board', 'players',
                      self.gf('annoying.fields.JSONField')(default=[[0], [0]]),
                      keep_default=False)


        # Changing field 'Board.created_at'
        db.alter_column('game_board', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Deleting field 'Board.players'
        db.delete_column('game_board', 'players')


        # Changing field 'Board.created_at'
        db.alter_column('game_board', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    models = {
        'game.board': {
            'Meta': {'object_name': 'Board'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'players': ('annoying.fields.JSONField', [], {'default': '[[0], [0]]'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {'default': '2'})
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