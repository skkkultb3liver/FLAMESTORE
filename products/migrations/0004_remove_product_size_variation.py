# Generated by Django 4.1.2 on 2023-03-23 11:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_product_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='size',
        ),
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variation_category', models.CharField(choices=[('size', 'size')], max_length=100)),
                ('variation_value', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
    ]
