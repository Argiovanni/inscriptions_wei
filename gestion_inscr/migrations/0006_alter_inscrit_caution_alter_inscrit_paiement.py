# Generated by Django 4.2.6 on 2024-08-17 18:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_inscr', '0005_inscrit_caution_paye_inscrit_place_paye_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscrit',
            name='caution',
            field=models.CharField(choices=[('L', 'Lydia'), ('C', 'Chèque'), ('E', 'Espèce')], default='L', max_length=1),
        ),
        migrations.AlterField(
            model_name='inscrit',
            name='paiement',
            field=models.CharField(choices=[('L', 'Lydia'), ('C', 'Chèque'), ('E', 'Espèce')], default='L', max_length=1),
        ),
    ]
