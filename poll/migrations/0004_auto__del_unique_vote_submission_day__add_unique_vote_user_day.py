# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['submission', 'day']
        db.delete_unique(u'poll_vote', ['submission_id', 'day'])

        # Adding unique constraint on 'Vote', fields ['user', 'day']
        db.create_unique(u'poll_vote', ['user_id', 'day'])


    def backwards(self, orm):
        # Removing unique constraint on 'Vote', fields ['user', 'day']
        db.delete_unique(u'poll_vote', ['user_id', 'day'])

        # Adding unique constraint on 'Vote', fields ['submission', 'day']
        db.create_unique(u'poll_vote', ['submission_id', 'day'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'poll.poll': {
            'Meta': {'object_name': 'Poll'},
            'bot_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'frequency': ('django.db.models.fields.IntegerField', [], {'default': '24'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'stub': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'submission_removal': ('django.db.models.fields.IntegerField', [], {'default': '168'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'poll.submission': {
            'Meta': {'object_name': 'Submission'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'poll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'poll_submissions'", 'to': u"orm['poll.Poll']"}),
            'submitted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_submissions'", 'to': u"orm['website.UserProfile']"}),
            'votes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['website.UserProfile']", 'through': u"orm['poll.Vote']", 'symmetrical': 'False'})
        },
        u'poll.vote': {
            'Meta': {'unique_together': "(('user', 'day'),)", 'object_name': 'Vote'},
            'day': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'submission_votes'", 'to': u"orm['poll.Submission']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_votes'", 'to': u"orm['website.UserProfile']"})
        },
        u'website.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'email_settings': ('django.db.models.fields.CharField', [], {'default': "'posts'", 'max_length': '64'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'profile_pic': ('django.db.models.fields.files.ImageField', [], {'default': 'None', 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['poll']