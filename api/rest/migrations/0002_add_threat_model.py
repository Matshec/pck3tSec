# Generated by Django 3.0.5 on 2020-04-17 15:31

from django.db import migrations, models
import django.db.models.deletion
import rest.enum_classes


class Migration(migrations.Migration):

    dependencies = [
        ('rest', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='host',
            name='fqd_name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='host',
            name='last_accessed',
            field=models.DateTimeField(),
        ),
        migrations.CreateModel(
            name='Threat',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('threat_type', models.CharField(choices=[(rest.enum_classes.ThreatType['HOST'], 'HOST'), (rest.enum_classes.ThreatType['FILE'], 'FILE'), (rest.enum_classes.ThreatType['USER_DEFINED'], 'USER_DEFINED')], max_length=20, null=True)),
                ('threat_details', models.TextField()),
                ('http_path', models.CharField(default='', max_length=2048)),
                ('discovered', models.DateTimeField()),
                ('host_source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rest.Host')),
            ],
        ),
    ]