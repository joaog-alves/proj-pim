# Generated by Django 4.2.16 on 2024-09-25 16:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_atendente_usuario_alter_gerente_usuario_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(auto_now=True)),
                ('hora', models.TimeField(auto_now=True)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('consulta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.consulta')),
            ],
        ),
    ]
