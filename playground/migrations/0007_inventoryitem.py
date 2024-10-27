# Generated by Django 5.1.2 on 2024-10-27 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playground', '0006_delete_emaillog_rename_email_body_user_state'),
    ]

    operations = [
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
    ]
