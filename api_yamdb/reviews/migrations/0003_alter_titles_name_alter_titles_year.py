# Generated by Django 4.1.3 on 2022-11-29 21:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_alter_categories_name_alter_genres_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='name',
            field=models.CharField(max_length=256, verbose_name='Произведение'),
        ),
        migrations.AlterField(
            model_name='titles',
            name='year',
            field=models.PositiveIntegerField(db_index=True),
        ),
    ]