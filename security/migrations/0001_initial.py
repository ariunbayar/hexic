# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Account'
        s = 'django.db.models.fields%s'
        db.create_table('security_account', (
            ('id', self.gf(s % '.AutoField')(primary_key=True)),
            ('phone_number', self.gf(s % '.IntegerField')()),
            ('pin_code', self.gf(s % '.IntegerField')()),
            ('credit', self.gf(s % '.IntegerField')()),
        ))
        db.send_create_signal('security', ['Account'])

    def backwards(self, orm):
        # Deleting model 'Account'
        db.delete_table('security_account')

    s = 'django.db.models.fields%s'
    models = {
        'security.account': {
            'Meta': {'object_name': 'Account'},
            'credit': (s % '.IntegerField', [], {}),
            'id': (s % '.AutoField', [], {'primary_key': 'True'}),
            'phone_number': (s % '.IntegerField', [], {}),
            'pin_code': (s % '.IntegerField', [], {})
        }
    }

    complete_apps = ['security']
