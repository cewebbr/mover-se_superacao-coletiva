# Generated by Django 4.1.1 on 2022-12-23 19:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0003_alter_topic_project_messagevote'),
    ]

    operations = [
        migrations.RenameField(
            model_name='messagevote',
            old_name='content',
            new_name='value',
        ),
    ]