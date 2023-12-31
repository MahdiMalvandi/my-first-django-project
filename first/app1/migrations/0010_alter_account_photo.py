# Generated by Django 4.2.6 on 2023-10-25 11:01

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0009_alter_account_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='photo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=['middle', 'center'], force_format=None, keep_meta=True, null=True, quality=60, scale=None, size=[500, 500], upload_to='account-image/'),
        ),
    ]
