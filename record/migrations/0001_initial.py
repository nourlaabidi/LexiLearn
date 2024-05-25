# Generated by Django 5.0.4 on 2024-05-22 07:23

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="AudioFile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("audio", models.FileField(upload_to="audio/")),
                ("transcription", models.TextField(blank=True, null=True)),
            ],
        ),
    ]
