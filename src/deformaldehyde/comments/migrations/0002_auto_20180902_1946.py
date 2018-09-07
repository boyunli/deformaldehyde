# Generated by Django 2.0.7 on 2018-09-02 11:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('comments', '0001_initial'),
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Account', verbose_name='作者'),
        ),
        migrations.AddField(
            model_name='comment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.Article', verbose_name='文章'),
        ),
        migrations.AddField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='comments.Comment', verbose_name='上级评论'),
        ),
    ]