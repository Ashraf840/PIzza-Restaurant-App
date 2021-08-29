# Generated by Django 3.2.6 on 2021-08-25 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='Email')),
                ('company_name', models.CharField(blank=True, default='Not Available', max_length=200, verbose_name='Company Name')),
                ('phone', models.CharField(blank=True, default='Null', max_length=20, verbose_name='Company Phone')),
                ('first_name', models.CharField(blank=True, default='Anonymous', max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, default='User', max_length=50, verbose_name='Last Name')),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Male', max_length=10, verbose_name='Gender')),
                ('date_joined', models.DateField(auto_now_add=True, verbose_name='Date Joined')),
                ('last_login', models.DateTimeField(auto_now_add=True, verbose_name='Last Login')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'User List',
            },
        ),
    ]
