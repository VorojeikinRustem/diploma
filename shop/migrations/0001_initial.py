# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-03 10:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_amount', models.FloatField()),
                ('closed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='CartElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('open', '\u041f\u0440\u0438\u043d\u044f\u0442'), ('prepared', '\u041e\u0444\u043e\u0440\u043c\u043b\u0435\u043d\u0438\u0435'), ('cancel', '\u041e\u0442\u043c\u0435\u043d\u0435\u043d'), ('deliver', '\u0414\u043e\u0441\u0442\u0430\u0432\u043b\u044f\u0435\u0442\u0441\u044f'), ('completed', '\u0414\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d')], default='open', max_length=20)),
                ('username', models.CharField(max_length=50)),
                ('phone', models.PositiveIntegerField()),
                ('address', models.CharField(max_length=254)),
                ('email', models.EmailField(max_length=100)),
                ('express_delivery', models.BooleanField()),
                ('checkout_datetime', models.DateTimeField(auto_now_add=True)),
                ('cart', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='shop.Cart')),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='images/sneakers')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.SlugField()),
                ('price', models.PositiveIntegerField()),
                ('brand', models.CharField(choices=[('asics', 'Asics'), ('jordan', 'Jordan'), ('nike', 'Nike'), ('new_balance', 'New Balance')], default='asics', max_length=15)),
                ('available', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.PositiveIntegerField(choices=[(32, b'32'), (33, b'33'), (34, b'34'), (35, b'35'), (36, b'36'), (37, b'37'), (38, b'38'), (39, b'39'), (40, b'40'), (41, b'41'), (42, b'42'), (43, b'43'), (44, b'44'), (45, b'45'), (46, b'46'), (47, b'47')], default=45)),
                ('available', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product')),
            ],
        ),
        migrations.AddField(
            model_name='photo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='cartelement',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Product'),
        ),
        migrations.AddField(
            model_name='cartelement',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.Size'),
        ),
    ]
