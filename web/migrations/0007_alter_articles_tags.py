# Generated by Django 4.1.5 on 2025-03-12 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0006_alter_tag_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articles',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='articles', to='web.tag'),
        ),
    ]
