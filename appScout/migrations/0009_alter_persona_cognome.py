# Generated by Django 5.1.1 on 2024-09-17 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appScout', '0008_alter_conto_user_alter_persona_user_alter_spesa_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='persona',
            name='cognome',
            field=models.TextField(),
        ),
    ]
