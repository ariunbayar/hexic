# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Account'
        db.create_table('security_account', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone_number', self.gf('django.db.models.fields.IntegerField')()),
            ('pin_code', self.gf('django.db.models.fields.IntegerField')()),
            ('credit', self.gf('django.db.models.fields.IntegerField')()),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('security', ['Account'])


    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table('security_account')


    models = {
        'security.account': {
            'Meta': {'object_name': 'Account'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'credit': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.IntegerField', [], {}),
            'pin_code': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['security']