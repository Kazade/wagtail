# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.db.migrations.operations.base import Operation
from djangae.contrib.contenttypes.models import SimulatedContentTypeManager


class PatchMigrationsOperation(Operation):

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        pass

    def state_forwards(self, app_label, state):
        contenttype = state.models[('contenttypes', 'contenttype')]
        contenttype.managers[0] = ('objects', SimulatedContentTypeManager(model=contenttype))


class Migration(migrations.Migration):

    run_before = [
        ('home', '0001_initial'),
        ('wagtailadmin', '0001_initial'),
        ('wagtailcore', '0001_initial'),
        ('wagtaildocs', '0001_initial'),
        ('wagtailembeds', '0001_initial'),
        ('wagtailforms', '0001_initial'),
        ('wagtailimages', '0001_initial'),
        ('wagtailredirects', '0001_initial'),
        ('wagtailsearch', '0001_initial'),
        ('wagtailusers', '0001_initial'),
    ]

    operations = [
        PatchMigrationsOperation(),
    ]
