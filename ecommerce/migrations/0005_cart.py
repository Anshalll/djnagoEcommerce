# Generated by Django 4.2.5 on 2023-10-04 14:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0004_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_assoc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.product')),
                ('user_assoc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ecommerce.users')),
            ],
        ),
    ]
