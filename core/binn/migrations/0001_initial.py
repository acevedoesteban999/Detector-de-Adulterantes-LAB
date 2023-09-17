# Generated by Django 4.2.3 on 2023-07-31 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BinnacleMessages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(choices=[('I', 'Información'), ('R', 'Reportes'), ('A', 'Advertencias'), ('E', 'Error')], max_length=1)),
                ('identifier_message', models.CharField(max_length=50)),
                ('reason', models.CharField(max_length=50)),
                ('timedate', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]