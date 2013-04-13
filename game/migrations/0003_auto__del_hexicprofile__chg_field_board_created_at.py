# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'HexicProfile'
        db.delete_table('game_hexicprofile')


        # Changing field 'Board.created_at'
        db.alter_column('game_board', 'created_at', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Adding model 'HexicProfile'
        db.create_table('game_hexicprofile', (
            ('color', self.gf('django.db.models.fields.CharField')(default='#ffffff', max_length=7)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['security.Account'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('game', ['HexicProfile'])


        # Changing field 'Board.created_at'
        db.alter_column('game_board', 'created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True))

    models = {
        'game.board': {
            'Meta': {'object_name': 'Board'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 4, 13, 0, 0)'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'status': ('django.db.models.fields.PositiveIntegerField', [], {})
        }
    }

    complete_apps = ['game']