# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Board.players'
        db.add_column('game_board', 'players',
                      self.gf('django.db.models.fields.CommaSeparatedIntegerField')(default=[], max_length=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Board.players'
        db.delete_column('game_board', 'players')


    models = {
        'game.board': {
            'Meta': {'object_name': 'Board'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'players': ('django.db.models.fields.CommaSeparatedIntegerField', [], {'default': '[]', 'max_length': '2'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['game']