# Generated by Django 4.2.3 on 2023-07-14 03:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MoiveData",
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
                ("title_kor", models.CharField(max_length=100)),
                ("title_eng", models.CharField(max_length=100)),
                ("poster_url", models.TextField()),
                ("rating_aud", models.FloatField()),
                ("rating_cri", models.FloatField()),
                ("rating_net", models.FloatField()),
                ("genre", models.CharField(max_length=100)),
                ("showtimes", models.CharField(max_length=100)),
                ("release_date", models.CharField(max_length=100)),
                ("rate", models.CharField(max_length=100)),
                ("summary", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="StaffData",
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
                ("role", models.CharField(max_length=100)),
                ("image_url", models.TextField()),
                (
                    "movie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="movielist.moivedata",
                    ),
                ),
            ],
        ),
    ]
