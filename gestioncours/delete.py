@login_required
def modifier_etudiant(request, pk):
    etudiant = get_object_or_404(Etudiant, pk=pk)
    
    if request.method == 'POST':
        form = EtudiantForm(request.POST, instance=etudiant)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations de l'étudiant ont été modifiées avec succès.")
            return redirect('dashboard')
    else:
        form = EtudiantForm(instance=etudiant)
    
    return render(request, 'admin/etudiant_form.html', {'form': form, 'etudiant': etudiant})

@login_required
def modifier_cours(request, pk):
    cours = get_object_or_404(Cours, pk=pk)
    
    if request.method == 'POST':
        form = CoursForm(request.POST, instance=cours)
        if form.is_valid():
            form.save()
            messages.success(request, "Les informations du cours ont été modifiées avec succès.")
            return redirect('dashboard')
    else:
        form = CoursForm(instance=cours)
    
    return render(request, 'admin/cours_form.html', {'form': form, 'cours': cours})

@login_required
def modifier_professeur(request, pk):
    professeur = get_object_or_404(Professeur, pk=pk)

    if request.method == 'POST':
        form = ProfesseurForm(request.POST, instance=professeur)
        if form.is_valid():
            form.save()
            messages.success(request, "Le professeur a été mis à jour avec succès.")
            return redirect('dashboard')
    else:
        form = ProfesseurForm(instance=professeur)

    return render(request, 'admin/professeur_form.html', {'form': form, 'professeur': professeur})

@login_required
def modifier_inscription(request, pk):
    ins = get_object_or_404(Inscription, pk=pk)
    if request.method == 'POST':
        form = InscriptionForm(request.POST, instance=ins)
        if form.is_valid():
            form.save()
            messages.success(request, "Inscription modifiée.")
            return redirect('dashboard')
    else:
        form = InscriptionForm(instance=ins)
    return render(request, 'admin/inscription_form.html', {'form': form})


@login_required
def modifier_horaire(request, pk):
    h = get_object_or_404(HoraireCours, pk=pk)
    if request.method == 'POST':
        form = HoraireCoursForm(request.POST, instance=h)
        if form.is_valid():
            form.save()
            messages.success(request, "Horaire modifié.")
            return redirect('dashboard')
    else:
        form = HoraireCoursForm(instance=h)
    return render(request, 'admin/horaire_form.html', {'form': form})


@login_required
def modifier_article(request, pk):
    art = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES, instance=art)
        if form.is_valid():
            form.save()
            messages.success(request, "Article modifié.")
            return redirect('dashboard')
    else:
        form = ArticleForm(instance=art)
    return render(request, 'admin/article_form.html', {'form': form})

@login_required
def modifier_evenement(request, pk):
    evt = get_object_or_404(Evenement, pk=pk)
    if request.method == 'POST':
        form = EvenementForm(request.POST, request.FILES, instance=evt)
        if form.is_valid():
            form.save()
            messages.success(request, "Événement modifié.")
            return redirect('dashboard')
    else:
        form = EvenementForm(instance=evt)
    return render(request, 'admin/evenement_form.html', {'form': form})

@login_required
def modifier_annonce(request, pk):
    an = get_object_or_404(Annonce, pk=pk)
    if request.method == 'POST':
        form = AnnonceForm(request.POST, request.FILES, instance=an)
        if form.is_valid():
            form.save()
            messages.success(request, "Annonce modifiée.")
            return redirect('dashboard')
    else:
        form = AnnonceForm(instance=an)
    return render(request, 'admin/annonce_form.html', {'form': form})


@login_required
def modifier_programme(request, pk):
    programme = get_object_or_404(Programme, pk=pk)
    if request.method == 'POST':
        form = ProgrammeForm(request.POST, instance=programme)
        if form.is_valid():
            form.save()
            messages.success(request, "Programme modifié.")
            return redirect('dashboard')
    else:
        form = ProgrammeForm(instance=programme)
    return render(request, 'admin/programme_form.html', {'form': form})


@login_required
def modifier_axe(request, pk):
    axe = get_object_or_404(AxeRecherche, pk=pk)
    if request.method == 'POST':
        form = AxeRechercheForm(request.POST, instance=axe)
        if form.is_valid():
            form.save()
            messages.success(request, "Axe de recherche modifié.")
            return redirect('dashboard')
    else:
        form = AxeRechercheForm(instance=axe)
    return render(request, 'admin/axe_form.html', {'form': form})


@login_required
def modifier_publication(request, pk):
    pub = get_object_or_404(PublicationRecherche, pk=pk)
    if request.method == 'POST':
        form = PublicationRechercheForm(request.POST, instance=pub)
        if form.is_valid():
            form.save()
            messages.success(request, "Publication modifiée.")
            return redirect('dashboard')
    else:
        form = PublicationRechercheForm(instance=pub)
    return render(request, 'admin/publication_form.html', {'form': form})


@login_required
def modifier_livre(request, pk):
    livre = get_object_or_404(Livre, pk=pk)
    if request.method == 'POST':
        form = LivreForm(request.POST, instance=livre)
        if form.is_valid():
            form.save()
            messages.success(request, "Livre modifié.")
            return redirect('dashboard')
    else:
        form = LivreForm(instance=livre)
    return render(request, 'admin/livre_form.html', {'form': form})


@login_required
def modifier_personnel(request, pk):
    pers = get_object_or_404(Personnel, pk=pk)
    if request.method == 'POST':
        form = PersonnelForm(request.POST, request.FILES, instance=pers)
        if form.is_valid():
            form.save()
            messages.success(request, "Membre du personnel modifié.")
            return redirect('dashboard')
    else:
        form = PersonnelForm(instance=pers)
    return render(request, 'admin/personnel_form.html', {'form': form})


@login_required
def modifier_etape_admission(request, pk):
    etp = get_object_or_404(EtapeAdmission, pk=pk)
    if request.method == 'POST':
        form = EtapeAdmissionForm(request.POST, instance=etp)
        if form.is_valid():
            form.save()
            messages.success(request, "Étape d'admission modifiée.")
            return redirect('dashboard')
    else:
        form = EtapeAdmissionForm(instance=etp)
    return render(request, 'admin/etape_admission_form.html', {'form': form})

@login_required
def modifier_demande_admission(request, pk):
    dem = get_object_or_404(DemandeAdmission, pk=pk)
    if request.method == 'POST':
        form = DemandeAdmissionForm(request.POST, instance=dem)
        if form.is_valid():
            form.save()
            messages.success(request, "Demande d'admission modifiée.")
            return redirect('dashboard')
    else:
        form = DemandeAdmissionForm(instance=dem)
    return render(request, 'admin/demande_admission_form.html', {'form': form})
