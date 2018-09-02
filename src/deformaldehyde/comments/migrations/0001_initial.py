# Generated by Django 2.0.7 on 2018-09-02 11:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=500, verbose_name='正文')),
                ('is_enable', models.BooleanField(default=True, verbose_name='是否显示')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='更新时间')),
            ],
            options={
                'verbose_name': '评论',
                'get_latest_by': 'create_time',
                'verbose_name_plural': '评论',
                'ordering': ['-create_time'],
            },
        ),
    ]
