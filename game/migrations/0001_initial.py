# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HexicProfile'
        db.create_table('game_hexicprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['security.Account'])),
            ('color', self.gf('django.db.models.fields.CharField')(default='#ffffff', max_length=7)),
        ))
        db.send_create_signal('game', ['HexicProfile'])


    def backwards(self, orm):
        # Deleting model 'HexicProfile'
        db.delete_table('game_hexicprofile')


    models = {
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
