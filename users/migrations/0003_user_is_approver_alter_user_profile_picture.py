# Generated by Django 4.1.1 on 2022-12-13 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_rename_profile_pricture_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_approver',
            field=models.BooleanField(default=False, verbose_name='Pode aprovar projetos?'),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='users/profile_prictures/%Y/%m/%d/', verbose_name='Foto de Perfil'),
        ),
    ]
