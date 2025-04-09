# Generated by Django 5.1.1 on 2025-04-07 12:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('analysis', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('category', models.CharField(choices=[('CLEANSER', 'Cleanser'), ('MOISTURIZER', 'Moisturizer'), ('SUNSCREEN', 'Sunscreen'), ('TREATMENT', 'Treatment')], max_length=20)),
                ('ingredients', models.TextField()),
                ('suitable_for', models.JSONField(default=list)),
                ('is_vegan', models.BooleanField(default=False)),
                ('is_organic', models.BooleanField(default=False)),
                ('is_fragrance_free', models.BooleanField(default=False)),
                ('image_url', models.URLField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Recommendation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_viewed', models.BooleanField(default=False)),
                ('analysis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='analysis.skinanalysis')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommendations.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
