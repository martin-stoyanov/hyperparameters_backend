# Generated by Django 2.2.1 on 2019-06-04 16:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HPJS_Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parameter_name', models.CharField(max_length=50)),
                ('hpjs_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.HPJS_Model')),
            ],
        ),
        migrations.CreateModel(
            name='ParameterValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=50)),
                ('parameter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Parameter')),
            ],
        ),
        migrations.CreateModel(
            name='Trial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trial', models.IntegerField()),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('hpjs_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.HPJS_Model')),
            ],
        ),
        migrations.DeleteModel(
            name='mainModel',
        ),
        migrations.AddField(
            model_name='parametervalue',
            name='trial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Trial'),
        ),
    ]
