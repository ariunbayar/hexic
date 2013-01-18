# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sms'
        db.create_table('api_sms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('account', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['security.Account'], null=True, blank=True)),
            ('action', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('date_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('api', ['Sms'])


    def backwards(self, orm):
        # Deleting model 'Sms'
        db.delete_table('api_sms')


    models = {
        'api.sms': {
            'Meta': {'object_name': 'Sms'},
            'account': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['security.Account']", 'null': 'True', 'blank': 'True'}),
            'action': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'date_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sender': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '255'})
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

    complete_apps = ['api']