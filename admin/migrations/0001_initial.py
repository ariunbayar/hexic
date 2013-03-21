# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Admin'
        s = 'django.db.models.fields%s'
        db.create_table('admin_admin', (
            ('id', self.gf(s % '.AutoField')(primary_key=True)),
            ('user_name', self.gf(s % '.CharField')(max_length=50)),
            ('email', self.gf(s % '.EmailField')(max_length=75)),
            ('password', self.gf(s % '.CharField')(max_length=50)),
        ))
        db.send_create_signal('admin', ['Admin'])

    def backwards(self, orm):
        # Deleting model 'Admin'
        db.delete_table('admin_admin')

    s = 'django.db.models.fields%s'
    models = {
        'admin.admin': {
            'Meta': {'object_name': 'Admin'},
            'email': (s % '.EmailField', [], {'max_length': '75'}),
            'id': (s % '.AutoField', [], {'primary_key': 'True'}),
            'password': (s % '.CharField', [], {'max_length': '50'}),
            'user_name': (s % '.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['admin']
