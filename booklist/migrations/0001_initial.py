# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-15 09:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_editor', models.BooleanField(default=False)),
                ('position', models.IntegerField()),
            ],
            options={
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='Bind',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BindRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('range_top', models.PositiveIntegerField()),
                ('range_price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('bind', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.Bind')),
            ],
            options={
                'ordering': ['range_top'],
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.CharField(blank=True, default='', max_length=200, null=True)),
                ('isbn', models.BigIntegerField(default=0, unique=True)),
                ('weight', models.PositiveIntegerField(default=0)),
                ('price_on_cover', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('cover_photo', models.ImageField(null=True, upload_to='covers')),
            ],
        ),
        migrations.CreateModel(
            name='BookSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('upper_category', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='booklist.Category')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=50)),
                ('is_with_wings', models.BooleanField(default=False)),
                ('is_dust_jacket', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('year', models.PositiveIntegerField()),
                ('comment', models.CharField(blank=True, default='', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ForeignEdition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveIntegerField(default=1)),
                ('year', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='NumberOfPages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arabic', models.PositiveIntegerField(default=0)),
                ('roman', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Part',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('part_name', models.CharField(max_length=20)),
                ('part_number', models.PositiveIntegerField()),
                ('number_of_parts', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('secondname', models.CharField(blank=True, default='', max_length=50)),
                ('surname', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Publisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=50)),
                ('short_name', models.CharField(default=None, max_length=30, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.City')),
            ],
        ),
        migrations.CreateModel(
            name='XeroBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('xero_pages', models.IntegerField(default=0)),
                ('book', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='booklist.Book')),
            ],
        ),
        migrations.AddField(
            model_name='foreignedition',
            name='language',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='booklist.Language'),
        ),
        migrations.AddField(
            model_name='foreignedition',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.Publisher'),
        ),
        migrations.AddField(
            model_name='foreignedition',
            name='translator',
            field=models.ManyToManyField(to='booklist.Person'),
        ),
        migrations.AddField(
            model_name='city',
            name='country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.Country'),
        ),
        migrations.AddField(
            model_name='bookseries',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.Publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(to='booklist.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='cover',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='booklist.Cover'),
        ),
        migrations.AddField(
            model_name='book',
            name='edition',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='booklist.Edition'),
        ),
        migrations.AddField(
            model_name='book',
            name='foreign_edition',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='booklist.ForeignEdition'),
        ),
        migrations.AddField(
            model_name='book',
            name='format',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='booklist.Format'),
        ),
        migrations.AddField(
            model_name='book',
            name='number_of_pages',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='booklist.NumberOfPages'),
        ),
        migrations.AddField(
            model_name='book',
            name='part',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='booklist.Part'),
        ),
        migrations.AddField(
            model_name='book',
            name='publisher',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='booklist.Publisher'),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='booklist.BookSeries'),
        ),
        migrations.AddField(
            model_name='author',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.Person'),
        ),
        migrations.AddField(
            model_name='author',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='booklist.Book'),
        ),
        migrations.AlterUniqueTogether(
            name='author',
            unique_together=set([('book', 'author', 'is_editor', 'position')]),
        ),
    ]