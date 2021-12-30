# Generated by Django 4.0 on 2021-12-30 07:52

import classes.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('info', models.TextField(blank=True)),
                ('code', models.SlugField(max_length=7, unique=True)),
                ('class_teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='class_teacher', to='Users.user')),
                ('students', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Contents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('info', models.TextField(blank=True)),
                ('classes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classes')),
            ],
        ),
        migrations.CreateModel(
            name='ContentFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('files', models.FileField(upload_to=classes.models.getUploadDir)),
                ('contents', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.contents')),
            ],
        ),
    ]