# Generated by Django 4.2.5 on 2024-01-28 03:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loanproapp', '0003_alter_loanapplicant_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanapplicant',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
