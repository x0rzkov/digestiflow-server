# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 08:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [("flowcells", "0005_laneindexhistogram_sample_size")]

    operations = [
        migrations.AlterModelOptions(
            name="laneindexhistogram", options={"ordering": ("flowcell", "lane", "index_read_no")}
        ),
        migrations.RenameField(
            model_name="laneindexhistogram", old_name="read_no", new_name="index_read_no"
        ),
        migrations.AlterUniqueTogether(
            name="laneindexhistogram", unique_together=set([("flowcell", "lane", "index_read_no")])
        ),
    ]
