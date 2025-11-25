# Generated migration for adding container and vehicle specific fields

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inspections', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='inspection',
            name='container_number',
            field=models.CharField(blank=True, help_text='Container number (e.g., ABCD1234567)', max_length=50),
        ),
        migrations.AddField(
            model_name='inspection',
            name='seal_number',
            field=models.CharField(blank=True, help_text='Seal/Lock number', max_length=50),
        ),
        migrations.AddField(
            model_name='inspection',
            name='booking_number',
            field=models.CharField(blank=True, help_text='Booking or BL number', max_length=100),
        ),
        migrations.AddField(
            model_name='inspection',
            name='vessel_name',
            field=models.CharField(blank=True, help_text='Vessel/Ship name', max_length=200),
        ),
        migrations.AddField(
            model_name='inspection',
            name='voyage_number',
            field=models.CharField(blank=True, help_text='Voyage number', max_length=50),
        ),
        migrations.AddField(
            model_name='inspection',
            name='container_type',
            field=models.CharField(blank=True, help_text='Container type (20ft, 40ft, etc.)', max_length=50),
        ),
        migrations.AddField(
            model_name='inspection',
            name='container_size',
            field=models.CharField(blank=True, help_text='Container size', max_length=20),
        ),
        migrations.AddField(
            model_name='inspection',
            name='cargo_description',
            field=models.TextField(blank=True, help_text='Description of cargo/goods'),
        ),
        migrations.AddField(
            model_name='inspection',
            name='cargo_weight',
            field=models.DecimalField(blank=True, decimal_places=2, help_text='Cargo weight in kg', max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='inspection',
            name='vehicle_plate',
            field=models.CharField(blank=True, help_text='Vehicle license plate', max_length=20),
        ),
        migrations.AddField(
            model_name='inspection',
            name='vehicle_model',
            field=models.CharField(blank=True, help_text='Vehicle model', max_length=100),
        ),
        migrations.AddField(
            model_name='inspection',
            name='vehicle_year',
            field=models.IntegerField(blank=True, help_text='Vehicle year', null=True),
        ),
        migrations.AddField(
            model_name='inspection',
            name='vehicle_vin',
            field=models.CharField(blank=True, help_text='Vehicle VIN number', max_length=50),
        ),
    ]
