# reclamation/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Reclamation

@login_required
def liste_reclamations(request):

    reclamations = Reclamation.objects.filter(user=request.user)
    
    return render(request, 'reclamation/liste_reclamations.html', {'reclamations': reclamations})

@login_required
def creer_reclamation(request):
    if request.method == 'POST':
        titre = request.POST.get('titre')
        description = request.POST.get('description')
        print(request.user)
        print(titre)
        print(description)
        # Validation manuelle des données
        if titre and description:
            print(request.user)
            Reclamation.objects.create(titre=titre, description=description, user=request.user)
            return redirect('liste_reclamations')
        
    return render(request, 'reclamation/creer_reclamation.html')

@login_required
def modifier_reclamation(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reclamation.titre = request.POST.get('titre')
        reclamation.description = request.POST.get('description')
        
        # Validation manuelle
        if reclamation.titre and reclamation.description:
            reclamation.save()
            return redirect('liste_reclamations')
    
    return render(request, 'reclamation/modifier_reclamation.html', {'reclamation': reclamation})

@login_required
def supprimer_reclamation(request, pk):
    reclamation = get_object_or_404(Reclamation, pk=pk, user=request.user)
    
    if request.method == 'POST':
        reclamation.delete()
        return redirect('liste_reclamations')
    
    return render(request, 'reclamation/supprimer_reclamation.html', {'reclamation': reclamation})
