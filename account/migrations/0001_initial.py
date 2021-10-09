# Generated by Django 3.2.7 on 2021-09-16 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log in this site', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=False, help_text='Designates whether this user should br treated as active . Unselect this instade of deleting accounts', verbose_name='active')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('headline', models.CharField(blank=True, max_length=120, null=True)),
                ('gender', models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female')], max_length=10, null=True)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('country', django_countries.fields.CountryField(blank=True, max_length=2, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('is_author', models.BooleanField(default=False)),
                ('image', models.ImageField(blank=True, default='default/default.png', null=True, upload_to='user_image/')),
                ('account_slug', models.SlugField(max_length=264, unique=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Institution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('subject', models.CharField(max_length=60)),
                ('degree', models.CharField(choices=[('Bachelor of Arts: BA', 'Bachelor of Arts: BA'), ('Bachelor of Business Administration: BBA', 'Bachelor of Business Administration: BBA'), ('Bachelor of Management Studies: BMS', 'Bachelor of Management Studies: BMS'), ('Bachelor of Science: BSc', 'Bachelor of Science: BSc'), ('Bachelor of Commerce: Bcom', 'Bachelor of Commerce: Bcom'), ('Bachelor of Computer Applications: BCA', 'Bachelor of Computer Applications: BCA'), ('Bachelor of Fine Arts: BFA', 'Bachelor of Fine Arts: BFA'), ('Bachelor of Laws: LLB', 'Bachelor of Laws: LLB'), ('Bachelor of Engineering: BE', 'Bachelor of Engineering: BE'), ('Bachelor of Technology: BTech', 'Bachelor of Technology: BTech'), ('Bachelor of Education: BEd', 'Bachelor of Education: BEd'), ('Bachelor of Medicine, Bachelor of Surgery: MBBS', 'Bachelor of Medicine, Bachelor of Surgery: MBBS'), ('Bachelor of Veterinary Science: BVSc', 'Bachelor of Veterinary Science: BVSc'), ('Bachelor of Architecture: BArch', 'Bachelor of Architecture: BArch'), ('Master of Arts (M.A.)', 'Master of Arts (M.A.)'), ('Master of Social Work (MSW)', 'Master of Social Work (MSW)'), ('Master of Business Administration (M.B.A.)', 'Master of Business Administration (M.B.A.)'), ('Master of Computer Applications (M.C.A.)', 'Master of Computer Applications (M.C.A.)'), ('Master of Engineering (M.Eng.)', 'Master of Engineering (M.Eng.)'), ('Master of Philosophy (M.Phil.)', 'Master of Philosophy (M.Phil.)'), ('Master of Science (M.Sc.)', 'Master of Science (M.Sc.)'), ('Master of Technology (M.Tech.)', 'Master of Technology (M.Tech.)'), ('Master of Statistics (M.Stat.)', 'Master of Statistics (M.Stat.)'), ('Master of Laws (LL.M.)', 'Master of Laws (LL.M.)'), ('Master of Commerce (M.Com.)', 'Master of Commerce (M.Com.)'), ('Master of Architecture (M.Arch.)', 'Master of Architecture (M.Arch.)'), ('Master of Veterinary Science (MVSc)', 'Master of Veterinary Science (MVSc)')], max_length=60)),
                ('start_year', models.IntegerField(default=2021)),
                ('graduated', models.BooleanField(default=False)),
                ('end_year', models.IntegerField()),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]