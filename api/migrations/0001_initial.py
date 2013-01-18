# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Sms'
        s = 'django.db.models.fields%s'
        db.create_table('api_sms', (
            ('id', self.gf(s % '.AutoField')(primary_key=True)),
            ('sender', self.gf(s % '.CharField')(max_length=20)),
            ('text', self.gf(s % '.CharField')(max_length=255)),
            ('account', self.gf(s % '.related.ForeignKey')(
                to=orm['security.Account'], null=True, blank=True)),
            ('action', self.gf(s % '.SmallIntegerField')(default=0)),
            ('date_time', self.gf(s % '.DateTimeField')(
                auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('api', ['Sms'])

    def backwards(self, orm):
        # Deleting model 'Sms'
        db.delete_table('api_sms')

    s = 'django.db.models.fields%s'
    models = {
        'api.sms': {
            'Meta': {'object_name': 'Sms'},
            'account': (s % '.related.ForeignKey', [], {
                'to': "orm['security.Account']",
                'null': 'True', 'blank': 'True'}),
            'action': (s % '.SmallIntegerField', [], {'default': '0'}),
            'date_time': (s % '.DateTimeField', [], {
                'auto_now_add': 'True',
                'blank': 'True'}),
            'id': (s % '.AutoField', [], {'primary_key': 'True'}),
            'sender': (s % '.CharField', [], {'max_length': '20'}),
            'text': (s % '.CharField', [], {'max_length': '255'})
        },
        'security.account': {
            'Meta': {'object_name': 'Account'},
            'created_at': (s % '.DateTimeField', [], {
                'auto_now_add': 'True',
                'blank': 'True'}),
            'credit': (s % '.IntegerField', [], {}),
            'id': (s % '.AutoField', [], {'primary_key': 'True'}),
            'phone_number': (s % '.IntegerField', [], {}),
            'pin_code': (s % '.IntegerField', [], {})
        }
    }

    complete_apps = ['api']
