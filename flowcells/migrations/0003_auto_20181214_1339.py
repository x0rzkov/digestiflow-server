# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-14 12:39
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("flowcells", "0002_knownindexcontamination")]

    operations = [
        migrations.RemoveField(model_name="flowcell", name="silence_index_errors"),
        migrations.AddField(
            model_name="flowcell",
            name="lanes_suppress_no_sample_found_for_observed_index_warning",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(),
                blank=True,
                default=list,
                help_text="The lanes for which indexes without matching entry in the sample sheet should be ignored",
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="flowcell",
            name="lanes_suppress_no_sample_sheet_warning",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.PositiveIntegerField(),
                blank=True,
                default=list,
                help_text="The lanes for which missing sample sheet information should be suppressed",
                size=None,
            ),
        ),
        migrations.AddField(
            model_name="library",
            name="suppress_barcode1_not_observed_error",
            field=models.BooleanField(
                default=False,
                help_text='Suppress "index not observed" error in barcode 1 for this library.',
            ),
        ),
        migrations.AddField(
            model_name="library",
            name="suppress_barcode2_not_observed_error",
            field=models.BooleanField(
                default=False,
                help_text='Suppress "index not observed" error in barcode 2 for this library.',
            ),
        ),
    ]
