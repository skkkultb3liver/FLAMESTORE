# Generated by Django 4.1.2 on 2023-03-14 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0002_productcategory_key'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productcategory',
            options={'ordering': ['key'], 'verbose_name': 'Product category', 'verbose_name_plural': 'Product categories'},
        ),
    ]
