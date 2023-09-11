# Generated by Django 4.2.5 on 2023-09-11 02:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Imagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.CharField(max_length=255)),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=50)),
                ('contenido', models.TextField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('receptor_type', models.IntegerField()),
                ('post_type', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('apellidos', models.CharField(max_length=50)),
                ('username', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255)),
                ('contasenia', models.CharField(max_length=60)),
                ('esta_Activo', models.BooleanField(default=True)),
                ('es_Admin', models.BooleanField(default=False)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('actualizado_en', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_nacimiento', models.DateField()),
                ('genero', models.CharField(max_length=10)),
                ('imagen', models.CharField(max_length=255)),
                ('imagen_header', models.CharField(max_length=255)),
                ('titulo', models.CharField(max_length=255)),
                ('bio', models.CharField(max_length=255)),
                ('info_contacto', models.TextField()),
                ('email_publico', models.CharField(max_length=255)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.level')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='PostImagen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.imagen')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.post')),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='autor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.usuario'),
        ),
        migrations.AddField(
            model_name='post',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.level'),
        ),
        migrations.CreateModel(
            name='Portafolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=200)),
                ('descripcion', models.TextField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.level')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Notificaciones',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('not_type', models.IntegerField()),
                ('fue_leido', models.BooleanField(default=False)),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('receptor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_recibe', to='intSocial.usuario')),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.post')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_envia', to='intSocial.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.IntegerField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.post')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.usuario')),
            ],
        ),
        migrations.AddField(
            model_name='imagen',
            name='level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.level'),
        ),
        migrations.AddField(
            model_name='imagen',
            name='portafolio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='intSocial.portafolio'),
        ),
        migrations.AddField(
            model_name='imagen',
            name='usuario',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.usuario'),
        ),
        migrations.CreateModel(
            name='Grupos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imagen', models.CharField(max_length=255)),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField()),
                ('status', models.IntegerField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='intSocial.usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField()),
                ('creado_en', models.DateTimeField(auto_now_add=True)),
                ('ref', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.post')),
                ('respuesta_a', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='respuestas', to='intSocial.comentario')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='intSocial.usuario')),
            ],
        ),
    ]
