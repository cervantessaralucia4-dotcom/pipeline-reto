from django.db import migrations


def seed_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    UserProfile = apps.get_model('authentication', 'UserProfile')

    users_data = [
        {'username': 'admin_ips',    'password': 'Admin2026*',  'rol': 'administrador'},
        {'username': 'medico_ips',   'password': 'Medico2026*', 'rol': 'medico'},
        {'username': 'analista_ips', 'password': 'Analista2026*','rol': 'analista'},
    ]

    for data in users_data:
        user, created = User.objects.get_or_create(
            username=data['username'],
            defaults={'is_staff': data['rol'] == 'administrador', 'is_superuser': data['rol'] == 'administrador'}
        )
        if created:
            user.set_password(data['password'])
            user.save()
            UserProfile.objects.create(user=user, rol=data['rol'])


def reverse_seed(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username__in=['admin_ips', 'medico_ips', 'analista_ips']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('authentication', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(seed_users, reverse_seed),
    ]
