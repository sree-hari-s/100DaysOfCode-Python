# Generated by Django 4.1 on 2023-04-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_rename_subject_id_teacher_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='subject',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
