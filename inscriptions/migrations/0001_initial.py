# Generated by Django 4.2.16 on 2025-02-06 02:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Annonce',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('contenu', models.TextField()),
                ('date_publication', models.DateTimeField(auto_now_add=True)),
                ('est_active', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='annonces/')),
                ('organisateur', models.CharField(blank=True, max_length=255, null=True)),
                ('lieu', models.CharField(blank=True, max_length=255, null=True)),
                ('date_evenement', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(help_text="Le titre de l'article", max_length=200)),
                ('contenu', models.TextField(help_text="Le contenu de l'article")),
                ('auteur', models.CharField(help_text="L'auteur de l'article", max_length=100)),
                ('date_publication', models.DateTimeField(default=django.utils.timezone.now, help_text="Date de publication de l'article")),
                ('image', models.ImageField(blank=True, help_text="Image associée à l'article", null=True, upload_to='articles/')),
                ('est_active', models.BooleanField(default=True, help_text="Indique si l'article est actif ou non")),
            ],
        ),
        migrations.CreateModel(
            name='Etudiant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('niveau', models.CharField(choices=[('Preparatoire', 'Préparatoire'), ('Premiere Annee', 'Première Année'), ('Deuxieme Annee', 'Deuxième Année'), ('Troisieme Annee', 'Troisième Année'), ('Quatrieme Annee', 'Quatrième Année')], default='Preparatoire', max_length=50)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telephone', models.CharField(max_length=15)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='etudiant', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Evenement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titre', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('date_debut', models.DateTimeField()),
                ('date_fin', models.DateTimeField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='evenements/')),
                ('lieu', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Professeur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('Charles Vorbe', 'Charles Vorbe'), ('Dominique Muscadin', 'Dominique MUSCADIN'), ('Emmanuel Milord', 'Emmanuel Milord'), ('Etienne Oremil', 'Etienne Oremil'), ('Georges Legagneur', 'Georges LEGAGNEUR'), ('Hancy Pierre', 'Hancy Pierre'), ('Hubermane Ciguino', 'Hubermane Ciguino'), ('Janes Louis', 'Janes LOUIS'), ('Jean Evrard Jean Charles', 'Jean Evrard Jean Charles'), ('Jean Luc Tondreau', 'Jean Luc Tondreau'), ('Jean Pierre Ciguino', 'Jean Pierre CIGUINO'), ('Jean Ronel Sistanis', 'Jean Ronel Sistanis'), ('Jean Roy FAUSTIN', 'Jean Roy FAUSTIN'), ('Jerome M', 'Jerome M'), ('Job Silver', 'Job SILVER'), ('Julio Elisna', 'Julio Elisna'), ('Kenaz Brunis', 'Kénaz BRUNIS'), ('Kenley Brutus', 'Kenley Brutus'), ('Max Lubin', 'Max Lubin'), ('Murielle Antoine', 'Murielle ANTOINE'), ('Roosevelt Millard', 'Roosevelt Millard'), ('Schmied Saint Fleur', 'Schmied Saint Fleur'), ('Simeon Francois', 'Siméon FRANCOIS'), ('Vosh Dathus', 'Vosh Dathus')], max_length=100)),
                ('specialisation', models.CharField(choices=[('Mathematiques', 'Mathématiques'), ('Philosophie', 'Philosophie'), ('Histoire', 'Histoire'), ('Droit', 'Droit'), ('Economie', 'Économie'), ('Francais', 'Français'), ('Creole', 'Créole'), ('OTI', 'Organisation du Travail'), ('Caraibe', 'Monde Caraïbe'), ('Intro Aux Sc Hum', 'Intro Aux Sc Hum'), ('HIPS', 'Histoire Des Idees Politiques et Sociales')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Cours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(choices=[('HIPS', 'Histoire des Idées Politiques et Sociales (HIPS)'), ('CREOLE', 'Créole: Expression Écrite et Orale'), ('MATHS', 'Mathématiques'), ('ECONOMIE', "Introduction à l'Économie"), ('Intro Aux SC HUM', 'Introduction aux Sciences Humaines'), ('PHILO', 'Introduction à la Philosophie'), ('OTI', 'Organisation du Travail Intellectuel'), ('DROIT', 'Introduction au Droit'), ('FRANCAIS', 'Français: Expression Écrite et Orale'), ('CARAIBE', 'Monde Caraïbe'), ("HISTOIRE D'HAITI", "Histoire d'Haïti")], max_length=200)),
                ('specialisation', models.CharField(choices=[('Mathematiques', 'Mathématiques'), ('Philosophie', 'Philosophie'), ('Histoire', 'Histoire'), ('Droit', 'Droit'), ('Economie', 'Économie'), ('Francais', 'Français'), ('Creole', 'Créole'), ('OTI', 'Organisation du Travail Intellectuel'), ('Caraibe', 'Monde Caraïbe'), ('Intro Aux SC Hum', 'Intro Aux SC Hum'), ('HIPS', 'Histoire des idées Politiques et Sociales')], max_length=100)),
                ('capacite_maximale', models.PositiveIntegerField()),
                ('horaire', models.CharField(choices=[('Lundi 7H-10H', 'Lundi 7H:00 - 10H:00'), ('Lundi 10H-1H', 'Lundi 10H:00 - 1H:00'), ('Lundi 1H-4H', 'Lundi 1H:00 - 4H:00'), ('Mardi 7H-10H', 'Mardi 7H:00 - 10H:00'), ('Mardi 10H-1H', 'Mardi 10H:00 - 1H:00'), ('Mardi 1H-4H', 'Mardi 1H:00 - 4H:00'), ('Mercredi 7H-10H', 'Mercredi 7H:00 - 10H:00'), ('Mercredi 10H-1H', 'Mercredi 10H:00 - 1H:00'), ('Mercredi 1H-4H', 'Mercredi 1H:00 - 4H:00'), ('Jeudi 7H-10H', 'Jeudi 7H:00 - 10H:00'), ('Jeudi 10H-1H', 'Jeudi 10H:00 - 1H:00'), ('Jeudi 1H-4H', 'Jeudi 1H:00 - 4H:00'), ('Vendredi 7H-10H', 'Vendredi 7H:00 - 10H:00'), ('Vendredi 10H-1H', 'Vendredi 10H:00 - 1H:00'), ('Vendredi 1H-4H', 'Vendredi 1H:00 - 4H:00'), ('Samedi 7H-10H', 'Samedi 7H:00 - 10H:00'), ('Samedi 10H-1H', 'Samedi 10H:00 - 1H:00'), ('Samedi 1H-4H', 'Samedi 1H:00 - 4H:00')], max_length=50)),
                ('est_ferme', models.BooleanField(default=False)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
                ('professeurs', models.ManyToManyField(related_name='cours', to='inscriptions.professeur')),
            ],
        ),
        migrations.CreateModel(
            name='Inscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('cours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='inscriptions.cours')),
                ('etudiant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inscriptions', to='inscriptions.etudiant')),
            ],
            options={
                'unique_together': {('etudiant', 'cours')},
            },
        ),
    ]
