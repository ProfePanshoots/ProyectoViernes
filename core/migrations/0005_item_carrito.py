# Generated by Django 3.1.2 on 2023-06-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_subscription'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item_Carrito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_producto', models.CharField(max_length=40)),
                ('precio_producto', models.IntegerField()),
                ('imagen', models.ImageField(null=True, upload_to='items_carrito')),
                ('cantidad', models.IntegerField(default=1)),
                ('subtotal', models.IntegerField()),
            ],
            options={
                'db_table': 'db_items_carrito',
            },
        ),
    ]
