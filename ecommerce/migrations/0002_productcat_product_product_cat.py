# Generated by Django 4.2.5 on 2023-10-01 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductCat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('poduct_cat_type', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_cat',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='ecommerce.productcat'),
        ),
    ]
